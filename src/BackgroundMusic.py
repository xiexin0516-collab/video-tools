#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量级背景音乐生成器
专为YouTube短视频背景音乐设计
支持中英文国际化
"""

import numpy as np
import wave
import os
import random
import math
import json
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path

class I18nManager:
    """
    无硬编码国际化加载：
    1) 环境变量 VIDTOOLS_I18N_DIR
    2) 与可执行文件/脚本同目录的 ./i18n
    3) 当前工作目录 ./i18n
    4) PyInstaller 临时目录 sys._MEIPASS/i18n
    5) 仓库布局 ../docs/i18n
    6) 内置回退字典（最小集合，防止缺失崩溃）
    """
    def __init__(self, default_lang='zh'):
        self.current_lang = os.getenv('VIDTOOLS_LANG', default_lang)
        self._warned_missing = set()
        self.translations = {'en': {}, 'zh': {}}
        self._load_all()

    def _candidate_dirs(self):
        cands = []
        # 1) 显式指定
        env = os.getenv('VIDTOOLS_I18N_DIR')
        if env: cands.append(Path(env))
        # 2) 脚本/可执行文件同目录
        here = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
        cands += [
            here / 'i18n',
            Path.cwd() / 'i18n',
        ]
        # 3) PyInstaller 临时目录（若未命中上面的 here）
        if hasattr(sys, '_MEIPASS'):
            cands.append(Path(sys._MEIPASS) / 'i18n')
        # 4) 仓库典型结构 ../docs/i18n
        cands.append(Path(__file__).resolve().parent.parent / 'docs' / 'i18n')
        # 去重并保留存在的
        seen, out = set(), []
        for p in cands:
            try:
                rp = p.resolve()
                if rp not in seen and rp.exists():
                    seen.add(rp); out.append(rp)
            except Exception:
                pass
        return out

    def _load_json(self, p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _load_all(self):
        # 先尝试外部文件
        for d in self._candidate_dirs():
            zh = self._load_json(d / 'zh.json')
            en = self._load_json(d / 'en.json')
            # 只要有任一语言命中就并入（后发现的覆盖先前键）
            if zh: self.translations['zh'].update(zh)
            if en: self.translations['en'].update(en)
        # 最后兜底：内置极小字典（避免界面关键项缺失导致奔溃）
        builtin_en = {
            "bgm_title": "Background Music Generator",
            "bgm_subtitle": "Designed for YouTube Short Videos",
            "bgm_description": "No GPU required, Pure Python Implementation",
            "bgm_styles_title": "Available Styles:",
            "bgm_styles_mysterious": "🌟 Mysterious & Suspenseful",
            "bgm_styles_peaceful": "😌 Peaceful & Calm",
            "bgm_styles_tense": "⚡ Tense Atmosphere",
            "bgm_styles_hopeful": "🌅 Hopeful & Uplifting",
            "bgm_input_duration": "Music duration (seconds):",
            "bgm_input_filename": "Output filename:",
            "bgm_generation_start": "Start Generation",
            "bgm_generation_processing": "Generating...",
            "bgm_completion_success": "Generation completed!",
            "bgm_completion_final": "Background music generation completed!",
            "bgm_language_switched": "Language switched to: {lang}",
            "bgm_interaction_error": "Program error: {error}",
            "bgm_browse": "Browse",
            "bgm_file_dialog_title": "Choose output file",
            "bgm_success": "Success",
            "bgm_error": "Error",
            "bgm_error_duration": "Duration must be greater than 0",
            "bgm_error_duration_invalid": "Please enter a valid duration",
            "bgm_error_filename": "Please enter a filename",
            "bgm_generation_style": "Style: {style}",
            "bgm_generation_duration": "Duration: {duration}s",
            "bgm_generation_filename": "Filename: {filename}",
            "bgm_generation_melody": "Generating main melody...",
            "bgm_generation_counter": "Generating counter melody...",
            "bgm_generation_bass": "Generating bass line...",
            "bgm_generation_pad": "Generating pad...",
            "bgm_generation_strings": "Generating strings...",
            "bgm_generation_piano": "Generating piano arpeggios...",
            "bgm_generation_drums": "Generating drums...",
            "bgm_generation_texture": "Generating ambient texture...",
            "bgm_generation_orchestral": "Generating orchestral layers...",
            "bgm_generation_mixing": "Mixing...",
            "bgm_completion_features": "Features: modal melody, counter melody, dynamic bass, drums, strings, piano, ambience",
            "bgm_completion_orchestral": "Orchestral: high strings, choir pad, brass swells, plucks",
            "bgm_completion_characteristics": "Markov motion, motif development, rhythm templates, humanize",
            "bgm_completion_melody": "Melody: mode-based with motif variations",
            "bgm_completion_structure": "Form: A–B–A'",
            "bgm_completion_filesize": "File size: {size:.1f}MB",
            "bgm_completion_location": "Saved to: {path}",
            "bgm_language_current": "Current language: English",
            "bgm_language_switch": "Switch language (1=中文, 2=English): ",
            "bgm_input_select_style": "Choose style (1-4): ",
            "bgm_completion_usage": "Can be directly imported into PR as background music",
            "bgm_interaction_continue": "Generate other styles? (y/n): ",
            "bgm_interaction_interrupted": "Program interrupted by user",
            "bgm_gui_start_failed": "Failed to start GUI: {error}",
            "bgm_fallback_cli": "Falling back to command line mode...",
            "bgm_generation_failed": "Generation failed",
            "bgm_language_zh": "中文",
            "bgm_language_en": "English",
        }
        builtin_zh = {
            "bgm_title": "轻量级背景音乐生成器",
            "bgm_subtitle": "专为YouTube短视频设计",
            "bgm_description": "无需GPU，纯Python实现",
            "bgm_styles_title": "可用风格:",
            "bgm_styles_mysterious": "🌟 神秘悬疑",
            "bgm_styles_peaceful": "😌 平静舒缓",
            "bgm_styles_tense": "⚡ 紧张氛围",
            "bgm_styles_hopeful": "🌅 希望向上",
            "bgm_input_duration": "音乐时长 (秒):",
            "bgm_input_filename": "输出文件名:",
            "bgm_generation_start": "开始生成",
            "bgm_generation_processing": "正在生成...",
            "bgm_completion_success": "生成完成!",
            "bgm_completion_final": "背景音乐生成完成!",
            "bgm_language_switched": "语言已切换为: {lang}",
            "bgm_interaction_error": "程序运行出错: {error}",
            "bgm_browse": "浏览",
            "bgm_file_dialog_title": "选择输出文件",
            "bgm_success": "成功",
            "bgm_error": "错误",
            "bgm_error_duration": "时长必须大于0",
            "bgm_error_duration_invalid": "请输入有效的时长",
            "bgm_error_filename": "请输入文件名",
            "bgm_generation_style": "生成风格: {style}",
            "bgm_generation_duration": "时长: {duration}秒",
            "bgm_generation_filename": "文件名: {filename}",
            "bgm_generation_melody": "生成主旋律...",
            "bgm_generation_counter": "生成对位旋律...",
            "bgm_generation_bass": "生成低音线...",
            "bgm_generation_pad": "生成和声垫...",
            "bgm_generation_strings": "生成弦乐...",
            "bgm_generation_piano": "生成钢琴琶音...",
            "bgm_generation_drums": "生成鼓点...",
            "bgm_generation_texture": "生成环境纹理...",
            "bgm_generation_orchestral": "生成管弦乐层...",
            "bgm_generation_mixing": "混音中...",
            "bgm_completion_features": "包含：调式旋律、对位、动态低音、鼓点、弦乐、钢琴、环境音",
            "bgm_completion_orchestral": "管弦层：高弦、合唱垫、铜管冲击、拨弦点缀",
            "bgm_completion_characteristics": "特性：马尔可夫转移、动机发展、节奏模版、人性化",
            "bgm_completion_melody": "旋律：基于调式并支持动机变形",
            "bgm_completion_structure": "结构：A–B–A'",
            "bgm_completion_filesize": "文件大小：{size:.1f}MB",
            "bgm_completion_location": "保存位置：{path}",
            "bgm_language_current": "当前语言: 中文",
            "bgm_language_switch": "切换语言 (1=中文, 2=English): ",
            "bgm_input_select_style": "请选择风格 (1-4): ",
            "bgm_completion_usage": "可以直接导入PR作为背景音乐使用",
            "bgm_interaction_continue": "是否生成其他风格? (y/n): ",
            "bgm_interaction_interrupted": "程序已被用户中断",
            "bgm_gui_start_failed": "启动GUI失败: {error}",
            "bgm_fallback_cli": "回退到命令行模式...",
            "bgm_generation_failed": "生成失败",
            "bgm_language_zh": "中文",
            "bgm_language_en": "English",
        }
        # 只在缺失时补齐
        for k, v in builtin_en.items():
            self.translations['en'].setdefault(k, v)
        for k, v in builtin_zh.items():
            self.translations['zh'].setdefault(k, v)
    
    def t(self, key, **kwargs):
        # 语言不存在则回退到英文再到 key 本身
        s = (self.translations.get(self.current_lang, {}) or {}).get(
            key,
            self.translations.get('en', {}).get(key, key)
        )
        try:
            return s.format(**kwargs)
        except Exception:
            # 记录一次缺失，避免刷屏
            mk = (self.current_lang, key)
            if mk not in self._warned_missing:
                self._warned_missing.add(mk)
                # 可换成 logging.warning
                print(f"[i18n] missing key: {mk}")
            return s
    
    def switch_language(self, lang):
        """切换语言"""
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False
    
    def get_language_name(self, lang):
        """获取语言名称"""
        names = {'zh': '中文', 'en': 'English'}
        return names.get(lang, lang)

# --- i18n glue: replace language_loader ---
from pathlib import Path
import json as _json

_CFG = Path.home() / ".bgm_i18n.json"

def _load_saved_lang():
    try:
        if _CFG.exists():
            return _json.loads(_CFG.read_text(encoding="utf-8")).get("lang", "zh")
    except Exception:
        pass
    return "zh"

# 全局唯一的 I18nManager，初始用保存的语言
_I18N = I18nManager(default_lang=_load_saved_lang())

class _LangProxy:
    """提供 lang.get(key, default) 的兼容接口"""
    def get(self, key, default=None, **kwargs):
        txt = _I18N.t(key, **kwargs)
        if txt == key and default is not None:  # 没翻译时回退 default
            return default
        return txt

lang = _LangProxy()

def get_saved_language():
    return _I18N.current_lang

def switch_language(new_lang: str) -> bool:
    ok = _I18N.switch_language(new_lang)
    if ok:
        try:
            _CFG.write_text(_json.dumps({"lang": new_lang}, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    return ok

class SimpleBackgroundMusicGenerator:
    def __init__(self, i18n_manager=None):
        self.sample_rate = 44100
        self.bit_depth = 16
        self.i18n = i18n_manager or _I18N
        
    def generate_tone(self, frequency, duration, amplitude=0.3, fade_in=0.1, fade_out=0.1):
        """生成单个音调"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # 生成基础正弦波
        wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # 添加淡入淡出
        fade_in_samples = int(fade_in * self.sample_rate)
        fade_out_samples = int(fade_out * self.sample_rate)
        
        # 淡入
        if fade_in_samples > 0:
            fade_in_curve = np.linspace(0, 1, fade_in_samples)
            wave_data[:fade_in_samples] *= fade_in_curve
        
        # 淡出
        if fade_out_samples > 0:
            fade_out_curve = np.linspace(1, 0, fade_out_samples)
            wave_data[-fade_out_samples:] *= fade_out_curve
            
        return wave_data
    
    def generate_chord(self, frequencies, duration, amplitude=0.2):
        """生成和弦"""
        chord_data = np.zeros(int(self.sample_rate * duration))
        
        for freq in frequencies:
            tone = self.generate_tone(freq, duration, amplitude/len(frequencies))
            chord_data += tone
            
        return chord_data
    
    def add_reverb(self, audio_data, delay=0.05, decay=0.3):
        """添加简单混响效果"""
        delay_samples = int(delay * self.sample_rate)
        reverb_data = audio_data.copy()
        
        for i in range(1, 4):  # 3次回声
            delayed = np.pad(audio_data, (delay_samples * i, 0), mode='constant')[:-delay_samples * i]
            reverb_data += delayed * (decay ** i)
        
        return reverb_data
    
    def generate_ambient_pad(self, duration=30, style="mysterious"):
        """生成环境音垫 - 增强版"""
        
        # 不同风格的和弦进行 + 旋律变化
        chord_progressions = {
            "mysterious": {
                "chords": [
                    [220, 261, 311],    # A minor
                    [207, 246, 311],    # Ab major
                    [196, 233, 293],    # G major  
                    [220, 261, 329],    # A minor add9
                    [185, 220, 277],    # F# dim
                    [196, 233, 293]     # G major
                ],
                "bass_pattern": [110, 103.5, 98, 110, 92.5, 98],
                "melody": [440, 523, 466, 440, 415, 466]
            },
            "peaceful": {
                "chords": [
                    [261, 329, 392],    # C major
                    [220, 277, 329],    # A minor
                    [246, 311, 369],    # F major
                    [293, 349, 440],    # G major
                    [220, 277, 329],    # A minor
                    [261, 329, 392]     # C major
                ],
                "bass_pattern": [130.5, 110, 123, 146.5, 110, 130.5],
                "melody": [523, 440, 466, 523, 440, 523]
            },
            "tense": {
                "chords": [
                    [233, 277, 349],    # Bb minor
                    [207, 246, 311],    # Ab major
                    [185, 220, 277],    # F# dim
                    [196, 233, 293],    # G minor
                    [174, 207, 261],    # F minor
                    [196, 233, 293]     # G minor
                ],
                "bass_pattern": [116.5, 103.5, 92.5, 98, 87, 98],
                "melody": [349, 311, 277, 293, 261, 293]
            },
            "hopeful": {
                "chords": [
                    [261, 329, 392],    # C major
                    [293, 369, 440],    # G major
                    [220, 277, 329],    # A minor
                    [246, 311, 369],    # F major
                    [293, 369, 440],    # G major
                    [261, 329, 392]     # C major
                ],
                "bass_pattern": [130.5, 146.5, 110, 123, 146.5, 130.5],
                "melody": [523, 587, 440, 466, 587, 523]
            }
        }
        
        progression_data = chord_progressions.get(style, chord_progressions["mysterious"])
        chords = progression_data["chords"]
        bass_pattern = progression_data["bass_pattern"]
        melody_notes = progression_data["melody"]
        
        chord_duration = duration / len(chords)
        audio_data = np.array([])
        
        for i, (chord_freqs, bass_freq, melody_freq) in enumerate(zip(chords, bass_pattern, melody_notes)):
            # 生成和弦 (主体)
            chord = self.generate_chord(chord_freqs, chord_duration, 0.12)
            
            # 生成低音
            bass = self.generate_tone(bass_freq, chord_duration, 0.15)
            
            # 生成旋律线 (更明显的变化)
            melody_amp = 0.08 + (i % 3) * 0.02  # 音量变化
            melody = self.generate_tone(melody_freq, chord_duration, melody_amp, 
                                      fade_in=0.3, fade_out=0.2)
            
            # 添加高次谐波丰富音色
            harmonic2 = self.generate_tone(melody_freq * 2, chord_duration, melody_amp * 0.3)
            harmonic3 = self.generate_tone(melody_freq * 3, chord_duration, melody_amp * 0.15)
            
            # 合并所有元素
            combined = chord + bass + melody + harmonic2 + harmonic3
            
            # 添加动态包络
            envelope = self.create_dynamic_envelope(len(combined), style, i)
            combined *= envelope
            
            audio_data = np.concatenate([audio_data, combined])
        
        # 添加更丰富的混响
        audio_data = self.add_advanced_reverb(audio_data)
        
        # 添加细微的调制效果
        audio_data = self.add_subtle_modulation(audio_data, duration)
        
        # 标准化音量
        audio_data = audio_data / np.max(np.abs(audio_data)) * 0.6
        
        return audio_data
    
    def create_dynamic_envelope(self, length, style, chord_index):
        """创建动态包络"""
        t = np.linspace(0, 1, length)
        
        if style == "mysterious":
            # 神秘风格：波动起伏
            base_env = 0.7 + 0.3 * np.sin(2 * np.pi * t * 0.5)
            variation = 0.1 * np.sin(2 * np.pi * t * 3)
        elif style == "tense":
            # 紧张风格：逐渐增强
            base_env = 0.5 + 0.4 * t + 0.1 * np.sin(2 * np.pi * t * 2)
            variation = 0.15 * np.sin(2 * np.pi * t * 5)
        elif style == "hopeful":
            # 希望风格：上升趋势
            base_env = 0.6 + 0.3 * np.sqrt(t) + 0.1 * np.sin(2 * np.pi * t)
            variation = 0.05 * np.sin(2 * np.pi * t * 1.5)
        else:  # peaceful
            # 平和风格：温和变化
            base_env = 0.8 + 0.2 * np.sin(2 * np.pi * t * 0.3)
            variation = 0.05 * np.sin(2 * np.pi * t * 1)
        
        return base_env + variation
    
    def add_advanced_reverb(self, audio_data, room_size=0.7):
        """添加高级混响效果"""
        reverb_data = audio_data.copy()
        
        # 多重延迟 + 衰减
        delays = [0.03, 0.07, 0.12, 0.18, 0.25]  # 不同延迟时间
        decays = [0.4, 0.3, 0.2, 0.15, 0.1]     # 对应衰减
        
        for delay, decay in zip(delays, decays):
            delay_samples = int(delay * self.sample_rate)
            if delay_samples < len(audio_data):
                delayed = np.pad(audio_data, (delay_samples, 0), mode='constant')[:-delay_samples]
                reverb_data += delayed * decay * room_size
        
        return reverb_data
    
    def generate_drum_pattern(self, duration, style="mysterious"):
        """生成鼓点节奏 - 增强版"""
        samples = int(self.sample_rate * duration)
        drum_track = np.zeros(samples)
        
        # 更丰富的鼓点模式，增加变化
        patterns = {
            "mysterious": {
                "kick": [0, 4, 8, 12, 16, 20, 24, 28],  # 每4拍一个kick
                "snare": [2, 6, 10, 14, 18, 22, 26, 30],  # 反拍snare
                "hihat": [1, 2.5, 4.5, 6, 7.5, 9, 10.5, 12.5, 14, 15.5],  # 密集hihat
                "crash": [0, 16]  # 重音
            },
            "tense": {
                "kick": [0, 3, 6, 8, 11, 14, 16, 19, 22, 24, 27, 30],  # 不规则节奏
                "snare": [4, 8, 12, 16, 20, 24, 28],  # 强拍
                "hihat": [i * 0.5 for i in range(64)],  # 快速hihat
                "crash": [0, 8, 16, 24]
            },
            "peaceful": {
                "kick": [0, 8, 16, 24],  # 稀疏kick
                "snare": [4, 12, 20, 28],  # 简单snare
                "hihat": [2, 6, 10, 14, 18, 22, 26, 30],  # 轻柔hihat
                "crash": [0]
            },
            "hopeful": {
                "kick": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],  # 密集kick
                "snare": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31],  # 反拍
                "hihat": [i * 0.25 for i in range(128)],  # 超密集
                "crash": [0, 8, 16, 24]
            }
        }
        
        pattern = patterns.get(style, patterns["mysterious"])
        beat_duration = duration / 32  # 32拍，更细腻
        
        # 添加动态音量变化
        for i, beat_time in enumerate(pattern["kick"]):
            volume = 0.4 + 0.2 * np.sin(i * 0.5)  # 动态音量
            kick_sound = self.create_kick_drum(beat_time * beat_duration, volume, duration)
            drum_track += kick_sound
        
        for i, beat_time in enumerate(pattern["snare"]):
            volume = 0.3 + 0.15 * np.sin(i * 0.3)
            snare_sound = self.create_snare_drum(beat_time * beat_duration, volume, duration)
            drum_track += snare_sound
            
        for i, beat_time in enumerate(pattern["hihat"]):
            volume = 0.1 + 0.05 * np.sin(i * 0.2)
            hihat_sound = self.create_hihat(beat_time * beat_duration, volume, duration)
            drum_track += hihat_sound
        
        # 添加crash镲
        for beat_time in pattern.get("crash", []):
            crash_sound = self.create_crash_cymbal(beat_time * beat_duration, 0.2, duration)
            drum_track += crash_sound
        
        return drum_track
    
    def create_crash_cymbal(self, start_time, amplitude, total_duration):
        """创建crash镲音色"""
        duration = 2.0  # 长衰减
        samples = int(self.sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)  # 不含端点
        
        # 复杂的高频噪音 + 金属音色
        noise = amplitude * np.random.normal(0, 1, samples)
        
        # 多个频率的正弦波模拟金属声
        metallic = 0
        freqs = [1200, 1800, 2400, 3600, 4800]
        for freq in freqs:
            metallic += amplitude * 0.1 * np.sin(2 * np.pi * freq * t)
        
        crash = (noise * 0.7 + metallic * 0.3) * np.exp(-t * 1.5)
        
        return self._safe_place(crash, start_time, total_duration)
    
    def generate_bass_line(self, duration=30, style="mysterious"):
        """生成动态低音线"""
        progressions = {
            "mysterious": [
                (110, 2), (103.5, 1), (98, 1), (110, 2), (92.5, 1), (98, 1),
                (87, 2), (98, 1), (110, 1), (92.5, 2), (98, 2)
            ],
            "peaceful": [
                (130.5, 4), (110, 4), (123, 4), (146.5, 4), (110, 4), (130.5, 4)
            ],
            "tense": [
                (116.5, 1), (103.5, 0.5), (92.5, 0.5), (98, 1), (87, 1), 
                (98, 0.5), (110, 0.5), (103.5, 1), (92.5, 2)
            ],
            "hopeful": [
                (130.5, 2), (146.5, 1), (110, 1), (123, 2), (146.5, 1), 
                (165, 1), (130.5, 2), (146.5, 2)
            ]
        }
        
        progression = progressions.get(style, progressions["mysterious"])
        
        audio_data = np.array([])
        total_beats = sum(beat for _, beat in progression)
        beat_duration = duration / total_beats
        
        for freq, beats in progression:
            note_duration = beat_duration * beats
            
            # 生成带有rhythm感的低音
            bass_note = self.generate_rhythmic_bass(freq, note_duration, 0.3)
            audio_data = np.concatenate([audio_data, bass_note])
        
        return audio_data
    
    def generate_rhythmic_bass(self, frequency, duration, amplitude):
        """生成有节奏感的低音"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # 基础低音
        fundamental = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # 添加sub-bass
        sub_bass = amplitude * 0.5 * np.sin(2 * np.pi * frequency * 0.5 * t)
        
        # 添加节奏感的包络（快速attack + sustain + release）
        attack_time = 0.05
        release_time = 0.2
        attack_samples = int(attack_time * self.sample_rate)
        release_samples = int(release_time * self.sample_rate)
        
        envelope = np.ones(samples)
        
        # Attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Release
        if release_samples > 0 and release_samples < samples:
            envelope[-release_samples:] = np.linspace(1, 0.3, release_samples)
        
        # 添加轻微的低频振荡
        lfo = 1 + 0.1 * np.sin(2 * np.pi * 4 * t)  # 4Hz LFO
        
        bass_sound = (fundamental + sub_bass) * envelope * lfo
        
        return bass_sound
    
    # ======= 新增：音乐工具（调式+马尔可夫） =======
    def _note_freq(self, midi_note):
        """MIDI音符转频率"""
        # A4=440Hz, MIDI 69
        return 440.0 * (2 ** ((midi_note - 69) / 12.0))

    def _scale_degrees(self, root_midi=57, mode="aeolian"):
        """
        返回给定调式的 1~7 度 MIDI 列表（支持多八度展开）
        root_midi: A3=57 作为根音示例
        mode: aeolian(自然小调), dorian, phrygian, ionian(自然大调), mixolydian 等
        """
        modes = {
            "aeolian":     [0, 2, 3, 5, 7, 8, 10],  # 自然小调
            "dorian":      [0, 2, 3, 5, 7, 9, 10],
            "phrygian":    [0, 1, 3, 5, 7, 8, 10],
            "ionian":      [0, 2, 4, 5, 7, 9, 11], # 自然大调
            "mixolydian":  [0, 2, 4, 5, 7, 9, 10],
        }
        intervals = modes.get(mode, modes["aeolian"])
        # 展开两组八度，避免旋律卡在单组音域
        pool = []
        for octave in [-12, 0, 12]:
            pool += [root_midi + i + octave for i in intervals]
        return pool

    def _build_markov(self, style="mysterious", complexity=3):
        """
        返回一个"度数索引"的转移概率表，控制旋律的走向。
        complexity 越高 → 跳进概率更大、变化更活跃
        """
        # 以 7 度为基（不含八度复制），定义"下一个度数"分布
        base = np.array([
            # 到下一个度（0..6）的概率（行=当前度数）
            # 让中间音 (3/4度) 稍更稳定，边缘音(1/7度)倾向向内回
            [0.10,0.20,0.25,0.20,0.15,0.06,0.04],
            [0.12,0.18,0.22,0.20,0.16,0.08,0.04],
            [0.08,0.16,0.24,0.22,0.18,0.08,0.04],
            [0.06,0.12,0.22,0.28,0.20,0.08,0.04],
            [0.08,0.14,0.20,0.24,0.20,0.10,0.04],
            [0.10,0.16,0.20,0.22,0.18,0.10,0.04],
            [0.12,0.18,0.22,0.20,0.16,0.08,0.04],
        ])
        # 复杂度提升 → 提高"跳两度/三度"的概率
        jump_boost = min(max(complexity-2, 0), 3) * 0.02  # 0~0.06
        for i in range(7):
            for j in range(7):
                if abs(j - i) >= 2:
                    base[i, j] += jump_boost
            base[i] = base[i] / base[i].sum()
        return base

    def generate_dynamic_melody(self, duration=30, style="mysterious", complexity=3, seed=None):
        """
        基于调式 + 马尔可夫 + 节奏模版 + 动机变形 的旋律生成
        complexity: 1~5（推荐 3），越大越活跃跳进越多
        """
        import random
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # 选择调式与根音：按风格给默认（可自行调整）
        if style in ("mysterious", "tense"):
            mode = "dorian" if style=="mysterious" else "phrygian"
            root = 57  # A3
        elif style == "peaceful":
            mode = "ionian"; root = 60  # C4
        else:  # hopeful
            mode = "mixolydian"; root = 62  # D4

        scale_pool = self._scale_degrees(root, mode)
        base_scale = scale_pool[7:14]  # 取中间一组 7 度作为"核心度数"
        markov = self._build_markov(style, complexity)

        # 节奏模版（拍长相对单位；包含休止=0）
        rhythms_bank = [
            [1, 1, 1, 1],                # 均分四拍
            [1.5, 0.5, 1, 1],            # 附点节奏
            [0.5, 0.5, 1, 2],            # 先紧后松
            [0.75,0.75,0.5,1,1],         # 小切分
            [2, 1, 1],                   # 长—短—短
            [1, 0, 1, 2],                # 含休止
        ]
        # 每小节选择一个节奏模版；每两个小节做一次变形（扩展/紧缩/打乱一个音）
        tempo_bpm = 84 if style in ("mysterious","tense") else 92
        sec_per_beat = 60.0 / tempo_bpm

        # 动机（以"度数索引(0..6)"表示），先随机生成一小段动机
        motif_len = 4
        cur_degree = 3  # 从中性稳定音开始（类似3/4度）
        motif = [cur_degree]
        for _ in range(motif_len-1):
            cur_degree = np.random.choice(range(7), p=markov[cur_degree])
            motif.append(int(cur_degree))

        # 动机变形器：原型、逆行、转位（围绕中轴）、节奏扩展/紧缩
        def mutate_motif(m):
            ops = ["identity", "retrograde", "inversion"]
            op = random.choice(ops)
            if op == "retrograde":
                m2 = list(reversed(m))
            elif op == "inversion":
                axis = 3  # 以中度为轴
                m2 = [axis - (d - axis) for d in m]
                m2 = [min(max(d,0),6) for d in m2]
            else:
                m2 = m[:]
            return m2

        # 合成音符并拼接
        audio = np.array([])
        total_time = 0.0

        # 音量/力度随机微调
        def vel():
            return 0.12 + random.random()*0.06  # 0.12~0.18

        # 简单人性化：起音抖动（≤10ms）、时值±5%
        def humanize(dur):
            d = dur * (0.95 + random.random()*0.10)
            d = max(d, 1.0 / self.sample_rate)  # 防 0，至少 1 个样本
            jitter = int(0.01 * self.sample_rate * random.random())  # <=10ms
            return d, jitter

        # 进行到目标时长
        phrase_idx = 0
        while total_time < duration:
            rhythms = random.choice(rhythms_bank)
            # 每两个乐句对动机做变形
            motif_now = motif if (phrase_idx % 2 == 0) else mutate_motif(motif)

            # 将动机按节奏铺开（超出则循环/截断）
            deg_seq = (motif_now * ((len(rhythms)+len(motif_now)-1)//len(motif_now)))[:len(rhythms)]

            for deg, beats in zip(deg_seq, rhythms):
                note_sec = beats * sec_per_beat
                if total_time + note_sec > duration:
                    note_sec = duration - total_time
                    if note_sec <= 0: break
                
                # 最小时长钳制，至少 1 个样本
                note_sec = max(note_sec, 1.0 / self.sample_rate)

                # 50%概率休止（当节奏片段里给了0或随机触发）
                if beats == 0 or (random.random() < 0.15 and beats <= 1.0):
                    # 休止：填充静音
                    rest = np.zeros(int(self.sample_rate * note_sec))
                    audio = np.concatenate([audio, rest])
                else:
                    midi = base_scale[deg]  # 映射到核心音域
                    # 偶尔跃升/下降八度，增强线条
                    if random.random() < 0.12:
                        midi += random.choice([-12, 12])

                    freq = self._note_freq(midi)
                    dur_h, jitter = humanize(note_sec)

                    # 复用现有的富表现音色（谐波+ADSR+颤音）
                    note = self.generate_expressive_note(freq, dur_h, vel())

                    # 在开头加一点点静音做"起音抖动"
                    if jitter > 0:
                        note = np.concatenate([np.zeros(jitter), note])

                    audio = np.concatenate([audio, note])

                total_time += note_sec
                if total_time >= duration: break

            phrase_idx += 1

        # 限幅
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.9
        return audio

    def generate_counter_melody(self, duration=30, style="mysterious", complexity=2, seed=None):
        """
        更稀疏、更高音域的回应旋律；大量休止避免拥挤
        """
        import random
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # 直接基于主旋律再造：调用上面的旋律但提高音域&增加休止
        base = self.generate_dynamic_melody(duration, style, max(1, complexity-1), seed)
        # 稀疏化：抽取"峰值片段"，其余衰减
        win = int(0.08 * self.sample_rate)
        env = np.ones_like(base) * 0.4
        # 每 0.8 秒挑一小段 200ms 提升作为"回答"
        step = int(0.8 * self.sample_rate)
        burst = int(0.2 * self.sample_rate)
        i = 0
        while i < len(env):
            if random.random() < 0.45:
                env[i:i+burst] = 1.0
            i += step
        # 高八度并轻微镂空
        counter = base * env
        counter = counter * 0.7
        return counter

    # ======= 新增：管弦层 + 段落感 =======
    def _adsr(self, n, a=0.02, d=0.1, s=0.7, r=0.2):
        """简易 ADSR 包络，输入样本数 n，参数为秒"""
        A = int(a * self.sample_rate); D = int(d * self.sample_rate); R = int(r * self.sample_rate)
        S = max(n - A - D - R, 0)
        env = np.zeros(n)
        if A > 0: env[:A] = np.linspace(0, 1, A)
        if D > 0: env[A:A+D] = np.linspace(1, s, D)
        if S > 0: env[A+D:A+D+S] = s
        if R > 0: env[A+D+S:A+D+S+R] = np.linspace(s, 0, R)
        if len(env) < n: env = np.pad(env, (0, n-len(env)))
        return env

    def _synth_pluck(self, freq, duration, amp=0.12):
        """拨弦/吉他感：谐波叠加 + 快速衰减 + 轻微噪声击发"""
        n = int(self.sample_rate * duration); t = np.linspace(0, duration, n, False)
        harm = (1.0*np.sin(2*np.pi*freq*t) +
                0.6*np.sin(2*np.pi*2*freq*t) +
                0.35*np.sin(2*np.pi*3*freq*t))
        click = 0.02*np.random.normal(0, 1, n)
        env = self._adsr(n, a=0.005, d=0.12, s=0.35, r=0.18)
        return amp * (harm + click) * env

    def _synth_choir_pad(self, freq, duration, amp=0.08):
        """合唱 Pad：正弦+噪声气息+慢速颤音"""
        n = int(self.sample_rate * duration); t = np.linspace(0, duration, n, False)
        vib = 1 + 0.01*np.sin(2*np.pi*5*t)
        breath = 0.02*np.random.normal(0, 1, n)
        sig = (np.sin(2*np.pi*freq*t*vib) + 0.5*np.sin(2*np.pi*freq*2*t*vib)) * 0.8 + breath
        env = self._adsr(n, a=0.4, d=0.6, s=0.85, r=0.8)
        return amp * sig * env

    def _swell_brass(self, freq, duration, amp=0.14):
        """铜管冲击：慢起-快推-快收，带一点饱和"""
        n = int(self.sample_rate * duration); t = np.linspace(0, duration, n, False)
        core = (np.sin(2*np.pi*freq*t) + 0.4*np.sin(2*np.pi*2*freq*t))
        env = np.power(np.clip(t/duration, 0, 1), 1.5)  # 上扬
        env *= np.exp(-t*1.3) + 0.25                     # 推进后略收
        sig = np.tanh(core * 2.2) * env
        return amp * sig

    def generate_orchestral_layer(self, duration=30, style="mysterious"):
        """
        生成管弦乐叠加层：高弦群持续、木管/合唱垫、铜管分段冲击、拨弦点缀
        返回 dict：{'strings_hi','choir','brass','pluck'}
        """
        # 超简化版本，直接使用现有函数
        layer = {}
        
        # 基于风格设置调式中心
        if style in ("mysterious","tense"): root = 440.0  # A4
        elif style == "peaceful": root = 523.25           # C5
        else: root = 493.88                                # B4/D调附近明亮

        # 1) 高弦群（使用现有弦乐函数）
        layer["strings_hi"] = self.generate_string_section(duration, style) * 0.3

        # 2) 合唱 Pad（使用现有和声垫函数）
        layer["choir"] = self.generate_ambient_pad(duration, style) * 0.2

        # 3) 铜管冲击（使用现有低音函数作为基础）
        layer["brass"] = self.generate_bass_line(duration, style) * 0.4

        # 4) 拨弦点缀（使用现有钢琴函数作为基础）
        layer["pluck"] = self.generate_piano_arpeggios(duration, style) * 0.3

        # 轻量混响 & 归一
        for k in layer:
            layer[k] = self.add_advanced_reverb(layer[k])
            mx = np.max(np.abs(layer[k])) or 1.0
            layer[k] = layer[k] / mx * 0.6
        return layer

    def _section_envelope(self, duration, scheme="ABA"):
        """
        生成分段强度包络（0~1）。A(前奏) 20%，B(堆叠) 50%，A'(回归增强) 30%。
        """
        n = int(self.sample_rate * duration)
        t = np.linspace(0, 1, n, False)
        A = (t < 0.2) * (t/0.2)                        # 0→1
        B = ((t >= 0.2) & (t < 0.7)) * 1.0             # 稳态
        Ap = (t >= 0.7) * (0.7 + 0.3*(t-0.7)/0.3)      # 0.7→1.0
        env = A + B + Ap
        return np.clip(env / env.max(), 0, 1)

    def _safe_place(self, segment: np.ndarray, start_time: float, total_duration: float) -> np.ndarray:
        """把 segment 安全贴到长度为 total_duration 的时间轴上，自动处理边界与零长切片。"""
        total = int(self.sample_rate * total_duration)
        out = np.zeros(total, dtype=float)
        if segment is None or len(segment) == 0 or total <= 0:
            return out
        start = int(round(start_time * self.sample_rate))
        # 允许极小负起点（人性化抖动导致）
        if start < 0:
            segment = segment[-start:]
            start = 0
        if start >= total:
            return out
        end = min(start + len(segment), total)
        if end <= start:
            return out
        out[start:end] = segment[:end - start]
        return out
    
    def generate_expressive_note(self, frequency, duration, amplitude):
        """生成有表现力的音符"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # 基础音符
        fundamental = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # 添加谐波丰富音色
        harmonic2 = amplitude * 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
        harmonic3 = amplitude * 0.2 * np.sin(2 * np.pi * frequency * 3 * t)
        
        # 表现力包络（模拟真实乐器）
        attack_time = 0.1
        decay_time = 0.2
        sustain_level = 0.7
        
        attack_samples = int(attack_time * self.sample_rate)
        decay_samples = int(decay_time * self.sample_rate)
        
        envelope = np.ones(samples) * sustain_level
        
        # ADSR包络
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        if decay_samples > 0 and attack_samples + decay_samples < samples:
            decay_start = attack_samples
            decay_end = attack_samples + decay_samples
            envelope[decay_start:decay_end] = np.linspace(1, sustain_level, decay_samples)
        
        # 添加颤音
        vibrato = 1 + 0.05 * np.sin(2 * np.pi * 5 * t)
        
        note_sound = (fundamental + harmonic2 + harmonic3) * envelope * vibrato
        
        return note_sound
    
    def create_kick_drum(self, start_time, amplitude, total_duration):
        """创建底鼓音色"""
        duration = 0.3
        samples = int(self.sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)  # 不含端点
        
        # 低频正弦波 + 快速衰减包络
        frequency = 60 * np.exp(-t * 8)  # 频率从60Hz快速下降
        kick = amplitude * np.sin(2 * np.pi * frequency * t) * np.exp(-t * 6)
        
        # 添加点击音
        click = amplitude * 0.3 * np.random.normal(0, 1, samples) * np.exp(-t * 20)
        kick += click
        
        return self._safe_place(kick, start_time, total_duration)
    
    def create_snare_drum(self, start_time, amplitude, total_duration):
        """创建军鼓音色"""
        duration = 0.2
        samples = int(self.sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)  # 不含端点
        
        # 中频正弦波 + 噪音
        tone = amplitude * 0.4 * np.sin(2 * np.pi * 200 * t) * np.exp(-t * 8)
        noise = amplitude * 0.6 * np.random.normal(0, 1, samples) * np.exp(-t * 10)
        snare = tone + noise
        
        return self._safe_place(snare, start_time, total_duration)
    
    def create_hihat(self, start_time, amplitude, total_duration):
        """创建高帽音色"""
        duration = 0.1
        samples = int(self.sample_rate * duration)
        
        t = np.linspace(0, duration, samples, False)  # 不含端点
        
        # 高频噪音
        hihat = amplitude * np.random.normal(0, 1, samples) * np.exp(-t * 15)
        
        # 高通滤波效果（简化）
        hihat = hihat * (1 - np.exp(-t * 50))
        
        return self._safe_place(hihat, start_time, total_duration)
    
    def generate_string_section(self, duration=30, style="mysterious"):
        """生成弦乐声部"""
        # 弦乐和弦进行（比主和弦高一个八度）
        progressions = {
            "mysterious": [[440, 523, 622], [414, 493, 622], [392, 466, 587], [440, 523, 659]],
            "peaceful": [[523, 659, 784], [440, 554, 659], [493, 622, 740], [587, 698, 880]],
            "tense": [[466, 554, 698], [415, 493, 622], [370, 440, 554], [392, 466, 587]],
            "hopeful": [[523, 659, 784], [587, 698, 880], [440, 554, 659], [493, 622, 740]]
        }
        
        progression = progressions.get(style, progressions["mysterious"])
        chord_duration = duration / len(progression)
        audio_data = np.array([])
        
        for chord_freqs in progression:
            # 弦乐特有的缓慢attack
            string_chord = self.generate_string_chord(chord_freqs, chord_duration, 0.08)
            audio_data = np.concatenate([audio_data, string_chord])
        
        return audio_data
    
    def generate_string_chord(self, frequencies, duration, amplitude):
        """生成弦乐和弦"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        chord_data = np.zeros(samples)
        
        for freq in frequencies:
            # 基础正弦波
            fundamental = amplitude * np.sin(2 * np.pi * freq * t)
            
            # 添加弦乐特有的谐波
            harmonic2 = amplitude * 0.3 * np.sin(2 * np.pi * freq * 2 * t)
            harmonic3 = amplitude * 0.2 * np.sin(2 * np.pi * freq * 3 * t)
            
            # 弦乐的慢attack包络
            attack_time = duration * 0.3
            attack_samples = int(attack_time * self.sample_rate)
            envelope = np.ones(samples)
            if attack_samples > 0:
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
            
            string_voice = (fundamental + harmonic2 + harmonic3) * envelope
            chord_data += string_voice
        
        return chord_data / len(frequencies)
    
    def generate_piano_arpeggios(self, duration=30, style="mysterious"):
        """生成钢琴琶音"""
        progressions = {
            "mysterious": [220, 261, 311, 261, 246, 293, 349, 293, 196, 233, 293, 233],
            "peaceful": [261, 329, 392, 329, 220, 277, 329, 277, 246, 311, 369, 311],
            "tense": [233, 277, 349, 277, 207, 246, 311, 246, 185, 220, 277, 220],
            "hopeful": [261, 329, 392, 329, 293, 369, 440, 369, 220, 277, 329, 277]
        }
        
        notes = progressions.get(style, progressions["mysterious"])
        note_duration = duration / len(notes)
        audio_data = np.array([])
        
        for freq in notes:
            piano_note = self.generate_piano_note(freq, note_duration, 0.1)
            audio_data = np.concatenate([audio_data, piano_note])
        
        return audio_data
    
    def generate_piano_note(self, frequency, duration, amplitude):
        """生成钢琴音符"""
        samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, samples, False)
        
        # 钢琴的复杂谐波结构
        fundamental = amplitude * np.sin(2 * np.pi * frequency * t)
        harmonic2 = amplitude * 0.5 * np.sin(2 * np.pi * frequency * 2 * t)
        harmonic3 = amplitude * 0.25 * np.sin(2 * np.pi * frequency * 3 * t)
        harmonic4 = amplitude * 0.125 * np.sin(2 * np.pi * frequency * 4 * t)
        
        # 钢琴的快attack，慢decay包络
        attack_time = 0.05
        attack_samples = int(attack_time * self.sample_rate)
        
        envelope = np.exp(-t * 2)  # 指数衰减
        if attack_samples > 0:
            envelope[:attack_samples] *= np.linspace(0, 1, attack_samples)
        
        piano_sound = (fundamental + harmonic2 + harmonic3 + harmonic4) * envelope
        
        return piano_sound
    
    def generate_ambient_texture(self, duration=30):
        """生成环境纹理音效"""
        samples = int(self.sample_rate * duration)
        
        # 生成粉红噪音（比白噪音更自然）
        white_noise = np.random.normal(0, 0.05, samples)
        
        # 简单的粉红噪音滤波
        b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        a = [1, -2.494956002, 2.017265875, -0.522189400]
        
        # 简化的滤波处理
        pink_noise = white_noise * 0.1
        
        # 添加缓慢的音量变化
        t = np.linspace(0, duration, samples, False)
        volume_env = 0.3 + 0.2 * np.sin(2 * np.pi * t / (duration/3))
        
        ambient_texture = pink_noise * volume_env
        
        return ambient_texture
    
    def save_audio(self, audio_data, filename):
        """保存音频文件"""
        # 转换为16位整数
        audio_16bit = (audio_data * 32767).astype(np.int16)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_16bit.tobytes())
    
    def add_subtle_modulation(self, audio_data, duration):
        """添加细微的调制效果"""
        t = np.linspace(0, duration, len(audio_data))
        
        # LFO (低频振荡器) 用于音量调制
        lfo = 1 + 0.05 * np.sin(2 * np.pi * 0.3 * t)  # 0.3Hz的慢速调制
        
        # 细微的颤音效果
        vibrato = 1 + 0.02 * np.sin(2 * np.pi * 5 * t)  # 5Hz颤音
        
        return audio_data * lfo * vibrato

    def generate_youtube_bgm(self, style="mysterious", duration=30, filename="youtube_bgm.wav"):
        """生成YouTube背景音乐 - 动态增强版"""
        print(self.i18n.t('bgm_generation_style', style=style))
        print(self.i18n.t('bgm_generation_duration', duration=duration))
        print(self.i18n.t('bgm_generation_filename', filename=filename))
        print(self.i18n.t('bgm_generation_processing'))
        
        # 确保所有音轨长度一致
        target_samples = int(self.sample_rate * duration)
        
        # 1. 生成动态主旋律（高级旋律引擎）
        print(self.i18n.t('bgm_generation_melody'))
        melody = self.generate_dynamic_melody(duration, style, complexity=4, seed=None)
        melody = self.ensure_length(melody, target_samples)
        
        # 可选：对位
        print(self.i18n.t('bgm_generation_counter'))
        counter_melody = self.generate_counter_melody(duration, style, complexity=3)
        counter_melody = self.ensure_length(counter_melody, target_samples)
        
        # 2. 生成动态低音线
        print(self.i18n.t('bgm_generation_bass'))
        bass = self.generate_bass_line(duration, style)
        bass = self.ensure_length(bass, target_samples)
        
        # 3. 生成和声音垫
        print(self.i18n.t('bgm_generation_pad'))
        main_pad = self.generate_ambient_pad(duration, style)
        main_pad = self.ensure_length(main_pad, target_samples)
        
        # 4. 生成弦乐声部
        print(self.i18n.t('bgm_generation_strings'))
        strings = self.generate_string_section(duration, style)
        strings = self.ensure_length(strings, target_samples)
        
        # 5. 生成钢琴琶音
        print(self.i18n.t('bgm_generation_piano'))
        piano = self.generate_piano_arpeggios(duration, style)
        piano = self.ensure_length(piano, target_samples)
        
        # 6. 生成动态鼓点
        print(self.i18n.t('bgm_generation_drums'))
        drums = self.generate_drum_pattern(duration, style)
        drums = self.ensure_length(drums, target_samples)
        
        # 7. 生成环境纹理
        print(self.i18n.t('bgm_generation_texture'))
        texture = self.generate_ambient_texture(duration)
        texture = self.ensure_length(texture, target_samples)
        
        # 7.5 生成管弦层
        print(self.i18n.t('bgm_generation_orchestral'))
        orch = self.generate_orchestral_layer(duration, style)
        
        # 确保管弦层长度一致
        for k in orch:
            orch[k] = self.ensure_length(orch[k], target_samples)
        
        # 分段推进包络
        seg_env = self._section_envelope(duration, scheme="ABA")
        
        # 动态混音 - 不同风格的乐器平衡和动态变化
        print(self.i18n.t('bgm_generation_mixing'))
        if style == "mysterious":
            mixed_audio = (melody * 0.30 +
                          counter_melody * 0.12 +
                          bass * 0.35 +
                          main_pad * 0.20 +
                          strings * 0.15 +
                          piano * 0.10 +
                          drums * 0.30 +
                          texture * 0.15 +
                          (orch["strings_hi"] * 0.22 + orch["choir"] * 0.18 +
                           orch["brass"] * 0.16 + orch["pluck"] * 0.12) * seg_env)
        elif style == "tense":
            mixed_audio = (melody * 0.35 +
                          counter_melody * 0.10 +
                          bass * 0.40 +
                          main_pad * 0.15 +
                          strings * 0.25 +
                          piano * 0.05 +
                          drums * 0.50 +
                          texture * 0.10 +
                          (orch["strings_hi"] * 0.20 + orch["choir"] * 0.12 +
                           orch["brass"] * 0.22 + orch["pluck"] * 0.10) * seg_env)
        elif style == "peaceful":
            mixed_audio = (melody * 0.25 +
                          counter_melody * 0.15 +
                          bass * 0.20 +
                          main_pad * 0.40 +
                          strings * 0.30 +
                          piano * 0.25 +
                          drums * 0.10 +
                          texture * 0.25 +
                          (orch["strings_hi"] * 0.24 + orch["choir"] * 0.22 +
                           orch["brass"] * 0.08 + orch["pluck"] * 0.10) * seg_env)
        else:  # hopeful
            mixed_audio = (melody * 0.40 +
                          counter_melody * 0.15 +
                          bass * 0.25 +
                          main_pad * 0.20 +
                          strings * 0.20 +
                          piano * 0.30 +
                          drums * 0.40 +
                          texture * 0.10 +
                          (orch["strings_hi"] * 0.20 + orch["choir"] * 0.14 +
                           orch["brass"] * 0.18 + orch["pluck"] * 0.12) * seg_env)
        
        # 添加动态音量变化（让整首曲子有起伏）
        t = np.linspace(0, duration, len(mixed_audio))
        dynamic_envelope = 0.8 + 0.2 * np.sin(2 * np.pi * t / (duration/2))  # 慢速音量变化
        mixed_audio *= dynamic_envelope
        
        # 整体淡入淡出
        fade_samples = int(2 * self.sample_rate)  # 2秒淡入淡出
        if len(mixed_audio) > fade_samples * 2:
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            mixed_audio[:fade_samples] *= fade_in
            mixed_audio[-fade_samples:] *= fade_out
        
        # 最终调制和动态压缩
        mixed_audio = self.add_subtle_modulation(mixed_audio, duration)
        
        # 动态范围压缩（让音乐更紧凑）
        mixed_audio = self.compress_dynamics(mixed_audio)
        
        # 保存文件
        self.save_audio(mixed_audio, filename)
        
        file_size = os.path.getsize(filename) / (1024 * 1024)
        print(self.i18n.t('bgm_completion_success'))
        print(self.i18n.t('bgm_completion_features'))
        print(self.i18n.t('bgm_completion_orchestral'))
        print(self.i18n.t('bgm_completion_characteristics'))
        print(self.i18n.t('bgm_completion_melody'))
        print(self.i18n.t('bgm_completion_structure'))
        print(self.i18n.t('bgm_completion_filesize', size=file_size))
        print(self.i18n.t('bgm_completion_location', path=os.path.abspath(filename)))
        
        return filename
    
    def compress_dynamics(self, audio_data, ratio=3.0, threshold=0.7):
        """动态范围压缩"""
        # 简单的压缩器
        compressed = audio_data.copy()
        
        # 找到超过阈值的部分
        over_threshold = np.abs(compressed) > threshold
        
        # 对超过阈值的部分进行压缩
        compressed[over_threshold] = np.sign(compressed[over_threshold]) * (
            threshold + (np.abs(compressed[over_threshold]) - threshold) / ratio
        )
        
        return compressed
    
    def ensure_length(self, audio_array, target_length):
        """确保音频数组长度一致"""
        current_length = len(audio_array)
        
        if current_length == target_length:
            return audio_array
        elif current_length < target_length:
            # 如果太短，用零填充
            return np.pad(audio_array, (0, target_length - current_length), mode='constant')
        else:
            # 如果太长，截断
            return audio_array[:target_length]

class BackgroundMusicGUI:
    """背景音乐生成器 GUI 界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.generator = SimpleBackgroundMusicGenerator()
        self.setup_ui()
        self.update_language()
        
    def setup_ui(self):
        """设置用户界面"""
        self.root.title(lang.get('bgm_title', '轻量级背景音乐生成器'))
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 居中显示窗口
        self.center_window()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 语言切换按钮（右上角）
        self.create_language_selector(main_frame)
        
        # 标题
        self.title_var = tk.StringVar(value=lang.get('bgm_title', '轻量级背景音乐生成器'))
        title_label = ttk.Label(main_frame, textvariable=self.title_var, 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        self.subtitle_var = tk.StringVar(value=lang.get('bgm_subtitle', '专为YouTube短视频设计'))
        subtitle_label = ttk.Label(main_frame, textvariable=self.subtitle_var)
        subtitle_label.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        # 风格选择
        self.styles_title_var = tk.StringVar(value=lang.get('bgm_styles_title', '可用风格:'))
        ttk.Label(main_frame, textvariable=self.styles_title_var).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.style_var = tk.StringVar(value="mysterious")
        style_frame = ttk.Frame(main_frame)
        style_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.style_buttons = {}
        styles = [
            ("mysterious", "bgm_styles_mysterious"),
            ("peaceful", "bgm_styles_peaceful"), 
            ("tense", "bgm_styles_tense"),
            ("hopeful", "bgm_styles_hopeful")
        ]
        
        for i, (style_id, lang_key) in enumerate(styles):
            btn = ttk.Radiobutton(style_frame, text=lang.get(lang_key, style_id), 
                                 variable=self.style_var, value=style_id)
            btn.grid(row=0, column=i, padx=5, sticky=tk.W)
            self.style_buttons[style_id] = btn
        
        # 时长设置
        self.duration_label_var = tk.StringVar(value=lang.get('bgm_input_duration', '音乐时长 (秒):'))
        ttk.Label(main_frame, textvariable=self.duration_label_var).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar(value="30")
        duration_entry = ttk.Entry(main_frame, textvariable=self.duration_var, width=10)
        duration_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # 文件名设置
        self.filename_label_var = tk.StringVar(value=lang.get('bgm_input_filename', '输出文件名:'))
        ttk.Label(main_frame, textvariable=self.filename_label_var).grid(row=5, column=0, sticky=tk.W, pady=5)
        filename_frame = ttk.Frame(main_frame)
        filename_frame.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        filename_frame.columnconfigure(0, weight=1)
        
        self.filename_var = tk.StringVar(value="bgm_mysterious.wav")
        filename_entry = ttk.Entry(filename_frame, textvariable=self.filename_var)
        filename_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.browse_btn = ttk.Button(filename_frame, text=lang.get('bgm_browse', '浏览'), command=self.browse_file)
        self.browse_btn.grid(row=0, column=1)
        
        # 生成按钮
        self.generate_btn = ttk.Button(main_frame, text=lang.get('bgm_generation_start', '开始生成'), 
                                      command=self.start_generation, style='Accent.TButton')
        self.generate_btn.grid(row=6, column=0, columnspan=3, pady=20)
        
        # 进度条
        self.progress_var = tk.StringVar(value="")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=7, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 状态显示
        self.status_var = tk.StringVar(value="")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground='green')
        status_label.grid(row=9, column=0, columnspan=3, pady=5)
        
        # 绑定事件
        self.style_var.trace('w', self.on_style_change)
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_language_selector(self, parent):
        """创建语言选择器"""
        lang_frame = ttk.Frame(parent)
        lang_frame.grid(row=0, column=2, sticky=tk.E, pady=5)
        
        current_lang = get_saved_language()
        lang_text = lang.get('bgm_language_zh', '中文') if current_lang == "zh" else lang.get('bgm_language_en', 'English')
        
        self.lang_btn = ttk.Button(lang_frame, text=lang_text, command=self.toggle_language)
        self.lang_btn.pack()
        
    def toggle_language(self):
        """切换语言"""
        current_lang = get_saved_language()
        new_lang = "en" if current_lang == "zh" else "zh"
        
        if switch_language(new_lang):
            self.update_language()
            messagebox.showinfo(lang.get('bgm_success', '成功'), lang.get('bgm_language_switched', f'语言已切换为: {new_lang}'))
            
    def update_language(self):
        """更新界面语言"""
        # 更新窗口标题
        self.root.title(lang.get('bgm_title', '轻量级背景音乐生成器'))
        
        # 更新语言按钮
        current_lang = get_saved_language()
        lang_text = lang.get('bgm_language_zh', '中文') if current_lang == "zh" else lang.get('bgm_language_en', 'English')
        self.lang_btn.config(text=lang_text)
        
        # 更新所有文本
        for style_id, btn in self.style_buttons.items():
            lang_key = f"bgm_styles_{style_id}"
            btn.config(text=lang.get(lang_key, style_id))
            
        # 更新其他控件文本
        self.generate_btn.config(text=lang.get('bgm_generation_start', '开始生成'))
        
        # 更新所有标签文本 - 需要重新创建或更新标签
        self.update_all_labels()
        
    def update_all_labels(self):
        """更新所有标签的文本"""
        # 更新标题和副标题
        self.title_var.set(lang.get('bgm_title', '轻量级背景音乐生成器'))
        self.subtitle_var.set(lang.get('bgm_subtitle', '专为YouTube短视频设计'))
        
        # 更新标签
        self.styles_title_var.set(lang.get('bgm_styles_title', '可用风格:'))
        self.duration_label_var.set(lang.get('bgm_input_duration', '音乐时长 (秒):'))
        self.filename_label_var.set(lang.get('bgm_input_filename', '输出文件名:'))
        
        # 更新按钮
        self.browse_btn.config(text=lang.get('bgm_browse', '浏览'))
        self.generate_btn.config(text=lang.get('bgm_generation_start', '开始生成'))
        
    def on_style_change(self, *args):
        """风格改变时的回调"""
        style = self.style_var.get()
        self.filename_var.set(f"bgm_{style}.wav")
        
    def browse_file(self):
        """浏览文件对话框"""
        filename = filedialog.asksaveasfilename(
            title=lang.get('bgm_file_dialog_title', '选择输出文件'),
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.filename_var.set(filename)
            
    def start_generation(self):
        """开始生成音乐"""
        try:
            # 验证输入
            duration = int(self.duration_var.get())
            if duration <= 0:
                messagebox.showerror(lang.get('bgm_error', '错误'), lang.get('bgm_error_duration', '时长必须大于0'))
                return
                
            filename = self.filename_var.get()
            if not filename:
                messagebox.showerror(lang.get('bgm_error', '错误'), lang.get('bgm_error_filename', '请输入文件名'))
                return
                
            if not filename.endswith('.wav'):
                filename += '.wav'
                self.filename_var.set(filename)
                
            # 禁用生成按钮
            self.generate_btn.config(state='disabled')
            self.progress_bar.start()
            self.progress_var.set(lang.get('bgm_generation_processing', '正在生成...'))
            self.status_var.set("")
            
            # 在新线程中生成音乐
            thread = threading.Thread(target=self.generate_music, args=(duration, filename))
            thread.daemon = True
            thread.start()
            
        except ValueError:
            messagebox.showerror(lang.get('bgm_error', '错误'), lang.get('bgm_error_duration_invalid', '请输入有效的时长'))
            self.generate_btn.config(state='normal')
            self.progress_bar.stop()
            
    def generate_music(self, duration, filename):
        """生成音乐（在后台线程中运行）"""
        try:
            style = self.style_var.get()
            
            # 更新进度
            self.root.after(0, lambda: self.progress_var.set(lang.get('bgm_generation_style', f'生成风格: {style}')))
            
            # 生成音乐
            result = self.generator.generate_youtube_bgm(style, duration, filename)
            
            # 更新状态
            self.root.after(0, lambda: self.progress_var.set(lang.get('bgm_completion_success', '生成完成!')))
            self.root.after(0, lambda: self.status_var.set(lang.get('bgm_completion_final', '背景音乐生成完成!')))
            
        except Exception as e:
            error_msg = lang.get('bgm_interaction_error', f'程序运行出错: {e}')
            self.root.after(0, lambda: messagebox.showerror(lang.get('bgm_error', '错误'), error_msg))
            self.root.after(0, lambda: self.status_var.set(lang.get('bgm_generation_failed', '生成失败')))
            
        finally:
            # 恢复界面
            self.root.after(0, lambda: self.generate_btn.config(state='normal'))
            self.root.after(0, lambda: self.progress_bar.stop())
            self.root.after(0, lambda: self.progress_var.set(""))
            
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数 - 启动GUI界面"""
    try:
        # 启动GUI界面
        app = BackgroundMusicGUI()
        app.run()
    except Exception as e:
        print(_I18N.t('bgm_gui_start_failed', error=e))
        # 如果GUI启动失败，回退到命令行模式
        print(_I18N.t('bgm_fallback_cli'))
        main_cli()

def main_cli():
    """命令行模式（备用）"""
    # 使用全局国际化管理器
    i18n = _I18N
    
    print(i18n.t('bgm_title'))
    print(i18n.t('bgm_subtitle'))
    print(i18n.t('bgm_description'))
    print("="*50)
    
    # 语言选择
    print(f"\n{i18n.t('bgm_language_current')}")
    lang_choice = input(i18n.t('bgm_language_switch')).strip()
    if lang_choice == '2':
        i18n.switch_language('en')
        print(i18n.t('bgm_language_switched', lang=i18n.get_language_name('en')))
    elif lang_choice == '1':
        i18n.switch_language('zh')
        print(i18n.t('bgm_language_switched', lang=i18n.get_language_name('zh')))
    
    generator = SimpleBackgroundMusicGenerator(i18n)
    
    # 可用风格
    styles = {
        "1": ("mysterious", i18n.t('bgm_styles_mysterious')),
        "2": ("peaceful", i18n.t('bgm_styles_peaceful')),
        "3": ("tense", i18n.t('bgm_styles_tense')),
        "4": ("hopeful", i18n.t('bgm_styles_hopeful'))
    }
    
    print(f"\n{i18n.t('bgm_styles_title')}")
    for key, (style_id, description) in styles.items():
        print(f"  {key}. {description}")
    
    # 选择风格
    choice = input(f"\n{i18n.t('bgm_input_select_style')}").strip()
    style_id, style_name = styles.get(choice, ("mysterious", i18n.t('bgm_styles_mysterious')))
    
    # 设置时长
    duration_input = input(i18n.t('bgm_input_duration')).strip()
    duration = int(duration_input) if duration_input.isdigit() else 30
    
    # 设置文件名
    filename_input = input(i18n.t('bgm_input_filename')).strip()
    filename = filename_input if filename_input else f"bgm_{style_id}.wav"
    if not filename.endswith('.wav'):
        filename += '.wav'
    
    # 生成音乐
    print(f"\n🚀 {i18n.t('bgm_generation_start')} {style_name} 风格的背景音乐...")
    result = generator.generate_youtube_bgm(style_id, duration, filename)
    
    print(f"\n{i18n.t('bgm_completion_final')}")
    print(i18n.t('bgm_completion_usage'))
    
    # 询问是否继续生成
    if input(f"\n{i18n.t('bgm_interaction_continue')}").lower().startswith('y'):
        main_cli()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{_I18N.t('bgm_interaction_interrupted')}")
    except Exception as e:
        print(f"\n{_I18N.t('bgm_interaction_error', error=e)}")