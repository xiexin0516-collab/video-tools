@echo off
chcp 65001 >nul
echo ================================================
echo 发布格式转换器到GitHub Releases
echo ================================================
echo.

echo 🚀 开始发布流程...
echo.

python publish_release.py

echo.
echo ================================================
echo 发布流程完成！
echo ================================================
echo.
echo 按任意键退出...
pause >nul
