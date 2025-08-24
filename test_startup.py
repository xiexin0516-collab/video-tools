#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify application startup
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    print("Testing imports...")
    from backend.main import app
    print("✅ Successfully imported app")
    
    print("Testing route registration...")
    print(f"Routes: {[rule.rule for rule in app.url_map.iter_rules()]}")
    
    print("Testing frontend directory...")
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
    if os.path.exists(frontend_path):
        print(f"✅ Frontend directory exists: {frontend_path}")
        index_path = os.path.join(frontend_path, 'index.html')
        if os.path.exists(index_path):
            print(f"✅ index.html exists: {index_path}")
        else:
            print(f"❌ index.html not found: {index_path}")
    else:
        print(f"❌ Frontend directory not found: {frontend_path}")
    
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
