📄 README.md 给 Cursor 的文档（英文，专为多语言字幕工具的网页部署）
# SubtitleEditor Web — Multi-language Video Tool Platform (Initial Tool)

## 🧩 Project Goal

This is the first tool of a future multi-tool suite for video creators. It is a **multi-language, web-based subtitle editor**, currently open for free use, especially for creators in the U.S. with international audiences. More tools will be added in the future under a unified interface (same domain).

## 🌍 Multi-language

The web interface must support multilingual users (at least English + Chinese). Language can be detected automatically or selected manually via UI.

## 🛠️ Tech Stack

You may choose any frontend/backend stack that supports:
- Web-based UI (subtitle editing timeline, text input, file upload)
- Backend for subtitle parsing, saving, and exporting (TXT / SRT)
- Multi-language UI support (i18n)

Recommended stack:
- Frontend: React + i18n + Tailwind CSS
- Backend: Flask / FastAPI / Node.js / etc.
- Deployment: GitHub → Render.com (Auto Deploy)
- Future: Add more tools to the platform (tool buttons / pages)

## 🎯 Core Features (MVP for v1)

- Upload an audio file (MP3 / WAV / M4A)
- Upload a subtitle file (TXT / SRT)
- View + Edit subtitle text alongside audio waveform
- Timeline-based subtitle editor
- Export SRT or TXT file
- Multilingual interface toggle (EN / 中文)

## 📁 Folder Structure



video-tools/
├── frontend/
│ ├── index.html (React-based UI)
│ └── i18n/
│ └── en.json, zh.json
├── backend/
│ ├── main.py (Flask or FastAPI)
│ └── services/
│ └── subtitle_parser.py
├── static/
│ └── demo_subtitles.srt
├── README.md
└── requirements.txt


## 🚀 Deployment

### 快速部署到 Render.com

1. **推送代码到GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit: SubtitleEditor Web"
   git push origin main
   ```

2. **在Render.com上部署**:
   - 访问 [Render.com](https://render.com)
   - 创建新的Web Service
   - 连接GitHub仓库 `video-tools`
   - 配置设置：
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd backend && gunicorn main:app --bind 0.0.0.0:$PORT`
     - **Plan**: Free

3. **配置自定义域名**:
   - 域名: `vidtools.tools` (已注册)
   - 在Render.com设置中添加自定义域名
   - 配置DNS记录

4. **自动部署**:
   - 每次推送到main分支时自动重新部署
   - 可在Render.com仪表板查看部署状态

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python run.py

# 访问 http://localhost:5000
```

详细部署说明请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔜 Future Plan

This web platform will evolve into a **toolbox for YouTube creators**, offering utilities like:
- Watermark remover
- Audio extractor
- Voice-to-subtitle (Whisper integration)
- Bilingual subtitle merger
- Frame-level editing helper
- YouTube metadata optimizer

Each tool will be added as a button on homepage.

## 👤 Maintainer

- 🇺🇸 Project owner is based in the U.S.
- Target audience includes creators with multilingual needs
- Initial tool is **free** for all; future tools may include **freemium features**
- GitHub: [https://github.com/xiexin0516-collab/video-tools](https://github.com/xiexin0516-collab/video-tools)

✅ 你可以做的下一步：

将上述文档粘贴为项目根目录下的 README.md 文件（给 Cursor 看）

在 Cursor 中打开你的 video-tools GitHub 仓库

让 Cursor 阅读 README.md，然后给它任务提示：

Deploy this project to Render.com using my GitHub repo. Make sure it's accessible via vidtools.tools. 