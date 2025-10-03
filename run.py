#!/usr/bin/env python3
"""Utilidades para ejecutar los distintos componentes del proyecto."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_backend() -> int:
    env = os.environ.copy()
    env.setdefault("FLASK_APP", "backend.app")
    command = [sys.executable, "-m", "flask", "run", "--host", "0.0.0.0", "--port", "8000"]
    return subprocess.call(command, cwd=ROOT, env=env)


def run_agent() -> int:
    command = [sys.executable, "-m", "agent.main"]
    return subprocess.call(command, cwd=ROOT)


def run_frontend(port: int) -> int:
    command = [sys.executable, "-m", "http.server", str(port), "--directory", str(ROOT / "frontend")]
    return subprocess.call(command)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launcher para Telegram Monitor Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("backend", help="Inicia el API Flask")
    subparsers.add_parser("agent", help="Ejecuta el agente IA una vez")
    frontend_parser = subparsers.add_parser("frontend", help="Sirve la interfaz web estática")
    frontend_parser.add_argument("--port", type=int, default=3000)

    args = parser.parse_args()

    if args.command == "backend":
        sys.exit(run_backend())
    if args.command == "agent":
        sys.exit(run_agent())
    if args.command == "frontend":
        sys.exit(run_frontend(args.port))


if __name__ == "__main__":
    main()
