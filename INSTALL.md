# Video Tools Platform - 安装指南

## 📋 系统要求

- **操作系统**: Windows 10/11 (64位)
- **Python**: 3.8 或更高版本
- **内存**: 建议 8GB 或更多
- **存储空间**: 至少 2GB 可用空间

## 🚀 快速安装

### 1. 安装 Python 依赖

```bash
# 克隆或下载项目后，在项目根目录运行：
pip install -r requirements.txt
```

### 2. 验证安装

```bash
# 测试 Cinematic Photo FX
python src/CinematicPhotoFX.py

# 测试 Cinematic Darken Tool
python src/cinematic_darken.py

# 测试 Format Converter
python src/format_converter.py
```

## 📦 依赖包说明

### 核心依赖
- **pyinstaller**: 用于打包可执行文件
- **PyQt5**: GUI框架 (字幕编辑器使用)
- **moviepy**: 视频处理库
- **ffmpeg-python**: FFmpeg Python绑定
- **Pillow**: 图像处理库
- **numpy**: 数值计算库

### 内置模块
- **tkinter**: Python内置GUI库 (Cinematic Photo FX使用)
- **json**: 配置文件处理
- **os, sys**: 系统操作

## 🛠️ 构建可执行文件

### Cinematic Photo FX
```bash
# 运行构建脚本
python src/build_cinematic_photo_fx.py

# 或使用批处理文件
scripts\build_cinematic_photo_fx.bat
```

### Cinematic Darken Tool
```bash
# 运行构建脚本
python src/build_cinematic_darken.py

# 或使用批处理文件
scripts\build_cinematic_darken.bat
```

### Format Converter
```bash
# 运行构建脚本
python src/build_format_converter.py

# 或使用批处理文件
scripts\build_format_converter.bat
```

## 🌐 多语言支持

所有工具都支持中英文双语：

### 切换语言
- **Cinematic Photo FX**: 通过配置文件 `src/config.json` 设置
- **其他工具**: 程序启动时自动检测系统语言

### 语言文件位置
- **统一国际化系统**: `docs/i18n/zh.json`, `docs/i18n/en.json`
- **所有工具**: 网站和桌面程序都使用同一套翻译文件

## 🔧 故障排除

### 常见问题

1. **ImportError: No module named 'moviepy'**
   ```bash
   pip install moviepy==1.0.3
   ```

2. **ImportError: No module named 'PIL'**
   ```bash
   pip install Pillow==10.0.1
   ```

3. **PyInstaller 构建失败**
   ```bash
   pip install pyinstaller==5.13.2
   ```

4. **FFmpeg 相关错误**
   - 确保系统已安装 FFmpeg
   - 或使用 `pip install ffmpeg-python==0.2.0`

### 性能优化

- **Cinematic Photo FX**: 建议每次处理不超过50张图片
- **视频处理**: 确保有足够的磁盘空间用于临时文件
- **内存使用**: 大文件处理时建议关闭其他程序

## 📞 技术支持

如果遇到问题，请：
1. 检查 Python 版本 (需要 3.8+)
2. 确认所有依赖已正确安装
3. 查看错误日志信息
4. 联系技术支持

## 📄 许可证

MIT License - 免费使用和修改

---

**注意**: 所有工具都完全在本地运行，不会向服务器发送任何数据，保护您的隐私安全。
