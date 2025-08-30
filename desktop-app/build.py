#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面版应用打包脚本
使用 PyInstaller 打包为 Windows 可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """打包为可执行文件"""
    print("开始打包桌面版应用...")
    
    # 确保在正确的目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包为单个文件
        "--windowed",                   # 无控制台窗口
        "--name=video-tools",           # 可执行文件名称
        "--icon=icon.ico",              # 应用图标
        "--add-data=icon.ico;.",        # 包含图标文件
        "--hidden-import=cv2",          # 包含 OpenCV
        "--hidden-import=PIL",          # 包含 Pillow
        "--hidden-import=numpy",        # 包含 NumPy
        "main.py"                       # 主程序文件
    ]
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("打包成功！")
        print(result.stdout)
        
        # 移动生成的文件
        dist_dir = script_dir / "dist"
        if dist_dir.exists():
            exe_file = dist_dir / "video-tools.exe"
            if exe_file.exists():
                # 复制到项目根目录
                target_file = script_dir.parent / "video-tools-windows.exe"
                shutil.copy2(exe_file, target_file)
                print(f"可执行文件已生成: {target_file}")
        
        # 清理临时文件
        cleanup_temp_files()
        
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    return True

def cleanup_temp_files():
    """清理临时文件"""
    script_dir = Path(__file__).parent
    
    # 删除 build 目录
    build_dir = script_dir / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("已清理 build 目录")
    
    # 删除 dist 目录
    dist_dir = script_dir / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("已清理 dist 目录")
    
    # 删除 spec 文件
    spec_file = script_dir / "video-tools.spec"
    if spec_file.exists():
        spec_file.unlink()
        print("已清理 spec 文件")

def install_dependencies():
    """安装依赖"""
    print("安装依赖包...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("依赖安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 视频工具平台 - 桌面版打包工具 ===")
    
    # 检查依赖
    if not install_dependencies():
        print("依赖安装失败，退出打包")
        return
    
    # 执行打包
    if build_executable():
        print("\n✅ 打包完成！")
        print("可执行文件: video-tools-windows.exe")
        print("文件位置: 项目根目录")
    else:
        print("\n❌ 打包失败！")

if __name__ == "__main__":
    main()
