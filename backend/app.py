#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Tools Platform - Flask Backend
Supabase Auth + PostgreSQL + Storage
"""

import os
import json
import jwt
import requests
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL', 'http://localhost')
app.config['SUPABASE_JWKS_URL'] = os.getenv('SUPABASE_JWKS_URL', 'http://localhost')
app.config['SUPABASE_SERVICE_ROLE'] = os.getenv('SUPABASE_SERVICE_ROLE', 'dummy-key')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///test.db')

# 启用CORS
CORS(app, origins=['https://vidtools.tools', 'http://localhost:3000', '*'])

# 数据库配置 - 添加错误处理
try:
    Base = declarative_base()
    engine = create_engine(app.config['DATABASE_URL'])
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = scoped_session(SessionLocal)
except Exception as e:
    print(f"数据库连接错误: {e}")
    # 使用内存数据库作为后备
    engine = create_engine('sqlite:///:memory:')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = scoped_session(SessionLocal)

# 数据模型
class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    audio_url = Column(Text)
    subtitles = Column(Text)  # JSON字符串
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'audio_url': self.audio_url,
            'subtitles': json.loads(self.subtitles) if self.subtitles else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# 创建数据库表
Base.metadata.create_all(bind=engine)

# JWT JWKS缓存
jwks_cache = {
    'keys': None,
    'expires_at': None
}

def get_jwks():
    """获取Supabase JWKS"""
    now = datetime.utcnow()
    
    # 检查缓存是否有效
    if (jwks_cache['keys'] and jwks_cache['expires_at'] and 
        now < jwks_cache['expires_at']):
        return jwks_cache['keys']
    
    try:
        response = requests.get(app.config['SUPABASE_JWKS_URL'])
        response.raise_for_status()
        jwks = response.json()
        
        # 缓存JWKS，有效期1小时
        jwks_cache['keys'] = jwks
        jwks_cache['expires_at'] = now + timedelta(hours=1)
        
        return jwks
    except Exception as e:
        print(f"获取JWKS失败: {e}")
        return None

def verify_jwt(token):
    """验证Supabase JWT令牌"""
    try:
        # 获取JWKS
        jwks = get_jwks()
        if not jwks:
            return None
        
        # 解码JWT头部获取kid
        header = jwt.get_unverified_header(token)
        kid = header.get('kid')
        
        if not kid:
            return None
        
        # 找到对应的公钥
        public_key = None
        for key in jwks['keys']:
            if key['kid'] == kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                break
        
        if not public_key:
            return None
        
        # 验证JWT
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience='authenticated',
            issuer=app.config['SUPABASE_URL']
        )
        
        return payload
    except Exception as e:
        print(f"JWT验证失败: {e}")
        return None

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # 将用户信息添加到请求上下文
        request.user_id = payload.get('sub')
        request.user_email = payload.get('email')
        
        return f(*args, **kwargs)
    
    return decorated_function

# 路由
@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({'ok': True, 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/projects', methods=['GET'])
@require_auth
def get_projects():
    """获取用户项目列表"""
    try:
        projects = db_session.query(Project).filter(
            Project.user_id == request.user_id
        ).order_by(Project.updated_at.desc()).all()
        
        return jsonify({
            'success': True,
            'projects': [project.to_dict() for project in projects]
        })
    except Exception as e:
        print(f"获取项目失败: {e}")
        return jsonify({'error': '获取项目失败'}), 500

@app.route('/api/projects', methods=['POST'])
@require_auth
def create_project():
    """创建新项目"""
    try:
        data = request.get_json()
        name = data.get('name')
        audio_url = data.get('audio_url')
        subtitles = data.get('subtitles', [])
        
        if not name:
            return jsonify({'error': '项目名称不能为空'}), 400
        
        project = Project(
            user_id=request.user_id,
            name=name,
            audio_url=audio_url,
            subtitles=json.dumps(subtitles, ensure_ascii=False)
        )
        
        db_session.add(project)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        })
    except Exception as e:
        db_session.rollback()
        print(f"创建项目失败: {e}")
        return jsonify({'error': '创建项目失败'}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
@require_auth
def get_project(project_id):
    """获取单个项目"""
    try:
        project = db_session.query(Project).filter(
            Project.id == project_id,
            Project.user_id == request.user_id
        ).first()
        
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        })
    except Exception as e:
        print(f"获取项目失败: {e}")
        return jsonify({'error': '获取项目失败'}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@require_auth
def update_project(project_id):
    """更新项目"""
    try:
        project = db_session.query(Project).filter(
            Project.id == project_id,
            Project.user_id == request.user_id
        ).first()
        
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            project.name = data['name']
        if 'audio_url' in data:
            project.audio_url = data['audio_url']
        if 'subtitles' in data:
            project.subtitles = json.dumps(data['subtitles'], ensure_ascii=False)
        
        project.updated_at = datetime.utcnow()
        db_session.commit()
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        })
    except Exception as e:
        db_session.rollback()
        print(f"更新项目失败: {e}")
        return jsonify({'error': '更新项目失败'}), 500

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@require_auth
def delete_project(project_id):
    """删除项目"""
    try:
        project = db_session.query(Project).filter(
            Project.id == project_id,
            Project.user_id == request.user_id
        ).first()
        
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        db_session.delete(project)
        db_session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db_session.rollback()
        print(f"删除项目失败: {e}")
        return jsonify({'error': '删除项目失败'}), 500

@app.route('/api/storage/sign', methods=['POST'])
@require_auth
def sign_storage_url():
    """生成Supabase Storage签名URL"""
    try:
        data = request.get_json()
        path = data.get('path')
        operation = data.get('operation', 'upload')
        
        if not path:
            return jsonify({'error': '文件路径不能为空'}), 400
        
        # 使用Supabase服务角色密钥生成签名URL
        headers = {
            'Authorization': f'Bearer {app.config["SUPABASE_SERVICE_ROLE"]}',
            'Content-Type': 'application/json'
        }
        
        if operation == 'upload':
            # 生成上传签名URL
            url = f"{app.config['SUPABASE_URL']}/storage/v1/object/sign/vidtools/{path}"
            response = requests.post(url, headers=headers, json={
                'expiresIn': 3600  # 1小时有效期
            })
        else:
            # 生成下载签名URL
            url = f"{app.config['SUPABASE_URL']}/storage/v1/object/sign/vidtools/{path}"
            response = requests.post(url, headers=headers, json={
                'expiresIn': 3600
            })
        
        response.raise_for_status()
        result = response.json()
        
        return jsonify({
            'success': True,
            'signedUrl': result.get('signedURL'),
            'path': path
        })
    except Exception as e:
        print(f"生成签名URL失败: {e}")
        return jsonify({'error': '生成签名URL失败'}), 500

# 静态文件服务
@app.route('/')
def index():
    """主页"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/login/')
def login():
    """登录页"""
    return send_from_directory('../frontend/login', 'index.html')

@app.route('/subtitle-editor/')
def subtitle_editor():
    """字幕编辑器"""
    return send_from_directory('../frontend/subtitle-editor', 'index.html')

@app.route('/admin/')
def admin():
    """管理员页面"""
    return send_from_directory('../frontend/admin', 'index.html')

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
    # 开发模式
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
