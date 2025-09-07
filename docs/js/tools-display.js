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
        this.updateToolsCount();
        this.bindEvents();
    }
    
    // 渲染分类标签
    renderCategories() {
        const categoriesContainer = document.getElementById('categories-tabs');
        if (!categoriesContainer) return;
        
        const categories = window.toolsManager.categories;
        const currentLang = window.I18N ? window.I18N.currentLang : 'zh';
        
        let html = `
            <button class="category-tab active" data-category="all">
                ${window.I18N ? window.I18N.t('category.all') : '🏠 全部工具'}
            </button>
        `;
        
        categories.forEach(category => {
            const categoryName = category.name[currentLang] || category.name;
            html += `
                <button class="category-tab" data-category="${category.id}">
                    ${category.icon} ${categoryName}
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
            const currentLang = window.I18N ? window.I18N.currentLang : 'zh';
            
            // 获取多语言内容
            const toolName = typeof tool.name === 'object' ? tool.name[currentLang] || tool.name : tool.name;
            const toolDescription = typeof tool.description === 'object' ? tool.description[currentLang] || tool.description : tool.description;
            const toolFeatures = typeof tool.features === 'object' ? tool.features[currentLang] || tool.features : tool.features;
            const toolRequirements = typeof tool.systemRequirements === 'object' ? tool.systemRequirements[currentLang] || tool.systemRequirements : tool.systemRequirements;
            
            html += `
                <div class="tool-card" data-tool-id="${tool.id}">
                    <div class="tool-header">
                        <div class="tool-icon">${tool.icon}</div>
                        <div class="tool-info">
                            <h4 class="tool-name">${toolName}</h4>
                            <div class="tool-meta">
                                <span class="tool-version">${tool.version}</span>
                                <span class="tool-size">${tool.fileSize}</span>
                                ${statusBadge}
                            </div>
                        </div>
                    </div>
                    
                    <p class="tool-description">${toolDescription}</p>
                    
                    <div class="tool-features">
                        ${toolFeatures.slice(0, 3).map(feature => 
                            `<span class="feature-tag">${feature}</span>`
                        ).join('')}
                        ${toolFeatures.length > 3 ? 
                            `<span class="feature-more">+${toolFeatures.length - 3} ${window.I18N ? window.I18N.t('features.more') : 'more'}</span>` : 
                            ''
                        }
                    </div>
                    
                    <div class="tool-actions">
                        ${downloadButton}
                        <button class="btn-secondary tool-details" onclick="showToolDetails('${tool.id}')">
                            ${window.I18N ? window.I18N.t('btn.details') : '📋 详情'}
                        </button>
                    </div>
                </div>
            `;
        });
        
        if (tools.length === 0) {
            const t = (k) => window.I18N ? window.I18N.t(k) : k;
            html = `
                <div class="no-tools">
                    <div class="no-tools-icon">🔍</div>
                    <h3>${t('tools.no_results')}</h3>
                    <p>${t('tools.no_results_hint')}</p>
                </div>
            `;
        }
        
        toolsContainer.innerHTML = html;
    }
    
    // 获取状态徽章
    getStatusBadge(status) {
        const t = (k) => window.I18N ? window.I18N.t(k) : k;
        const badges = {
            'stable': `<span class="status-badge stable">${t('status.stable')}</span>`,
            'beta': `<span class="status-badge beta">${t('status.beta')}</span>`,
            'alpha': `<span class="status-badge alpha">${t('status.alpha')}</span>`,
            'coming-soon': `<span class="status-badge coming-soon">${t('status.coming_soon')}</span>`
        };
        return badges[status] || '';
    }
    
    // 获取下载按钮
    getDownloadButton(tool) {
        const t = (k) => window.I18N ? window.I18N.t(k) : k;
        if (tool.status === 'coming-soon') {
            return `
                <button class="btn-secondary coming-soon-btn" disabled>
                    ${t('btn.coming_soon')}
                </button>
            `;
        }
        
        if (tool.downloadUrl && tool.downloadUrl !== '#') {
            return `
                <button class="btn-primary download-btn" onclick="downloadTool('${tool.id}')">
                    ${t('btn.download')}
                </button>
            `;
        }
        
        return `
            <button class="btn-secondary" disabled>
                ${t('btn.unavailable')}
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
    
    // 更新工具数量统计
    updateToolsCount() {
        const toolsCountElement = document.getElementById('toolsCount');
        if (toolsCountElement && window.toolsManager) {
            const stableToolsCount = window.toolsManager.getStableTools().length;
            toolsCountElement.textContent = stableToolsCount;
        }
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
    
    const currentLang = window.I18N ? window.I18N.currentLang : 'zh';
    const toolName = typeof tool.name === 'object' ? tool.name[currentLang] || tool.name : tool.name;
    const toolDescription = typeof tool.description === 'object' ? tool.description[currentLang] || tool.description : tool.description;
    const toolFeatures = typeof tool.features === 'object' ? tool.features[currentLang] || tool.features : tool.features;
    const toolRequirements = typeof tool.systemRequirements === 'object' ? tool.systemRequirements[currentLang] || tool.systemRequirements : tool.systemRequirements;
    
    const t = (k) => window.I18N ? window.I18N.t(k) : k;
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${tool.icon} ${toolName}</h3>
                <button class="close-btn" onclick="closeToolDetails()">×</button>
            </div>
            
            <div class="modal-body">
                <div class="tool-meta-info">
                    <div class="meta-item">
                        <span class="meta-label">${t('details.version')}</span>
                        <span class="meta-value">${tool.version}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">${t('details.size')}</span>
                        <span class="meta-value">${tool.fileSize}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">${t('details.requirements')}</span>
                        <span class="meta-value">${toolRequirements}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">${t('details.status')}</span>
                        <span class="meta-value">${statusBadge}</span>
                    </div>
                </div>
                
                <div class="tool-description-full">
                    <h4>${t('details.description')}</h4>
                    <p>${toolDescription}</p>
                </div>
                
                <div class="tool-features-full">
                    <h4>${t('details.features')}</h4>
                    <div class="features-list">
                        ${toolFeatures.map(feature => 
                            `<div class="feature-item">• ${feature}</div>`
                        ).join('')}
                    </div>
                </div>
            </div>
            
            <div class="modal-footer">
                ${downloadButton}
                <button class="btn-secondary" onclick="closeToolDetails()">${t('btn.close')}</button>
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
        const t = (k) => window.I18N ? window.I18N.t(k) : k;
        alert(t('btn.unavailable'));
        return;
    }
    
    window.open(tool.downloadUrl, '_blank');
}

// 初始化工具展示系统
document.addEventListener('DOMContentLoaded', () => {
    window.toolsDisplay = new ToolsDisplay();
});
