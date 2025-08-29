@echo off
chcp 65001 >nul
echo 🚀 开始部署视频工具平台...

REM 检查环境
echo 📋 检查部署环境...

REM 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)
echo ✅ Python已安装

REM 检查Node.js版本（如果需要）
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js已安装
) else (
    echo ⚠️  Node.js未安装（可选）
)

REM 安装后端依赖
echo 📦 安装后端依赖...
cd backend
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ 后端依赖安装成功
    ) else (
        echo ❌ 后端依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo ❌ 未找到requirements.txt文件
    pause
    exit /b 1
)
cd ..

REM 检查环境变量配置
echo 🔧 检查环境变量配置...
if not exist "backend\.env" (
    if exist "backend\config.env.example" (
        echo ⚠️  未找到.env文件，请复制config.env.example为.env并配置
        copy "backend\config.env.example" "backend\.env"
        echo 📝 已创建.env文件模板，请编辑配置
    ) else (
        echo ❌ 未找到环境变量配置文件
        pause
        exit /b 1
    )
) else (
    echo ✅ 环境变量配置文件存在
)

REM 创建必要的目录
echo 📁 创建必要目录...
if not exist "backend\uploads" mkdir "backend\uploads"
if not exist "backend\logs" mkdir "backend\logs"
echo ✅ 目录创建完成

REM 测试后端服务
echo 🧪 测试后端服务...
cd backend
python -c "import sys; sys.path.append('.'); from app import app; print('✅ 后端应用导入成功')"
if %errorlevel% neq 0 (
    echo ❌ 后端应用导入失败
    pause
    exit /b 1
)
cd ..

REM 前端构建（如果需要）
echo 🏗️  检查前端文件...
if exist "frontend" (
    echo ✅ 前端目录存在
    REM 检查是否有构建需求
    if exist "frontend\package.json" (
        echo 📦 检测到package.json，安装前端依赖...
        cd frontend
        npm install
        if %errorlevel% equ 0 (
            echo ✅ 前端依赖安装成功
        ) else (
            echo ⚠️  前端依赖安装失败，继续部署
        )
        cd ..
    )
) else (
    echo ❌ 前端目录不存在
    pause
    exit /b 1
)

echo.
echo 📋 部署完成！
echo.
echo 🔧 下一步操作：
echo 1. 编辑 backend\.env 文件，配置Supabase和其他环境变量
echo 2. 启动后端服务: cd backend ^&^& python app.py
echo 3. 前端服务: 使用任何静态文件服务器，如 python -m http.server 3000
echo.
echo 🌐 访问地址：
echo    前端: http://localhost:3000
echo    后端API: http://localhost:5000
echo.
echo 📚 更多信息请查看 README.md
pause
