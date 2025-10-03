"""Main orchestration for the Telegram monitoring agent."""
from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from .config import Settings
from .preview import PreviewConsole
from .publisher import PostPublisher
from .state import AgentState
from .telegram_monitor import TelegramMonitor
from .url_processor import ProcessedURL, URLProcessor
from .utils import deduplicate, extract_urls


class MonitoringWorkflow:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.monitor = TelegramMonitor(
            server_url=settings.telegram_server_url,
            api_key=settings.telegram_api_key,
            chat_id=settings.telegram_chat_id,
        )
        self.processor = URLProcessor(
            api_key=settings.openai_api_key,
            summary_model=settings.summary_model,
            image_model=settings.image_model,
            timeout=settings.request_timeout,
        )
        self.publisher = PostPublisher(settings.backend_base_url, timeout=settings.request_timeout)
        self.preview = PreviewConsole()
        self.state = AgentState.from_file(settings.state_file)

    def _review(self, processed: ProcessedURL) -> Optional[ProcessedURL]:
        while True:
            decision = self.preview.present(processed)
            if decision.status == "accepted":
                return processed
            if decision.status == "discarded":
                return None
            if decision.status == "modify":
                if decision.updated_title:
                    processed.title = decision.updated_title
                if decision.updated_summary:
                    processed.summary = decision.updated_summary
                if decision.regenerate_image:
                    print("Generando una nueva imagen...")
                    processed.image_url = self.processor.generate_image(
                        title=processed.title,
                        description=processed.summary,
                    )
                print("Se actualizó la previsualización. Vuelve a revisar los datos.")

    def run_once(self) -> None:
        print("📡 Recuperando mensajes desde Telegram...")
        messages = self.monitor.fetch_messages_sync(since_id=self.state.last_message_id)
        if not messages:
            print("No hay mensajes nuevos.")
            return

        urls_to_process: List[str] = []
        for message in messages:
            urls = extract_urls(message.text)
            urls_to_process.extend(urls)
            self.state.last_message_id = message.id

        unique_urls = deduplicate(urls_to_process)
        if not unique_urls:
            print("Los mensajes nuevos no contienen URLs.")
            self.state.save(self.settings.state_file)
            return

        print(f"Se encontraron {len(unique_urls)} URLs para procesar.")

        for url in unique_urls:
            try:
                processed = self.processor.process(url)
            except Exception as error:
                print(f"Error procesando {url}: {error}")
                continue

            reviewed = self._review(processed)
            if not reviewed:
                print("Publicación descartada por el usuario.")
                continue

            payload = asdict(reviewed)
            print("Publicando en la aplicación web...")
            try:
                created = self.publisher.publish(payload)
                print(f"✅ Publicación creada con ID {created.get('id')}")
            except Exception as error:
                print(f"Error al publicar el contenido: {error}")

        self.state.save(self.settings.state_file)


def run_workflow(settings: Optional[Settings] = None) -> None:
    settings = settings or Settings()
    workflow = MonitoringWorkflow(settings)
    workflow.run_once()
