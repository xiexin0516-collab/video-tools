#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动上字幕改版新版本打包脚本
"""

import os
import sys
import subprocess
import shutil

def build_manual_subtitle_editor():
    """打包手动上字幕改版新版本"""
    
    print("🚀 开始打包手动上字幕改版新版本...")
    
    # 检查依赖
    try:
        import PyQt5
        print("✅ PyQt5 已安装")
    except ImportError:
        print("❌ PyQt5 未安装，请先运行: pip install PyQt5")
        return False
    
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
    except ImportError:
        print("❌ PyInstaller 未安装，请先运行: pip install pyinstaller")
        return False
    
    # 打包手动上字幕改版新版本
    print("\n📦 打包手动上字幕改版新版本...")
    subtitle_cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个可执行文件
        "--windowed",  # 不显示控制台窗口
        "--name", "ManualSubtitleEditor",
        "--add-data", "locales;locales",  # 包含语言文件
        "--add-data", "config.json;.",  # 包含配置文件
        "--hidden-import", "PyQt5.QtMultimedia",
        "--hidden-import", "PyQt5.QtMultimediaWidgets",
        "手动上字幕改版新版本.py"
    ]
    
    try:
        print(f"执行命令: {' '.join(subtitle_cmd)}")
        result = subprocess.run(subtitle_cmd, check=True, capture_output=True, text=True)
        print("✅ 手动上字幕改版新版本打包成功！")
        print("输出文件位置: dist/ManualSubtitleEditor.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    print("\n🎉 手动上字幕改版新版本打包完成！")
    print("📁 输出文件位置: dist/ 目录")
    print("   - ManualSubtitleEditor.exe (手动上字幕改版新版本)")
    
    return True

def clean_build_files():
    """清理打包产生的临时文件"""
    print("\n🧹 清理临时文件...")
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

def create_release_package():
    """创建发布包"""
    print("\n📦 创建发布包...")
    
    release_dir = "release_package_manual"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # 复制可执行文件
    exe_source = "dist/ManualSubtitleEditor.exe"
    exe_dest = f"{release_dir}/ManualSubtitleEditor.exe"
    
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, exe_dest)
        print(f"✅ 已复制可执行文件: {exe_dest}")
    else:
        print(f"❌ 可执行文件不存在: {exe_source}")
        return False
    
    # 复制必要文件
    files_to_copy = [
        ("config.json", "config.json"),
        ("README.md", "README.md"),
        ("CHANGELOG.md", "CHANGELOG.md"),
        ("LICENSE", "LICENSE")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, f"{release_dir}/{dst}")
            print(f"✅ 已复制文件: {dst}")
        else:
            print(f"⚠️ 文件不存在: {src}")
    
    # 复制语言文件目录
    if os.path.exists("locales"):
        shutil.copytree("locales", f"{release_dir}/locales")
        print("✅ 已复制语言文件目录")
    
    print(f"\n🎉 发布包创建完成！")
    print(f"📁 发布包位置: {release_dir}/")
    print(f"📦 包含文件:")
    print(f"   - ManualSubtitleEditor.exe (主程序)")
    print(f"   - config.json (配置文件)")
    print(f"   - locales/ (语言文件)")
    print(f"   - README.md (说明文档)")
    print(f"   - CHANGELOG.md (更新日志)")
    print(f"   - LICENSE (许可证)")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("手动上字幕改版新版本 - 打包工具")
    print("=" * 60)
    
    # 检查当前目录
    if not os.path.exists("手动上字幕改版新版本.py"):
        print("❌ 错误：当前目录下没有找到 '手动上字幕改版新版本.py' 文件")
        print("请确保在正确的目录下运行此脚本")
        return False
    
    # 执行打包
    if build_manual_subtitle_editor():
        # 创建发布包
        create_release_package()
        # 清理临时文件
        clean_build_files()
        
        print("\n" + "=" * 60)
        print("🎉 打包流程完成！")
        print("📁 可执行文件: dist/ManualSubtitleEditor.exe")
        print("📦 发布包: release_package_manual/")
        print("=" * 60)
        return True
    else:
        print("\n❌ 打包失败！")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
