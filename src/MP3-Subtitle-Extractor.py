#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP3 Subtitle Extractor
专业的MP3音频转字幕工具，支持Whisper语音识别和自动翻译
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import whisper
import argostranslate.package
import argostranslate.translate

class I18nManager:
    """国际化管理器 - 使用现有的docs/i18n/结构"""
    def __init__(self, default_lang='zh'):
        self.current_lang = default_lang
        self.translations = {'en': {}, 'zh': {}}
        self._load_translations()
    
    def _load_translations(self):
        """加载翻译文件"""
        # 尝试多个可能的路径
        possible_paths = [
            Path(__file__).parent.parent / 'docs' / 'i18n',
            Path(__file__).parent / 'i18n',
            Path.cwd() / 'docs' / 'i18n',
            Path.cwd() / 'i18n'
        ]
        
        for i18n_dir in possible_paths:
            if i18n_dir.exists():
                zh_file = i18n_dir / 'zh.json'
                en_file = i18n_dir / 'en.json'
                
                if zh_file.exists():
                    try:
                        with open(zh_file, 'r', encoding='utf-8') as f:
                            self.translations['zh'].update(json.load(f))
                    except Exception as e:
                        print(f"Warning: Failed to load zh.json: {e}")
                
                if en_file.exists():
                    try:
                        with open(en_file, 'r', encoding='utf-8') as f:
                            self.translations['en'].update(json.load(f))
                    except Exception as e:
                        print(f"Warning: Failed to load en.json: {e}")
                break
        
        # 添加MP3提取器专用的翻译键
        self._add_mp3_extractor_keys()
    
    def _add_mp3_extractor_keys(self):
        """添加MP3提取器专用的翻译键"""
        mp3_keys_zh = {
            "mp3_extractor_title": "MP3字幕提取器",
            "mp3_extractor_subtitle": "专业的MP3音频转字幕工具",
            "select_mp3_file": "选择MP3文件",
            "mp3_files": "MP3文件",
            "start_extraction": "开始提取",
            "extracting": "正在提取...",
            "extraction_complete": "提取完成",
            "extraction_failed": "提取失败",
            "loading_model": "正在加载模型...",
            "model_loaded": "模型加载完成",
            "transcribing_audio": "正在转录音频...",
            "translating_text": "正在翻译文本...",
            "saving_file": "正在保存文件...",
            "file_saved": "文件已保存",
            "no_file_selected": "未选择文件",
            "whisper_model_loading": "开始加载Whisper模型（首次使用可能需要几分钟下载）...",
            "translation_model_missing": "未安装翻译模型，无法翻译。\n请先安装Argos Translate的English → Chinese模型。",
            "output_file_saved": "输出文件已保存",
            "english_text": "英文文本",
            "chinese_text": "中文文本",
            "extraction_progress": "提取进度",
            "current_step": "当前步骤",
            "language_switch": "语言切换",
            "about": "关于",
            "version": "版本",
            "author": "作者",
            "description": "使用Whisper AI进行语音识别，支持自动翻译为中文"
        }
        
        mp3_keys_en = {
            "mp3_extractor_title": "MP3 Subtitle Extractor",
            "mp3_extractor_subtitle": "Professional MP3 audio to subtitle tool",
            "select_mp3_file": "Select MP3 File",
            "mp3_files": "MP3 Files",
            "start_extraction": "Start Extraction",
            "extracting": "Extracting...",
            "extraction_complete": "Extraction Complete",
            "extraction_failed": "Extraction Failed",
            "loading_model": "Loading Model...",
            "model_loaded": "Model Loaded",
            "transcribing_audio": "Transcribing Audio...",
            "translating_text": "Translating Text...",
            "saving_file": "Saving File...",
            "file_saved": "File Saved",
            "no_file_selected": "No file selected",
            "whisper_model_loading": "Loading Whisper model (first time may take a few minutes to download)...",
            "translation_model_missing": "Translation model not installed, cannot translate.\nPlease install Argos Translate English → Chinese model first.",
            "output_file_saved": "Output file saved",
            "english_text": "English Text",
            "chinese_text": "Chinese Text",
            "extraction_progress": "Extraction Progress",
            "current_step": "Current Step",
            "language_switch": "Language Switch",
            "about": "About",
            "version": "Version",
            "author": "Author",
            "description": "Uses Whisper AI for speech recognition with automatic Chinese translation"
        }
        
        # 合并到现有翻译中
        self.translations['zh'].update(mp3_keys_zh)
        self.translations['en'].update(mp3_keys_en)
    
    def t(self, key, **kwargs):
        """获取翻译文本"""
        text = self.translations.get(self.current_lang, {}).get(
            key, 
            self.translations.get('en', {}).get(key, key)
        )
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    
    def switch_language(self, lang):
        """切换语言"""
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False

