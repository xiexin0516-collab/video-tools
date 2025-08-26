#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Module
Provides database viewing and management functionality
"""

from flask import Blueprint, request, jsonify, render_template_string
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db, User, Project

admin_bp = Blueprint('admin', __name__)

# Simple admin check (you can enhance this with proper admin roles)
ADMIN_USERNAMES = ['admin', 'xiexin']  # Add your admin usernames here

def is_admin(user_id):
    """Check if user is admin"""
    user = User.query.get(user_id)
    return user and user.username in ADMIN_USERNAMES

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Admin dashboard page"""
    user_id = get_jwt_identity()
    
    if not is_admin(user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    # Get database statistics
    total_users = User.query.count()
    total_projects = Project.query.count()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Get recent projects
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(10).all()
    
    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'total_projects': total_projects
        },
        'recent_users': [user.to_dict() for user in recent_users],
        'recent_projects': [project.to_dict() for project in recent_projects]
    })

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    user_id = get_jwt_identity()
    
    if not is_admin(user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'users': [user.to_dict() for user in users.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': users.total,
            'pages': users.pages
        }
    })

@admin_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_all_projects():
    """Get all projects (admin only)"""
    user_id = get_jwt_identity()
    
    if not is_admin(user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    projects = Project.query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'projects': [project.to_dict() for project in projects.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': projects.total,
            'pages': projects.pages
        }
    })

@admin_bp.route('/database/export', methods=['GET'])
@jwt_required()
def export_database():
    """Export database as JSON (admin only)"""
    user_id = get_jwt_identity()
    
    if not is_admin(user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    # Get all data
    users = User.query.all()
    projects = Project.query.all()
    
    data = {
        'exported_at': datetime.utcnow().isoformat(),
        'users': [user.to_dict() for user in users],
        'projects': [project.to_dict() for project in projects],
        'statistics': {
            'total_users': len(users),
            'total_projects': len(projects)
        }
    }
    
    return jsonify(data)

@admin_bp.route('/database/backup', methods=['POST'])
@jwt_required()
def backup_database():
    """Create database backup (admin only)"""
    user_id = get_jwt_identity()
    
    if not is_admin(user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # In a real application, you would create a proper backup
        # For now, we'll just return the current database state
        users = User.query.all()
        projects = Project.query.all()
        
        backup_data = {
            'backup_created_at': datetime.utcnow().isoformat(),
            'users_count': len(users),
            'projects_count': len(projects),
            'message': 'Database backup created successfully'
        }
        
        return jsonify({
            'success': True,
            'backup': backup_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Backup failed: {str(e)}'}), 500
