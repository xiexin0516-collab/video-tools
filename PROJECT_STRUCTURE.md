# 📁 项目结构

## 🧹 清理后的文件组织

```
video-tools/
├── 📄 README.md              # 项目说明文档
├── 📄 DEPLOYMENT.md          # 详细部署说明
├── 📄 requirements.txt       # Python依赖包
├── 📄 render.yaml           # Render.com部署配置
├── 📄 wsgi.py               # WSGI入口点（生产环境）
├── 📄 run.py                # 本地开发启动脚本
├── 📄 .gitignore            # Git忽略文件配置
├── 📁 frontend/             # 前端文件
│   ├── 📄 index.html        # 主页面（React应用）
│   └── 📁 i18n/            # 国际化文件
│       ├── 📄 en.json      # 英文翻译
│       └── 📄 zh.json      # 中文翻译
├── 📁 backend/              # 后端文件
│   ├── 📄 main.py          # Flask应用主文件
│   ├── 📁 services/        # 服务层
│   │   └── 📄 subtitle_parser.py  # 字幕解析服务
│   └── 📁 uploads/         # 文件上传目录（空）
└── 📁 static/              # 静态文件
    └── 📄 demo_subtitles.srt  # 示例字幕文件
```

## 🗑️ 已删除的临时文件

- ❌ `subtitle_editor.py` - 旧的PyQt5桌面应用文件
- ❌ `test_app.py` - 测试脚本
- ❌ `DEPLOYMENT_GUIDE.md` - 临时部署指南
- ❌ `backend/__pycache__/` - Python缓存文件
- ❌ `backend/services/__pycache__/` - Python缓存文件

## ✅ 保留的核心文件

### 部署相关
- `render.yaml` - Render.com配置
- `wsgi.py` - 生产环境入口点
- `requirements.txt` - 依赖管理

### 应用代码
- `frontend/index.html` - 前端界面
- `backend/main.py` - Flask后端
- `backend/services/subtitle_parser.py` - 字幕处理服务

### 文档
- `README.md` - 项目说明
- `DEPLOYMENT.md` - 部署指南

### 配置
- `.gitignore` - Git忽略规则
- `run.py` - 本地开发脚本

## 🚀 准备部署

项目现在已清理完毕，可以安全地推送到GitHub：

```bash
git add .
git commit -m "Clean project structure for deployment"
git push origin main
```

然后按照 `DEPLOYMENT.md` 中的步骤部署到Render.com。
