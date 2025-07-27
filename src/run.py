#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Aplicação Flask Principal
Análise Ultra-Detalhada de Mercado com IA Avançada
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import traceback

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importa blueprints e serviços
from routes.analysis import analysis_bp
from routes.user import user_bp
from routes.pdf_generator import pdf_bp
from services.gemini_client import GeminiClient
from services.deep_search_service import DeepSearchService
from services.attachment_service import AttachmentService

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # Cria diretório de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configuração CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))
    
    # Registra blueprints
    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(pdf_bp, url_prefix='/api')
    
    # Rota principal
    @app.route('/')
    def index():
        """Página principal da aplicação"""
        return render_template('enhanced_index.html')
    
    # Health check
    @app.route('/api/health')
    def health_check():
        """Verifica status da aplicação"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        })
    
    # Status da aplicação
    @app.route('/api/app_status')
    def app_status():
        """Retorna status detalhado dos serviços"""
        try:
            # Verifica serviços
            gemini_available = bool(os.getenv('GEMINI_API_KEY'))
            deepseek_available = bool(os.getenv('DEEPSEEK_API_KEY'))
            supabase_available = bool(os.getenv('SUPABASE_URL'))
            
            return jsonify({
                'app_name': 'ARQV30 Enhanced',
                'version': '2.0.0',
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'gemini': {'available': gemini_available},
                    'deepseek': {'available': deepseek_available},
                    'supabase': {'available': supabase_available},
                    'attachments': {'available': True}
                },
                'environment': {
                    'python_version': sys.version,
                    'flask_env': os.getenv('FLASK_ENV', 'production')
                }
            })
        except Exception as e:
            logger.error(f"Erro ao verificar status: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    # Handler de erro global
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handler global para exceções"""
        logger.error(f"Erro não tratado: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': str(e) if app.debug else 'Erro interno',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    # Handler para 404
    @app.errorhandler(404)
    def not_found(e):
        """Handler para páginas não encontradas"""
        return jsonify({
            'error': 'Recurso não encontrado',
            'message': 'O endpoint solicitado não existe',
            'timestamp': datetime.now().isoformat()
        }), 404
    
    return app

def main():
    """Função principal para executar a aplicação"""
    try:
        app = create_app()
        
        # Configurações do servidor
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV') == 'development'
        
        logger.info(f"Iniciando ARQV30 Enhanced v2.0")
        logger.info(f"Servidor: http://{host}:{port}")
        logger.info(f"Debug: {debug}")
        
        # Inicia o servidor
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
        
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()

