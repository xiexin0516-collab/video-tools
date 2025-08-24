#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to check file paths
"""

import os
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"Script directory: {os.path.dirname(__file__)}")

# Check if frontend directory exists
frontend_path = os.path.join(os.getcwd(), 'frontend')
print(f"Frontend path: {frontend_path}")
print(f"Frontend exists: {os.path.exists(frontend_path)}")

if os.path.exists(frontend_path):
    print(f"Frontend contents: {os.listdir(frontend_path)}")
    
    index_path = os.path.join(frontend_path, 'index.html')
    print(f"Index path: {index_path}")
    print(f"Index exists: {os.path.exists(index_path)}")

# Check relative to script directory
script_frontend = os.path.join(os.path.dirname(__file__), 'frontend')
print(f"Script frontend path: {script_frontend}")
print(f"Script frontend exists: {os.path.exists(script_frontend)}")

# Test send_from_directory
from flask import Flask, send_from_directory

app = Flask(__name__)

try:
    with app.test_client() as client:
        # Test with absolute path
        response = client.get('/')
        print(f"Root response status: {response.status_code}")
        print(f"Root response: {response.data}")
        
        # Test with relative path
        print(f"Current directory contents: {os.listdir('.')}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
