// 国际化配置
window.I18N = {
    // 当前语言
    currentLang: 'en',
    
    // 语言配置
    languages: {
        zh: {
            name: '中文',
            flag: '🇨🇳'
        },
        en: {
            name: 'English',
            flag: '🇺🇸'
        }
    },
    
    // 翻译文本
    translations: {
        zh: {
            // 头部
            'header.title': '视频工具平台',
            'header.subtitle': '专业的视频处理工具',
            
            // 主要内容
            'hero.title': '专业的视频处理工具',
            'hero.subtitle': '一站式视频编辑、字幕制作、音频处理解决方案',
            
            // 搜索
            'search.placeholder': '🔍 搜索工具...',
            
            // 工具
            'tools.title': '工具列表',
            'tools.no_results': '没有找到相关工具',
            'tools.no_results_hint': '尝试调整搜索关键词或选择其他分类',
            
            // 分类
            'category.all': '🏠 全部工具',
            'category.subtitle': '🎬 字幕工具',
            'category.video': '🎥 视频处理',
            'category.audio': '🎵 音频处理',
            'category.image': '🖼️ 图片处理',
            
            // 工具状态
            'status.stable': '✅ 稳定版',
            'status.beta': '🧪 测试版',
            'status.alpha': '⚠️ 预览版',
            'status.coming_soon': '🚀 即将推出',
            
            // 按钮
            'btn.download': '📥 下载桌面版',
            'btn.details': '📋 详情',
            'btn.coming_soon': '🚀 即将推出',
            'btn.unavailable': '📥 下载暂不可用',
            'btn.close': '关闭',
            
            // 工具详情
            'details.version': '版本:',
            'details.size': '文件大小:',
            'details.requirements': '系统要求:',
            'details.status': '状态:',
            'details.description': '功能描述',
            'details.features': '主要功能',
            
            // 模态框
            'modal.download_title': '📥 下载桌面版',
            'modal.features_title': '💡 功能特色',
            
            // 功能特色
            'features.image_processing': '🖼️ 图片处理',
            'features.screenshot': '📸 截屏工具',
            'features.video_processing': '🎬 视频处理',
            'features.efficient': '⚡ 高效便捷',
            'features.more': '更多',
            
                         // 功能详细描述
             'features.smart_scaling': '智能图片缩放',
             'features.format_conversion': '格式转换 (JPG/PNG/WEBP)',
             'features.image_compression': '图片压缩优化',
             'features.batch_processing': '批量处理',
             'features.full_screenshot': '全屏截图',
             'features.area_screenshot': '区域截图',
             'features.window_screenshot': '窗口截图',
             'features.delayed_screenshot': '延时截图',
             'features.video_conversion': '视频格式转换',
             'features.subtitle_editing': '字幕编辑制作',
             'features.audio_extraction': '音频提取',
             'features.video_compression': '视频压缩',
             'features.no_registration': '无需注册登录',
             'features.cross_platform': '跨平台支持',
             'features.offline_use': '完全离线使用',
             'features.simple_interface': '界面简洁',
             'features.easy_operate': '操作简单',
             
             // 完整功能描述（整句翻译）
             'features.smart_scaling_full': '智能图片缩放 - 调整尺寸时保持清晰度',
             'features.format_conversion_full': '格式转换 (JPG/PNG/WEBP) - 支持主流格式',
             'features.image_compression_full': '图片压缩优化 - 减小文件大小同时保持视觉质量',
             'features.batch_processing_full': '批量处理 - 一次处理多张图片，提高效率',
             'features.full_screenshot_full': '全屏截图 - 一键捕获整个屏幕',
             'features.area_screenshot_full': '区域截图 - 自由选择捕获区域',
             'features.window_screenshot_full': '窗口截图 - 精确捕获指定窗口',
             'features.delayed_screenshot_full': '延时截图 - 设置延迟时间，捕获动态内容',
             'features.video_conversion_full': '视频格式转换 - 支持 MP4、AVI、MOV 等主流格式',
             'features.subtitle_editing_full': '字幕编辑制作 - 创建、编辑和同步字幕文件',
             'features.audio_extraction_full': '音频提取 - 从视频中提取高质量音频',
             'features.video_compression_full': '视频压缩 - 减小文件大小同时保持质量',
             'features.no_registration_full': '无需注册登录 - 所有功能免费使用，无隐藏费用',
             'features.cross_platform_full': '跨平台支持 - 支持 Windows、macOS 和 Linux',
             'features.offline_use_full': '完全离线使用 - 完全本地操作，无需网络，保护隐私和安全',
             'features.simple_interface_full': '界面简洁 - 操作简单，适合所有用户',
            
            // 新增功能介绍区域
            'features.core_features_title': '🎯 核心功能详解',
            'features.image_processing_title': '图像处理工具',
            'features.image_processing_desc': '专业的图像处理解决方案，支持多种格式和批量操作',
            'features.screenshot_tools_title': '截图工具集',
            'features.screenshot_tools_desc': '功能强大的截图工具，满足各种截图需求',
            'features.video_processing_title': '视频处理中心',
            'features.video_processing_desc': '全面的视频编辑和处理功能，支持多种格式',
            'features.advantages_title': '使用优势',
            'features.advantages_desc': '为什么选择我们的工具平台',
            'features.learn_more': '了解详情',
            'features.download_now': '立即下载',
            
            // 使用教程区域
            'tutorial.title': '📚 使用教程',
            'tutorial.quick_start': '快速开始',
            'tutorial.quick_start_desc': '了解如何下载和安装我们的工具',
            'tutorial.demo': '功能演示',
            'tutorial.demo_desc': '观看各工具的实际操作演示',
            'tutorial.faq': '常见问题',
            'tutorial.faq_desc': '解答使用过程中的常见问题',
            'tutorial.view_details': '查看详情 →',
            'tutorial.start_demo': '开始演示 →',
            'tutorial.contact_us': '联系我们 →',
            
            // 底部导航
            'footer.quick_links': '快速链接',
            'footer.home': '首页',
            'footer.about': '关于我们',
            'footer.contact': '联系我们',
            'footer.legal': '法律条款',
            'footer.privacy': '隐私政策',
            'footer.terms': '服务条款',
            'footer.copyright': '© 2025 Video Tools Platform. All rights reserved.',
            
            // 下载信息
            'download.windows': '🪟 Windows 版本',
            'download.windows_desc': '支持 Windows 10/11 (64位)',
            'download.windows_btn': '📥 下载 Windows 版 (v1.0.0)',
            'download.no_registration': '💡 无需注册，下载即可使用',
            'download.link_not_ready': '下载链接暂未准备好，请稍后再试',
            
            // 语言
            'language.chinese': '中文',
            'language.english': 'English',
            
            // 模态框
            'modal.cinematic_darken_desc': '专业的电影级视频调暗工具 - Windows 10/11 (64-bit)',
            'modal.download_tip': '💡 无需注册，下载即用 - 智能调节视频亮度，改善画面质量',
        
        // Stats section
        'stats.downloads': '下载次数',
        'stats.tools': '工具数量',
        'stats.updated': '最后更新'
        },
        
        en: {
            // Header
            'header.title': 'Video Tools Platform',
            'header.subtitle': 'Professional Video Processing Tools',
            
            // Main content
            'hero.title': 'Professional Video Processing Tools',
            'hero.subtitle': 'One-stop solution for video editing, subtitle creation, and audio processing',
            
            // Search
            'search.placeholder': '🔍 Search tools...',
            
            // Tools
            'tools.title': 'Tools List',
            'tools.no_results': 'No tools found',
            'tools.no_results_hint': 'Try adjusting search keywords or selecting other categories',
            
            // Categories
            'category.all': '🏠 All Tools',
            'category.subtitle': '🎬 Subtitle Tools',
            'category.video': '🎥 Video Processing',
            'category.audio': '🎵 Audio Processing',
            'category.image': '🖼️ Image Processing',
            
            // Tool status
            'status.stable': '✅ Stable',
            'status.beta': '🧪 Beta',
            'status.alpha': '⚠️ Alpha',
            'status.coming_soon': '🚀 Coming Soon',
            
            // Buttons
            'btn.download': '📥 Download Desktop',
            'btn.details': '📋 Details',
            'btn.coming_soon': '🚀 Coming Soon',
            'btn.unavailable': '📥 Download Unavailable',
            'btn.close': 'Close',
            
            // Tool details
            'details.version': 'Version:',
            'details.size': 'File Size:',
            'details.requirements': 'System Requirements:',
            'details.status': 'Status:',
            'details.description': 'Feature Description',
            'details.features': 'Main Features',
            
            // Modals
            'modal.download_title': '📥 Download Desktop',
            'modal.features_title': '💡 Features',
            
            // Features
            'features.image_processing': '🖼️ Image Processing',
            'features.screenshot': '📸 Screenshot Tools',
            'features.video_processing': '🎬 Video Processing',
            'features.efficient': '⚡ Efficient & Convenient',
            'features.more': 'more',
            
                         // Feature detailed descriptions
             'features.smart_scaling': 'Smart image scaling',
             'features.format_conversion': 'Format conversion (JPG/PNG/WEBP)',
             'features.image_compression': 'Image compression optimization',
             'features.batch_processing': 'Batch processing',
             'features.full_screenshot': 'Full-screen screenshot',
             'features.area_screenshot': 'Area screenshot',
             'features.window_screenshot': 'Window screenshot',
             'features.delayed_screenshot': 'Delayed screenshot',
             'features.video_conversion': 'Video format conversion',
             'features.subtitle_editing': 'Subtitle editing and creation',
             'features.audio_extraction': 'Audio extraction',
             'features.video_compression': 'Video compression',
             'features.no_registration': 'No registration required',
             'features.cross_platform': 'Cross-platform support',
             'features.offline_use': 'Completely offline use',
             'features.simple_interface': 'Simple interface',
             'features.easy_operate': 'Easy to operate',
             
             // Complete feature descriptions (full sentence translation)
             'features.smart_scaling_full': 'Smart image scaling - Keep clarity while adjusting size',
             'features.format_conversion_full': 'Format conversion (JPG/PNG/WEBP) - Support mainstream formats',
             'features.image_compression_full': 'Image compression optimization - Reduce file size while maintaining visual quality',
             'features.batch_processing_full': 'Batch processing - Process multiple images at once, improving efficiency',
             'features.full_screenshot_full': 'Full-screen screenshot - One-click capture of entire screen',
             'features.area_screenshot_full': 'Area screenshot - Freely select capture area',
             'features.window_screenshot_full': 'Window screenshot - Precisely capture specified window',
             'features.delayed_screenshot_full': 'Delayed screenshot - Set delay time, capture dynamic content',
             'features.video_conversion_full': 'Video format conversion - Support MP4, AVI, MOV and other mainstream formats',
             'features.subtitle_editing_full': 'Subtitle editing and creation - Create, edit and sync subtitle files',
             'features.audio_extraction_full': 'Audio extraction - Extract high-quality audio from videos',
             'features.video_compression_full': 'Video compression - Reduce file size while maintaining quality',
             'features.no_registration_full': 'No registration required - All features free to use, no hidden fees',
             'features.cross_platform_full': 'Cross-platform support - Works on Windows, macOS, and Linux',
             'features.offline_use_full': 'Offline use - Completely local operation, no internet required, protecting privacy and security',
             'features.simple_interface_full': 'Simple interface - Easy operation, suitable for all users',
            
            // New features introduction section
            'features.core_features_title': '🎯 Core Features Details',
            'features.image_processing_title': 'Image Processing Tools',
            'features.image_processing_desc': 'Professional image processing solutions supporting multiple formats and batch operations',
            'features.screenshot_tools_title': 'Screenshot Tools',
            'features.screenshot_tools_desc': 'Powerful screenshot tools for various capture needs',
            'features.video_processing_title': 'Video Processing Center',
            'features.video_processing_desc': 'Comprehensive video editing and processing features supporting multiple formats',
            'features.advantages_title': 'Why Choose Us',
            'features.advantages_desc': 'Why choose our tools platform',
            'features.learn_more': 'Learn More',
            'features.download_now': 'Download Now',
            
            // Tutorial section
            'tutorial.title': '📚 User Guide',
            'tutorial.quick_start': 'Quick Start',
            'tutorial.quick_start_desc': 'Learn how to download and install our tools',
            'tutorial.demo': 'Feature Demo',
            'tutorial.demo_desc': 'Watch actual operation demos of various tools',
            'tutorial.faq': 'FAQ',
            'tutorial.faq_desc': 'Answer common questions during use',
            'tutorial.view_details': 'View Details →',
            'tutorial.start_demo': 'Start Demo →',
            'tutorial.contact_us': 'Contact Us →',
            
            // Footer navigation
            'footer.quick_links': 'Quick Links',
            'footer.home': 'Home',
            'footer.about': 'About Us',
            'footer.contact': 'Contact',
            'footer.legal': 'Legal',
            'footer.privacy': 'Privacy Policy',
            'footer.terms': 'Terms of Service',
            'footer.copyright': '© 2025 Video Tools Platform. All rights reserved.',
            
            // Download info
            'download.windows': '🪟 Windows Version',
            'download.windows_desc': 'Supports Windows 10/11 (64-bit)',
            'download.windows_btn': '📥 Download Windows (v1.0.0)',
            'download.no_registration': '💡 No registration required, download and use immediately',
            'download.link_not_ready': 'Download link not ready yet, please try again later',
            
            // Language
            'language.chinese': '中文',
            'language.english': 'English',
            
            // Modal
            'modal.cinematic_darken_desc': 'Professional cinematic video darkening tool - Windows 10/11 (64-bit)',
            'modal.download_tip': '💡 No registration required, download and use - Smart video brightness adjustment, improve picture quality',
        
        // Stats section
        'stats.downloads': 'Downloads',
        'stats.tools': 'Tools',
        'stats.updated': 'Updated'
        }
    },
    
    // 初始化
    init() {
        // 从localStorage获取保存的语言设置
        const savedLang = localStorage.getItem('preferred_language');
        if (savedLang && this.languages[savedLang]) {
            this.currentLang = savedLang;
        }
        
        // 应用语言
        this.applyLanguage(this.currentLang);
        
        // 更新语言按钮状态
        this.updateLanguageButtons();
    },
    
    // 切换语言
    switchLanguage(lang) {
        if (this.languages[lang]) {
            this.currentLang = lang;
            localStorage.setItem('preferred_language', lang);
            this.applyLanguage(lang);
            this.updateLanguageButtons();
        }
    },
    
    // 应用语言
    applyLanguage(lang) {
        const translations = this.translations[lang];
        if (!translations) return;
        
        // 更新所有带有 data-i18n 属性的元素
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[key]) {
                element.textContent = translations[key];
            }
        });
        
        // 更新所有带有 data-i18n-placeholder 属性的元素
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            if (translations[key]) {
                element.placeholder = translations[key];
            }
        });
        
        // 重新渲染工具列表（如果工具展示系统已初始化）
        if (window.toolsDisplay) {
            window.toolsDisplay.renderCategories();
            window.toolsDisplay.renderTools();
        }
    },
    
    // 更新语言按钮状态
    updateLanguageButtons() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-lang') === this.currentLang) {
                btn.classList.add('active');
            }
        });
    },
    
    // 获取翻译文本
    t(key) {
        const translations = this.translations[this.currentLang];
        return translations ? translations[key] || key : key;
    }
};

// 全局语言切换函数
window.switchLanguage = function(lang) {
    window.I18N.switchLanguage(lang);
};

// 页面加载完成后初始化国际化
document.addEventListener('DOMContentLoaded', () => {
    window.I18N.init();
});
