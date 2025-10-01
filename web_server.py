#!/usr/bin/env python3
"""
🌐 Telegram Monitor - Servidor Web
Interfaz web para visualizar y controlar el monitoreo de Telegram
Basado en el monitor simple que ya funciona correctamente
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import json
import logging
import os
import shutil
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv, set_key
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

def check_configuration():
    """Verificar si la configuración básica está completa"""
    env_file = Path('.env')
    if not env_file.exists():
        return False, "missing_env", "Archivo .env no existe"
    
    load_dotenv()
    # Solo requerimos credenciales, TARGET_CHAT ahora es opcional (selección dinámica)
    required_vars = ['TG_APP_ID', 'TG_API_HASH', 'TG_PHONE']
    
    for var in required_vars:
        if not os.getenv(var):
            return False, "needs_setup", f"Variable {var} no está configurada"
    
    return True, "configured", "Configuración de credenciales completa"

def check_credentials_only():
    """Verificar solo si tenemos credenciales (sin TARGET_CHAT)"""
    env_file = Path('.env')
    if not env_file.exists():
        return False, None, None, None
    
    load_dotenv()
    api_id = os.getenv('TG_APP_ID')
    api_hash = os.getenv('TG_API_HASH')
    phone = os.getenv('TG_PHONE')
    
    if api_id and api_hash and phone:
        return True, api_id, api_hash, phone
    
    return False, None, None, None

def ensure_mcp_authentication():
    """Asegurar que MCP esté autenticado usando credenciales de .env"""
    has_creds, api_id, api_hash, phone = check_credentials_only()
    
    if not has_creds:
        logger.error("❌ No se encontraron credenciales en .env")
        return False, "No se encontraron credenciales en .env"
    
    logger.info("🔐 Autenticando MCP con credenciales de .env...")
    return authenticate_telegram_mcp(api_id, api_hash, phone)

def authenticate_telegram_mcp(api_id, api_hash, phone):
    """Autenticar con el servidor MCP de Telegram"""
    try:
        # Verificar que npx esté disponible
        npx_path = shutil.which("npx")
        if not npx_path:
            return False, "NPX no está instalado. Instala Node.js primero."
        
        # Preparar comando de autenticación
        cmd = [
            npx_path, 
            "-y", 
            "@chaindead/telegram-mcp", 
            "auth",
            "--app-id", str(api_id),
            "--api-hash", str(api_hash),
            "--phone", str(phone)
        ]
        
        logger.info(f"🔑 Ejecutando autenticación MCP...")
        
        # Ejecutar comando de autenticación
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # Timeout de 60 segundos
        )
        
        if result.returncode == 0:
            logger.info("✅ Autenticación MCP exitosa")
            return True, "Autenticación exitosa"
        else:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Error desconocido"
            logger.error(f"❌ Error en autenticación MCP: {error_msg}")
            return False, f"Error de autenticación: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return False, "Timeout en autenticación. El proceso tomó demasiado tiempo."
    except Exception as e:
        logger.error(f"❌ Excepción en autenticación MCP: {e}")
        return False, f"Error interno: {str(e)}"

class WebTelegramMonitor(SimpleTelegramMonitor):
    """Extensión del monitor simple para uso con interfaz web"""
    
    def __init__(self, target_chat=None):
        # Si no se proporciona target_chat, intentar obtenerlo del .env (retrocompatibilidad)
        if target_chat is None:
            load_dotenv()
            target_chat = os.getenv('TARGET_CHAT')
        
        # Establecer temporalmente TARGET_CHAT para SimpleTelegramMonitor
        if target_chat:
            os.environ['TARGET_CHAT'] = target_chat
            
        super().__init__()
        self.target_chat = target_chat
        self.latest_messages = []
        self.latest_urls = []
        self.stats = {
            'total_messages': 0,
            'total_urls': 0,
            'last_check': None,
            'status': 'stopped',
            'target_chat': target_chat
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
    """Iniciar el monitoreo con chat seleccionado dinámicamente"""
    global monitor, monitor_thread, monitor_running
    
    if monitor_running:
        return jsonify({'success': False, 'message': 'Monitor ya está corriendo'})
    
    try:
        # Obtener chat seleccionado del request
        data = request.json or {}
        target_chat = data.get('target_chat')
        
        if not target_chat:
            return jsonify({'success': False, 'message': 'Debes seleccionar un chat para monitorear'})
        
        # Verificar configuración básica (credenciales)
        is_configured, status, message = check_configuration()
        if status != "configured":
            return jsonify({'success': False, 'message': f'Configuración incompleta: {message}'})
        
        # Asegurar autenticación MCP antes de iniciar
        auth_success, auth_message = ensure_mcp_authentication()
        if not auth_success:
            return jsonify({'success': False, 'message': f'Error de autenticación MCP: {auth_message}'})
        
        # Crear monitor con el chat seleccionado dinámicamente
        monitor = WebTelegramMonitor(target_chat=target_chat)
        monitor_running = True
        
        monitor_thread = threading.Thread(target=monitor.start_monitoring_web)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        logger.info(f"🚀 Monitor iniciado para chat: {target_chat}")
        return jsonify({'success': True, 'message': f'Monitor iniciado para el chat seleccionado'})
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

@app.route('/api/reload-config', methods=['POST'])
def reload_config():
    """Recargar configuración y reautenticar MCP después del setup"""
    try:
        logger.info("🔄 Recargando configuración...")
        
        # Verificar que existe el archivo .env
        if not os.path.exists('.env'):
            return jsonify({
                'success': False, 
                'message': 'No se encontró el archivo .env. Completa el setup primero.'
            })
        
        # Recargar variables de entorno
        from dotenv import load_dotenv
        load_dotenv(override=True)
        logger.info("📋 Variables de entorno recargadas")
        
        # Verificar que tenemos las credenciales necesarias
        has_creds, api_id, api_hash, phone = check_credentials_only()
        if not has_creds:
            return jsonify({
                'success': False, 
                'message': 'Credenciales incompletas en .env'
            })
        
        # Reautenticar MCP con las nuevas credenciales
        logger.info("🔐 Reautenticando MCP...")
        success, message = authenticate_telegram_mcp(api_id, api_hash, phone)
        
        if success:
            logger.info("✅ Configuración recargada y MCP reautenticado correctamente")
            return jsonify({
                'success': True, 
                'message': 'Configuración recargada correctamente. El monitoreo está listo para usar.'
            })
        else:
            logger.error(f"❌ Error en reautenticación MCP: {message}")
            return jsonify({
                'success': False, 
                'message': f'Error al reautenticar MCP: {message}'
            })
            
    except Exception as e:
        logger.error(f"❌ Error al recargar configuración: {e}")
        return jsonify({
            'success': False, 
            'message': f'Error al recargar configuración: {str(e)}'
        })

# Rutas de configuración
@app.route('/api/setup/verify-credentials', methods=['POST'])
def verify_credentials():
    """Verificar credenciales de Telegram y autenticar MCP"""
    try:
        data = request.json
        api_id = data.get('api_id')
        api_hash = data.get('api_hash')
        phone = data.get('phone')
        
        if not all([api_id, api_hash, phone]):
            return jsonify({
                'success': False,
                'message': 'Faltan credenciales requeridas'
            })
        
        # Ejecutar autenticación MCP
        auth_success, auth_message = authenticate_telegram_mcp(api_id, api_hash, phone)
        
        if not auth_success:
            return jsonify({
                'success': False,
                'message': f'Error de autenticación MCP: {auth_message}'
            })
        
        # Guardar credenciales temporalmente en variables de entorno
        # para las siguientes operaciones
        os.environ['TG_APP_ID'] = str(api_id)
        os.environ['TG_API_HASH'] = str(api_hash)
        os.environ['TG_PHONE'] = str(phone)
        
        # Si llegamos aquí, la autenticación fue exitosa
        return jsonify({
            'success': True,
            'message': 'Credenciales verificadas y autenticación MCP exitosa'
        })
        
    except Exception as e:
        logger.error(f"Error verificando credenciales: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al verificar credenciales: {str(e)}'
        })

@app.route('/api/setup/get-chats')
def get_chats():
    """Obtener lista de chats disponibles"""
    try:
        # Verificar si tenemos credenciales en .env
        has_creds, api_id, api_hash, phone = check_credentials_only()
        
        if has_creds:
            # Usar credenciales de .env
            # Asegurar autenticación MCP primero
            auth_success, auth_message = ensure_mcp_authentication()
            if not auth_success:
                return jsonify({
                    'success': False,
                    'message': f'Error de autenticación MCP: {auth_message}'
                })
            
            temp_monitor = SimpleTelegramMonitor(api_id, api_hash)
        else:
            # Usar credenciales temporales de variables de entorno
            temp_monitor = SimpleTelegramMonitor()
        
        # Obtener lista de chats
        chats = temp_monitor.get_available_chats()
        
        return jsonify({
            'success': True,
            'chats': chats
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo chats: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al obtener chats: {str(e)}'
        })

@app.route('/api/chats')
def get_available_chats():
    """Obtener lista de chats disponibles para el dashboard"""
    try:
        # Verificar si tenemos credenciales
        has_creds, api_id, api_hash, phone = check_credentials_only()
        
        if not has_creds:
            return jsonify({
                'success': False,
                'message': 'No hay credenciales configuradas. Completa el setup primero.'
            })
        
        # Asegurar autenticación MCP
        auth_success, auth_message = ensure_mcp_authentication()
        if not auth_success:
            return jsonify({
                'success': False,
                'message': f'Error de autenticación MCP: {auth_message}'
            })
        
        # Crear monitor temporal para obtener chats
        temp_monitor = SimpleTelegramMonitor(api_id, api_hash)
        
        # Obtener lista de chats
        chats = temp_monitor.get_available_chats()
        
        return jsonify({
            'success': True,
            'chats': chats
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo chats para dashboard: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al obtener chats: {str(e)}'
        })

@app.route('/api/setup/save-config', methods=['POST'])
def save_config():
    """Guardar credenciales básicas en archivo .env (sin TARGET_CHAT para flexibilidad)"""
    try:
        logger.info("💾 Guardando credenciales en .env (sin TARGET_CHAT)")
        
        # Crear archivo .env con la configuración
        env_file = Path('.env')
        
        # Verificar si ya tenemos credenciales en .env (para caso de actualización)
        has_existing_creds, existing_api_id, existing_api_hash, existing_phone = check_credentials_only()
        
        if has_existing_creds:
            # Usar credenciales existentes de .env
            api_id = existing_api_id
            api_hash = existing_api_hash  
            phone = existing_phone
            logger.info("📋 Usando credenciales existentes de .env")
        else:
            # Obtener credenciales de las variables de entorno temporales
            api_id = os.getenv('TG_APP_ID')
            api_hash = os.getenv('TG_API_HASH')
            phone = os.getenv('TG_PHONE')
            logger.info("🔄 Usando credenciales temporales")
        
        # Verificar que tenemos todas las credenciales necesarias
        if not all([api_id, api_hash, phone]):
            missing = []
            if not api_id: missing.append('TG_APP_ID')
            if not api_hash: missing.append('TG_API_HASH')  
            if not phone: missing.append('TG_PHONE')
            
            logger.error(f"❌ Faltan credenciales: {missing}")
            return jsonify({
                'success': False,
                'message': f'Faltan credenciales requeridas: {", ".join(missing)}'
            })
        
        # Crear contenido del .env (SIN TARGET_CHAT para selección dinámica)
        env_content = f"""# 🔐 Variables de entorno para Telegram Monitor Agent
