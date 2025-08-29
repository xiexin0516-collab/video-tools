# 视频工具平台

专业的视频处理工具平台，支持字幕编辑、音频处理、视频特效等功能。

## 🏗️ 架构

- **前端**: 静态网站 (HTML/CSS/JavaScript)
- **后端**: Flask API服务 (Python)
- **认证**: Supabase Auth
- **数据库**: Supabase PostgreSQL
- **存储**: Supabase Storage
- **部署**: Render平台

## 🚀 快速开始

### 方法一：使用部署脚本（推荐）

#### Windows用户
```bash
# 双击运行部署脚本
deploy.bat
```

#### Linux/Mac用户
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 方法二：手动部署

#### 1. 环境准备

确保已安装：
- Python 3.8+
- Node.js 16+ (可选)

#### 2. 克隆项目
```bash
git clone https://github.com/your-username/video-tools.git
cd video-tools
```

#### 3. 后端配置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp config.env.example .env
# 编辑 .env 文件，填入 Supabase 配置
```

#### 4. 前端配置

前端是静态文件，无需构建，直接部署即可。

#### 5. 启动服务

```bash
# 启动后端服务
cd backend
python app.py

# 新开终端，启动前端服务
cd frontend
python -m http.server 3000
```

## 📁 项目结构

```
/
├─ frontend/           # 静态前端
│  ├─ index.html       # 主页
│  ├─ login/           # 登录页面
│  ├─ subtitle-editor/ # 字幕编辑器
│  ├─ admin/           # 管理员面板
│  └─ js/
│     ├─ api.js        # API客户端
│     ├─ supabaseClient.js  # Supabase客户端
│     └─ app.js        # 主应用逻辑
├─ backend/            # Flask API服务
│  ├─ app.py           # 主应用
│  ├─ requirements.txt # 依赖
│  ├─ config.env.example # 环境变量模板
│  └─ uploads/         # 文件上传目录
├─ deploy.sh           # Linux/Mac部署脚本
├─ deploy.bat          # Windows部署脚本
├─ render.yaml         # Render部署配置
└─ README.md           # 说明文档
```

## 🔧 开发指南

### 后端开发

#### API接口

所有API接口都以 `/api` 开头，需要认证的接口需要在请求头中包含：
```
Authorization: Bearer <supabase-access-token>
```

#### 主要接口

**健康检查**
- `GET /api/health` - 服务健康检查

**用户认证**
- `GET /api/auth/profile` - 获取用户信息

**项目管理**
- `GET /api/projects` - 获取用户项目列表
- `POST /api/projects` - 创建新项目
- `GET /api/projects/<id>` - 获取单个项目
- `PUT /api/projects/<id>` - 更新项目
- `DELETE /api/projects/<id>` - 删除项目

**文件处理**
- `POST /api/upload` - 文件上传
- `POST /api/subtitles/generate` - 生成字幕
- `POST /api/subtitles/export` - 导出字幕

#### 添加新接口

1. 在 `backend/app.py` 中添加新的路由
2. 使用 `@require_auth` 装饰器保护需要认证的接口
3. 返回JSON格式的响应

```python
@app.route('/api/example', methods=['GET'])
@require_auth
def example_endpoint():
    try:
        # 你的逻辑
        return jsonify({'message': '成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 前端开发

#### API客户端

前端使用 `frontend/js/api.js` 中的API客户端与后端通信：

```javascript
// 获取项目列表
const projects = await api.getProjects();

// 创建项目
const newProject = await api.createProject({ name: '新项目' });

// 上传文件
const result = await api.uploadFile(file);
```

#### 添加新功能

1. 在 `frontend/js/api.js` 中添加新的API方法
2. 在前端页面中调用API
3. 处理响应和错误

```javascript
// 在api.js中添加
async newFeature(data) {
    return this.request('/new-feature', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

// 在页面中使用
try {
    const result = await api.newFeature(data);
    console.log('成功:', result);
} catch (error) {
    console.error('失败:', error);
}
```

## 🌐 部署

### Render平台部署

项目已配置好Render部署，包括：

1. **前端静态网站** (`vidtools-frontend`)
2. **后端API服务** (`vidtools-backend`)

#### 环境变量配置

在Render Dashboard中为后端服务配置以下环境变量：

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE=your-service-role-key
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

### 其他平台部署

#### Vercel部署前端
```bash
# 安装Vercel CLI
npm i -g vercel

# 部署前端
cd frontend
vercel
```

#### Railway部署后端
```bash
# 安装Railway CLI
npm i -g @railway/cli

# 部署后端
cd backend
railway login
railway init
railway up
```

## 🔒 安全说明

- 前端不要暴露 `SERVICE_ROLE_KEY`
- 所有文件上传使用签名URL
- 数据库启用行级安全策略
- JWT令牌通过Supabase JWKS验证
- API接口使用认证装饰器保护

## 🐛 常见问题

### 1. 后端启动失败
- 检查Python版本是否为3.8+
- 确认所有依赖已安装：`pip install -r requirements.txt`
- 检查环境变量配置是否正确

### 2. 前端无法连接后端
- 确认后端服务正在运行
- 检查CORS配置
- 确认API地址正确

### 3. 认证失败
- 检查Supabase配置
- 确认JWT令牌有效
- 检查认证头格式

### 4. 文件上传失败
- 检查文件大小限制
- 确认上传目录权限
- 检查存储配置

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建 Pull Request

## 📞 支持

如有问题，请：
1. 查看 [常见问题](#-常见问题) 部分
2. 搜索 [Issues](https://github.com/your-username/video-tools/issues)
3. 创建新的 Issue 