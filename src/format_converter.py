#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Format Converter - Integrated with Video Tools Platform
Supports multiple languages, configuration management, and modern UI
"""

import sys
import os
import json
import ffmpeg
from datetime import datetime

# Import PyQt5 components
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    print("✅ PyQt5 导入成功")
except ImportError as e:
    print(f"❌ PyQt5 导入失败: {e}")
    print("请安装 PyQt5: pip install PyQt5")
    input("按回车键退出...")
    sys.exit(1)

class LanguageManager:
    """Language management system integrated with website"""
    
    def __init__(self):
        self.current_lang = 'en'  # Default English (consistent with website)
        self.lang_data = {}
        self.load_language()
    
    def load_language(self):
        """Load language files from docs/i18n directory"""
        try:
            # Try to load from docs/i18n first (website structure)
            lang_file = os.path.join(os.path.dirname(__file__), '..', 'docs', 'i18n', f'{self.current_lang}.json')
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.lang_data = json.load(f)
                print(f"✅ 语言文件加载成功: {lang_file}")
                return
                
        except Exception as e:
            print(f"⚠️ 语言文件加载失败: {e}")
        
        # 直接使用默认语言数据，避免复杂的文件加载逻辑
        self.lang_data = self.get_default_language()
        print(f"✅ 使用默认语言数据: {self.current_lang}")
    
    def get_default_language(self):
        """Default language data for format converter"""
        if self.current_lang == 'en':
            return {
                "format_converter": {
                    "title": "Video Format Converter",
                    "select_file": "Select Video File",
                    "convert": "Start Conversion",
                    "converting": "Converting...",
                    "convert_success": "Conversion Complete",
                    "convert_failed": "Conversion Failed",
                    "select_output": "Select Output Directory",
                    "output_format": "Output Format",
                    "resolution": "Resolution",
                    "quality": "Quality",
                    "preset": "Preset",
                    "batch_convert": "Batch Conversion",
                    "progress": "Progress",
                    "file_size": "File Size",
                    "duration": "Duration",
                    "settings": "Settings",
                    "about": "About",
                    "browse": "Browse...",
                    "conversion_control": "Conversion Control",
                    "conversion_progress": "Conversion Progress",
                    "ready": "Ready",
                    "language_label": "Language:",
                    "warning": "Warning",
                    "success": "Success",
                    "error": "Error"
                }
            }
        else:
            return {
                "format_converter": {
                    "title": "视频格式转换器",
                    "select_file": "选择视频文件",
                    "convert": "开始转换",
                    "converting": "正在转换...",
                    "convert_success": "转换完成",
                    "convert_failed": "转换失败",
                    "select_output": "选择输出目录",
                    "output_format": "输出格式",
                    "resolution": "分辨率",
                    "quality": "质量",
                    "preset": "预设",
                    "batch_convert": "批量转换",
                    "progress": "进度",
                    "file_size": "文件大小",
                    "duration": "时长",
                    "settings": "设置",
                    "about": "关于",
                    "browse": "浏览...",
                    "conversion_control": "转换控制",
                    "conversion_progress": "转换进度",
                    "ready": "准备就绪",
                    "language_label": "语言:",
                    "warning": "警告",
                    "success": "成功",
                    "error": "错误"
                }
            }
    
    def get_text(self, key, default=""):
        """Get text by key with fallback"""
        try:
            # 尝试从format_converter部分获取
            if "format_converter" in self.lang_data:
                result = self.lang_data["format_converter"].get(key, default)
                if result:
                    return result
            
            # 如果format_converter部分不存在或没有找到key，使用默认值
            return default
        except Exception as e:
            print(f"获取语言文本失败: {key}, 错误: {e}")
            return default
    
    def switch_language(self, lang):
        """Switch language"""
        print(f"正在切换语言到: {lang}")
        self.current_lang = lang
        self.load_language()
        print(f"语言数据加载完成，当前语言: {self.current_lang}")
        print(f"可用的键: {list(self.lang_data.keys())}")
        if "format_converter" in self.lang_data:
            print(f"format_converter键: {list(self.lang_data['format_converter'].keys())}")

class ConfigManager:
    """Configuration management system integrated with website"""
    
    def __init__(self):
        self.tools_config = {}
        self.load_tools_config()
    
    def load_tools_config(self):
        """Load tools configuration from tools-config.js"""
        try:
            # Try to load from docs/js directory
            config_file = os.path.join(os.path.dirname(__file__), '..', 'docs', 'js', 'tools-config.js')
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract tools configuration from JavaScript
                    self.parse_js_config(content)
                    print(f"✅ 工具配置加载成功: {config_file}")
                    return
                    
        except Exception as e:
            print(f"⚠️ 工具配置加载失败: {e}")
        
        # Default configuration if file not found
        self.tools_config = self.get_default_config()
    
    def parse_js_config(self, content):
        """Parse JavaScript configuration file"""
        try:
            # Simple parsing for tools configuration
            # This is a basic implementation, can be enhanced
            if 'format-converter' in content or 'format_converter' in content:
                self.tools_config = {
                    "id": "format-converter",
                    "name": "视频格式转换器",
                    "version": "v1.0.0",
                    "description": "专业的视频格式转换工具，支持多种格式和参数调节"
                }
        except Exception as e:
            print(f"⚠️ 配置解析失败: {e}")
    
    def get_default_config(self):
        """Default configuration for format converter"""
        return {
            "id": "format-converter",
            "name": "视频格式转换器",
            "version": "v1.0.0",
            "description": "专业的视频格式转换工具，支持多种格式和参数调节"
        }

class VideoConverter:
    """Core video conversion functionality"""
    
    def __init__(self):
        self.supported_formats = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv']
        self.resolution_presets = [
            ('720p', 1280, 720),
            ('1080p', 1920, 1080),
            ('4K', 3840, 2160),
            ('Custom', 0, 0)
        ]
        self.quality_presets = [
            ('High', 18),
            ('Medium', 23),
            ('Low', 28),
            ('Custom', 23)
        ]
        self.encoding_presets = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
    
    def convert_video(self, input_path, output_path, resolution=None, quality=None, preset='fast'):
        """Convert video with specified parameters"""
        try:
            # Build ffmpeg command
            stream = ffmpeg.input(input_path)
            
            # Apply resolution filter if specified
            if resolution and resolution != (0, 0):
                stream = stream.filter('scale', resolution[0], resolution[1])
            
            # Set output parameters
            output_args = {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'preset': preset,
                'overwrite_output': True
            }
            
            # Apply quality setting
            if quality:
                output_args['crf'] = quality
            
            # Run conversion
            stream.output(output_path, **output_args).run(overwrite_output=True)
            
            return True, ""
            
        except ffmpeg.Error as e:
            return False, f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}"
        except Exception as e:
            return False, f"Conversion error: {str(e)}"

class FormatConverterUI(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.lang_manager = LanguageManager()
        self.config_manager = ConfigManager()
        self.video_converter = VideoConverter()
        self.conversion_thread = None
        
        self.init_ui()
        self.load_config()
    
    # —— 小工具：占位符与文件过滤器 —— #
    def _ph_select_file(self):
        return "Select a video file..." if self.lang_manager.current_lang=='en' else "请选择要转换的视频文件..."
    
    def _ph_select_folder(self):
        return "Select a folder containing video files..." if self.lang_manager.current_lang=='en' else "请选择包含视频文件的文件夹..."
    
    def _video_filter(self):
        if self.lang_manager.current_lang=='en':
            return "Video files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv);;All files (*.*)"
        else:
            return "视频文件 (*.mp4 *.avi *.mov *.mkv *.wmv *.flv);;所有文件 (*.*)"
    
    def _t(self, key, zh, en):
        return en if self.lang_manager.current_lang=='en' else zh
    
    def _rebuild_resolution_combo(self):
        """重建分辨率下拉框，使用当前语言"""
        self.resolution_combo.clear()
        if self.lang_manager.current_lang == 'en':
            custom = "Custom"
        else:
            custom = "自定义"
        for name, w, h in self.video_converter.resolution_presets:
            if name == 'Custom':
                text = f"{custom}"
            else:
                text = f"{name} ({w}x{h})"
            self.resolution_combo.addItem(text)
        # 默认选择1080p
        self.resolution_combo.setCurrentText('1080p (1920x1080)')
    
    def _rebuild_quality_combo(self):
        """重建质量下拉框，使用当前语言"""
        self.quality_combo.clear()
        if self.lang_manager.current_lang == 'en':
            names = {'High':'High','Medium':'Medium','Low':'Low','Custom':'Custom'}
        else:
            names = {'High':'高','Medium':'中','Low':'低','Custom':'自定义'}
        for name, crf in self.video_converter.quality_presets:
            self.quality_combo.addItem(f"{names.get(name,name)} (CRF: {crf})")
        # 默认选择Medium
        self.quality_combo.setCurrentText('Medium (CRF: 23)' if self.lang_manager.current_lang == 'en' else '中 (CRF: 23)')
    
    def _rebuild_comboboxes_localized(self):
        """重建所有下拉框，使用当前语言"""
        # 保存索引
        res_idx = self.resolution_combo.currentIndex()
        qlt_idx = self.quality_combo.currentIndex()
        
        # 重建分辨率
        self._rebuild_resolution_combo()
        self.resolution_combo.setCurrentIndex(min(res_idx, self.resolution_combo.count()-1))
        
        # 重建质量
        self._rebuild_quality_combo()
        self.quality_combo.setCurrentIndex(min(qlt_idx, self.quality_combo.count()-1))
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(self.lang_manager.get_text("title", "视频格式转换器"))
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # File selection section
        self.create_file_section(main_layout)
        
        # Settings section
        self.create_settings_section(main_layout)
        
        # Conversion section
        self.create_conversion_section(main_layout)
        
        # Progress section
        self.create_progress_section(main_layout)
        
        # Status bar
        self.statusBar().showMessage(self.lang_manager.get_text("title", "视频格式转换器"))
    
    def create_file_section(self, parent_layout):
        """Create file selection section"""
        self.file_group = QGroupBox(self.lang_manager.get_text("select_file", "选择视频文件"))
        layout = QVBoxLayout(self.file_group)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText(self._ph_select_file())  # ✅ 占位符本地化
        self.file_path_edit.setReadOnly(True)
        
        self.browse_btn = QPushButton(self.lang_manager.get_text("browse", "浏览..."))  # ✅ 保存引用
        self.browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_btn)
        layout.addLayout(file_layout)
        
        # Batch mode
        self.batch_checkbox = QCheckBox(self.lang_manager.get_text("batch_convert", "批量转换"))
        self.batch_checkbox.stateChanged.connect(self.toggle_batch_mode)
        layout.addWidget(self.batch_checkbox)
        
        parent_layout.addWidget(self.file_group)
    
    def create_settings_section(self, parent_layout):
        """Create settings section"""
        self.settings_group = QGroupBox(self.lang_manager.get_text("settings", "设置"))
        layout = QGridLayout(self.settings_group)
        
        # Output format
        self.output_format_label = QLabel(self.lang_manager.get_text("output_format", "输出格式"))
        layout.addWidget(self.output_format_label, 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(['MP4', 'AVI', 'MOV', 'MKV'])
        self.format_combo.setCurrentText('MP4')
        layout.addWidget(self.format_combo, 0, 1)
        
        # Resolution
        self.resolution_label = QLabel(self.lang_manager.get_text("resolution", "分辨率"))
        layout.addWidget(self.resolution_label, 1, 0)
        self.resolution_combo = QComboBox()
        self._rebuild_resolution_combo()
        layout.addWidget(self.resolution_combo, 1, 1)
        
        # Quality
        self.quality_label = QLabel(self.lang_manager.get_text("quality", "质量"))
        layout.addWidget(self.quality_label, 2, 0)
        self.quality_combo = QComboBox()
        self._rebuild_quality_combo()
        layout.addWidget(self.quality_combo, 2, 1)
        
        # Preset
        self.preset_label = QLabel(self.lang_manager.get_text("preset", "预设"))
        layout.addWidget(self.preset_label, 3, 0)
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(self.video_converter.encoding_presets)
        self.preset_combo.setCurrentText('fast')
        layout.addWidget(self.preset_combo, 3, 1)
        
        parent_layout.addWidget(self.settings_group)
    
    def create_conversion_section(self, parent_layout):
        """Create conversion control section"""
        self.control_group = QGroupBox(self.lang_manager.get_text("conversion_control", "转换控制"))
        layout = QHBoxLayout(self.control_group)
        
        # Convert button
        self.convert_btn = QPushButton(self.lang_manager.get_text("convert", "开始转换"))
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #6b7280;
            }
        """)
        self.convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_btn)
        
        # Language switch
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel(self.lang_manager.get_text("language_label", "语言:"))
        lang_layout.addWidget(self.lang_label)
        
        self.zh_btn = QPushButton("中文")
        self.zh_btn.clicked.connect(lambda: self.switch_language('zh'))
        lang_layout.addWidget(self.zh_btn)
        
        self.en_btn = QPushButton("English")
        self.en_btn.clicked.connect(lambda: self.switch_language('en'))
        lang_layout.addWidget(self.en_btn)
        
        layout.addLayout(lang_layout)
        
        parent_layout.addWidget(self.control_group)
    
    def create_progress_section(self, parent_layout):
        """Create progress display section"""
        self.progress_group = QGroupBox(self.lang_manager.get_text("conversion_progress", "转换进度"))
        layout = QVBoxLayout(self.progress_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel(self.lang_manager.get_text("ready", "准备就绪"))
        layout.addWidget(self.status_label)
        
        # Log text - 简化显示，只显示操作状态
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(80)  # 减小高度
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText(self._t("log_placeholder", "操作日志将在这里显示...", "Operation logs will be displayed here..."))  # 添加占位符提示
        layout.addWidget(self.log_text)
        
        parent_layout.addWidget(self.progress_group)
    
    def load_config(self):
        """Load configuration and update UI"""
        config = self.config_manager.tools_config
        if config:
            self.setWindowTitle(f"{config.get('name', '视频格式转换器')} {config.get('version', 'v1.0.0')}")
            # 移除工具信息显示，避免重复和冗余
    
    def browse_file(self):
        """Browse for video file"""
        if self.batch_checkbox.isChecked():
            title = self._t("sel_dir", "选择包含视频文件的文件夹", "Select a folder containing video files")
            folder = QFileDialog.getExistingDirectory(self, title)
            if folder:
                self.file_path_edit.setText(folder)
                self.log_text.append(f"📁 {self._t('folder_selected', '已选择文件夹', 'Folder selected')}: {os.path.basename(folder)}")
        else:
            title = self.lang_manager.get_text("select_file", "选择视频文件")
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                title,
                "",
                self._video_filter()
            )
            if file_path:
                self.file_path_edit.setText(file_path)
                self.log_text.append(f"📄 {self._t('file_selected', '已选择文件', 'File selected')}: {os.path.basename(file_path)}")
    
    def toggle_batch_mode(self, state):
        """Toggle between single file and batch mode"""
        self.file_path_edit.setPlaceholderText(self._ph_select_folder() if state == Qt.Checked else self._ph_select_file())
    
    def start_conversion(self):
        """Start video conversion"""
        file_path = self.file_path_edit.text().strip()
        if not file_path:
            QMessageBox.warning(self, self.lang_manager.get_text("warning", "警告"), 
                               self._t("no_file_selected", "请先选择要转换的文件或文件夹", "Please select a file or folder to convert"))
            return
        
        # Get conversion parameters
        resolution_idx = self.resolution_combo.currentIndex()
        quality_idx = self.quality_combo.currentIndex()
        preset = self.preset_combo.currentText()
        
        # Parse parameters
        resolution = self.video_converter.resolution_presets[resolution_idx][1:]
        quality = self.video_converter.quality_presets[quality_idx][1]
        
        # Start conversion
        if self.batch_checkbox.isChecked():
            self.start_batch_conversion(file_path, resolution, quality, preset)
        else:
            self.start_single_conversion(file_path, resolution, quality, preset)
    
    def start_single_conversion(self, input_path, resolution, quality, preset):
        """Start single file conversion"""
        # Generate output path
        folder, filename = os.path.split(input_path)
        name, ext = os.path.splitext(filename)
        output_format = self.format_combo.currentText().lower()
        output_path = os.path.join(folder, f"{name}_converted.{output_format}")
        
        # Update UI
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText(self.lang_manager.get_text("converting", "正在转换..."))
        self.log_text.append(f"🔄 {self._t('start_converting', '开始转换', 'Start converting')}: {filename}")
        
        # Run conversion in thread
        self.conversion_thread = ConversionThread(
            self.video_converter, input_path, output_path, resolution, quality, preset
        )
        self.conversion_thread.result.connect(self.conversion_finished)  # ✅ 改连 result
        self.conversion_thread.start()
    
    def start_batch_conversion(self, folder_path, resolution, quality, preset):
        """Start batch conversion"""
        # Find video files in folder
        video_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in self.video_converter.supported_formats):
                video_files.append(os.path.join(folder_path, file))
        
        if not video_files:
            QMessageBox.warning(self, self.lang_manager.get_text("warning", "警告"), 
                               self._t("no_video_files", "所选文件夹中没有找到视频文件", "No video files found in the selected folder"))
            return
        
        self.log_text.append(f"📁 {self._t('found_videos', '找到', 'Found')} {len(video_files)} {self._t('video_files', '个视频文件', 'video files')}")
        # For now, just convert the first file as example
        self.start_single_conversion(video_files[0], resolution, quality, preset)
    
    def conversion_finished(self, success, err):
        """Handle conversion completion"""
        self.convert_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_label.setText(self.lang_manager.get_text("convert_success", "转换完成"))
            self.log_text.append(f"✅ {self._t('convert_complete', '转换完成', 'Conversion complete')}")
            QMessageBox.information(self, self.lang_manager.get_text("success", "成功"),
                                    self.lang_manager.get_text("convert_success", "转换完成"))
        else:
            self.status_label.setText(self.lang_manager.get_text("convert_failed", "转换失败"))
            self.log_text.append(f"❌ {self._t('convert_failed', '转换失败', 'Conversion failed')}")
            QMessageBox.critical(self, self.lang_manager.get_text("error", "错误"),
                                 err or self.lang_manager.get_text("convert_failed", "转换失败"))
    
    def switch_language(self, lang):
        """Switch application language"""
        if self.lang_manager.current_lang == lang:
            return
            
        self.lang_manager.switch_language(lang)
        self.update_ui_language()
    
    def update_ui_language(self):
        """Update UI text after language change"""
        try:
            # 窗口与分组标题
            self.setWindowTitle(self.lang_manager.get_text("title", "视频格式转换器"))
            self.file_group.setTitle(self.lang_manager.get_text("select_file", "选择视频文件"))
            self.settings_group.setTitle(self.lang_manager.get_text("settings", "设置"))
            self.control_group.setTitle(self.lang_manager.get_text("conversion_control", "转换控制"))
            self.progress_group.setTitle(self.lang_manager.get_text("conversion_progress", "转换进度"))
            
            # 标签/按钮
            self.output_format_label.setText(self.lang_manager.get_text("output_format", "输出格式"))
            self.resolution_label.setText(self.lang_manager.get_text("resolution", "分辨率"))
            self.quality_label.setText(self.lang_manager.get_text("quality", "质量"))
            self.preset_label.setText(self.lang_manager.get_text("preset", "预设"))
            self.convert_btn.setText(self.lang_manager.get_text("convert", "开始转换"))
            self.lang_label.setText(self.lang_manager.get_text("language_label", "语言:"))
            self.browse_btn.setText(self.lang_manager.get_text("browse", "浏览..."))
            self.batch_checkbox.setText(self.lang_manager.get_text("batch_convert", "批量转换"))
            self.status_label.setText(self.lang_manager.get_text("ready", "准备就绪"))
            
            # 语言切换按钮
            self.zh_btn.setText("中文")
            self.en_btn.setText("English")
            
            # 占位符文本
            self.file_path_edit.setPlaceholderText(self._ph_select_folder() if self.batch_checkbox.isChecked() else self._ph_select_file())
            
            # 组合框重建
            self._rebuild_comboboxes_localized()
            
            # 状态栏
            self.statusBar().showMessage(self.lang_manager.get_text("title", "视频格式转换器"))
            
            # 清空日志，避免累积信息
            if hasattr(self, 'log_text'):
                self.log_text.clear()
                self.log_text.setPlaceholderText(self._t("log_placeholder", "操作日志将在这里显示...", "Operation logs will be displayed here..."))
            
            # Force UI refresh
            self.update()
            
        except Exception as e:
            self.log_text.append(f"{self._t('lang_switch_failed', '语言切换更新失败', 'Language switch update failed')}: {str(e)}")
            print(f"语言切换更新失败: {str(e)}")

class ConversionThread(QThread):
    """Thread for video conversion to prevent UI freezing"""
    result = pyqtSignal(bool, str)  # ✅ 自定义信号
    
    def __init__(self, converter, input_path, output_path, resolution, quality, preset):
        super().__init__()
        self.converter = converter
        self.input_path = input_path
        self.output_path = output_path
        self.resolution = resolution
        self.quality = quality
        self.preset = preset
    
    def run(self):
        """Run conversion in thread"""
        ok, err = self.converter.convert_video(
            self.input_path, self.output_path, self.resolution, self.quality, self.preset
        )
        self.result.emit(ok, err or "")

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = FormatConverterUI()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
