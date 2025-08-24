#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify root route functionality
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.main import app
    
    # Create a test client
    with app.test_client() as client:
        print("Testing root route...")
        response = client.get('/')
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Root route works!")
            print(f"Content length: {len(response.data)}")
            print(f"Content preview: {response.data[:200]}...")
        else:
            print("❌ Root route failed!")
            print(f"Response: {response.data}")
            
        print("\nTesting API route...")
        response = client.get('/api/languages')
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("✅ API route works!")
            print(f"Response: {response.data}")
        else:
            print("❌ API route failed!")
            print(f"Response: {response.data}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
