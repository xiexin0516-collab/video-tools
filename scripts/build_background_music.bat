@echo off
chcp 65001 >nul
echo ================================================
echo 背景音乐生成器 - 打包工具
echo ================================================
echo.

echo 🚀 开始打包流程...
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)

REM 检查PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo 📦 开始打包BackgroundMusic...
echo.

REM 创建输出目录
if not exist "releases" mkdir releases
if not exist "releases\BackgroundMusic-v1.0.0" mkdir "releases\BackgroundMusic-v1.0.0"

REM 使用PyInstaller打包
pyinstaller --onefile ^
    --windowed ^
    --name "BackgroundMusic" ^
    --distpath "releases\BackgroundMusic-v1.0.0" ^
    --workpath "build" ^
    --specpath "build" ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    --hidden-import "tkinter.filedialog" ^
    --hidden-import "tkinter.messagebox" ^
    --hidden-import "numpy" ^
    --hidden-import "wave" ^
    --hidden-import "json" ^
    --hidden-import "threading" ^
    --hidden-import "pathlib" ^
    "src/BackgroundMusic.py"

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo 📝 创建说明文件...

REM 创建README文件
echo 背景音乐生成器 v1.0.0 > "releases\BackgroundMusic-v1.0.0\README.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 功能特点: >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - 支持4种音乐风格：神秘悬疑、平静舒缓、紧张氛围、希望向上 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - 高级旋律引擎：基于调式音阶和马尔可夫链 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - 管弦级编曲：包含弦乐、钢琴、鼓点、环境音效 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - 支持中英文界面切换 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - 可自定义音乐时长和输出文件名 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 使用方法: >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 1. 双击运行BackgroundMusic.exe >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 2. 选择音乐风格 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 3. 设置时长和文件名 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 4. 点击"开始生成"按钮 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 5. 等待生成完成 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 系统要求: >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - Windows 10/11 (64位) >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo - 无需安装Python或其他依赖 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 版本: v1.0.0 >> "releases\BackgroundMusic-v1.0.0\README.txt"
echo 更新日期: %date% >> "releases\BackgroundMusic-v1.0.0\README.txt"

REM 创建版本文件
echo v1.0.0 > "releases\BackgroundMusic-v1.0.0\version.txt"

REM 创建使用说明
echo 背景音乐生成器使用说明 > "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo 1. 音乐风格选择: >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 神秘悬疑：适合悬疑、惊悚类视频 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 平静舒缓：适合放松、冥想类视频 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 紧张氛围：适合动作、紧张类视频 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 希望向上：适合励志、正能量类视频 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo 2. 时长设置: >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 建议时长：15-60秒 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 默认时长：30秒 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo 3. 输出文件: >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 格式：WAV >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 质量：44.1kHz, 16bit >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 可直接导入PR、剪映等视频编辑软件 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo. >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo 4. 语言切换: >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 点击右上角语言按钮切换中英文 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"
echo    - 语言设置会自动保存 >> "releases\BackgroundMusic-v1.0.0\使用说明.txt"

echo.
echo 📦 创建压缩包...

REM 创建ZIP压缩包
cd releases
powershell -command "Compress-Archive -Path 'BackgroundMusic-v1.0.0\*' -DestinationPath 'BackgroundMusic-v1.0.0.zip' -Force"
cd ..

if errorlevel 1 (
    echo ❌ 创建压缩包失败
    pause
    exit /b 1
)

echo.
echo ================================================
echo 打包完成！
echo ================================================
echo.
echo 📁 可执行文件位置: releases\BackgroundMusic-v1.0.0\BackgroundMusic.exe
echo 📦 发布包位置: releases\BackgroundMusic-v1.0.0.zip
echo.
echo 🎵 功能特点:
echo - 支持4种音乐风格
echo - 高级旋律引擎
echo - 管弦级编曲
echo - 中英文界面
echo - 无需安装依赖
echo.
echo 按任意键退出...
pause >nul
