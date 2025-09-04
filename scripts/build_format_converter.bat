@echo off
chcp 65001 >nul
echo ================================================
echo 视频格式转换器 - 打包工具
echo ================================================
echo.

echo 🚀 开始打包流程...
echo.

python build_format_converter.py

echo.
echo ================================================
echo 打包完成！
echo ================================================
echo.
echo 📁 可执行文件位置: dist\FormatConverter.exe
echo 📦 发布包位置: release_package_format_converter\
echo.
echo 按任意键退出...
pause >nul
