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

# Import the Flask app
from backend.main import app

if __name__ == '__main__':
    print("🚀 Starting SubtitleEditor Web...")
    print("📁 Project directory:", os.getcwd())
    
    # Get port from environment variable (for production) or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print("📖 API documentation: http://localhost:5000/api/")
    print("=" * 50)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
