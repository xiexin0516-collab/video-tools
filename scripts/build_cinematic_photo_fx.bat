@echo off
chcp 65001 >nul
echo ================================================
echo 电影级图片特效工具 - 打包工具
echo ================================================
echo.

echo 🚀 开始打包流程...
echo.

python src/CinematicPhotoFX.py

echo.
echo ================================================
echo 打包完成！
echo ================================================
echo.
echo 📁 可执行文件位置: dist\CinematicPhotoFX.exe
echo 📦 发布包位置: release_package_cinematic_photo_fx\
echo.
echo 按任意键退出...
pause >nul
