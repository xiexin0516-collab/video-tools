// 国际化配置
window.I18N = {
    // 当前语言
    currentLang: 'zh',
    
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
            
            // 下载信息
            'download.windows': '🪟 Windows 版本',
            'download.windows_desc': '支持 Windows 10/11 (64位)',
            'download.windows_btn': '📥 下载 Windows 版 (v1.0.0)',
            'download.no_registration': '💡 无需注册，下载即可使用'
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
            
            // Download info
            'download.windows': '🪟 Windows Version',
            'download.windows_desc': 'Supports Windows 10/11 (64-bit)',
            'download.windows_btn': '📥 Download Windows (v1.0.0)',
            'download.no_registration': '💡 No registration required, download and use immediately'
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
