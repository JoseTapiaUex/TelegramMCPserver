"""Utilities to fetch and summarise article content."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from readability import Document
from openai import OpenAI


@dataclass
class ProcessedURL:
    title: str
    summary: str
    source_url: str
    image_url: Optional[str]
    release_date: str
    provider: str
    type: str


class URLProcessor:
    """Fetches HTML pages, extracts relevant data and delegates AI summarisation."""

    def __init__(self, *, api_key: str, summary_model: str, image_model: str, timeout: int = 20) -> None:
        self.client = OpenAI(api_key=api_key)
        self.summary_model = summary_model
        self.image_model = image_model
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "TelegramMonitorAgent/1.0 (+https://github.com/chaindead/telegram-mcp)",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            }
        )

    def _download(self, url: str) -> tuple[str, str]:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text, response.url

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        og_title = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "twitter:title"})
        if og_title and og_title.get("content"):
            return og_title["content"].strip()
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        description = soup.find("meta", attrs={"name": "description"}) or soup.find(
            "meta", property="og:description"
        )
        if description and description.get("content"):
            return description["content"].strip()
        return None

    def _extract_image(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        for attribute in ("og:image", "twitter:image", "twitter:image:src"):
            meta = soup.find("meta", property=attribute) or soup.find("meta", attrs={"name": attribute})
            if meta and meta.get("content"):
                return urljoin(base_url, meta["content"].strip())
        first_image = soup.find("img")
        if first_image and first_image.get("src"):
            return urljoin(base_url, first_image["src"].strip())
        return None

    def _derive_type(self, soup: BeautifulSoup) -> str:
        article = soup.find("article")
        if article is not None:
            return "Artículo"
        og_type = soup.find("meta", property="og:type")
        if og_type and og_type.get("content"):
            return og_type["content"].replace("_", " ").title()
        return "Noticia"

    def summarise(self, *, title: str, description: str, body: str) -> str:
        prompt = (
            "Genera un resumen de máximo 3 líneas en español del contenido proporcionado. "
            "Utiliza un estilo periodístico conciso." 
        )
        response = self.client.responses.create(
            model=self.summary_model,
            input=[
                {"role": "system", "content": "Eres un asistente que crea resúmenes informativos en español."},
                {
                    "role": "user",
                    "content": f"Título: {title}\nDescripción: {description}\nContenido:\n{body}",
                },
            ],
            max_output_tokens=180,
        )
        text = getattr(response, "output_text", "")
        if not text:
            output = getattr(response, "output", [])
            if output:
                content = output[0].get("content", [])
                if content:
                    text = content[0].get("text", "")
        return text.strip()

    def generate_image(self, *, title: str, description: str) -> Optional[str]:
        prompt = (
            "Ilustración digital moderna para un artículo titulado '{title}'. "
            "Temática: {description}. Estilo limpio, colores vibrantes, formato 16:9."
        ).format(title=title, description=description[:180])
        result = self.client.images.generate(model=self.image_model, prompt=prompt, size="1024x1024")
        data = getattr(result, "data", [])
        if data:
            first = data[0]
            url = getattr(first, "url", None)
            if url:
                return url
            b64_json = getattr(first, "b64_json", None)
            if b64_json:
                return f"data:image/png;base64,{b64_json}"
        return None

    def process(self, url: str) -> ProcessedURL:
        html, final_url = self._download(url)
        soup = BeautifulSoup(html, "html.parser")
        try:
            document = Document(html)
            article_html = document.summary(html_partial=True)
            short_title = document.short_title()
        except Exception:
            article_html = soup.get_text(separator=" ")
            short_title = soup.title.string if soup.title and soup.title.string else None
        article_text = BeautifulSoup(article_html, "html.parser").get_text(separator=" ")
        article_text = re.sub(r"\s+", " ", article_text).strip()

        title = self._extract_title(soup) or short_title or "Sin título"
        description = self._extract_description(soup) or article_text[:300]
        image_url = self._extract_image(soup, final_url)
        content_type = self._derive_type(soup)

        summary = self.summarise(title=title, description=description, body=article_text)
        if not summary:
            summary = (description or article_text)[:240]
        if not image_url:
            image_url = self.generate_image(title=title, description=summary)

        parsed = urlparse(final_url)
        provider = parsed.netloc

        return ProcessedURL(
            title=title,
            summary=summary,
            source_url=final_url,
            image_url=image_url,
            release_date=datetime.utcnow().strftime("%Y-%m-%d"),
            provider=provider,
            type=content_type,
        )