# Generado automáticamente por la configuración web

# Credenciales de Telegram API
TG_APP_ID={api_id}
TG_API_HASH={api_hash}
TG_PHONE={phone}

# Configuración opcional
MONITORING_INTERVAL=60
MAX_MESSAGES_PER_CHECK=50

# Base de datos
DB_PATH=data/posts.db

# Servidor web
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=true

# Nota: TARGET_CHAT se selecciona dinámicamente en el dashboard
"""
        
        # Escribir archivo .env
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        logger.info(f"✅ Credenciales guardadas en {env_file} - TARGET_CHAT será selección dinámica")
        
        return jsonify({
            'success': True,
            'message': 'Credenciales guardadas correctamente'
        })
        
    except Exception as e:
        logger.error(f"Error guardando configuración: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al guardar configuración: {str(e)}'
        })

@app.route('/setup')
def setup():
    """Página de configuración"""
    # Verificar qué necesitamos configurar
    has_creds, api_id, api_hash, phone = check_credentials_only()
    
    setup_data = {
        'has_credentials': has_creds,
        'needs_target_chat': False  # Ya no necesitamos TARGET_CHAT en .env
    }
    
    if has_creds:
        # Tenemos credenciales, redirigir al dashboard donde se seleccionará el chat dinámicamente
        return redirect(url_for('index'))
    
    return render_template('setup.html', **setup_data)

# Ruta principal
@app.route('/')
def index():
    """Página principal"""
    # Verificar configuración básica (solo credenciales)
    is_configured, status, message = check_configuration()
    
    if status == "needs_setup":
        # Faltan credenciales básicas - ir a setup
        return redirect(url_for('setup'))
    elif status == "configured":
        # Tenemos credenciales básicas - mostrar dashboard con selector de chat
        auth_success, auth_message = ensure_mcp_authentication()
        if not auth_success:
            logger.warning(f"⚠️ Error de autenticación MCP: {auth_message}")
            # Aún mostrar dashboard pero con advertencia
        else:
            logger.info("✅ MCP autenticado correctamente")
        
        return render_template('index.html')
    
    # Fallback a setup
    return redirect(url_for('setup'))

if __name__ == '__main__':
    print("🌐 Iniciando servidor web del monitor de Telegram")
    
    # Verificar configuración
    is_configured, status, message = check_configuration()
    
    if status == "needs_setup":
        print(f"⚠️ {message}")
        print("🔗 Abre http://localhost:5000/setup para configurar")
    elif status == "configured":
        print("✅ Configuración encontrada")
        
        # Intentar autenticación MCP automática
        auth_success, auth_message = ensure_mcp_authentication()
        if auth_success:
            print("🔐 Autenticación MCP exitosa")
            print("🔗 Dashboard disponible en: http://localhost:5000")
        else:
            print(f"⚠️ Advertencia de autenticación MCP: {auth_message}")
            print("🔗 Dashboard disponible en: http://localhost:5000 (con limitaciones)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)