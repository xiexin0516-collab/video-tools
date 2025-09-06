// 工具配置文件 - 集中管理所有工具信息
window.TOOLS_CONFIG = {
    // 工具分类
    categories: [
        {
            id: 'subtitle',
            name: {
                zh: '字幕工具',
                en: 'Subtitle Tools'
            },
            icon: '🎬',
            description: {
                zh: '专业的字幕制作和编辑工具',
                en: 'Professional subtitle creation and editing tools'
            }
        },
        {
            id: 'video',
            name: {
                zh: '视频处理',
                en: 'Video Processing'
            },
            icon: '🎥',
            description: {
                zh: '视频格式转换和编辑工具',
                en: 'Video format conversion and editing tools'
            }
        },
        {
            id: 'audio',
            name: {
                zh: '音频处理',
                en: 'Audio Processing'
            },
            icon: '🎵',
            description: {
                zh: '音频提取和编辑工具',
                en: 'Audio extraction and editing tools'
            }
        },
        {
            id: 'image',
            name: {
                zh: '图片处理',
                en: 'Image Processing'
            },
            icon: '🖼️',
            description: {
                zh: '图片格式转换和编辑工具',
                en: 'Image format conversion and editing tools'
            }
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
            name: {
                zh: '音频提取器',
                en: 'Audio Extractor'
            },
            category: 'audio',
            icon: '🎵',
            description: {
                zh: '从视频中提取高质量音频，支持多种格式转换',
                en: 'Extract high-quality audio from videos with multi-format conversion support'
            },
            version: 'v1.0.0',
            downloadUrl: '#',
            features: {
                zh: [
                    '多格式支持',
                    '高质量提取',
                    '批量处理',
                    '格式转换'
                ],
                en: [
                    'Multi-format support',
                    'High-quality extraction',
                    'Batch processing',
                    'Format conversion'
                ]
            },
            systemRequirements: {
                zh: 'Windows 10/11 (64位)',
                en: 'Windows 10/11 (64-bit)'
            },
            fileSize: '25MB',
            status: 'coming-soon'
        },
        {
            id: 'cinematic-darken',
            name: {
                zh: '电影级调暗工具',
                en: 'Cinematic Darken Tool'
            },
            category: 'video',
            icon: '🎬',
            description: {
                zh: '专业的电影级视频调暗工具，智能调节亮度，改善画面质量',
                en: 'Professional cinematic video darkening tool with intelligent brightness adjustment'
            },
            version: 'v1.1.1',
            downloadUrl: 'https://github.com/xiexin0516-collab/video-tools/releases/download/v1.1.1/CinematicDarken-v1.1.1.zip',
            features: {
                zh: [
                    '电影级调暗',
                    '智能亮度调节',
                    '多格式支持',
                    '实时预览'
                ],
                en: [
                    'Cinematic darkening',
                    'Smart brightness adjustment',
                    'Multi-format support',
                    'Real-time preview'
                ]
            },
            systemRequirements: {
                zh: 'Windows 10/11 (64位)',
                en: 'Windows 10/11 (64-bit)'
            },
            fileSize: '30MB',
            status: 'stable'
        },
        {
            id: 'background-music-generator',
            name: {
                zh: '背景音乐生成',
                en: 'Background Music Generator'
            },
            category: 'audio',
            icon: '🎼',
            description: {
                zh: 'AI智能生成背景音乐，完美匹配视频内容',
                en: 'AI-powered background music generation that perfectly matches video content'
            },
            version: 'v1.0.0',
            downloadUrl: '#',
            features: {
                zh: [
                    'AI智能生成',
                    '风格匹配',
                    '时长调节',
                    '版权免费'
                ],
                en: [
                    'AI-powered generation',
                    'Style matching',
                    'Duration adjustment',
                    'Copyright free'
                ]
            },
            systemRequirements: {
                zh: 'Windows 10/11 (64位)',
                en: 'Windows 10/11 (64-bit)'
            },
            fileSize: '45MB',
            status: 'coming-soon'
        },
        {
            id: 'cinematic-photo-fx',
            name: {
                zh: '电影级图片特效',
                en: 'Cinematic Photo FX'
            },
            category: 'image',
            icon: '🎬',
            description: {
                zh: '专业的电影级图片特效工具，将静态图片转换为动态视频，支持多种电影级特效',
                en: 'Professional cinematic photo effects tool that converts static images to dynamic videos with multiple cinematic effects'
            },
            version: 'v1.1.2',
            downloadUrl: 'https://github.com/xiexin0516-collab/video-tools/releases/download/v1.1.2/CinematicPhotoFX-v1.1.2.zip',
            features: {
                zh: [
                    '14种电影级特效',
                    '推拉镜头效果',
                    '移动旋转效果',
                    '滤镜特效',
                    '淡入淡出过渡',
                    '批量处理'
                ],
                en: [
                    '14 cinematic effects',
                    'Zoom in/out effects',
                    'Pan and rotation effects',
                    'Filter effects',
                    'Fade transitions',
                    'Batch processing'
                ]
            },
            systemRequirements: {
                zh: 'Windows 10/11 (64位)',
                en: 'Windows 10/11 (64-bit)'
            },
            fileSize: '35MB',
            status: 'stable'
        },
        {
            id: 'format-converter',
            name: {
                zh: '视频格式转换器',
                en: 'Video Format Converter'
            },
            category: 'video',
            icon: '🔄',
            description: {
                zh: '专业的视频格式转换工具，支持多种格式、参数调节和批量转换',
                en: 'Professional video format conversion tool with multi-format support, parameter adjustment and batch conversion'
            },
            version: 'v1.1.0',
            downloadUrl: 'https://github.com/xiexin0516-collab/video-tools/releases/download/v1.1.0/FormatConverter-v1.1.0.zip',
            features: {
                zh: [
                    '多格式支持',
                    '参数可调节',
                    '批量转换',
                    '多语言界面',
                    '智能预设'
                ],
                en: [
                    'Multi-format support',
                    'Adjustable parameters',
                    'Batch conversion',
                    'Multi-language interface',
                    'Smart presets'
                ]
            },
            systemRequirements: {
                zh: 'Windows 10/11 (64位)',
                en: 'Windows 10/11 (64-bit)'
            },
            fileSize: '25MB',
            status: 'stable'
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
        return this.tools.filter(tool => {
            const name = typeof tool.name === 'string' ? tool.name : tool.name.zh;
            const description = typeof tool.description === 'string' ? tool.description : tool.description.zh;
            return name.toLowerCase().includes(lowerKeyword) ||
                   description.toLowerCase().includes(lowerKeyword);
        });
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
