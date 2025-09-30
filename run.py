#!/usr/bin/env python3
"""
🚀 Telegram Monitor - Script de Inicio
Launcher principal para el sistema de monitoreo de Telegram
"""

import sys
import subprocess
import argparse
import os
from pathlib import Path

def check_env_config():
    """Verificar si la configuración está completa"""
    env_file = Path('.env')
    if not env_file.exists():
        return False
    
    # Cargar variables de entorno
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['TG_APP_ID', 'TG_API_HASH', 'TG_PHONE', 'TARGET_CHAT']
        
        for var in required_vars:
            if not os.getenv(var):
                return False
        
        return True
    except ImportError:
        print("❌ Error: python-dotenv no está instalado")
        return False

def run_cli_monitor():
    """Ejecutar monitor en modo consola"""
    print("🤖 Iniciando Telegram Monitor - Modo CLI")
    print("📡 Monitoreo en consola sin interfaz web")
    
    # Verificar configuración
    if not check_env_config():
        print("❌ Configuración incompleta. Usa modo web (--web) para configurar.")
        return
    
    print("🔄 Presiona Ctrl+C para detener\n")
    
    try:
        subprocess.run([sys.executable, "simple_monitor.py"])
    except KeyboardInterrupt:
        print("\n👋 Monitor detenido")
    except FileNotFoundError:
        print("❌ Error: No se encontró simple_monitor.py")

def run_web_server():
    """Ejecutar servidor web con dashboard"""
    print("🌐 Iniciando Telegram Monitor - Modo Web")
    print("📊 Dashboard disponible en: http://localhost:5000")
    print("🔄 Presiona Ctrl+C para detener\n")
    
    try:
        subprocess.run([sys.executable, "web_server.py"])
    except KeyboardInterrupt:
        print("\n👋 Servidor web detenido")
    except FileNotFoundError:
        print("❌ Error: No se encontró web_server.py")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="🤖 Telegram Monitor - Agente de Monitoreo Inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python run.py           # Modo CLI (consola)
  python run.py --web     # Modo Web (dashboard)
  
Proyecto desarrollado para curso de Programación Asistido por IA
        """
    )
    
    parser.add_argument(
        "--web", 
        action="store_true",
        help="Iniciar en modo web con dashboard"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🤖 TELEGRAM MONITOR - AGENTE DE MONITOREO INTELIGENTE")
    print("=" * 60)
    
    if args.web:
        run_web_server()
    else:
        run_cli_monitor()

if __name__ == "__main__":
    main()