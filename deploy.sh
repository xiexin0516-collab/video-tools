#!/bin/bash

# 视频工具平台部署脚本
# 用于部署前后端分离的网站

echo "🚀 开始部署视频工具平台..."

# 检查环境
echo "📋 检查部署环境..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [[ $python_version < "3.8" ]]; then
    echo "❌ Python版本过低，需要3.8或更高版本"
    exit 1
fi
echo "✅ Python版本: $python_version"

# 检查Node.js版本（如果需要）
if command -v node &> /dev/null; then
    node_version=$(node --version | grep -o '[0-9]\+')
    echo "✅ Node.js版本: $(node --version)"
else
    echo "⚠️  Node.js未安装（可选）"
fi

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ 后端依赖安装成功"
    else
        echo "❌ 后端依赖安装失败"
        exit 1
    fi
else
    echo "❌ 未找到requirements.txt文件"
    exit 1
fi
cd ..

# 检查环境变量配置
echo "🔧 检查环境变量配置..."
if [ ! -f "backend/.env" ]; then
    if [ -f "backend/config.env.example" ]; then
        echo "⚠️  未找到.env文件，请复制config.env.example为.env并配置"
        cp backend/config.env.example backend/.env
        echo "📝 已创建.env文件模板，请编辑配置"
    else
        echo "❌ 未找到环境变量配置文件"
        exit 1
    fi
else
    echo "✅ 环境变量配置文件存在"
fi

# 创建必要的目录
echo "📁 创建必要目录..."
mkdir -p backend/uploads
mkdir -p backend/logs
echo "✅ 目录创建完成"

# 测试后端服务
echo "🧪 测试后端服务..."
cd backend
python3 -c "
import os
import sys
sys.path.append('.')
try:
    from app import app
    print('✅ 后端应用导入成功')
except Exception as e:
    print(f'❌ 后端应用导入失败: {e}')
    sys.exit(1)
"
cd ..

# 前端构建（如果需要）
echo "🏗️  检查前端文件..."
if [ -d "frontend" ]; then
    echo "✅ 前端目录存在"
    # 检查是否有构建需求
    if [ -f "frontend/package.json" ]; then
        echo "📦 检测到package.json，安装前端依赖..."
        cd frontend
        npm install
        if [ $? -eq 0 ]; then
            echo "✅ 前端依赖安装成功"
        else
            echo "⚠️  前端依赖安装失败，继续部署"
        fi
        cd ..
    fi
else
    echo "❌ 前端目录不存在"
    exit 1
fi

# 启动服务
echo "🚀 启动服务..."
echo ""
echo "📋 部署完成！"
echo ""
echo "🔧 下一步操作："
echo "1. 编辑 backend/.env 文件，配置Supabase和其他环境变量"
echo "2. 启动后端服务: cd backend && python3 app.py"
echo "3. 前端服务: 使用任何静态文件服务器，如 python3 -m http.server 3000"
echo ""
echo "🌐 访问地址："
echo "   前端: http://localhost:3000"
echo "   后端API: http://localhost:5000"
echo ""
echo "📚 更多信息请查看 README.md"
