#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Management Module
Handles CRUD operations for subtitle projects
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db, Project, User

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    """Get all projects for current user"""
    try:
        user_id = get_jwt_identity()
        
        # Get projects with pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        projects = Project.query.filter_by(user_id=user_id)\
            .order_by(Project.updated_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'projects': [project.to_dict() for project in projects.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': projects.total,
                'pages': projects.pages,
                'has_next': projects.has_next,
                'has_prev': projects.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get projects: {str(e)}'}), 500

@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Get specific project by ID"""
    try:
        user_id = get_jwt_identity()
        
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'success': True,
            'project': project.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get project: {str(e)}'}), 500

@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    """Create new project"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'error': 'Project name is required'}), 400
        
        # Check if project name already exists for this user
        existing_project = Project.query.filter_by(user_id=user_id, name=name).first()
        if existing_project:
            return jsonify({'error': 'Project name already exists'}), 409
        
        # Create new project
        new_project = Project(
            user_id=user_id,
            name=name,
            audio_file=data.get('audio_file', ''),
            subtitles_json=data.get('subtitles_json', '[]')
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project created successfully',
            'project': new_project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create project: {str(e)}'}), 500

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update project"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Update fields
        if 'name' in data:
            name = data['name'].strip()
            if not name:
                return jsonify({'error': 'Project name cannot be empty'}), 400
            
            # Check if name already exists for this user
            existing_project = Project.query.filter(
                Project.user_id == user_id,
                Project.name == name,
                Project.id != project_id
            ).first()
            if existing_project:
                return jsonify({'error': 'Project name already exists'}), 409
            
            project.name = name
        
        if 'audio_file' in data:
            project.audio_file = data['audio_file']
        
        if 'subtitles' in data:
            project.set_subtitles(data['subtitles'])
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project updated successfully',
            'project': project.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update project: {str(e)}'}), 500

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete project"""
    try:
        user_id = get_jwt_identity()
        
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete project: {str(e)}'}), 500

@projects_bp.route('/<int:project_id>/duplicate', methods=['POST'])
@jwt_required()
def duplicate_project(project_id):
    """Duplicate project"""
    try:
        user_id = get_jwt_identity()
        
        original_project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not original_project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Create duplicate with new name
        new_name = f"{original_project.name} (Copy)"
        counter = 1
        while Project.query.filter_by(user_id=user_id, name=new_name).first():
            new_name = f"{original_project.name} (Copy {counter})"
            counter += 1
        
        new_project = Project(
            user_id=user_id,
            name=new_name,
            audio_file=original_project.audio_file,
            subtitles_json=original_project.subtitles_json
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project duplicated successfully',
            'project': new_project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to duplicate project: {str(e)}'}), 500