class MP3SubtitleExtractor:
    """MP3字幕提取器主类"""
    
    def __init__(self):
        self.i18n = I18nManager()
        self.root = tk.Tk()
        self.setup_ui()
        self.audio_path = None
        self.model = None
        
    def setup_ui(self):
        """设置用户界面"""
        self.root.title(self.i18n.t("mp3_extractor_title"))
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # 创建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        self.title_label = ttk.Label(self.main_frame, text=self.i18n.t("mp3_extractor_title"), 
                                    font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        self.subtitle_label = ttk.Label(self.main_frame, text=self.i18n.t("mp3_extractor_subtitle"))
        self.subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # 语言切换
        self.lang_frame = ttk.Frame(self.main_frame)
        self.lang_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        self.lang_label = ttk.Label(self.lang_frame, text=self.i18n.t("language_switch") + ":")
        self.lang_label.pack(side=tk.LEFT)
        
        self.lang_var = tk.StringVar(value=self.i18n.current_lang)
        self.lang_combo = ttk.Combobox(self.lang_frame, textvariable=self.lang_var, 
                                      values=['zh', 'en'], state='readonly', width=10)
        self.lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # 文件选择
        self.file_frame = ttk.LabelFrame(self.main_frame, text=self.i18n.t("select_mp3_file"), padding="10")
        self.file_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        self.file_frame.columnconfigure(1, weight=1)
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_var, state='readonly')
        self.file_entry.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_btn = ttk.Button(self.file_frame, text="...", width=3, command=self.browse_file)
        self.browse_btn.grid(row=0, column=2)
        
        # 进度显示
        self.progress_frame = ttk.LabelFrame(self.main_frame, text=self.i18n.t("extraction_progress"), padding="10")
        self.progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        self.progress_frame.columnconfigure(0, weight=1)
        
        self.step_var = tk.StringVar(value=self.i18n.t("current_step") + ": " + self.i18n.t("no_file_selected"))
        self.step_label = ttk.Label(self.progress_frame, textvariable=self.step_var)
        self.step_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 结果显示
        result_title = self.i18n.t("english_text") + " / " + self.i18n.t("chinese_text")
        self.result_frame = ttk.LabelFrame(self.main_frame, text=result_title, padding="10")
        self.result_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(5, weight=1)
        
        # 创建文本框和滚动条
        self.text_frame = ttk.Frame(self.result_frame)
        self.text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(self.text_frame, wrap=tk.WORD, height=10, state='disabled')
        self.scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=self.scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=6, column=0, columnspan=3, pady=(0, 10))
        
        self.extract_btn = ttk.Button(self.button_frame, text=self.i18n.t("start_extraction"), 
                                     command=self.start_extraction, state='disabled')
        self.extract_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.about_btn = ttk.Button(self.button_frame, text=self.i18n.t("about"), command=self.show_about)
        self.about_btn.pack(side=tk.LEFT)
        
    def on_language_change(self, event=None):
        """语言切换事件"""
        new_lang = self.lang_var.get()
        if self.i18n.switch_language(new_lang):
            # 重新设置界面文本
            self.root.title(self.i18n.t("mp3_extractor_title"))
            # 这里可以添加更多界面元素的文本更新
            self.update_ui_text()
    
    def update_ui_text(self):
        """更新界面文本"""
        # 更新窗口标题
        self.root.title(self.i18n.t("mp3_extractor_title"))
        
        # 更新标题和副标题
        self.title_label.config(text=self.i18n.t("mp3_extractor_title"))
        self.subtitle_label.config(text=self.i18n.t("mp3_extractor_subtitle"))
        
        # 更新语言切换标签
        self.lang_label.config(text=self.i18n.t("language_switch") + ":")
        
        # 更新文件选择框架标题
        self.file_frame.config(text=self.i18n.t("select_mp3_file"))
        
        # 更新进度框架标题
        self.progress_frame.config(text=self.i18n.t("extraction_progress"))
        
        # 更新结果显示框架标题
        result_title = self.i18n.t("english_text") + " / " + self.i18n.t("chinese_text")
        self.result_frame.config(text=result_title)
        
        # 更新按钮文本
        self.extract_btn.config(text=self.i18n.t("start_extraction"))
        self.about_btn.config(text=self.i18n.t("about"))
        
        # 更新状态文本
        if self.audio_path:
            self.step_var.set(self.i18n.t("current_step") + ": " + self.i18n.t("file_saved"))
        else:
            self.step_var.set(self.i18n.t("current_step") + ": " + self.i18n.t("no_file_selected"))
    
    def browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title=self.i18n.t("select_mp3_file"),
            filetypes=[(self.i18n.t("mp3_files"), "*.mp3"), ("All files", "*.*")]
        )
        if file_path:
            self.audio_path = file_path
            self.file_var.set(file_path)
            self.extract_btn.config(state='normal')
            self.step_var.set(self.i18n.t("current_step") + ": " + self.i18n.t("file_saved"))
            self.progress_var.set(0)
    
    def start_extraction(self):
        """开始提取"""
        if not self.audio_path:
            messagebox.showerror(self.i18n.t("error"), self.i18n.t("no_file_selected"))
            return
        
        # 在新线程中执行提取
        self.extract_btn.config(state='disabled', text=self.i18n.t("extracting"))
        thread = threading.Thread(target=self.extract_subtitle)
        thread.daemon = True
        thread.start()
    
    def extract_subtitle(self):
        """提取字幕（在后台线程中执行）"""
        try:
            # 步骤1: 加载模型
            self.root.after(0, lambda: self.step_var.set(
                self.i18n.t("current_step") + ": " + self.i18n.t("loading_model")))
            self.root.after(0, lambda: self.progress_var.set(10))
            
            if not self.model:
                self.model = whisper.load_model("medium")
            
            self.root.after(0, lambda: self.step_var.set(
                self.i18n.t("current_step") + ": " + self.i18n.t("model_loaded")))
            self.root.after(0, lambda: self.progress_var.set(30))
            
            # 步骤2: 转录音频
            self.root.after(0, lambda: self.step_var.set(
                self.i18n.t("current_step") + ": " + self.i18n.t("transcribing_audio")))
            self.root.after(0, lambda: self.progress_var.set(50))
            
            result = self.model.transcribe(self.audio_path, language="en", verbose=False)
            all_text = " ".join([seg['text'].strip() for seg in result['segments']]).strip()

            self.root.after(0, lambda: self.progress_var.set(70))
            
            # 步骤3: 翻译文本
            self.root.after(0, lambda: self.step_var.set(
                self.i18n.t("current_step") + ": " + self.i18n.t("translating_text")))
            
            # 检查翻译模型
            installed_languages = argostranslate.translate.get_installed_languages()
            from_lang = next((lang for lang in installed_languages if lang.code == "en"), None)
            to_lang = next((lang for lang in installed_languages if lang.code == "zh"), None)

            if from_lang and to_lang:
                translation = from_lang.get_translation(to_lang)
                translated_text = translation.translate(all_text)
            else:
                translated_text = self.i18n.t("translation_model_missing")
            
            self.root.after(0, lambda: self.progress_var.set(90))
            
            # 步骤4: 保存文件
            self.root.after(0, lambda: self.step_var.set(
                self.i18n.t("current_step") + ": " + self.i18n.t("saving_file")))
            
            # 使用国际化的文件名
            base_name = os.path.splitext(self.audio_path)[0]
            if self.i18n.current_lang == 'zh':
                output_txt = base_name + '_英文中文.txt'
            else:
                output_txt = base_name + '_English_Chinese.txt'
            
            with open(output_txt, 'w', encoding='utf-8') as f:
                f.write("=== " + self.i18n.t("english_text") + " ===\n")
                f.write(all_text + '\n\n')
                f.write("=== " + self.i18n.t("chinese_text") + " ===\n")
                f.write(translated_text + '\n')

            # 更新界面
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.step_var.set(
                self.i18n.t("current_step") + ": " + self.i18n.t("extraction_complete")))
            
            # 显示结果
            result_display = f"=== {self.i18n.t('english_text')} ===\n{all_text}\n\n=== {self.i18n.t('chinese_text')} ===\n{translated_text}"
            self.root.after(0, lambda: self.show_result(result_display))
            
            # 显示成功消息
            self.root.after(0, lambda: messagebox.showinfo(
                self.i18n.t("success"), 
                f"{self.i18n.t('output_file_saved')}: {output_txt}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                self.i18n.t("error"), 
                f"{self.i18n.t('extraction_failed')}: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.extract_btn.config(
                state='normal', text=self.i18n.t("start_extraction")))
    
    def show_result(self, text):
        """显示结果"""
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, text)
        self.result_text.config(state='disabled')
    
    def show_about(self):
        """显示关于对话框"""
        about_text = f"""{self.i18n.t('mp3_extractor_title')} v1.0.0

{self.i18n.t('description')}

{self.i18n.t('version')}: 1.0.0
{self.i18n.t('author')}: Video Tools Platform

GitHub: https://github.com/xiexin0516-collab/video-tools
Website: https://vidtools.tools/
"""
        messagebox.showinfo(self.i18n.t("about"), about_text)
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = MP3SubtitleExtractor()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()