/**
 * API客户端 - 处理与后端的通信
 */

class API {
    constructor() {
        this.baseURL = window.location.origin;
        this.apiURL = `${this.baseURL}/api`;
    }

    // 获取认证头
    getAuthHeaders() {
        const token = localStorage.getItem('supabase.auth.token');
        if (token) {
            const parsedToken = JSON.parse(token);
            return {
                'Authorization': `Bearer ${parsedToken.access_token}`,
                'Content-Type': 'application/json'
            };
        }
        return {
            'Content-Type': 'application/json'
        };
    }

    // 通用请求方法
    async request(endpoint, options = {}) {
        const url = `${this.apiURL}${endpoint}`;
        const config = {
            headers: this.getAuthHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }

    // 健康检查
    async healthCheck() {
        return this.request('/health');
    }

    // 用户相关API
    async getUserProfile() {
        return this.request('/auth/profile');
    }

    // 项目管理API
    async getProjects() {
        return this.request('/projects');
    }

    async createProject(projectData) {
        return this.request('/projects', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
    }

    async getProject(projectId) {
        return this.request(`/projects/${projectId}`);
    }

    async updateProject(projectId, projectData) {
        return this.request(`/projects/${projectId}`, {
            method: 'PUT',
            body: JSON.stringify(projectData)
        });
    }

    async deleteProject(projectId) {
        return this.request(`/projects/${projectId}`, {
            method: 'DELETE'
        });
    }

    // 文件上传API
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const url = `${this.apiURL}/upload`;
        const config = {
            method: 'POST',
            headers: {
                'Authorization': this.getAuthHeaders().Authorization
            },
            body: formData
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('文件上传失败:', error);
            throw error;
        }
    }

    // 字幕处理API
    async generateSubtitles(audioFile) {
        return this.request('/subtitles/generate', {
            method: 'POST',
            body: JSON.stringify({ audio_file: audioFile })
        });
    }

    async exportSubtitles(subtitles, format = 'srt') {
        return this.request('/subtitles/export', {
            method: 'POST',
            body: JSON.stringify({ subtitles, format })
        });
    }

    // 下载文件
    downloadFile(content, filename, mimeType = 'text/plain') {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// 创建全局API实例
window.api = new API();

// 导出API类（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
