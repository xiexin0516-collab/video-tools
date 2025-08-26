#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Models
Defines User and Project models for the subtitle editor
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and project management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationship to projects
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Project(db.Model):
    """Project model for storing subtitle projects"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    audio_file = db.Column(db.String(500))  # File path or URL
    subtitles_json = db.Column(db.Text)  # JSON string of subtitles
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'audio_file': self.audio_file,
            'subtitles': json.loads(self.subtitles_json) if self.subtitles_json else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def set_subtitles(self, subtitles):
        """Set subtitles as JSON string"""
        self.subtitles_json = json.dumps(subtitles, ensure_ascii=False)
        self.updated_at = datetime.utcnow()
    
    def get_subtitles(self):
        """Get subtitles as list"""
        return json.loads(self.subtitles_json) if self.subtitles_json else []
