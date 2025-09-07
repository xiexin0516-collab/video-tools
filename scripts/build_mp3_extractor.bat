@echo off
echo Building MP3 Subtitle Extractor...

REM 检查PyInstaller是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM 创建发布目录
if not exist "releases\MP3SubtitleExtractor-v1.0.0" mkdir "releases\MP3SubtitleExtractor-v1.0.0"

REM 使用PyInstaller打包
pyinstaller --onefile ^
    --windowed ^
    --name "MP3SubtitleExtractor" ^
    --distpath "releases\MP3SubtitleExtractor-v1.0.0" ^
    --workpath "build" ^
    --specpath "build" ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    --hidden-import "tkinter.filedialog" ^
    --hidden-import "tkinter.messagebox" ^
    --hidden-import "whisper" ^
    --hidden-import "argostranslate" ^
    --hidden-import "argostranslate.package" ^
    --hidden-import "argostranslate.translate" ^
    --hidden-import "threading" ^
    --hidden-import "pathlib" ^
    --hidden-import "json" ^
    "src/MP3-Subtitle-Extractor.py"

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

REM 创建使用说明文件
echo Creating documentation...

REM 创建中文使用说明
(
echo MP3字幕提取器 v1.0.0
echo ===================
echo.
echo 功能说明：
echo - 使用Whisper AI进行语音识别
echo - 支持自动翻译为中文
echo - 生成英文和中文对照的文本文件
echo.
echo 使用方法：
echo 1. 双击运行 MP3SubtitleExtractor.exe
echo 2. 点击"选择MP3文件"按钮选择音频文件
echo 3. 点击"开始提取"按钮开始处理
echo 4. 等待处理完成，结果会显示在界面中
echo 5. 同时会在MP3文件同目录生成_英文中文.txt文件
echo.
echo 系统要求：
echo - Windows 10/11 ^(64位^)
echo - 首次使用需要下载Whisper模型（约1.5GB）
echo - 需要安装Argos Translate翻译模型
echo - 依赖包：pip install -r requirements.txt
echo.
echo 注意事项：
echo - 首次运行可能需要几分钟下载模型
echo - 确保有足够的磁盘空间
echo - 建议使用英文音频文件以获得最佳效果
echo.
echo 技术支持：
echo 如有问题，请访问：https://vidtools.tools/
) > "releases\MP3SubtitleExtractor-v1.0.0\使用说明.txt"

REM 创建英文使用说明
(
echo MP3 Subtitle Extractor v1.0.0
echo =============================
echo.
echo Features:
echo - Uses Whisper AI for speech recognition
echo - Supports automatic Chinese translation
echo - Generates English and Chinese text files
echo.
echo Usage:
echo 1. Double-click to run MP3SubtitleExtractor.exe
echo 2. Click "Select MP3 File" to choose audio file
echo 3. Click "Start Extraction" to begin processing
echo 4. Wait for completion, results will be displayed
echo 5. A _英文中文.txt file will be generated in the same directory
echo.
echo System Requirements:
echo - Windows 10/11 ^(64-bit^)
echo - First use requires downloading Whisper model ^(~1.5GB^)
echo - Requires Argos Translate translation model
echo - Dependencies: pip install -r requirements.txt
echo.
echo Notes:
echo - First run may take a few minutes to download models
echo - Ensure sufficient disk space
echo - English audio files recommended for best results
echo.
echo Support:
echo For issues, visit: https://vidtools.tools/
) > "releases\MP3SubtitleExtractor-v1.0.0\README.txt"

REM 创建版本信息文件
(
echo version=1.0.0
echo build_date=%date%
echo build_time=%time%
echo author=Video Tools Platform
echo description=MP3 Subtitle Extractor with Whisper AI
) > "releases\MP3SubtitleExtractor-v1.0.0\version.txt"

echo Build completed successfully!
echo Output directory: releases\MP3SubtitleExtractor-v1.0.0
pause
