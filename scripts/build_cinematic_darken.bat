@echo off
chcp 65001 >nul
echo ================================================
echo 电影级调暗工具 - 打包工具
echo ================================================
echo.

echo 🚀 开始打包流程...
echo.

python src/build_cinematic_darken.py

echo.
echo ================================================
echo 打包完成！
echo ================================================
echo.
echo 📁 可执行文件位置: dist\CinematicDarken.exe
echo 📦 发布包位置: release_package_cinematic_darken\
echo.
echo 按任意键退出...
pause >nul
