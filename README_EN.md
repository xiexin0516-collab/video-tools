# Manual Subtitle Editor - Professional Timeline-based Subtitle Creation Tool

A powerful subtitle editor designed specifically for video creators, featuring timeline-based editing, audio synchronization, and intelligent snap functionality.

## 🎯 Project Overview

This is a feature-rich subtitle editor designed specifically for video creators:

- **Timeline-based** - Completely avoids waveform synchronization issues
- **Audio Synchronization** - 100% accurate playback position synchronization
- **Smart Snap** - Automatic subtitle time alignment
- **Multi-language Support** - Chinese/English interface
- **Project Files** - Save and load editing projects

## 📁 Project Structure

```
video-tools/
├── frontend/                    # Official Website
│   ├── index.html              # Homepage
│   ├── js/                     # JavaScript files
│   └── subtitle-editor/        # Online editor
├── ManualSubtitleEditor-v1.0.0.zip # Release package
├── 手动上字幕改版新版本.py      # Main program source code
├── build_manual_subtitle.py    # Build script
├── locales/                    # Language files
└── README.md                   # Project documentation
```

## 🖥️ Subtitle Editor Features

### Core Features

* **🎬 Timeline Editing**  
   * Timeline-based, no waveform sync issues
   * Visual subtitle block editing
   * Smart zoom and navigation
* **🎵 Audio Synchronization**  
   * Audio file import and playback
   * 100% accurate playback position
   * Real-time timeline updates
* **🔗 Smart Snap**  
   * Automatic time point alignment
   * Multiple snap types
   * Adjustable snap sensitivity
   * Visual snap line indicators
* **📝 Text Management**  
   * Batch text import
   * Automatic text distribution
   * Text index reset

### Technology Stack

* **PyQt5** - Modern GUI framework
* **QMediaPlayer** - Audio playback support
* **PyInstaller** - Application packaging tool

## 🚀 Quick Start

### Download and Use

1. **Download Package**
   - Visit [Releases](https://github.com/xiexin0516-collab/video-tools/releases)
   - Download `ManualSubtitleEditor-v1.0.0.zip`

2. **Extract and Run**
   - Extract to any directory
   - Double-click `ManualSubtitleEditor.exe` to run

3. **Start Using**
   - Import audio file
   - Import text file
   - Create subtitles on timeline

### Development Environment

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Source Code**
   ```bash
   python 手动上字幕改版新版本.py
   ```

3. **Build and Release**
   ```bash
   python build_manual_subtitle.py
   ```

## 🌐 Official Website

The official website provides:
* Product feature introduction
* Desktop application download
* User usage guide

Visit: [https://vidtools.tools/](https://vidtools.tools/)

## 📦 Release Process

1. **Develop Features** - Modify source code
2. **Test and Verify** - Ensure functionality works
3. **Package Application** - Use build script
4. **Upload Release** - Upload to GitHub Releases
5. **Update Website** - Update download links

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

For questions or suggestions, please contact us through GitHub Issues.
