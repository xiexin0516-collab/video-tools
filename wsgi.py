#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI entry point for SubtitleEditor Web
Used for production deployment on Render.com
"""

import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory
os.chdir('backend')

# Import the Flask app
from main import app

# For production deployment
if __name__ == "__main__":
    app.run()
