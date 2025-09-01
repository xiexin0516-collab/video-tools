@echo off
chcp 65001 >nul
echo ================================================
echo 手动上字幕改版新版本 - 打包工具
echo ================================================
echo.

echo 🚀 开始打包流程...
echo.

python build_manual_subtitle.py

echo.
echo ================================================
echo 打包完成！
echo ================================================
echo.
echo 📁 可执行文件位置: dist\ManualSubtitleEditor.exe
echo 📦 发布包位置: release_package_manual\
echo.
echo 按任意键退出...
pause >nul
