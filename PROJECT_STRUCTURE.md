# Video Tools 项目结构

## 📁 目录结构

```
video-tools/
├── 📁 docs/                    # 网站文件
│   ├── 📄 index.html          # 主页面
│   ├── 📁 js/                 # JavaScript 文件
│   │   ├── download-stats.js  # 下载统计系统
│   │   ├── tools-config.js    # 工具配置
│   │   └── ...
│   ├── 📁 admin/              # 管理后台
│   │   └── stats.html         # 统计管理页面
│   └── 📄 CNAME               # 域名配置
│
├── 📁 src/                     # 源代码
│   ├── 📄 manual_subtitle_editor.py    # 字幕编辑器主程序
│   ├── 📄 language_loader.py           # 语言加载器
│   └── 📄 build_manual_subtitle.py     # 构建脚本
│
├── 📁 scripts/                 # 构建和部署脚本
│   └── 📄 build_manual.bat    # Windows 构建脚本
│
├── 📁 locales/                 # 多语言文件
│
├── 📁 .github/                 # GitHub 配置
│   └── 📁 workflows/           # GitHub Actions
│
├── 📄 README.md                # 中文说明文档
├── 📄 README_EN.md             # 英文说明文档
├── 📄 README-STATS.md          # 统计系统说明
├── 📄 PROJECT_STRUCTURE.md     # 项目结构说明（本文件）
├── 📄 LICENSE                  # MIT 许可证
├── 📄 .gitignore               # Git 忽略规则
├── 📄 requirements.txt         # Python 依赖
└── 📄 config.json              # 配置文件
```

## 🎯 核心组件

### 1. 字幕编辑器 (`src/manual_subtitle_editor.py`)
- 基于时间轴的专业字幕编辑工具
- 支持多种音频格式
- 智能吸附和实时预览

### 2. 网站平台 (`docs/`)
- 现代化的工具展示界面
- 下载统计系统
- 多语言支持

### 3. 构建系统 (`scripts/`)
- 自动化构建脚本
- 跨平台支持

## 🚀 开发指南

### 添加新工具
1. 在 `src/` 目录下创建新的 Python 文件
2. 在 `docs/js/tools-config.js` 中添加工具配置
3. 更新相关文档

### 修改网站
1. 主要文件在 `docs/` 目录
2. 样式和脚本在 `docs/js/` 目录
3. 多语言支持在 `locales/` 目录

### 构建和发布
1. 使用 `scripts/build_manual.bat` 构建 Windows 版本
2. 通过 GitHub Releases 发布软件包
3. 网站自动部署到 `vidtools.tools`

## 📋 文件命名规范

- **源代码文件**: 使用下划线命名法 (`snake_case`)
- **配置文件**: 使用小写和连字符 (`kebab-case`)
- **目录名**: 使用小写和连字符
- **避免**: 中文文件名、空格、特殊字符

## 🔧 维护说明

- 定期清理 `dist/` 和 `build/` 目录
- 使用 `.gitignore` 避免提交不必要的文件
- 大文件通过 GitHub Releases 发布，不要直接提交到仓库
- 保持目录结构清晰，便于维护和扩展

## 📞 技术支持

如有问题，请通过 GitHub Issues 联系我们。
