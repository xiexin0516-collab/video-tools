# 视频工具平台

专业的视频处理工具平台，提供桌面版应用和官方网站下载服务。

## 🎯 项目概述

本项目包含两个主要部分：
- **桌面版应用** (`desktop-app/`) - 功能完整的桌面工具
- **官方网站** (`frontend/`) - 产品展示和下载页面

## 📁 项目结构

```
video-tools/
├── desktop-app/          # 桌面版应用
│   ├── main.py          # 主程序入口
│   ├── requirements.txt # Python依赖
│   ├── build.py         # 自动打包脚本
│   ├── run.bat          # Windows运行脚本
│   ├── build.bat        # Windows打包脚本
│   └── README.md        # 桌面版说明文档
├── frontend/            # 官方网站
│   ├── index.html       # 主页
│   ├── js/             # JavaScript文件
│   └── subtitle-editor/ # 字幕编辑器（已弃用）
├── render.yaml          # Render部署配置
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明文档
```

## 🖥️ 桌面版应用

### 功能特色

- **🖼️ 图片处理工具**
  - 智能图片缩放
  - 格式转换 (JPG/PNG/WEBP)
  - 图片压缩优化

- **📸 截屏工具**
  - 全屏截图
  - 区域截图
  - 窗口截图

- **🎬 视频处理工具**
  - 视频格式转换
  - 音频提取
  - 视频压缩

### 技术栈

- **PyQt6** - 现代化GUI框架
- **OpenCV** - 计算机视觉库
- **Pillow** - 图像处理库
- **PyInstaller** - 应用打包工具

### 快速开始

1. **安装依赖**
   ```bash
   cd desktop-app
   pip install -r requirements.txt
   ```

2. **运行应用**
   ```bash
   python main.py
   # 或双击 run.bat
   ```

3. **打包发布**
   ```bash
   python build.py
   # 或双击 build.bat
   ```

## 🌐 官方网站

官方网站提供：
- 产品功能介绍
- 桌面版应用下载
- 用户使用指南

### 部署

使用 Render 平台自动部署：
- 静态网站服务
- 自动构建和部署
- 全球CDN加速

## 🚀 开发计划

### 第一阶段（MVP）
- [x] 基础界面框架
- [x] 官方网站
- [ ] 图片缩放功能
- [ ] 截屏功能

### 第二阶段
- [ ] 图片压缩功能
- [ ] 视频格式转换
- [ ] 音频提取功能

### 第三阶段
- [ ] 视频压缩功能
- [ ] 批量处理功能
- [ ] 高级设置选项

## 📦 发布流程

1. **开发功能** - 在 `desktop-app/` 中实现新功能
2. **测试验证** - 确保功能正常工作
3. **打包应用** - 使用 `build.py` 生成可执行文件
4. **上传发布** - 将 `.exe` 文件上传到 GitHub Releases
5. **更新网站** - 更新下载链接和版本信息

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。 