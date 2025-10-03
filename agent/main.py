"""Command line entry point for the Telegram monitoring agent."""
from __future__ import annotations

import argparse

from .config import settings
from .workflow import run_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Agente de monitoreo de Telegram")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Ejecuta el flujo una única vez (por defecto)",
    )
    _ = parser.parse_args()
    run_workflow(settings)


if __name__ == "__main__":
    main()
