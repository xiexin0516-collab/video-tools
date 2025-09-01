// 动态工具展示系统
class ToolsDisplay {
    constructor() {
        this.currentCategory = 'all';
        this.searchKeyword = '';
        this.init();
    }
    
    init() {
        this.renderCategories();
        this.renderTools();
        this.bindEvents();
    }
    
    // 渲染分类标签
    renderCategories() {
        const categoriesContainer = document.getElementById('categories-tabs');
        if (!categoriesContainer) return;
        
        const categories = window.toolsManager.categories;
        let html = `
            <button class="category-tab active" data-category="all">
                🏠 全部工具
            </button>
        `;
        
        categories.forEach(category => {
            html += `
                <button class="category-tab" data-category="${category.id}">
                    ${category.icon} ${category.name}
                </button>
            `;
        });
        
        categoriesContainer.innerHTML = html;
    }
    
    // 渲染工具列表
    renderTools() {
        const toolsContainer = document.getElementById('tools-grid');
        if (!toolsContainer) return;
        
        let tools = [];
        
        // 根据当前分类和搜索关键词筛选工具
        if (this.currentCategory === 'all') {
            tools = window.toolsManager.getAllTools();
        } else {
            tools = window.toolsManager.getToolsByCategory(this.currentCategory);
        }
        
        if (this.searchKeyword) {
            tools = window.toolsManager.searchTools(this.searchKeyword);
        }
        
        let html = '';
        
        tools.forEach(tool => {
            const statusBadge = this.getStatusBadge(tool.status);
            const downloadButton = this.getDownloadButton(tool);
            
            html += `
                <div class="tool-card" data-tool-id="${tool.id}">
                    <div class="tool-header">
                        <div class="tool-icon">${tool.icon}</div>
                        <div class="tool-info">
                            <h4 class="tool-name">${tool.name}</h4>
                            <div class="tool-meta">
                                <span class="tool-version">${tool.version}</span>
                                <span class="tool-size">${tool.fileSize}</span>
                                ${statusBadge}
                            </div>
                        </div>
                    </div>
                    
                    <p class="tool-description">${tool.description}</p>
                    
                    <div class="tool-features">
                        ${tool.features.slice(0, 3).map(feature => 
                            `<span class="feature-tag">${feature}</span>`
                        ).join('')}
                        ${tool.features.length > 3 ? 
                            `<span class="feature-more">+${tool.features.length - 3} 更多</span>` : 
                            ''
                        }
                    </div>
                    
                    <div class="tool-actions">
                        ${downloadButton}
                        <button class="btn-secondary tool-details" onclick="showToolDetails('${tool.id}')">
                            📋 详情
                        </button>
                    </div>
                </div>
            `;
        });
        
        if (tools.length === 0) {
            html = `
                <div class="no-tools">
                    <div class="no-tools-icon">🔍</div>
                    <h3>没有找到相关工具</h3>
                    <p>尝试调整搜索关键词或选择其他分类</p>
                </div>
            `;
        }
        
        toolsContainer.innerHTML = html;
    }
    
    // 获取状态徽章
    getStatusBadge(status) {
        const badges = {
            'stable': '<span class="status-badge stable">✅ 稳定版</span>',
            'beta': '<span class="status-badge beta">🧪 测试版</span>',
            'alpha': '<span class="status-badge alpha">⚠️ 预览版</span>',
            'coming-soon': '<span class="status-badge coming-soon">🚀 即将推出</span>'
        };
        return badges[status] || '';
    }
    
    // 获取下载按钮
    getDownloadButton(tool) {
        if (tool.status === 'coming-soon') {
            return `
                <button class="btn-secondary coming-soon-btn" disabled>
                    🚀 即将推出
                </button>
            `;
        }
        
        if (tool.downloadUrl && tool.downloadUrl !== '#') {
            return `
                <button class="btn-primary download-btn" onclick="downloadTool('${tool.id}')">
                    📥 下载桌面版
                </button>
            `;
        }
        
        return `
            <button class="btn-secondary" disabled>
                📥 下载暂不可用
            </button>
        `;
    }
    
    // 绑定事件
    bindEvents() {
        // 分类切换
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('category-tab')) {
                this.switchCategory(e.target.dataset.category);
            }
        });
        
        // 搜索功能
        const searchInput = document.getElementById('search-tools');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchKeyword = e.target.value;
                this.renderTools();
            });
        }
    }
    
    // 切换分类
    switchCategory(categoryId) {
        this.currentCategory = categoryId;
        this.searchKeyword = '';
        
        // 更新分类标签状态
        document.querySelectorAll('.category-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-category="${categoryId}"]`).classList.add('active');
        
        // 清空搜索框
        const searchInput = document.getElementById('search-tools');
        if (searchInput) {
            searchInput.value = '';
        }
        
        this.renderTools();
    }
    
    // 搜索工具
    searchTools(keyword) {
        this.searchKeyword = keyword;
        this.renderTools();
    }
}

// 工具详情模态框
function showToolDetails(toolId) {
    const tool = window.toolsManager.getToolById(toolId);
    if (!tool) return;
    
    const modal = document.getElementById('toolDetailsModal');
    if (!modal) return;
    
    const statusBadge = window.toolsDisplay.getStatusBadge(tool.status);
    const downloadButton = window.toolsDisplay.getDownloadButton(tool);
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${tool.icon} ${tool.name}</h3>
                <button class="close-btn" onclick="closeToolDetails()">×</button>
            </div>
            
            <div class="modal-body">
                <div class="tool-meta-info">
                    <div class="meta-item">
                        <span class="meta-label">版本:</span>
                        <span class="meta-value">${tool.version}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">文件大小:</span>
                        <span class="meta-value">${tool.fileSize}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">系统要求:</span>
                        <span class="meta-value">${tool.systemRequirements}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">状态:</span>
                        <span class="meta-value">${statusBadge}</span>
                    </div>
                </div>
                
                <div class="tool-description-full">
                    <h4>功能描述</h4>
                    <p>${tool.description}</p>
                </div>
                
                <div class="tool-features-full">
                    <h4>主要功能</h4>
                    <div class="features-list">
                        ${tool.features.map(feature => 
                            `<div class="feature-item">• ${feature}</div>`
                        ).join('')}
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                ${downloadButton}
                <button class="btn-secondary" onclick="closeToolDetails()">关闭</button>
            </div>
        </div>
    `;
    
    modal.classList.remove('hidden');
}

// 关闭工具详情
function closeToolDetails() {
    const modal = document.getElementById('toolDetailsModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// 下载工具
function downloadTool(toolId) {
    const tool = window.toolsManager.getToolById(toolId);
    if (!tool || !tool.downloadUrl || tool.downloadUrl === '#') {
        alert('下载链接暂不可用');
        return;
    }
    
    window.open(tool.downloadUrl, '_blank');
}

// 初始化工具展示系统
document.addEventListener('DOMContentLoaded', () => {
    window.toolsDisplay = new ToolsDisplay();
});
