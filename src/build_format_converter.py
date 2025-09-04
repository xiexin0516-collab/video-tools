#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format Converter Build Script
构建视频格式转换器的可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    """主构建流程"""
    print("🔧 开始构建视频格式转换器...")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    dist_dir = project_root / "dist"
    release_dir = project_root / "release_package_format_converter"
    
    # 确保目录存在
    dist_dir.mkdir(exist_ok=True)
    release_dir.mkdir(exist_ok=True)
    
    # 清理旧的构建文件
    print("🧹 清理旧的构建文件...")
    if (dist_dir / "FormatConverter.exe").exists():
        (dist_dir / "FormatConverter.exe").unlink()
    
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(exist_ok=True)
    
    # 构建可执行文件
    print("📦 使用PyInstaller构建可执行文件...")
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "FormatConverter",
            "--distpath", str(dist_dir),
            "--workpath", str(project_root / "build"),
            "--specpath", str(project_root / "build"),
            str(src_dir / "format_converter.py")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode != 0:
            print(f"❌ PyInstaller构建失败:")
            print(result.stderr)
            return False
            
        print("✅ PyInstaller构建成功!")
        
    except Exception as e:
        print(f"❌ 构建过程中出现错误: {e}")
        return False
    
    # 检查可执行文件是否生成
    exe_path = dist_dir / "FormatConverter.exe"
    if not exe_path.exists():
        print("❌ 可执行文件未生成!")
        return False
    
    print(f"✅ 可执行文件生成成功: {exe_path}")
    
    # 创建发布包
    print("📦 创建发布包...")
    
    # 复制可执行文件
    shutil.copy2(exe_path, release_dir / "FormatConverter.exe")
    
    # 创建说明文件
    readme_content = """# 视频格式转换器 v1.0.0

## 🎯 软件介绍
专业的视频格式转换工具，支持多种格式、参数调节和批量转换。

## ✨ 主要功能
- 多格式支持 (MP4, AVI, MOV, MKV, WMV, FLV)
- 参数可调节 (分辨率、质量、编码预设)
- 批量转换
- 多语言界面 (中文/英文)
- 智能预设

## 🚀 使用方法
1. 双击 FormatConverter.exe 启动程序
2. 选择要转换的视频文件或文件夹
3. 调整转换参数
4. 点击"开始转换"

## ⚙️ 系统要求
- Windows 10/11 (64位)
- 无需安装，解压即用

## 📄 许可证
MIT License - 免费使用和修改

## 🔗 相关链接
- 官方网站: https://vidtools.tools/
- 源代码: https://github.com/xiexin0516-collab/video-tools
"""
    
    with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 创建版本信息文件
    version_info = """[Version]
Version=1.0.0
BuildDate=2025-01-27
Author=Video Tools Platform
Description=Video Format Converter
"""
    
    with open(release_dir / "version.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print("✅ 发布包创建完成!")
    print(f"📁 发布包位置: {release_dir}")
    
    # 显示文件大小
    exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print(f"📊 可执行文件大小: {exe_size:.1f} MB")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 构建完成!")
    else:
        print("\n❌ 构建失败!")
        sys.exit(1)
