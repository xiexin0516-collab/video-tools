// 项目管理系统 - 对应桌面版项目保存/加载
class ProjectManager {
    constructor() {
        this.currentProject = new ProjectData();
        this.projectHistory = [];
        this.maxHistorySize = 10;
        
        // 事件回调
        this.onProjectSaved = null;
        this.onProjectLoaded = null;
        this.onProjectChanged = null;
        this.onError = null;
    }
    
    // 对应桌面版save_project方法
    saveProject(projectName = null) {
        try {
            if (projectName) {
                this.currentProject.projectName = projectName;
            }
            
            const projectData = {
                version: "1.0",
                projectName: this.currentProject.projectName,
                audioFile: this.currentProject.audioFile ? {
                    name: this.currentProject.audioFile.name,
                    size: this.currentProject.audioFile.size,
                    type: this.currentProject.audioFile.type
                } : null,
                audioUrl: this.currentProject.audioUrl,
                textLines: this.currentProject.importedTextLines,
                currentTextIndex: this.currentProject.currentTextLineIndex,
                subtitles: this.currentProject.subtitles.map(s => ({
                    id: s.id,
                    text: s.text,
                    startTime: s.startTime,
                    endTime: s.endTime,
                    selected: s.selected
                })),
                duration: this.currentProject.duration,
                currentPosition: this.currentProject.currentPosition,
                saveTime: new Date().toISOString(),
                lastModified: new Date().toISOString()
            };
            
            // 使用localStorage保存 - 对应桌面版文件保存
            const storageKey = `subtitle_project_${this.currentProject.projectName}`;
            localStorage.setItem(storageKey, JSON.stringify(projectData));
            
            // 添加到历史记录
            this.addToHistory(this.currentProject.projectName);
            
            if (this.onProjectSaved) {
                this.onProjectSaved({
                    projectName: this.currentProject.projectName,
                    data: projectData
                });
            }
            
            return {
                success: true,
                projectName: this.currentProject.projectName,
                message: `项目 "${this.currentProject.projectName}" 保存成功`
            };
            
        } catch (error) {
            console.error('Save project error:', error);
            if (this.onError) {
                this.onError(error);
            }
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // 对应桌面版open_project方法
    loadProject(projectName) {
        try {
            const storageKey = `subtitle_project_${projectName}`;
            const data = localStorage.getItem(storageKey);
            
            if (!data) {
                throw new Error(`项目 "${projectName}" 不存在`);
            }
            
            const projectData = JSON.parse(data);
            
            // 验证项目数据版本
            if (!projectData.version) {
                throw new Error('项目文件版本不兼容');
            }
            
            this.restoreProject(projectData);
            
            if (this.onProjectLoaded) {
                this.onProjectLoaded({
                    projectName: this.currentProject.projectName,
                    data: projectData
                });
            }
            
            return {
                success: true,
                projectName: this.currentProject.projectName,
                message: `项目 "${this.currentProject.projectName}" 加载成功`
            };
            
        } catch (error) {
            console.error('Load project error:', error);
            if (this.onError) {
                this.onError(error);
            }
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // 恢复项目数据
    restoreProject(projectData) {
        this.currentProject.projectName = projectData.projectName || "未命名项目";
        this.currentProject.audioUrl = projectData.audioUrl || null;
        this.currentProject.importedTextLines = projectData.textLines || [];
        this.currentProject.currentTextLineIndex = projectData.currentTextIndex || 0;
        this.currentProject.duration = projectData.duration || 0;
        this.currentProject.currentPosition = projectData.currentPosition || 0;
        
        // 恢复字幕数据
        this.currentProject.subtitles = (projectData.subtitles || []).map(s => {
            const subtitle = new SubtitleItem(s.text, s.startTime, s.endTime);
            subtitle.id = s.id;
            subtitle.selected = s.selected || false;
            return subtitle;
        });
        
        this.currentProject.lastModified = new Date(projectData.lastModified || Date.now());
        
        if (this.onProjectChanged) {
            this.onProjectChanged(this.currentProject);
        }
    }
    
    // 创建新项目
    createNewProject(projectName = "新项目") {
        this.currentProject = new ProjectData();
        this.currentProject.projectName = projectName;
        this.currentProject.lastModified = new Date();
        
        if (this.onProjectChanged) {
            this.onProjectChanged(this.currentProject);
        }
        
        return {
            success: true,
            projectName: this.currentProject.projectName,
            message: `新项目 "${this.currentProject.projectName}" 创建成功`
        };
    }
    
    // 获取所有保存的项目
    getAllProjects() {
        const projects = [];
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith('subtitle_project_')) {
                try {
                    const projectName = key.replace('subtitle_project_', '');
                    const data = localStorage.getItem(key);
                    const projectData = JSON.parse(data);
                    
                    projects.push({
                        name: projectName,
                        saveTime: projectData.saveTime,
                        lastModified: projectData.lastModified,
                        subtitleCount: projectData.subtitles ? projectData.subtitles.length : 0,
                        hasAudio: !!projectData.audioUrl,
                        duration: projectData.duration || 0
                    });
                } catch (error) {
                    console.warn('Failed to parse project:', key, error);
                }
            }
        }
        
        // 按最后修改时间排序
        projects.sort((a, b) => new Date(b.lastModified) - new Date(a.lastModified));
        
        return projects;
    }
    
    // 删除项目
    deleteProject(projectName) {
        try {
            const storageKey = `subtitle_project_${projectName}`;
            localStorage.removeItem(storageKey);
            
            // 从历史记录中移除
            this.removeFromHistory(projectName);
            
            return {
                success: true,
                message: `项目 "${projectName}" 删除成功`
            };
            
        } catch (error) {
            console.error('Delete project error:', error);
            if (this.onError) {
                this.onError(error);
            }
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // 导出项目为文件
    exportProject(projectName) {
        try {
            const storageKey = `subtitle_project_${projectName}`;
            const data = localStorage.getItem(storageKey);
            
            if (!data) {
                throw new Error(`项目 "${projectName}" 不存在`);
            }
            
            const projectData = JSON.parse(data);
            const blob = new Blob([JSON.stringify(projectData, null, 2)], {
                type: 'application/json'
            });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${projectName}.json`;
            a.click();
            URL.revokeObjectURL(url);
            
            return {
                success: true,
                message: `项目 "${projectName}" 导出成功`
            };
            
        } catch (error) {
            console.error('Export project error:', error);
            if (this.onError) {
                this.onError(error);
            }
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // 导入项目文件
    importProject(file) {
        return new Promise((resolve, reject) => {
            if (!file) {
                reject(new Error('No file provided'));
                return;
            }
            
            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    const projectData = JSON.parse(e.target.result);
                    
                    // 验证项目数据
                    if (!projectData.version || !projectData.projectName) {
                        throw new Error('Invalid project file format');
                    }
                    
                    // 检查项目名是否已存在
                    const existingProjects = this.getAllProjects();
                    const existingProject = existingProjects.find(p => p.name === projectData.projectName);
                    
                    if (existingProject) {
                        // 添加时间戳避免冲突
                        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                        projectData.projectName = `${projectData.projectName}_${timestamp}`;
                    }
                    
                    // 保存导入的项目
                    const storageKey = `subtitle_project_${projectData.projectName}`;
                    localStorage.setItem(storageKey, JSON.stringify(projectData));
                    
                    resolve({
                        success: true,
                        projectName: projectData.projectName,
                        message: `项目 "${projectData.projectName}" 导入成功`
                    });
                    
                } catch (error) {
                    reject(error);
                }
            };
            
            reader.onerror = (error) => {
                reject(error);
            };
            
            reader.readAsText(file);
        });
    }
    
    // 添加到历史记录
    addToHistory(projectName) {
        // 移除已存在的记录
        this.removeFromHistory(projectName);
        
        // 添加到开头
        this.projectHistory.unshift(projectName);
        
        // 限制历史记录大小
        if (this.projectHistory.length > this.maxHistorySize) {
            this.projectHistory = this.projectHistory.slice(0, this.maxHistorySize);
        }
        
        // 保存历史记录
        localStorage.setItem('subtitle_project_history', JSON.stringify(this.projectHistory));
    }
    
    // 从历史记录中移除
    removeFromHistory(projectName) {
        const index = this.projectHistory.indexOf(projectName);
        if (index > -1) {
            this.projectHistory.splice(index, 1);
            localStorage.setItem('subtitle_project_history', JSON.stringify(this.projectHistory));
        }
    }
    
    // 获取历史记录
    getHistory() {
        if (this.projectHistory.length === 0) {
            const savedHistory = localStorage.getItem('subtitle_project_history');
            if (savedHistory) {
                this.projectHistory = JSON.parse(savedHistory);
            }
        }
        return [...this.projectHistory];
    }
    
    // 清空历史记录
    clearHistory() {
        this.projectHistory = [];
        localStorage.removeItem('subtitle_project_history');
    }
    
    // 获取当前项目信息
    getCurrentProject() {
        return {
            name: this.currentProject.projectName,
            subtitleCount: this.currentProject.subtitles.length,
            hasAudio: !!this.currentProject.audioUrl,
            duration: this.currentProject.duration,
            lastModified: this.currentProject.lastModified,
            textLineCount: this.currentProject.importedTextLines.length
        };
    }
    
    // 检查项目是否有未保存的更改
    hasUnsavedChanges() {
        // 这里可以实现更复杂的更改检测逻辑
        return this.currentProject.subtitles.length > 0 || 
               this.currentProject.audioUrl || 
               this.currentProject.importedTextLines.length > 0;
    }
    
    // 自动保存
    autoSave() {
        if (this.hasUnsavedChanges()) {
            return this.saveProject();
        }
        return { success: true, message: '无需保存' };
    }
    
    // 备份项目
    backupProject() {
        const backupName = `${this.currentProject.projectName}_backup_${Date.now()}`;
        this.currentProject.projectName = backupName;
        return this.saveProject();
    }
    
    // 获取项目统计信息
    getProjectStats() {
        const projects = this.getAllProjects();
        const totalProjects = projects.length;
        const totalSubtitles = projects.reduce((sum, p) => sum + p.subtitleCount, 0);
        const projectsWithAudio = projects.filter(p => p.hasAudio).length;
        const totalDuration = projects.reduce((sum, p) => sum + p.duration, 0);
        
        return {
            totalProjects,
            totalSubtitles,
            projectsWithAudio,
            totalDuration,
            averageSubtitlesPerProject: totalProjects > 0 ? Math.round(totalSubtitles / totalProjects) : 0,
            averageDuration: totalProjects > 0 ? Math.round(totalDuration / totalProjects) : 0
        };
    }
    
    // 清理无效项目
    cleanupInvalidProjects() {
        const projects = this.getAllProjects();
        let cleanedCount = 0;
        
        projects.forEach(project => {
            try {
                const storageKey = `subtitle_project_${project.name}`;
                const data = localStorage.getItem(storageKey);
                JSON.parse(data); // 测试解析
            } catch (error) {
                // 删除无效项目
                localStorage.removeItem(`subtitle_project_${project.name}`);
                this.removeFromHistory(project.name);
                cleanedCount++;
            }
        });
        
        return {
            success: true,
            cleanedCount,
            message: `清理了 ${cleanedCount} 个无效项目`
        };
    }
    
    // 设置当前项目数据
    setCurrentProject(projectData) {
        this.currentProject = projectData;
        if (this.onProjectChanged) {
            this.onProjectChanged(this.currentProject);
        }
    }
    
    // 获取当前项目数据
    getCurrentProjectData() {
        return this.currentProject;
    }
}

// 导出类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProjectManager;
}
