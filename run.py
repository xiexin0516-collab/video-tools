#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SubtitleEditor Web - Startup Script
Run this script to start the web application
"""

import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory
os.chdir('backend')

# Import and run the Flask app
from main import app

if __name__ == '__main__':
    print("🚀 Starting SubtitleEditor Web...")
    print("📁 Backend directory:", os.getcwd())
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API documentation: http://localhost:5000/api/")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
