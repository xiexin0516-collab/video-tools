#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证SubtitleEditor Web功能
"""

import sys
import os
import json

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.subtitle_parser import SubtitleParser

def test_subtitle_parser():
    """测试字幕解析器功能"""
    print("🧪 测试字幕解析器...")
    
    parser = SubtitleParser()
    
    # 测试SRT格式解析
    srt_content = """1
00:00:00,000 --> 00:00:03,000
Hello, this is a test subtitle.

2
00:00:03,000 --> 00:00:06,000
This is the second subtitle line."""
    
    subtitles = parser.parse_srt_content(srt_content)
    print(f"✅ SRT解析成功，解析到 {len(subtitles)} 个字幕")
    
    # 测试TXT格式解析
    txt_content = """[00:00:00] Hello, this is a test subtitle.
[00:00:03] This is the second subtitle line."""
    
    subtitles = parser.parse_txt_content(txt_content)
    print(f"✅ TXT解析成功，解析到 {len(subtitles)} 个字幕")
    
    # 测试导出功能
    test_subtitles = [
        {
            'id': 1,
            'start_time': 0.0,
            'end_time': 3.0,
            'text': 'Hello, this is a test subtitle.',
            'duration': 3.0
        },
        {
            'id': 2,
            'start_time': 3.0,
            'end_time': 6.0,
            'text': 'This is the second subtitle line.',
            'duration': 3.0
        }
    ]
    
    srt_export = parser.export_subtitles(test_subtitles, 'srt')
    print(f"✅ SRT导出成功，长度: {len(srt_export)} 字符")
    
    txt_export = parser.export_subtitles(test_subtitles, 'txt')
    print(f"✅ TXT导出成功，长度: {len(txt_export)} 字符")
    
    # 测试验证功能
    is_valid, errors = parser.validate_subtitles(test_subtitles)
    print(f"✅ 字幕验证: {'通过' if is_valid else '失败'}")
    
    if not is_valid:
        for error in errors:
            print(f"   ❌ {error}")

def test_file_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")
    
    required_files = [
        'frontend/index.html',
        'frontend/i18n/en.json',
        'frontend/i18n/zh.json',
        'backend/main.py',
        'backend/services/subtitle_parser.py',
        'static/demo_subtitles.srt',
        'requirements.txt',
        'render.yaml',
        'run.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")

def test_i18n_files():
    """测试国际化文件"""
    print("\n🌐 测试国际化文件...")
    
    try:
        with open('frontend/i18n/en.json', 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        print(f"✅ 英文翻译文件加载成功，包含 {len(en_data)} 个翻译项")
        
        with open('frontend/i18n/zh.json', 'r', encoding='utf-8') as f:
            zh_data = json.load(f)
        print(f"✅ 中文翻译文件加载成功，包含 {len(zh_data)} 个翻译项")
        
        # 检查关键翻译项
        key_translations = ['title', 'subtitle', 'uploadAudio', 'uploadSubtitle']
        for key in key_translations:
            if key in en_data and key in zh_data:
                print(f"✅ 翻译项 '{key}' 存在")
            else:
                print(f"❌ 翻译项 '{key}' 缺失")
                
    except Exception as e:
        print(f"❌ 国际化文件测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始测试 SubtitleEditor Web...")
    print("=" * 50)
    
    test_file_structure()
    test_i18n_files()
    test_subtitle_parser()
    
    print("\n" + "=" * 50)
    print("✅ 所有测试完成！")
    print("\n📋 下一步操作:")
    print("1. 运行 'python run.py' 启动应用")
    print("2. 访问 http://localhost:5000 查看界面")
    print("3. 按照 DEPLOYMENT.md 部署到 Render.com")
    print("4. 配置域名 vidtools.tools")

if __name__ == '__main__':
    main()
