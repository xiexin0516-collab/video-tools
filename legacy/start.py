#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup script for production deployment
"""

from main import app, db
import os

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
