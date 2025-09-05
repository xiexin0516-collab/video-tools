#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cinematic Darken Tool - Integrated with Video Tools Platform
Supports multiple languages, configuration management, and modern UI
"""

import sys
import os
import json
import moviepy.editor as mp
from moviepy.video.fx.all import colorx
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
        """Get default language data for cinematic darken tool"""
        return {
            "cinematic_darken": {
                "title": "Cinematic Darken Tool" if self.current_lang == 'en' else "电影级调暗工具",
                "select_video": "Select Video File" if self.current_lang == 'en' else "选择视频文件",
                "output_path": "Output Path" if self.current_lang == 'en' else "输出路径",
                "brightness": "Brightness" if self.current_lang == 'en' else "亮度",
                "start_processing": "Start Processing" if self.current_lang == 'en' else "开始处理",
                "processing": "Processing..." if self.current_lang == 'en' else "处理中...",
                "success": "Video processed successfully!" if self.current_lang == 'en' else "视频处理成功！",
                "error": "Error" if self.current_lang == 'en' else "错误",
                "file_not_found": "File not found" if self.current_lang == 'en' else "文件未找到",
                "invalid_brightness": "Invalid brightness value" if self.current_lang == 'en' else "无效的亮度值",
                "processing_failed": "Processing failed" if self.current_lang == 'en' else "处理失败",
                "select_output": "Select Output Location" if self.current_lang == 'en' else "选择输出位置",
                "supported_formats": "Supported formats: MP4, AVI, MOV, MKV" if self.current_lang == 'en' else "支持格式：MP4, AVI, MOV, MKV",
                "brightness_tooltip": "Adjust video brightness (0.1-2.0, 1.0=original)" if self.current_lang == 'en' else "调整视频亮度 (0.1-2.0, 1.0=原始)"
            }
        }
    
    def get_text(self, key):
        """Get localized text"""
        keys = key.split('.')
        value = self.lang_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return key  # Return key if not found
        return value
    
    def switch_language(self, lang_code):
        """Switch language"""
        self.current_lang = lang_code
        self.load_language()

class CinematicDarkenTool(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.lang_manager = LanguageManager()
        self.input_file = ""
        self.output_file = ""
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(self.lang_manager.get_text('cinematic_darken.title'))
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel(self.lang_manager.get_text('cinematic_darken.title'))
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Language switch
        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        
        self.lang_btn = QPushButton("中文" if self.lang_manager.current_lang == 'en' else "English")
        self.lang_btn.clicked.connect(self.switch_language)
        self.lang_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        lang_layout.addWidget(self.lang_btn)
        layout.addLayout(lang_layout)
        
        # File selection
        file_group = QGroupBox(self.lang_manager.get_text('cinematic_darken.select_video'))
        file_layout = QVBoxLayout(file_group)
        
        file_input_layout = QHBoxLayout()
        self.file_label = QLabel(self.lang_manager.get_text('cinematic_darken.supported_formats'))
        self.file_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        file_input_layout.addWidget(self.file_label)
        file_input_layout.addStretch()
        
        self.select_file_btn = QPushButton("📁 " + self.lang_manager.get_text('cinematic_darken.select_video'))
        self.select_file_btn.clicked.connect(self.select_input_file)
        self.select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        file_input_layout.addWidget(self.select_file_btn)
        file_layout.addLayout(file_input_layout)
        
        self.file_path_label = QLabel("")
        self.file_path_label.setStyleSheet("color: #34495e; font-size: 14px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        file_layout.addWidget(self.file_path_label)
        
        layout.addWidget(file_group)
        
        # Output path
        output_group = QGroupBox(self.lang_manager.get_text('cinematic_darken.output_path'))
        output_layout = QVBoxLayout(output_group)
        
        output_input_layout = QHBoxLayout()
        self.output_path_label = QLabel("")
        self.output_path_label.setStyleSheet("color: #34495e; font-size: 14px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        output_input_layout.addWidget(self.output_path_label)
        output_input_layout.addStretch()
        
        self.select_output_btn = QPushButton("📁 " + self.lang_manager.get_text('cinematic_darken.select_output'))
        self.select_output_btn.clicked.connect(self.select_output_file)
        self.select_output_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        output_input_layout.addWidget(self.select_output_btn)
        output_layout.addLayout(output_input_layout)
        
        layout.addWidget(output_group)
        
        # Brightness control
        brightness_group = QGroupBox(self.lang_manager.get_text('cinematic_darken.brightness'))
        brightness_layout = QVBoxLayout(brightness_group)
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(10)
        self.brightness_slider.setMaximum(200)
        self.brightness_slider.setValue(70)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.valueChanged.connect(self.update_brightness_label)
        brightness_layout.addWidget(self.brightness_slider)
        
        self.brightness_label = QLabel("70%")
        self.brightness_label.setAlignment(Qt.AlignCenter)
        self.brightness_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        brightness_layout.addWidget(self.brightness_label)
        
        brightness_tooltip = QLabel(self.lang_manager.get_text('cinematic_darken.brightness_tooltip'))
        brightness_tooltip.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        brightness_tooltip.setAlignment(Qt.AlignCenter)
        brightness_layout.addWidget(brightness_tooltip)
        
        layout.addWidget(brightness_group)
        
        # Process button
        self.process_btn = QPushButton("🎬 " + self.lang_manager.get_text('cinematic_darken.start_processing'))
        self.process_btn.clicked.connect(self.process_video)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout.addWidget(self.status_label)
    
    def switch_language(self):
        """Switch between languages"""
        if self.lang_manager.current_lang == 'en':
            self.lang_manager.switch_language('zh')
            self.lang_btn.setText("English")
        else:
            self.lang_manager.switch_language('en')
            self.lang_btn.setText("中文")
        
        # Refresh UI
        self.init_ui()
    
    def update_brightness_label(self, value):
        """Update brightness label"""
        self.brightness_label.setText(f"{value}%")
    
    def select_input_file(self):
        """Select input video file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.lang_manager.get_text('cinematic_darken.select_video'),
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)"
        )
        
        if file_path:
            self.input_file = file_path
            self.file_path_label.setText(os.path.basename(file_path))
            self.update_process_button()
    
    def select_output_file(self):
        """Select output file location"""
        if not self.input_file:
            QMessageBox.warning(self, self.lang_manager.get_text('cinematic_darken.error'), 
                              self.lang_manager.get_text('cinematic_darken.file_not_found'))
            return
        
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        default_name = f"{base_name}_darkened.mp4"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.lang_manager.get_text('cinematic_darken.select_output'),
            default_name,
            "MP4 Files (*.mp4);;All Files (*)"
        )
        
        if file_path:
            self.output_file = file_path
            self.output_path_label.setText(os.path.basename(file_path))
            self.update_process_button()
    
    def update_process_button(self):
        """Update process button state"""
        if self.input_file and self.output_file:
            self.process_btn.setEnabled(True)
        else:
            self.process_btn.setEnabled(False)
    
    def process_video(self):
        """Process video with cinematic darkening"""
        if not self.input_file or not self.output_file:
            return
        
        try:
            # Show progress
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.process_btn.setEnabled(False)
            self.status_label.setText(self.lang_manager.get_text('cinematic_darken.processing'))
            
            # Calculate brightness factor
            brightness_percent = self.brightness_slider.value()
            brightness_factor = brightness_percent / 100.0
            
            # Process video
            QApplication.processEvents()  # Update UI
            
            clip = mp.VideoFileClip(self.input_file)
            darker_clip = colorx(clip, brightness_factor)
            darker_clip.write_videofile(self.output_file, codec="libx264", audio_codec="aac")
            
            # Clean up
            clip.close()
            darker_clip.close()
            
            # Success
            self.progress_bar.setVisible(False)
            self.status_label.setText(self.lang_manager.get_text('cinematic_darken.success'))
            QMessageBox.information(self, self.lang_manager.get_text('cinematic_darken.success'), 
                                  f"Video saved to: {self.output_file}")
            
        except Exception as e:
            # Error
            self.progress_bar.setVisible(False)
            self.status_label.setText(self.lang_manager.get_text('cinematic_darken.processing_failed'))
            QMessageBox.critical(self, self.lang_manager.get_text('cinematic_darken.error'), 
                               f"Error: {str(e)}")
        
        finally:
            self.process_btn.setEnabled(True)

def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = CinematicDarkenTool()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
