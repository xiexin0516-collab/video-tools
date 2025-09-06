import os
import sys
from moviepy.editor import *
from tkinter import Tk, filedialog, messagebox, simpledialog
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np
import random
from language_loader import lang, switch_language, get_saved_language

class VideoEffectsGenerator:
    def __init__(self):
        self.output_resolution = (1920, 1080)
        self.image_duration = 3
        self.fade_duration = 1
        self.fps = 24
        
    def create_film_grain(self, size, intensity=0.1):
        """创建胶片颗粒纹理"""
        grain = np.random.normal(0, intensity, size + (3,))
        grain = np.clip(grain * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(grain, 'RGB')
    
    def create_scratches_overlay(self, size, num_scratches=5):
        """创建划痕叠加层"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for _ in range(num_scratches):
            # 随机位置和长度的划痕
            x1 = random.randint(0, size[0])
            y1 = random.randint(0, size[1])
            length = random.randint(50, min(size[0], size[1]) // 4)
            angle = random.uniform(0, 360)
            
            x2 = x1 + int(length * np.cos(np.radians(angle)))
            y2 = y1 + int(length * np.sin(np.radians(angle)))
            
            # 白色半透明划痕
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 80), width=2)
        
        return img

    # 特效函数定义
    def effect_zoom_in(self, clip):
        """推拉镜头 - 放大"""
        return clip.fx(vfx.resize, lambda t: 1.0 + 0.15 * (t / clip.duration)).set_position("center")
    
    def effect_zoom_out(self, clip):
        """推拉镜头 - 缩小"""
        return clip.fx(vfx.resize, lambda t: 1.2 - 0.15 * (t / clip.duration)).set_position("center")
    
    def effect_pan_right(self, clip):
        """水平移动 - 向右"""
        return clip.set_position(lambda t: (int(-100 + 50 * t), "center"))
    
    def effect_pan_left(self, clip):
        """水平移动 - 向左"""
        return clip.set_position(lambda t: (int(100 - 50 * t), "center"))
    
    def effect_pan_up(self, clip):
        """垂直移动 - 向上"""
        return clip.set_position(lambda t: ("center", int(50 - 25 * t)))
    
    def effect_pan_down(self, clip):
        """垂直移动 - 向下"""
        return clip.set_position(lambda t: ("center", int(-50 + 25 * t)))
    
    def effect_rotate_slight(self, clip):
        """轻微旋转"""
        return clip.rotate(lambda t: 2 * np.sin(2 * np.pi * t / clip.duration))
    
    def effect_flip_horizontal(self, clip):
        """水平镜像"""
        return clip.fx(vfx.mirror_x)
    
    def effect_flip_vertical(self, clip):
        """垂直镜像"""
        return clip.fx(vfx.mirror_y)
    
    def effect_sepia_tint(self, clip):
        """怀旧泛黄滤镜"""
        def sepia_filter(gf, t):
            frame = gf(t)
            # 转换为sepia色调
            sepia_frame = np.zeros_like(frame)
            sepia_frame[:,:,0] = np.clip(frame[:,:,0] * 0.393 + frame[:,:,1] * 0.769 + frame[:,:,2] * 0.189, 0, 255)
            sepia_frame[:,:,1] = np.clip(frame[:,:,0] * 0.349 + frame[:,:,1] * 0.686 + frame[:,:,2] * 0.168, 0, 255)
            sepia_frame[:,:,2] = np.clip(frame[:,:,0] * 0.272 + frame[:,:,1] * 0.534 + frame[:,:,2] * 0.131, 0, 255)
            return sepia_frame
        return clip.fl(sepia_filter)
    
    def effect_cold_blue(self, clip):
        """冷蓝色调"""
        return clip.fx(vfx.colorx, 0.8).fx(vfx.lum_contrast, 0, 20, 128)
    
    def effect_black_white(self, clip):
        """黑白滤镜"""
        return clip.fx(vfx.blackwhite)
    
    def effect_film_grain(self, clip):
        """胶片颗粒效果"""
        def add_grain(gf, t):
            frame = gf(t)
            grain = np.random.normal(0, 15, frame.shape).astype(np.int16)
            noisy_frame = np.clip(frame.astype(np.int16) + grain, 0, 255).astype(np.uint8)
            return noisy_frame
        return clip.fl(add_grain)
    
    def effect_scratches(self, clip):
        """划痕效果"""
        scratch_overlay = self.create_scratches_overlay(self.output_resolution)
        scratch_path = "temp_scratches.png"
        scratch_overlay.save(scratch_path)
        
        if os.path.exists(scratch_path):
            overlay = (ImageClip(scratch_path)
                      .resize(clip.size)
                      .set_duration(clip.duration)
                      .set_opacity(0.3))
            result = CompositeVideoClip([clip, overlay])
            os.remove(scratch_path)  # 清理临时文件
            return result
        return clip
    
    def effect_fade(self, clip, duration):
        """淡入淡出"""
        return clip.crossfadein(duration).crossfadeout(duration)

    def get_effect_choices(self):
        """获取所有可用特效"""
        return {
            f"{lang.get('effects_zoom_in', '推拉镜头 - 放大')} (Zoom In)": self.effect_zoom_in,
            f"{lang.get('effects_zoom_out', '推拉镜头 - 缩小')} (Zoom Out)": self.effect_zoom_out,
            f"{lang.get('effects_pan_right', '水平移动 - 向右')} (Pan Right)": self.effect_pan_right,
            f"{lang.get('effects_pan_left', '水平移动 - 向左')} (Pan Left)": self.effect_pan_left,
            f"{lang.get('effects_pan_up', '垂直移动 - 向上')} (Pan Up)": self.effect_pan_up,
            f"{lang.get('effects_pan_down', '垂直移动 - 向下')} (Pan Down)": self.effect_pan_down,
            f"{lang.get('effects_rotate', '轻微旋转')} (Rotate)": self.effect_rotate_slight,
            f"{lang.get('effects_flip_h', '水平镜像')} (Flip H)": self.effect_flip_horizontal,
            f"{lang.get('effects_flip_v', '垂直镜像')} (Flip V)": self.effect_flip_vertical,
            f"{lang.get('effects_sepia', '怀旧泛黄')} (Sepia)": self.effect_sepia_tint,
            f"{lang.get('effects_cold_blue', '冷蓝色调')} (Cold Blue)": self.effect_cold_blue,
            f"{lang.get('effects_black_white', '黑白滤镜')} (B&W)": self.effect_black_white,
            f"{lang.get('effects_film_grain', '胶片颗粒')} (Film Grain)": self.effect_film_grain,
            f"{lang.get('effects_scratches', '划痕效果')} (Scratches)": self.effect_scratches
        }

    def select_images(self):
        """图片选择界面"""
        root = Tk()
        root.title(lang.get('select_images_title', '图片特效视频生成器 - 选择图片'))
        root.geometry("600x400")
        root.resizable(True, True)
        
        # 创建界面元素
        from tkinter import ttk, Label, Button, Listbox, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH, END, Frame
        
        # 主框架
        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # 语言切换：右上角按钮
        from tkinter import messagebox

        def current_lang_name():
            cur = get_saved_language()
            return "中文" if cur == "zh" else "English"

        def refresh_texts():
            # 按当前语言刷新界面文案
            from language_loader import lang  # 重新导入最新的lang
            root.title(lang.get('select_images_title', '图片特效视频生成器 - 选择图片'))
            title_label.config(text=f"🎬 {lang.get('select_images_desc', '请选择要处理的图片文件')}")
            info_label.config(text=lang.get('supported_formats_desc', '支持格式: PNG, JPG, JPEG, BMP, TIFF'))
            path_label.config(text="📁 " + lang.get('current_path', '当前路径:'))
            chosen_label.config(text=lang.get('chosen_files', '已选择的文件:'))
            browse_btn.config(text="📂 " + lang.get('browse', '浏览选择文件'))
            confirm_btn.config(text="✅ " + lang.get('confirm_start', '确认开始处理'))
            cancel_btn.config(text="❌ " + lang.get('cancel_exit', '取消退出'))
            status_label.config(text=lang.get('please_browse', "请点击'浏览选择文件'来选择图片"))
            tip_label.config(text="💡 " + lang.get('tip_multi_select', '提示: 可以同时选择多个图片文件进行批量处理'))
            lang_btn.config(text="🌐 " + current_lang_name())

        def toggle_language():
            new_lang = 'en' if get_saved_language() == 'zh' else 'zh'
            switch_language(new_lang)
            refresh_texts()
            messagebox.showinfo(
                lang.get('lang_switched_title', '语言已切换'),
                lang.get('lang_switched_body', '已切换为 {name}').format(name=current_lang_name())
            )

        lang_btn = Button(main_frame,
                          text="🌐 " + current_lang_name(),
                          command=toggle_language,
                          font=("Arial", 10), bg="#EEE", padx=10, pady=4)
        lang_btn.pack(anchor='ne')  # 放到右上角
        
        # 标题
        title_label = Label(main_frame, text="", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0,10))
        
        # 说明文字
        info_label = Label(main_frame, text="", font=("Arial", 10))
        info_label.pack(pady=(0,10))
        
        # 当前路径显示
        path_frame = Frame(main_frame)
        path_frame.pack(fill='x', pady=(0,10))
        
        path_label = Label(path_frame, text="", font=("Arial", 9))  # ← 原来写死"📁 当前路径:"
        path_label.pack(side=LEFT)
        current_path = Label(path_frame, text=os.getcwd(), font=("Arial", 9), fg="blue", wraplength=400)
        current_path.pack(side=LEFT, padx=(5,0))
        
        # 选中的文件列表框
        list_frame = Frame(main_frame)
        list_frame.pack(fill=BOTH, expand=True, pady=(0,15))
        
        chosen_label = Label(list_frame, text="", font=("Arial", 10, "bold"))
        chosen_label.pack(anchor='w')
        
        listbox_frame = Frame(list_frame)
        listbox_frame.pack(fill=BOTH, expand=True, pady=(5,0))
        
        listbox = Listbox(listbox_frame, font=("Arial", 9))
        scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        selected_files = []
        
        def browse_files():
            """浏览文件"""
            file_paths = filedialog.askopenfilenames(
                title=lang.get('file_dialog_title', "Select images (Ctrl for multi-select, order = timeline)"),
                initialdir=os.getcwd(),
                filetypes=[
                    (lang.get('filetypes_all_supported', "All supported images"), "*.png *.jpg *.jpeg *.bmp *.tiff"),
                    (lang.get('filetypes_png', "PNG files"), "*.png"),
                    (lang.get('filetypes_jpeg', "JPEG files"), "*.jpg *.jpeg"), 
                    (lang.get('filetypes_bmp', "BMP files"), "*.bmp"),
                    (lang.get('filetypes_tiff', "TIFF files"), "*.tiff"),
                    (lang.get('filetypes_all', "All files"), "*.*")
                ]
            )
            
            if file_paths:
                # 清空列表
                listbox.delete(0, END)
                selected_files.clear()
                
                # 保持用户选择的原始顺序，显示原始文件名
                for file_path in file_paths:
                    filename = os.path.basename(file_path)
                    listbox.insert(END, f"📷 {filename}")  # 显示原始文件名
                    selected_files.append(file_path)
                
                print(f"\n📋 {lang.get('video_generation_order', '视频生成顺序 (按您的选择顺序):')}")
                for idx, file_path in enumerate(file_paths, 1):
                    print(f"   {idx}. {os.path.basename(file_path)}")
                
                # 更新状态
                update_status()
        
        def update_status():
            """更新状态"""
            if selected_files:
                confirm_btn.config(state="normal", bg="#4CAF50")
                status_label.config(text=f"✅ {lang.get('selected_count_files', '已选择 {count} 个文件').format(count=len(selected_files))}", fg="green")
            else:
                confirm_btn.config(state="disabled", bg="gray")
                status_label.config(text=f"❌ {lang.get('no_files_selected', '未选择任何文件')}", fg="red")
        
        def confirm_selection():
            """确认选择"""
            if selected_files:
                root.quit()
                root.destroy()
        
        def cancel_selection():
            """取消选择"""
            selected_files.clear()
            root.quit()
            root.destroy()
        
        # 按钮框架
        button_frame = Frame(main_frame)
        button_frame.pack(fill='x', pady=(10,0))
        
        # 浏览按钮
        browse_btn = Button(button_frame, text="", command=browse_files, 
                           font=("Arial", 11, "bold"), bg="#2196F3", fg="white", 
                           padx=20, pady=8, relief="raised")
        browse_btn.pack(side=LEFT, padx=(0,10))
        
        # 确认按钮
        confirm_btn = Button(button_frame, text="", command=confirm_selection, 
                            font=("Arial", 11, "bold"), bg="gray", fg="white", 
                            padx=20, pady=8, state="disabled", relief="raised")
        confirm_btn.pack(side=LEFT, padx=(0,10))
        
        # 取消按钮
        cancel_btn = Button(button_frame, text="", command=cancel_selection, 
                           font=("Arial", 11), bg="#f44336", fg="white", 
                           padx=20, pady=8, relief="raised")
        cancel_btn.pack(side=RIGHT)
        
        # 状态框架
        status_frame = Frame(main_frame)
        status_frame.pack(fill='x', pady=(10,0))
        
        # 状态标签
        status_label = Label(status_frame, text="", 
                            font=("Arial", 10), fg="gray")
        status_label.pack()
        
        # 提示标签
        tip_label = Label(status_frame, text="", 
                         font=("Arial", 9), fg="blue")
        tip_label.pack(pady=(5,0))
        
        # 初始化文案
        refresh_texts()
        
        # 居中显示窗口
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # 初始化状态
        update_status()
        
        # 显示窗口并等待
        root.mainloop()
        
        return selected_files if selected_files else []

    def configure_settings(self):
        """设置配置界面"""
        root = Tk()
        root.withdraw()
        
        # 图片显示时长
        duration = simpledialog.askfloat(
            lang.get('video_settings', '视频设置'), 
            lang.get('image_duration_prompt', '每张图片显示时长 (秒):'), 
            initialvalue=3.0, 
            minvalue=0.5, 
            maxvalue=10.0
        )
        if duration:
            self.image_duration = duration
        
        # 淡入淡出时长
        fade = simpledialog.askfloat(
            lang.get('video_settings', '视频设置'), 
            lang.get('fade_duration_prompt', '淡入淡出时长 (秒):'), 
            initialvalue=1.0, 
            minvalue=0.0, 
            maxvalue=3.0
        )
        if fade is not None:
            self.fade_duration = fade
        
        root.destroy()

    def select_effects(self):
        """特效选择界面"""
        effect_choices = self.get_effect_choices()
        
        print("\n" + "="*60)
        print(f"📸 {lang.get('available_effects', '可用图像特效 (输入编号，多选用逗号分隔，如: 1,3,5)')}")
        print("="*60)
        
        effect_names = list(effect_choices.keys())
        for i, name in enumerate(effect_names, 1):
            print(f"{i:2d}. {name}")
        
        print(f"\n💡 {lang.get('recommended_combinations', '推荐组合:')}")
        print(f"   📚 {lang.get('historical_style', '历史档案风格: 10,13,14 (怀旧+颗粒+划痕) - 历史感、年代感')}")
        print(f"   🔬 {lang.get('scientific_style', '科学分析风格: 2,11,12 (缩小+冷蓝+黑白) - 理性、客观、技术感')}") 
        print(f"   🌟 {lang.get('mystery_style', '神秘悬疑风格: 1,7,10 (放大+旋转+怀旧) - 吸引注意、制造悬念')}")
        print(f"   🧠 {lang.get('psychological_style', '心理认知风格: 3,8,10 (右移+镜像+怀旧) - 记忆错乱、认知偏差感')}")
        print(f"   🗺️ {lang.get('exploration_style', '探险发现风格: 1,5,6 (放大+上移+下移) - 探索感、发现感')}")
        print(f"   ⚡ {lang.get('high_energy_style', '高能转折风格: 1,7 (放大+旋转) - 强调重点、戏剧张力')}")
        print("")
        print(f"   💡 {lang.get('youtube_suggestions', 'YouTube解说视频建议:')}")
        print(f"      • {lang.get('opening_intro', '开场引入 → 🌟神秘悬疑风格')}")
        print(f"      • {lang.get('historical_background', '历史背景 → 📚历史档案风格')}") 
        print(f"      • {lang.get('scientific_explanation', '科学解释 → 🔬科学分析风格')}")
        print(f"      • {lang.get('important_turning', '重要转折 → ⚡高能转折风格')}")
        print(f"      • {lang.get('psychological_phenomenon', '心理现象 → 🧠心理认知风格')}")
        print(f"      • {lang.get('exploration_discovery', '探索发现 → 🗺️探险发现风格')}")
        
        selected = input(f"\n{lang.get('select_effects_prompt', '请选择特效编号:')} ").strip()
        
        try:
            # 处理中文逗号和英文逗号
            selected = selected.replace('，', ',').replace('、', ',').replace(' ', '')
            selected_indices = []
            
            for x in selected.split(","):
                if x.strip().isdigit():
                    idx = int(x.strip()) - 1
                    if 0 <= idx < len(effect_names):
                        selected_indices.append(idx)
            
            if not selected_indices:
                print(f"❌ {lang.get('no_valid_effects', '没有选择有效的特效，将使用默认特效')}")
                return [effect_choices[effect_names[0]]]
            
            selected_effects = []
            print(f"\n✅ {lang.get('parsed_effects', '解析到 {count} 个特效:').format(count=len(selected_indices))}")
            
            for i in selected_indices:
                effect_name = effect_names[i]
                effect_func = effect_choices[effect_name]
                selected_effects.append(effect_func)
                print(f"   ✅ {i+1}. {effect_name}")
            
            return selected_effects
            
        except Exception as e:
            print(f"❌ {lang.get('input_parse_error', '输入解析错误: {error}').format(error=e)}")
            print(f"❌ {lang.get('will_use_default', '将使用默认特效')}")
            return [effect_choices[effect_names[0]]]

    def generate_video(self, image_paths, selected_effects, enable_fade, output_path):
        """生成视频"""
        if not image_paths:
            print(f"❌ {lang.get('no_images_selected', '没有选择图片')}")
            return False
        
        print(f"\n🎬 {lang.get('start_processing', '开始处理 {count} 张图片...').format(count=len(image_paths))}")
        print(f"📊 {lang.get('output_resolution', '输出分辨率: {width}x{height}').format(width=self.output_resolution[0], height=self.output_resolution[1])}")
        print(f"⏱️  {lang.get('image_duration_info', '每张图片时长: {duration}秒').format(duration=self.image_duration)}")
        print(f"🎞️  {lang.get('fps_info', '帧率: {fps}fps').format(fps=self.fps)}")
        print("="*60)
        
        clips = []
        total_images = len(image_paths)
        
        for idx, path in enumerate(image_paths, 1):
            # 显示进度条
            progress = (idx - 1) / total_images * 100
            bar_length = 30
            filled_length = int(bar_length * (idx - 1) // total_images)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            print(f"\r📊 {lang.get('processing_progress', '处理进度:')} [{bar}] {progress:.1f}% ({idx-1}/{total_images})", end='', flush=True)
            print(f"\n🖼️  {lang.get('processing_image', '正在处理:')} {os.path.basename(path)}")
            
            try:
                # 创建图片剪辑 - 裁剪并调整到1920x1080填满屏幕
                clip = ImageClip(path).set_duration(self.image_duration)
                
                # 获取原始尺寸
                original_w, original_h = clip.size
                target_w, target_h = self.output_resolution
                
                # 计算缩放比例，确保完全填满屏幕
                scale_w = target_w / original_w
                scale_h = target_h / original_h
                scale = max(scale_w, scale_h)  # 选择较大的缩放比例
                
                # 先缩放，然后获取实际尺寸，再裁剪到目标尺寸
                resized_clip = clip.resize(scale)
                w, h = resized_clip.size  # 获取缩放后的实际尺寸
                clip = resized_clip.crop(
                    x_center=w // 2, y_center=h // 2, 
                    width=target_w, height=target_h
                )
                
                # 应用选中的特效 (显示特效处理进度)
                for effect_idx, effect in enumerate(selected_effects, 1):
                    print(f"   ⚙️  {lang.get('applying_effect', '应用特效')} {effect_idx}/{len(selected_effects)}: {effect.__name__}")
                    clip = effect(clip)
                
                # 应用淡入淡出
                if enable_fade:
                    print(f"   🌅 {lang.get('applying_fade', '应用淡入淡出效果...')}")
                    clip = self.effect_fade(clip, self.fade_duration)
                
                clips.append(clip)
                
                # 最终进度更新
                progress = idx / total_images * 100
                filled_length = int(bar_length * idx // total_images)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                print(f"\r📊 {lang.get('processing_progress', '处理进度:')} [{bar}] {progress:.1f}% ({idx}/{total_images})", end='', flush=True)
                print(f" ✅ {lang.get('processing_complete', '完成!')}")
                
            except Exception as e:
                print(f"\n⚠️  {lang.get('image_processing_error', '处理图片 {path} 时出错: {error}').format(path=path, error=e)}")
                continue
        
        if not clips:
            print(f"\n❌ {lang.get('no_successful_images', '没有成功处理的图片')}")
            return False
        
        print(f"\n\n🎬 {lang.get('image_processing_done', '图片处理完成! 开始合成视频...')}")
        print("="*60)
        
        # 合成最终视频
        final_video = concatenate_videoclips(clips, method="compose")
        
        # 输出视频 (显示编码进度)
        print(f"💾 {lang.get('outputting_video', '正在输出视频:')} {os.path.basename(output_path)}")
        print(f"📁 {lang.get('output_path', '输出路径:')} {output_path}")
        print(f"⏳ {lang.get('encoding_please_wait', '正在编码，请耐心等待...')}")
        print(f"📊 {lang.get('encoding_progress', '编码进度:')}")
        
        try:
            # 确保输出目录存在
            output_dir_path = os.path.dirname(output_path)
            os.makedirs(output_dir_path, exist_ok=True)
            
            print(f"🎬 {lang.get('start_video_encoding', '开始视频编码...')}")
            final_video.write_videofile(
                output_path, 
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger='bar'  # 显示moviepy自带的进度条
            )
            
            print(f"\n\n✅ {lang.get('video_generation_complete', '视频生成完成!')}")
            print("="*60)
            print(f"📁 {lang.get('file_location', '文件位置:')} {output_path}")
            print(f"📏 {lang.get('video_duration', '视频时长:')} {final_video.duration:.1f}秒")
            
            # 等待文件系统同步，然后获取文件大小
            import time
            time.sleep(1)  # 等待1秒让文件系统同步
            
            try:
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path) / (1024*1024)
                    print(f"📊 {lang.get('file_size', '文件大小:')} {file_size:.1f} MB")
                else:
                    print(f"📊 {lang.get('file_size_unavailable', '文件大小: 无法获取 (文件可能仍在写入)')}")
            except Exception as size_error:
                print(f"📊 {lang.get('file_size_error', '文件大小: 无法获取 ({error})').format(error=size_error)}")
            
            # 清理内存
            final_video.close()
            for clip in clips:
                clip.close()
            
            return True
            
        except Exception as e:
            print(f"❌ {lang.get('video_output_failed', '视频输出失败: {error}').format(error=e)}")
            return False

def select_language():
    """Language selection interface"""
    root = Tk()
    root.title("Language Selection / 语言选择")
    root.geometry("400x200")
    root.resizable(False, False)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    from tkinter import ttk, Label, Button, Frame
    
    # Main frame
    main_frame = Frame(root)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    title_label = Label(main_frame, text="🌐 Please select language / 请选择语言", 
                       font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Language buttons frame
    button_frame = Frame(main_frame)
    button_frame.pack(pady=10)
    
    selected_language = [None]  # Use list to store the result
    
    def choose_language(lang_code):
        selected_language[0] = lang_code
        root.quit()
        root.destroy()
    
    # Chinese button
    chinese_btn = Button(button_frame, text="🇨🇳 中文 (Chinese)", 
                        font=("Arial", 12, "bold"), 
                        bg="#4CAF50", fg="white",
                        width=20, height=2,
                        command=lambda: choose_language('zh'))
    chinese_btn.pack(pady=5)
    
    # English button
    english_btn = Button(button_frame, text="🇺🇸 English", 
                        font=("Arial", 12, "bold"), 
                        bg="#2196F3", fg="white",
                        width=20, height=2,
                        command=lambda: choose_language('en'))
    english_btn.pack(pady=5)
    
    # Show window and wait for selection
    root.mainloop()
    
    return selected_language[0] if selected_language[0] else 'zh'

def main():
    # Check if language needs to be selected
    current_lang = get_saved_language()
    if not current_lang or current_lang not in ['zh', 'en']:
        selected_lang = select_language()
        if selected_lang:
            switch_language(selected_lang)
    
    print(f"🎬 {lang.get('app_title', '图片特效视频生成器')}")
    print(f"💻 {lang.get('system_info', '检测到配置: i5-6500 CPU + 16GB RAM + Intel HD Graphics 530')}")
    print(f"📝 {lang.get('recommendation', '建议: 每次处理不超过50张图片，单张图片不超过4K分辨率')}")
    
    generator = VideoEffectsGenerator()
    
    # 1. 选择图片
    print(f"\n📂 {lang.get('step1', '第一步: 选择图片文件')}")
    image_paths = generator.select_images()
    
    if not image_paths:
        print(f"❌ {lang.get('no_images_exit', '未选择图片，程序退出')}")
        return
    
    print(f"✅ {lang.get('selected_count', '已选择 {count} 张图片').format(count=len(image_paths))}")
    
    # 2. 选择特效 (提前到第二步)
    print(f"\n🎨 {lang.get('step2', '第二步: 选择图片特效')}")
    selected_effects = generator.select_effects()
    
    # 3. 配置设置 (根据特效选择来配置)
    print(f"\n⚙️  {lang.get('step3', '第三步: 配置视频参数')}")
    generator.configure_settings()
    
    # 4. 淡入淡出选择
    enable_fade = input(f"\n🌅 {lang.get('step4', '第四步: 是否启用淡入淡出过渡? (y/n):')} ").lower().startswith('y')
    
    # 5. 设置输出路径
    output_dir = os.path.dirname(image_paths[0])
    output_filename = input(f"\n💾 {lang.get('step5', '第五步: 输出文件名 (默认: output.mp4):')} ").strip()
    if not output_filename:
        output_filename = "output.mp4"
    if not output_filename.endswith('.mp4'):
        output_filename += '.mp4'
    
    # 使用os.path.join并规范化路径
    output_path = os.path.normpath(os.path.join(output_dir, output_filename))
    
    # 检查文件是否存在，询问是否覆盖
    if os.path.exists(output_path):
        print(f"\n⚠️  {lang.get('file_exists', '文件 \'{filename}\' 已存在!').format(filename=output_filename)}")
        overwrite = input(f"{lang.get('overwrite_prompt', '是否覆盖现有文件? (y/n):')} ").lower().startswith('y')
        if not overwrite:
            print(f"❌ {lang.get('user_cancelled', '用户取消操作')}")
            return
        else:
            print(f"✅ {lang.get('will_overwrite', '将覆盖现有文件')}")
    
    # 6. 生成视频
    print(f"\n🚀 {lang.get('step6', '第六步: 开始生成视频')}")
    success = generator.generate_video(image_paths, selected_effects, enable_fade, output_path)
    
    if success:
        print(f"\n🎉 {lang.get('processing_complete', '处理完成! 可以查看生成的视频文件了')}")
        
        # 询问是否继续处理
        if input(f"\n🔄 {lang.get('continue_processing', '是否继续处理其他图片? (y/n):')} ").lower().startswith('y'):
            main()
    else:
        print(f"\n❌ {lang.get('generation_failed_desc', '视频生成失败，请检查图片文件和设置')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n⏹️  {lang.get('program_interrupted', '程序已被用户中断')}")
    except Exception as e:
        print(f"\n❌ {lang.get('program_error', '程序运行出错: {error}').format(error=e)}")
        print(f"💡 {lang.get('check_files', '请检查图片文件是否损坏，或重新启动程序')}")