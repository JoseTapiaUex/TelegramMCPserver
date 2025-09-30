#!/usr/bin/env python3
"""
🤖 Telegram Monitor - Agente de Monitoreo Inteligente
Monitor de grupos de Telegram con detección automática de URLs
Desarrollado para curso de Programación Asistido por IA
"""

import subprocess
import json
import logging
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import re
from pathlib import Path

# Configuración desde variables de entorno
# ⚠️ IMPORTANTE: Define estas variables en tu archivo .env
TG_APP_ID = os.getenv("TG_APP_ID")
TG_API_HASH = os.getenv("TG_API_HASH")
TARGET_CHAT = os.getenv("TARGET_CHAT")  # Formato: cht[CHAT_ID] o nombre del grupo

# Validar que las credenciales estén configuradas
if not TG_APP_ID or not TG_API_HASH:
    print("❌ ERROR: TG_APP_ID y TG_API_HASH son requeridos")
    print("📝 Crea un archivo .env basado en .env.example con tus credenciales")
    exit(1)

if not TARGET_CHAT:
    print("❌ ERROR: TARGET_CHAT es requerido")
    print("📝 Define TARGET_CHAT en tu archivo .env (formato: cht[ID] o nombre del grupo)")
    exit(1)
MONITORING_INTERVAL = int(os.getenv("MONITORING_INTERVAL", "60"))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('telegram_monitor.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class SimpleTelegramMonitor:
    """Monitor simple de Telegram usando MCP"""
    
    def __init__(self):
        self.app_id = TG_APP_ID
        self.api_hash = TG_API_HASH
        self.target_chat = TARGET_CHAT
        self.processed_messages = set()  # Para evitar duplicados
        
        # Crear directorio de resultados
        os.makedirs("results", exist_ok=True)
    
    def start_monitoring(self):
        """Inicia el monitoreo continuo"""
        logger.info("🚀 Iniciando monitoreo simple de Telegram")
        logger.info(f"🎯 Chat objetivo: {self.target_chat}")
        logger.info(f"⏰ Intervalo: {MONITORING_INTERVAL} segundos")
        
        while True:
            try:
                logger.info("🔄 Buscando nuevos mensajes...")
                messages = self.get_messages_from_chat()
                
                if messages:
                    logger.info(f"📨 Encontrados {len(messages)} mensajes")
                    self.process_messages(messages)
                else:
                    logger.info("📭 No hay mensajes nuevos")
                
                logger.info(f"⏰ Esperando {MONITORING_INTERVAL} segundos...")
                time.sleep(MONITORING_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("👋 Deteniendo monitoreo...")
                break
            except Exception as e:
                logger.error(f"❌ Error en monitoreo: {e}")
                time.sleep(10)  # Esperar antes de reintentar
    
    def get_messages_from_chat(self) -> List[Dict[str, Any]]:
        """Obtiene mensajes del chat usando MCP"""
        try:
            # Buscar npx
            import shutil
            npx_path = shutil.which("npx")
            if not npx_path:
                logger.error("❌ NPX no encontrado")
                return []
            
            # Preparar entorno
            env = os.environ.copy()
            env.update({
                "TG_APP_ID": self.app_id,
                "TG_API_HASH": self.api_hash
            })
            
            # Comando MCP
            cmd = [npx_path, "@chaindead/telegram-mcp", "--app-id", self.app_id, "--api-hash", self.api_hash]
            
            # Ejecutar proceso MCP
            process = subprocess.Popen(
                cmd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                # Inicializar protocolo MCP
                init_msg = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "simple-monitor", "version": "1.0"}
                    }
                }
                
                process.stdin.write(json.dumps(init_msg) + '\n')
                process.stdin.flush()
                
                # Leer respuesta de inicialización
                init_response = process.stdout.readline()
                if not init_response:
                    logger.warning("⚠️ No se recibió respuesta de inicialización")
                    return []
                
                # Solicitar mensajes del chat
                chat_msg = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "tg_dialog",
                        "arguments": {
                            "name": self.target_chat
                        }
                    }
                }
                
                process.stdin.write(json.dumps(chat_msg) + '\n')
                process.stdin.flush()
                
                # Leer respuesta de mensajes
                chat_response = process.stdout.readline()
                if chat_response:
                    response_data = json.loads(chat_response.strip())
                    
                    if 'result' in response_data and response_data['result']:
                        return self.parse_messages(response_data['result'])
                    else:
                        logger.info("📭 No hay mensajes nuevos")
                        return []
                else:
                    logger.warning("⚠️ No se pudo conectar al chat")
                
            finally:
                process.stdin.close()
                process.terminate()
                process.wait(timeout=3)
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo mensajes: {e}")
            return []
    
    def parse_messages(self, result_data) -> List[Dict[str, Any]]:
        """Parsea la respuesta del MCP"""
        messages = []
        
        try:
            # Manejar el formato de respuesta del MCP
            if isinstance(result_data, dict) and 'content' in result_data:
                for item in result_data['content']:
                    if item.get('type') == 'text':
                        try:
                            # Parsear el JSON interno
                            chat_data = json.loads(item['text'])
                            if 'messages' in chat_data:
                                telegram_messages = chat_data['messages']
                                
                                for msg in telegram_messages:
                                    msg_id = f"{msg.get('when', '')}_{hash(msg.get('text', ''))}"
                                    
                                    # Evitar duplicados
                                    if msg_id in self.processed_messages:
                                        continue
                                    
                                    text = msg.get('text', '')
                                    urls = self.extract_urls(text)
                                    
                                    if urls:  # Solo mensajes con URLs
                                        message = {
                                            'id': msg_id,
                                            'text': text,
                                            'date': msg.get('when', datetime.now().isoformat()),
                                            'from': msg.get('who', 'unknown'),
                                            'urls': urls,
                                            'chat': self.target_chat
                                        }
                                        messages.append(message)
                                        self.processed_messages.add(msg_id)
                                        
                                        logger.info(f"🔗 Nueva URL de {message['from']}: {urls[0]}")
                        except json.JSONDecodeError:
                            logger.warning(f"⚠️ No se pudo parsear contenido: {item['text'][:100]}...")
            
        except Exception as e:
            logger.error(f"❌ Error parseando mensajes: {e}")
        
        return messages
    
    def extract_urls(self, text: str) -> List[str]:
        """Extrae URLs del texto"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def process_messages(self, messages: List[Dict[str, Any]]):
        """Procesa los mensajes encontrados"""
        for message in messages:
            try:
                # Guardar mensaje en archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"results/message_{timestamp}_{message['id'][:8]}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(message, f, indent=2, ensure_ascii=False)
                
                logger.info(f"💾 Mensaje guardado: {filename}")
                
                # Procesar cada URL
                for url in message['urls']:
                    self.process_url(url, message)
                    
            except Exception as e:
                logger.error(f"❌ Error procesando mensaje: {e}")
    
    def process_url(self, url: str, message: Dict[str, Any]):
        """Procesa una URL individual"""
        try:
            logger.info(f"🌐 Procesando URL: {url}")
            
            # Aquí podrías agregar scraping real si quieres
            # Por ahora solo lo registramos
            
            url_info = {
                'url': url,
                'found_in_message': message['id'],
                'from_user': message['from'],
                'timestamp': datetime.now().isoformat(),
                'status': 'detected'
            }
            
            # Guardar info de URL
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            url_filename = f"results/url_{timestamp}_{hash(url) % 10000}.json"
            
            with open(url_filename, 'w', encoding='utf-8') as f:
                json.dump(url_info, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🔗 URL procesada y guardada: {url_filename}")
            
        except Exception as e:
            logger.error(f"❌ Error procesando URL {url}: {e}")

def main():
    """Función principal"""
    monitor = SimpleTelegramMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main()