#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SubtitleEditor Web - Multi-language Video Tool Platform
Flask backend for subtitle editing web application
"""

from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
import json
import re
from datetime import timedelta
import uuid
from werkzeug.utils import secure_filename

# Import subtitle parser service
from services.subtitle_parser import SubtitleParser

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = '../static'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize subtitle parser
subtitle_parser = SubtitleParser()

# Supported file types
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg'}
ALLOWED_SUBTITLE_EXTENSIONS = {'srt', 'txt'}

def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def allowed_subtitle_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_SUBTITLE_EXTENSIONS

@app.route('/')
def index():
    """Serve the main application page"""
    return send_from_directory('../frontend', 'index.html')

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

@app.route('/api/subtitles/save', methods=['POST'])
def save_subtitles():
    """Save subtitles to project file"""
    try:
        data = request.get_json()
        project_name = data.get('project_name', 'untitled')
        subtitles = data.get('subtitles', [])
        audio_file = data.get('audio_file', '')
        
        project_data = {
            'project_name': project_name,
            'audio_file': audio_file,
            'subtitles': subtitles,
            'created_at': str(datetime.datetime.now()),
            'version': '1.0'
        }
        
        # Save to project file
        project_filename = f"{project_name}_{uuid.uuid4().hex[:8]}.json"
        project_path = os.path.join(app.config['UPLOAD_FOLDER'], project_filename)
        
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'project_file': project_filename,
            'message': 'Project saved successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subtitles/load', methods=['POST'])
def load_subtitles():
    """Load subtitles from project file"""
    try:
        data = request.get_json()
        project_file = data.get('project_file', '')
        
        project_path = os.path.join(app.config['UPLOAD_FOLDER'], project_file)
        
        if not os.path.exists(project_path):
            return jsonify({'error': 'Project file not found'}), 404
        
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return jsonify({
            'success': True,
            'project': project_data
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Application startup is handled by run.py in the root directory
