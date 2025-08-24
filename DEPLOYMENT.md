# 部署说明 - SubtitleEditor Web

## 🚀 部署到 Render.com

### 1. 准备工作

确保你的项目已经推送到GitHub仓库：
```bash
git add .
git commit -m "Initial commit: SubtitleEditor Web"
git push origin main
```

### 2. 在Render.com上部署

1. 访问 [Render.com](https://render.com) 并注册/登录
2. 点击 "New +" 按钮，选择 "Web Service"
3. 连接你的GitHub账户并选择 `video-tools` 仓库
4. 配置部署设置：
   - **Name**: `subtitleeditor-web`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn main:app --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`

### 3. 环境变量设置

在Render.com的Web Service设置中添加以下环境变量：
- `PYTHON_VERSION`: `3.9.16`
- `FLASK_ENV`: `production`

### 4. 自定义域名设置

1. 在Render.com的Web Service设置中找到 "Custom Domains"
2. 添加你的域名：`vidtools.tools`
3. 按照Render.com的指示配置DNS记录

### 5. 自动部署

- 每次推送到GitHub的main分支时，Render.com会自动重新部署
- 你可以在Render.com的仪表板中查看部署状态和日志

## 🛠️ 本地开发

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python run.py
```

应用将在 `http://localhost:5000` 启动

### 3. 开发模式

- 前端文件位于 `frontend/` 目录
- 后端文件位于 `backend/` 目录
- 静态文件位于 `static/` 目录

## 📁 项目结构

```
video-tools/
├── frontend/
│   ├── index.html          # 主页面
│   └── i18n/
│       ├── en.json         # 英文翻译
│       └── zh.json         # 中文翻译
├── backend/
│   ├── main.py             # Flask应用主文件
│   └── services/
│       └── subtitle_parser.py  # 字幕解析服务
├── static/
│   └── demo_subtitles.srt  # 示例字幕文件
├── requirements.txt        # Python依赖
├── render.yaml            # Render.com配置
├── run.py                 # 启动脚本
└── README.md              # 项目说明
```

## 🔧 API端点

### 字幕相关
- `POST /api/upload/subtitle` - 上传字幕文件
- `POST /api/subtitles/parse` - 解析字幕内容
- `POST /api/subtitles/export` - 导出字幕
- `POST /api/subtitles/save` - 保存项目
- `POST /api/subtitles/load` - 加载项目

### 音频相关
- `POST /api/upload/audio` - 上传音频文件

### 语言支持
- `GET /api/languages` - 获取支持的语言

## 🌐 多语言支持

应用支持中英文双语界面：
- 英文 (en)
- 中文 (zh)

用户可以通过界面右上角的语言切换器切换语言。

## 📝 功能特性

- ✅ 音频文件上传 (MP3, WAV, M4A, OGG)
- ✅ 字幕文件上传 (SRT, TXT)
- ✅ 音频可视化播放
- ✅ 字幕时间轴编辑
- ✅ 实时字幕同步
- ✅ 多语言界面
- ✅ 字幕导出 (SRT, TXT)
- ✅ 项目保存/加载
- ✅ 拖拽上传界面

## 🔮 未来计划

这个平台将发展成为YouTube创作者的完整工具箱，包括：
- 水印去除器
- 音频提取器
- 语音转字幕 (Whisper集成)
- 双语字幕合并器
- 帧级编辑助手
- YouTube元数据优化器

每个工具都将作为主页上的按钮添加。

## 📞 支持

如有问题，请通过以下方式联系：
- GitHub Issues: [项目仓库](https://github.com/xiexin0516-collab/video-tools)
- 邮箱: [项目维护者邮箱]

---

**注意**: 这是一个免费工具，专为视频创作者设计。所有功能都是免费的，无需注册即可使用。
