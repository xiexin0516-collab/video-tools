#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Tools Platform - Flask Backend (Minimal Version)
"""

import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# 启用CORS
CORS(app, origins=['*'])

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': '服务运行正常'})

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
