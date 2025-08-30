#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Desktop Application Framework
Supports multiple mini-programs/modules
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import internationalization support
from language_loader import lang

class MainApplication(QMainWindow):
    """Main desktop application window"""
    
    def __init__(self):
        super().__init__()
        self.modules = {}  # 存储所有模块
        self.current_module = None
        self.init_ui()
        self.load_modules()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(lang.get("app.title", "Multi-Tool Desktop App"))
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QHBoxLayout(central_widget)
        
        # 左侧模块选择面板
        self.create_module_panel(layout)
        
        # 右侧内容区域
        self.create_content_area(layout)
        
        # 设置菜单栏
        self.create_menu_bar()
        
    def create_module_panel(self, parent_layout):
        """Create module selection panel"""
        module_panel = QWidget()
        module_layout = QVBoxLayout(module_panel)
        
        # 模块选择标题
        title_label = QLabel(lang.get("app.modules", "应用模块"))
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        module_layout.addWidget(title_label)
        
        # 模块按钮容器
        self.module_buttons = QVBoxLayout()
        module_layout.addLayout(self.module_buttons)
        
        # 添加弹性空间
        module_layout.addStretch()
        
        # 设置面板样式
        module_panel.setMaximumWidth(200)
        module_panel.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-right: 1px solid #ccc;
            }
        """)
        
        parent_layout.addWidget(module_panel)
        
    def create_content_area(self, parent_layout):
        """Create main content area"""
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: white;
            }
        """)
        parent_layout.addWidget(self.content_stack)
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu(lang.get("menu.file", "文件"))
        
        # 设置菜单
        settings_menu = menubar.addMenu(lang.get("menu.settings", "设置"))
        
        # 语言设置
        lang_action = QAction(lang.get("menu.language", "语言"), self)
        lang_action.triggered.connect(self.show_language_settings)
        settings_menu.addAction(lang_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu(lang.get("menu.help", "帮助"))
        
    def load_modules(self):
        """Load all available modules"""
        # 字幕编辑器模块
        self.add_module("subtitle_editor", {
            "name": lang.get("module.subtitle_editor", "字幕编辑器"),
            "description": lang.get("module.subtitle_editor_desc", "时间轴字幕编辑工具"),
            "icon": "🎬",
            "file": "手动上字幕改版新版本.py"
        })
        
        # 这里可以添加更多模块
        # self.add_module("video_processor", {...})
        # self.add_module("audio_editor", {...})
        
    def add_module(self, module_id, module_info):
        """Add a new module to the application"""
        # 创建模块按钮
        btn = QPushButton(f"{module_info['icon']} {module_info['name']}")
        btn.setToolTip(module_info['description'])
        btn.clicked.connect(lambda: self.switch_module(module_id))
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        
        self.module_buttons.addWidget(btn)
        self.modules[module_id] = module_info
        
        # 创建模块内容页面
        module_widget = self.create_module_widget(module_id, module_info)
        self.content_stack.addWidget(module_widget)
        
    def create_module_widget(self, module_id, module_info):
        """Create widget for a specific module"""
        widget = QWidget()
        widget.setProperty("module_id", module_id)  # 设置模块ID属性
        layout = QVBoxLayout(widget)
        
        # 模块标题
        title = QLabel(module_info['name'])
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # 模块描述
        desc = QLabel(module_info['description'])
        desc.setStyleSheet("color: #666; padding: 5px 10px;")
        layout.addWidget(desc)
        
        # 启动模块按钮
        if module_id == "subtitle_editor":
            launch_btn = QPushButton(lang.get("btn.launch_editor", "启动字幕编辑器"))
            launch_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 14px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
            """)
            launch_btn.clicked.connect(self.launch_subtitle_editor)
            layout.addWidget(launch_btn)
        
        layout.addStretch()
        return widget
        
    def switch_module(self, module_id):
        """Switch to a different module"""
        if module_id in self.modules:
            # 找到对应的页面索引
            for i in range(self.content_stack.count()):
                if self.content_stack.widget(i).property("module_id") == module_id:
                    self.content_stack.setCurrentIndex(i)
                    break
                    
    def launch_subtitle_editor(self):
        """Launch the subtitle editor in a new window"""
        try:
            # 导入字幕编辑器模块
            import importlib.util
            # 获取当前脚本所在目录
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            subtitle_file = os.path.join(current_dir, "手动上字幕改版新版本.py")
            
            # 如果当前目录没有，尝试上级目录
            if not os.path.exists(subtitle_file):
                subtitle_file = os.path.join(os.path.dirname(current_dir), "手动上字幕改版新版本.py")
            
            spec = importlib.util.spec_from_file_location(
                "subtitle_editor", 
                subtitle_file
            )
            subtitle_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(subtitle_module)
            
            # 创建字幕编辑器窗口 - 修复类名
            if hasattr(subtitle_module, 'TimelineSubtitleTool'):
                self.subtitle_window = subtitle_module.TimelineSubtitleTool()
                self.subtitle_window.show()
            else:
                QMessageBox.warning(self, lang.get("msg.error", "错误"), lang.get("msg.editor_class_not_found", "无法找到字幕编辑器类"))
                
        except Exception as e:
            QMessageBox.critical(self, lang.get("msg.error", "错误"), lang.get("msg.editor_launch_failed", "启动字幕编辑器失败").format(error=str(e)))
            import traceback
            traceback.print_exc()
            
    def show_language_settings(self):
        """Show language settings dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle(lang.get("dialog.language", "语言设置"))
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # 语言选择
        lang_group = QGroupBox(lang.get("dialog.select_language", "选择语言"))
        lang_layout = QVBoxLayout(lang_group)
        
        zh_radio = QRadioButton(lang.get("lang.zh", "中文"))
        en_radio = QRadioButton(lang.get("lang.en", "English"))
        
        # 根据当前语言设置默认选择
        current_lang = self.get_current_language()
        if current_lang == "zh":
            zh_radio.setChecked(True)
        else:
            en_radio.setChecked(True)
            
        lang_layout.addWidget(zh_radio)
        lang_layout.addWidget(en_radio)
        layout.addWidget(lang_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton(lang.get("btn.ok", "确定"))
        cancel_btn = QPushButton(lang.get("btn.cancel", "取消"))
        
        ok_btn.clicked.connect(lambda: self.save_language("zh" if zh_radio.isChecked() else "en", dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.exec_()
        
    def get_current_language(self):
        """Get current language setting"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                import json
                config = json.load(f)
                return config.get("language", "zh")
        except:
            return "zh"
            
    def save_language(self, language, dialog):
        """Save language setting and reload UI"""
        try:
            # 保存语言设置
            with open("config.json", "w", encoding="utf-8") as f:
                import json
                json.dump({"language": language}, f, ensure_ascii=False, indent=2)
            
            # 重新加载语言包
            from language_loader import load_language
            global lang
            lang = load_language(language)
            
            # 实时更新界面
            self.reload_ui_language()
            
            QMessageBox.information(self, lang.get("msg.info", "提示"), lang.get("msg.language_saved", "语言设置已保存并实时更新"))
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, lang.get("msg.error", "错误"), lang.get("msg.language_save_failed", "保存语言设置失败").format(error=str(e)))
            import traceback
            traceback.print_exc()
    
    def reload_ui_language(self):
        """Reload UI with new language"""
        try:
            # 更新窗口标题
            self.setWindowTitle(lang.get("app.title", "Multi-Tool Desktop App"))
            
            # 重新加载模块信息（使用新的语言）
            self.reload_modules()
            
            # 更新菜单栏
            self.update_menu_bar()
            
        except Exception as e:
            print(f"界面语言更新失败: {e}")
            import traceback
            traceback.print_exc()
    
    def reload_modules(self):
        """Reload modules with new language"""
        # 清除现有模块按钮
        for i in reversed(range(self.module_buttons.count())):
            widget = self.module_buttons.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # 清除现有内容
        while self.content_stack.count() > 0:
            widget = self.content_stack.widget(0)
            self.content_stack.removeWidget(widget)
            widget.deleteLater()
        
        # 清空模块字典
        self.modules.clear()
        
        # 重新加载模块
        self.load_modules()
    

    
    def update_menu_bar(self):
        """Update menu bar with new language"""
        menubar = self.menuBar()
        menubar.clear()
        
        # 文件菜单
        file_menu = menubar.addMenu(lang.get("menu.file", "文件"))
        
        # 设置菜单
        settings_menu = menubar.addMenu(lang.get("menu.settings", "设置"))
        
        # 语言设置
        lang_action = QAction(lang.get("menu.language", "语言"), self)
        lang_action.triggered.connect(self.show_language_settings)
        settings_menu.addAction(lang_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu(lang.get("menu.help", "帮助"))
    


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建主窗口
    main_window = MainApplication()
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
