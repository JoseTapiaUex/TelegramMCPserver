"""Console-based preview and approval workflow."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .url_processor import ProcessedURL


@dataclass
class PreviewDecision:
    status: str
    updated_title: Optional[str] = None
    updated_summary: Optional[str] = None
    regenerate_image: bool = False


class PreviewConsole:
    def present(self, processed: ProcessedURL) -> PreviewDecision:
        print("\n" + "=" * 80)
        print("PREVISUALIZACIÓN DEL POST")
        print("Título:", processed.title)
        print("Resumen:", processed.summary)
        print("URL:", processed.source_url)
        print("Imagen:", processed.image_url or "(no disponible)")
        print("Proveedor:", processed.provider)
        print("Fecha de publicación:", processed.release_date)
        print("=" * 80)

        while True:
            choice = input("¿Aceptar (a), Modificar (m), Regenerar imagen (i) o Descartar (d)? ").strip().lower()
            if choice in {"a", ""}:
                return PreviewDecision(status="accepted")
            if choice == "d":
                return PreviewDecision(status="discarded")
            if choice == "i":
                return PreviewDecision(status="modify", regenerate_image=True)
            if choice == "m":
                new_title = input(f"Nuevo título (enter para mantener '{processed.title}'): ").strip()
                new_summary = input("Nuevo resumen (enter para mantener actual): ").strip()
                return PreviewDecision(
                    status="modify",
                    updated_title=new_title or None,
                    updated_summary=new_summary or None,
                )
            print("Opción no válida. Intenta nuevamente.")
