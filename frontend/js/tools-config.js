// 工具配置文件 - 集中管理所有工具信息
window.TOOLS_CONFIG = {
    // 工具分类
    categories: [
        {
            id: 'subtitle',
            name: '字幕工具',
            icon: '🎬',
            description: '专业的字幕制作和编辑工具'
        },
        {
            id: 'video',
            name: '视频处理',
            icon: '🎥',
            description: '视频格式转换和编辑工具'
        },
        {
            id: 'audio',
            name: '音频处理',
            icon: '🎵',
            description: '音频提取和编辑工具'
        },
        {
            id: 'image',
            name: '图片处理',
            icon: '🖼️',
            description: '图片格式转换和编辑工具'
        }
    ],
    
    // 工具列表
    tools: [
        {
            id: 'manual-subtitle-editor',
            name: {
                zh: '手动上字幕改版新版本',
                en: 'Manual Subtitle Editor'
            },
            category: 'subtitle',
            icon: '🎬',
            description: {
                zh: '专业的字幕制作工具，支持音频同步、时间轴编辑、多格式导出',
                en: 'Professional subtitle creation tool with audio sync, timeline editing, and multi-format export'
            },
            version: 'v1.0.0',
            downloadUrl: 'https://github.com/xiexin0516-collab/video-tools/releases/download/v1.0.0/ManualSubtitleEditor-v1.0.0.zip',
            features: {
                zh: [
                    '基于时间轴编辑',
                    '音频同步播放',
                    '智能吸附功能',
                    '多语言支持',
                    '工程文件保存'
                ],
                en: [
                    'Timeline-based editing',
                    'Audio synchronization',
                    'Smart snap function',
                    'Multi-language support',
                    'Project file saving'
                ]
            },
            systemRequirements: {
                zh: 'Windows 10/11 (64位)',
                en: 'Windows 10/11 (64-bit)'
            },
            fileSize: '38MB',
            status: 'stable' // stable, beta, alpha
        },
        {
            id: 'audio-extractor',
            name: '音频提取器',
            category: 'audio',
            icon: '🎵',
            description: '从视频中提取高质量音频，支持多种格式转换',
            version: 'v1.0.0',
            downloadUrl: '#',
            features: [
                '多格式支持',
                '高质量提取',
                '批量处理',
                '格式转换'
            ],
            systemRequirements: 'Windows 10/11 (64位)',
            fileSize: '25MB',
            status: 'coming-soon'
        },
        {
            id: 'video-light-adjuster',
            name: '视频光线调节',
            category: 'video',
            icon: '💡',
            description: '智能调节视频亮度、对比度，改善画面质量',
            version: 'v1.0.0',
            downloadUrl: '#',
            features: [
                '智能亮度调节',
                '对比度优化',
                '批量处理',
                '实时预览'
            ],
            systemRequirements: 'Windows 10/11 (64位)',
            fileSize: '30MB',
            status: 'coming-soon'
        },
        {
            id: 'background-music-generator',
            name: '背景音乐生成',
            category: 'audio',
            icon: '🎼',
            description: 'AI智能生成背景音乐，完美匹配视频内容',
            version: 'v1.0.0',
            downloadUrl: '#',
            features: [
                'AI智能生成',
                '风格匹配',
                '时长调节',
                '版权免费'
            ],
            systemRequirements: 'Windows 10/11 (64位)',
            fileSize: '45MB',
            status: 'coming-soon'
        },
        {
            id: 'video-effects',
            name: '视频特效',
            category: 'video',
            icon: '✨',
            description: '丰富的视频特效库，让您的视频更加精彩',
            version: 'v1.0.0',
            downloadUrl: '#',
            features: [
                '特效库',
                '实时预览',
                '参数调节',
                '批量应用'
            ],
            systemRequirements: 'Windows 10/11 (64位)',
            fileSize: '50MB',
            status: 'coming-soon'
        },
        {
            id: 'format-converter',
            name: '格式转换',
            category: 'video',
            icon: '🔄',
            description: '支持多种视频格式转换，适配不同平台需求',
            version: 'v1.0.0',
            downloadUrl: '#',
            features: [
                '多格式支持',
                '批量转换',
                '质量调节',
                '快速转换'
            ],
            systemRequirements: 'Windows 10/11 (64位)',
            fileSize: '35MB',
            status: 'coming-soon'
        }
    ]
};

// 工具管理类
class ToolsManager {
    constructor() {
        this.tools = window.TOOLS_CONFIG.tools;
        this.categories = window.TOOLS_CONFIG.categories;
    }
    
    // 获取所有工具
    getAllTools() {
        return this.tools;
    }
    
    // 按分类获取工具
    getToolsByCategory(categoryId) {
        return this.tools.filter(tool => tool.category === categoryId);
    }
    
    // 获取稳定版本的工具
    getStableTools() {
        return this.tools.filter(tool => tool.status === 'stable');
    }
    
    // 获取即将推出的工具
    getComingSoonTools() {
        return this.tools.filter(tool => tool.status === 'coming-soon');
    }
    
    // 搜索工具
    searchTools(keyword) {
        const lowerKeyword = keyword.toLowerCase();
        return this.tools.filter(tool => 
            tool.name.toLowerCase().includes(lowerKeyword) ||
            tool.description.toLowerCase().includes(lowerKeyword)
        );
    }
    
    // 获取工具详情
    getToolById(toolId) {
        return this.tools.find(tool => tool.id === toolId);
    }
    
    // 获取分类信息
    getCategoryById(categoryId) {
        return this.categories.find(category => category.id === categoryId);
    }
}

// 创建全局工具管理器实例
window.toolsManager = new ToolsManager();
