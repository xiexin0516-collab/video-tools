#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Desktop application build script for subtitle editor
"""

import os
import sys
import subprocess
import shutil

def build_desktop_app():
    """Build desktop application using PyInstaller"""
    
    print("开始打包桌面应用...")
    
    # 方法1：打包主应用框架
    print("\n1. 打包主应用框架...")
    main_cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个可执行文件
        "--windowed",  # 不显示控制台窗口
        "--name", "MultiToolApp",
        "--add-data", "locales;locales",  # 包含语言文件
        "--add-data", "config.json;.",  # 包含配置文件
        "main_app.py"
    ]
    
    try:
        print(f"执行命令: {' '.join(main_cmd)}")
        result = subprocess.run(main_cmd, check=True, capture_output=True, text=True)
        print("✅ 主应用打包成功！")
        print("输出文件位置: dist/MultiToolApp.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ 主应用打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    # 方法2：打包字幕编辑器独立版本
    print("\n2. 打包字幕编辑器独立版本...")
    subtitle_cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个可执行文件
        "--windowed",  # 不显示控制台窗口
        "--name", "SubtitleEditor",
        "--add-data", "locales;locales",  # 包含语言文件
        "--add-data", "config.json;.",  # 包含配置文件
        "手动上字幕改版新版本.py"
    ]
    
    try:
        print(f"执行命令: {' '.join(subtitle_cmd)}")
        result = subprocess.run(subtitle_cmd, check=True, capture_output=True, text=True)
        print("✅ 字幕编辑器打包成功！")
        print("输出文件位置: dist/SubtitleEditor.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ 字幕编辑器打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    print("\n🎉 所有应用打包完成！")
    print("📁 输出文件位置: dist/ 目录")
    print("   - MultiToolApp.exe (主应用框架)")
    print("   - SubtitleEditor.exe (字幕编辑器)")
    
    return True

def clean_build_files():
    """清理打包产生的临时文件"""
    print("\n清理临时文件...")
    dirs_to_clean = ['build', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ 已删除目录: {dir_name}")
            except Exception as e:
                print(f"⚠️ 删除目录失败 {dir_name}: {e}")
    
    for pattern in files_to_clean:
        for file in os.listdir('.'):
            if file.endswith('.spec'):
                try:
                    os.remove(file)
                    print(f"✅ 已删除文件: {file}")
                except Exception as e:
                    print(f"⚠️ 删除文件失败 {file}: {e}")

if __name__ == "__main__":
    print("🚀 桌面应用打包工具")
    print("=" * 50)
    
    # 检查依赖
    try:
        import PyQt5
        print("✅ PyQt5 已安装")
    except ImportError:
        print("❌ PyQt5 未安装，请先运行: pip install PyQt5")
        sys.exit(1)
    
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
    except ImportError:
        print("❌ PyInstaller 未安装，请先运行: pip install pyinstaller")
        sys.exit(1)
    
    # 执行打包
    success = build_desktop_app()
    
    if success:
        # 询问是否清理临时文件
        response = input("\n是否清理打包产生的临时文件？(y/n): ").lower()
        if response in ['y', 'yes', '是']:
            clean_build_files()
        
        print("\n🎊 打包流程完成！")
        print("💡 提示：")
        print("   - 可以直接运行 dist/ 目录下的 exe 文件")
        print("   - 建议将整个 dist/ 目录分发给用户")
        print("   - 用户无需安装Python即可运行")
    else:
        print("\n❌ 打包失败，请检查错误信息")
