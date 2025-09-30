#!/usr/bin/env python3
"""
🌐 Telegram Monitor - Servidor Web
Interfaz web para visualizar y controlar el monitoreo de Telegram
Basado en el monitor simple que ya funciona correctamente
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from simple_monitor import SimpleTelegramMonitor

# Configurar Flask
app = Flask(__name__, 
           template_folder='web',
           static_folder='web/static')
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Monitor global
monitor = None
monitor_thread = None
monitor_running = False

class WebTelegramMonitor(SimpleTelegramMonitor):
    """Extensión del monitor simple para uso con interfaz web"""
    
    def __init__(self):
        super().__init__()
        self.latest_messages = []
        self.latest_urls = []
        self.stats = {
            'total_messages': 0,
            'total_urls': 0,
            'last_check': None,
            'status': 'stopped'
        }
    
    def process_messages(self, messages):
        """Override para actualizar datos para la web"""
        super().process_messages(messages)
        
        # Actualizar datos para la interfaz web
        self.latest_messages = messages[-10:]  # Últimos 10 mensajes
        
        # Extraer URLs recientes
        urls = []
        for msg in messages:
            for url in msg.get('urls', []):
                urls.append({
                    'url': url,
                    'from': msg['from'],
                    'date': msg['date'],
                    'message_text': msg['text'][:100] + '...' if len(msg['text']) > 100 else msg['text']
                })
        self.latest_urls = urls[-20:]  # Últimas 20 URLs
        
        # Actualizar estadísticas
        self.stats['total_messages'] += len(messages)
        self.stats['total_urls'] += len(urls)
        self.stats['last_check'] = datetime.now().isoformat()
        self.stats['status'] = 'running'

    def start_monitoring_web(self):
        """Versión del monitoreo para uso web (sin loop infinito)"""
        global monitor_running
        
        logger.info("🚀 Iniciando monitoreo para interfaz web")
        self.stats['status'] = 'running'
        
        while monitor_running:
            try:
                logger.info("🔄 Revisando mensajes...")
                messages = self.get_messages_from_chat()
                
                if messages:
                    logger.info(f"📨 Encontrados {len(messages)} mensajes")
                    self.process_messages(messages)
                
                # Esperar intervalo
                import time
                time.sleep(60)  # Revisar cada minuto
                
            except Exception as e:
                logger.error(f"❌ Error en monitoreo web: {e}")
                self.stats['status'] = 'error'
                import time
                time.sleep(10)

# Rutas API
@app.route('/api/status')
def get_status():
    """Obtener estado actual del monitor"""
    global monitor
    
    if not monitor:
        return jsonify({
            'status': 'stopped',
            'total_messages': 0,
            'total_urls': 0,
            'last_check': None
        })
    
    return jsonify(monitor.stats)

@app.route('/api/messages')
def get_messages():
    """Obtener mensajes recientes"""
    global monitor
    
    if not monitor:
        return jsonify([])
    
    return jsonify(monitor.latest_messages)

@app.route('/api/urls')
def get_urls():
    """Obtener URLs recientes"""
    global monitor
    
    if not monitor:
        return jsonify([])
    
    return jsonify(monitor.latest_urls)

@app.route('/api/start', methods=['POST'])
def start_monitoring():
    """Iniciar el monitoreo"""
    global monitor, monitor_thread, monitor_running
    
    if monitor_running:
        return jsonify({'success': False, 'message': 'Monitor ya está corriendo'})
    
    try:
        monitor = WebTelegramMonitor()
        monitor_running = True
        
        monitor_thread = threading.Thread(target=monitor.start_monitoring_web)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return jsonify({'success': True, 'message': 'Monitor iniciado'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    """Detener el monitoreo"""
    global monitor_running, monitor
    
    monitor_running = False
    
    if monitor:
        monitor.stats['status'] = 'stopped'
    
    return jsonify({'success': True, 'message': 'Monitor detenido'})

# Ruta principal
@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

if __name__ == '__main__':
    print("🌐 Iniciando servidor web del monitor de Telegram")
    print("🔗 Accede a: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)