#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SubtitleEditor Web - Multi-language Video Tool Platform
Flask backend for subtitle editing web application with user authentication
"""

import os
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Import database and models
from models import db, User, Project

# Import blueprints
from auth import auth_bp
from projects import projects_bp
from admin import admin_bp

# Import subtitle parser service
from services.subtitle_parser import SubtitleParser

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-this')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///subtitle_editor.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['STATIC_FOLDER'] = '../static'
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    db.init_app(app)
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize subtitle parser
    subtitle_parser = SubtitleParser()
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Supported file types
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'aac'}
    ALLOWED_SUBTITLE_EXTENSIONS = {'srt', 'txt'}
    
    def allowed_audio_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS
    
    def allowed_subtitle_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_SUBTITLE_EXTENSIONS
    
    # Routes
    @app.route('/')
    def index():
        """Serve the main application page"""
        frontend_dir = '../frontend'
        return send_from_directory(frontend_dir, 'index.html')
    
    @app.route('/login')
    def login():
        """Serve the login page"""
        frontend_dir = '../frontend'
        return send_from_directory(frontend_dir, 'login.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Serve the dashboard page"""
        frontend_dir = '../frontend'
        return send_from_directory(frontend_dir, 'dashboard.html')
    
    @app.route('/admin')
    def admin():
        """Serve the admin page"""
        frontend_dir = '../frontend'
        return send_from_directory(frontend_dir, 'admin.html')
    
    @app.route('/api/languages')
    def get_languages():
        """Get available languages for the interface"""
        return jsonify({
            'languages': [
                {'code': 'en', 'name': 'English', 'native': 'English'},
                {'code': 'zh', 'name': 'Chinese', 'native': '中文'}
            ]
        })
    
    @app.route('/api/upload/audio', methods=['POST'])
    def upload_audio():
        """Upload audio file"""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_audio_file(file.filename):
                return jsonify({'error': 'Unsupported audio format'}), 400
            
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            file.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': unique_filename,
                'original_name': filename,
                'message': 'Audio file uploaded successfully'
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/upload/subtitle', methods=['POST'])
    def upload_subtitle():
        """Upload subtitle file"""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_subtitle_file(file.filename):
                return jsonify({'error': 'Unsupported subtitle format'}), 400
            
            # Read and parse subtitle file
            content = file.read().decode('utf-8')
            subtitles = subtitle_parser.parse_subtitle_file(content, file.filename)
            
            return jsonify({
                'success': True,
                'subtitles': subtitles,
                'filename': file.filename,
                'message': 'Subtitle file parsed successfully'
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/subtitles/parse', methods=['POST'])
    def parse_subtitles():
        """Parse subtitle text content"""
        try:
            data = request.get_json()
            content = data.get('content', '')
            format_type = data.get('format', 'srt')
            
            subtitles = subtitle_parser.parse_subtitle_content(content, format_type)
            
            return jsonify({
                'success': True,
                'subtitles': subtitles
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/subtitles/export', methods=['POST'])
    def export_subtitles():
        """Export subtitles to SRT or TXT format"""
        try:
            data = request.get_json()
            subtitles = data.get('subtitles', [])
            format_type = data.get('format', 'srt')
            
            content = subtitle_parser.export_subtitles(subtitles, format_type)
            
            return jsonify({
                'success': True,
                'content': content,
                'format': format_type
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """Serve static files"""
        return send_from_directory(app.config['STATIC_FOLDER'], filename)
    
    @app.route('/uploads/<path:filename>')
    def uploaded_files(filename):
        """Serve uploaded files"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/<path:filename>')
    def serve_frontend(filename):
        """Serve frontend files (catch-all for SPA routing)"""
        frontend_dir = '../frontend'
        return send_from_directory(frontend_dir, 'index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create app instance
app = create_app()

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
