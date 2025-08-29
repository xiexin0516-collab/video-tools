#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Tools Platform - Flask Backend API
"""

import os
import json
import jwt
import requests
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
app.config['SUPABASE_SERVICE_ROLE'] = os.getenv('SUPABASE_SERVICE_ROLE')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 启用CORS
CORS(app, origins=['*'])

# JWT验证装饰器
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': '缺少认证令牌'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            # 验证JWT令牌
            payload = jwt.decode(
                token, 
                options={"verify_signature": False}
            )
            request.user_id = payload.get('sub')
            return f(*args, **kwargs)
        except jwt.InvalidTokenError:
            return jsonify({'error': '无效的认证令牌'}), 401
    
    return decorated_function

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok', 
        'message': '服务运行正常',
        'timestamp': datetime.now().isoformat()
    })

# 用户认证相关API
@app.route('/api/auth/profile', methods=['GET'])
@require_auth
def get_user_profile():
    """获取用户信息"""
    try:
        # 这里可以调用Supabase API获取用户详细信息
        return jsonify({
            'user_id': request.user_id,
            'message': '用户信息获取成功'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 项目管理API
@app.route('/api/projects', methods=['GET'])
@require_auth
def get_projects():
    """获取用户项目列表"""
    try:
        # 这里应该从数据库获取项目列表
        # 暂时返回模拟数据
        projects = [
            {
                'id': 1,
                'name': '示例项目',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]
        return jsonify({'projects': projects})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
@require_auth
def create_project():
    """创建新项目"""
    try:
        data = request.get_json()
        project_name = data.get('name', '未命名项目')
        
        # 这里应该保存到数据库
        new_project = {
            'id': uuid.uuid4().int % 1000000,
            'name': project_name,
            'user_id': request.user_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'message': '项目创建成功',
            'project': new_project
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
@require_auth
def get_project(project_id):
    """获取单个项目"""
    try:
        # 这里应该从数据库获取项目
        project = {
            'id': project_id,
            'name': f'项目 {project_id}',
            'user_id': request.user_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return jsonify({'project': project})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@require_auth
def update_project(project_id):
    """更新项目"""
    try:
        data = request.get_json()
        # 这里应该更新数据库
        return jsonify({'message': '项目更新成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@require_auth
def delete_project(project_id):
    """删除项目"""
    try:
        # 这里应该从数据库删除项目
        return jsonify({'message': '项目删除成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 文件上传API
@app.route('/api/upload', methods=['POST'])
@require_auth
def upload_file():
    """文件上传"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            # 添加时间戳避免文件名冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            return jsonify({
                'message': '文件上传成功',
                'filename': filename,
                'file_path': file_path
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 字幕处理API
@app.route('/api/subtitles/generate', methods=['POST'])
@require_auth
def generate_subtitles():
    """生成字幕"""
    try:
        data = request.get_json()
        audio_file = data.get('audio_file')
        
        # 这里应该调用语音识别API生成字幕
        # 暂时返回模拟数据
        subtitles = [
            {
                'id': 1,
                'start_time': 0.0,
                'end_time': 2.5,
                'text': '欢迎使用视频工具平台'
            },
            {
                'id': 2,
                'start_time': 2.5,
                'end_time': 5.0,
                'text': '这是一个专业的视频处理工具'
            }
        ]
        
        return jsonify({
            'message': '字幕生成成功',
            'subtitles': subtitles
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subtitles/export', methods=['POST'])
@require_auth
def export_subtitles():
    """导出字幕"""
    try:
        data = request.get_json()
        subtitles = data.get('subtitles', [])
        format_type = data.get('format', 'srt')
        
        # 这里应该根据格式生成字幕文件
        if format_type == 'srt':
            content = ""
            for i, subtitle in enumerate(subtitles, 1):
                start_time = subtitle.get('start_time', 0)
                end_time = subtitle.get('end_time', 0)
                text = subtitle.get('text', '')
                
                content += f"{i}\n"
                content += f"{start_time:.3f} --> {end_time:.3f}\n"
                content += f"{text}\n\n"
        
        return jsonify({
            'message': '字幕导出成功',
            'content': content,
            'format': format_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 静态文件服务
@app.route('/')
def index():
    """主页"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/subtitle-editor/')
def subtitle_editor():
    """字幕编辑器"""
    return send_from_directory('../frontend/subtitle-editor', 'index.html')

# 通用静态文件路由
@app.route('/<path:filename>')
def static_files(filename):
    """静态文件"""
    return send_from_directory('../frontend', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    """JavaScript文件"""
    return send_from_directory('../frontend/js', filename)

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
