#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Release Publisher
发布脚本 - 将格式转换器发布到GitHub Releases
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_git_status():
    """检查Git状态"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=Path.cwd())
        if result.stdout.strip():
            print("⚠️  检测到未提交的更改:")
            print(result.stdout)
            response = input("是否继续发布? (y/N): ")
            if response.lower() != 'y':
                return False
        return True
    except Exception as e:
        print(f"❌ 检查Git状态失败: {e}")
        return False

def create_git_tag(version):
    """创建Git标签"""
    try:
        # 检查标签是否已存在
        result = subprocess.run(['git', 'tag', '-l', version], 
                              capture_output=True, text=True)
        if version in result.stdout:
            print(f"⚠️  标签 {version} 已存在")
            response = input("是否删除并重新创建? (y/N): ")
            if response.lower() == 'y':
                subprocess.run(['git', 'tag', '-d', version])
            else:
                return False
        
        # 创建标签
        subprocess.run(['git', 'tag', '-a', version, '-m', f'Release {version}'])
        print(f"✅ 创建标签 {version} 成功")
        return True
    except Exception as e:
        print(f"❌ 创建标签失败: {e}")
        return False

def push_to_github(version):
    """推送到GitHub"""
    try:
        # 推送代码
        subprocess.run(['git', 'push', 'origin', 'main'])
        print("✅ 推送代码成功")
        
        # 推送标签
        subprocess.run(['git', 'push', 'origin', version])
        print(f"✅ 推送标签 {version} 成功")
        return True
    except Exception as e:
        print(f"❌ 推送到GitHub失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始发布格式转换器到GitHub...")
    print("=" * 50)
    
    # 检查必要文件
    required_files = [
        'releases/FormatConverter-v1.0.0.zip',
        'docs/releases/RELEASE_FORMAT_CONVERTER_v1.0.0.md',
        'docs/releases/RELEASE_FORMAT_CONVERTER_v1.0.0_EN.md'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ 缺少必要文件: {file_path}")
            return False
    
    print("✅ 所有必要文件检查通过")
    
    # 检查Git状态
    if not check_git_status():
        print("❌ Git状态检查失败，取消发布")
        return False
    
    # 创建标签
    version = "v1.0.0"
    if not create_git_tag(version):
        print("❌ 创建标签失败，取消发布")
        return False
    
    # 推送到GitHub
    if not push_to_github(version):
        print("❌ 推送到GitHub失败，取消发布")
        return False
    
    print("=" * 50)
    print("🎉 发布成功!")
    print(f"📦 版本: {version}")
    print("🔗 GitHub Actions将自动构建并发布")
    print("⏳ 请等待几分钟后检查GitHub Releases页面")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
