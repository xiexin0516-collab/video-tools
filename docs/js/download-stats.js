/**
 * 下载统计管理
 * 用于跟踪和显示 vidtools.tools 的下载次数
 */

class DownloadStats {
    constructor() {
        this.stats = {
            totalDownloads: 0,
            lastUpdated: null,
            downloadHistory: []
        };
        this.init();
    }

    // 初始化
    init() {
        this.loadLocalStats();
        this.updateDisplay();
        this.fetchGitHubStats();
        
        // 每5分钟更新一次统计
        setInterval(() => {
            this.fetchGitHubStats();
        }, 5 * 60 * 1000);
    }

    // 加载本地统计
    loadLocalStats() {
        try {
            const saved = localStorage.getItem('vidtools_download_stats');
            if (saved) {
                this.stats = { ...this.stats, ...JSON.parse(saved) };
            }
        } catch (error) {
            console.error('加载本地统计失败:', error);
        }
    }

    // 保存本地统计
    saveLocalStats() {
        try {
            localStorage.setItem('vidtools_download_stats', JSON.stringify(this.stats));
        } catch (error) {
            console.error('保存本地统计失败:', error);
        }
    }

    // 从GitHub API获取下载统计
    async fetchGitHubStats() {
        try {
            // GitHub API endpoint for releases
            const apiUrl = 'https://api.github.com/repos/xiexin0516-collab/video-tools/releases';
            const response = await fetch(apiUrl);
            
            if (!response.ok) {
                throw new Error(`GitHub API 请求失败: ${response.status}`);
            }

            const releases = await response.json();
            let totalDownloads = 0;

            // 计算所有版本的下载总数
            releases.forEach(release => {
                if (release.assets && release.assets.length > 0) {
                    release.assets.forEach(asset => {
                        totalDownloads += asset.download_count || 0;
                    });
                }
            });

            // 更新统计
            this.stats.totalDownloads = totalDownloads;
            this.stats.lastUpdated = new Date().toISOString();
            this.saveLocalStats();
            this.updateDisplay();

            console.log(`GitHub 下载统计更新: ${totalDownloads} 次下载`);
        } catch (error) {
            console.error('获取GitHub统计失败:', error);
            // 如果GitHub API失败，使用本地统计
            this.updateDisplay();
        }
    }

    // 记录本地下载事件
    recordLocalDownload(toolName, platform) {
        const downloadEvent = {
            tool: toolName,
            platform: platform,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent
        };

        this.stats.downloadHistory.push(downloadEvent);
        
        // 只保留最近1000条记录
        if (this.stats.downloadHistory.length > 1000) {
            this.stats.downloadHistory = this.stats.downloadHistory.slice(-1000);
        }

        this.stats.totalDownloads++;
        this.saveLocalStats();
        this.updateDisplay();

        // 发送到Google Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'download', {
                'event_category': 'software_download',
                'event_label': toolName,
                'custom_parameter_1': platform,
                'custom_parameter_2': toolName
            });
        }

        console.log(`本地下载记录: ${toolName} - ${platform}`);
    }

    // 更新显示
    updateDisplay() {
        // 更新下载计数
        const countElement = document.getElementById('downloadCount');
        if (countElement) {
            const formattedCount = this.formatNumber(this.stats.totalDownloads);
            countElement.textContent = formattedCount;
            
            // 添加动画效果
            countElement.classList.add('animate-pulse');
            setTimeout(() => {
                countElement.classList.remove('animate-pulse');
            }, 1000);
        }

        // 更新工具数量
        const toolsCountElement = document.getElementById('toolsCount');
        if (toolsCountElement) {
            toolsCountElement.textContent = this.getToolsCount();
        }

        // 更新最后更新时间
        const lastUpdatedElement = document.getElementById('lastUpdated');
        if (lastUpdatedElement) {
            lastUpdatedElement.textContent = this.formatLastUpdated();
        }
    }

    // 格式化数字显示
    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    // 获取统计摘要
    getStatsSummary() {
        return {
            totalDownloads: this.stats.totalDownloads,
            lastUpdated: this.stats.lastUpdated,
            recentDownloads: this.stats.downloadHistory.slice(-10),
            platformStats: this.getPlatformStats()
        };
    }

    // 获取平台统计
    getPlatformStats() {
        const platformCounts = {};
        this.stats.downloadHistory.forEach(event => {
            platformCounts[event.platform] = (platformCounts[event.platform] || 0) + 1;
        });
        return platformCounts;
    }

    // 获取工具数量
    getToolsCount() {
        // 从工具配置中获取工具数量
        if (window.TOOLS_CONFIG && window.TOOLS_CONFIG.tools) {
            return window.TOOLS_CONFIG.tools.length;
        }
        return 6; // 默认值
    }

    // 格式化最后更新时间
    formatLastUpdated() {
        if (!this.stats.lastUpdated) return 'Today';
        
        const lastUpdate = new Date(this.stats.lastUpdated);
        const now = new Date();
        const diffTime = Math.abs(now - lastUpdate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) return 'Today';
        if (diffDays === 2) return 'Yesterday';
        if (diffDays <= 7) return `${diffDays - 1} days ago`;
        if (diffDays <= 30) return `${Math.floor(diffDays / 7)} weeks ago`;
        return `${Math.floor(diffDays / 30)} months ago`;
    }
}

// 全局下载统计实例
window.downloadStats = new DownloadStats();

// 导出下载统计函数供其他脚本使用
window.recordDownload = function(toolName, platform) {
    if (window.downloadStats) {
        window.downloadStats.recordLocalDownload(toolName, platform);
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 确保下载统计已初始化
    if (!window.downloadStats) {
        window.downloadStats = new DownloadStats();
    }
});
