// 主应用控制器 - 对应桌面版TimelineSubtitleTool主窗口
class SubtitleEditor {
    constructor() {
        // 初始化各个模块
        this.timeline = null;
        this.audioPlayer = new AudioPlayer();
        this.textManager = new TextManager();
        this.projectManager = new ProjectManager();
        
        // 应用状态
        this.isInitialized = false;
        this.currentLanguage = 'zh';
        
        // 初始化应用
        this.init();
    }
    
    // 初始化应用
    async init() {
        try {
            console.log('=== 字幕编辑器初始化开始 ===');
            
            // 等待DOM加载完成
            if (document.readyState === 'loading') {
                await new Promise(resolve => {
                    document.addEventListener('DOMContentLoaded', resolve);
                });
            }
            
            // 初始化时间轴编辑器
            this.initTimeline();
            
            // 连接事件
            this.connectEvents();
            
            // 初始化UI
            this.initUI();
            
            // 设置事件回调
            this.setupCallbacks();
            
            this.isInitialized = true;
            console.log('=== 字幕编辑器初始化完成 ===');
            
        } catch (error) {
            console.error('应用初始化失败:', error);
            this.showError('应用初始化失败: ' + error.message);
        }
    }
    
    // 初始化时间轴编辑器
    initTimeline() {
        const canvas = document.getElementById('timeline-canvas');
        if (!canvas) {
            throw new Error('找不到时间轴Canvas元素');
        }
        
        // 设置Canvas尺寸
        this.resizeCanvas();
        
        // 创建时间轴编辑器
        this.timeline = new TimelineEditor('timeline-canvas');
        
        // 监听窗口大小变化
        window.addEventListener('resize', () => {
            this.resizeCanvas();
        });
    }
    
    // 调整Canvas尺寸
    resizeCanvas() {
        const canvas = document.getElementById('timeline-canvas');
        if (canvas) {
            const container = canvas.parentElement;
            const rect = container.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
        }
    }
    
    // 对应桌面版的所有UI事件连接
    connectEvents() {
        // 时间轴事件 - 对应桌面版timeline信号
        this.timeline.onPositionChanged = (pos) => {
            this.audioPlayer.seekTo(pos);
        };
        
        this.timeline.onSubtitleAdded = (startTime, endTime) => {
            this.onSubtitleAdded(startTime, endTime);
        };
        
        this.timeline.onSubtitleSelected = (index) => {
            this.onSubtitleSelected(index);
        };
        
        this.timeline.onSubtitleChanged = (index, startTime, endTime) => {
            this.onSubtitleChanged(index, startTime, endTime);
        };
        
        this.timeline.onSubtitleDeleted = (index) => {
            this.onSubtitleDeleted(index);
        };
        
        // 音频事件 - 对应桌面版media_player信号  
        this.audioPlayer.onPositionChanged = (pos) => {
            this.timeline.setPosition(pos);
            this.updateTimeDisplay(pos);
        };
        
        this.audioPlayer.onDurationChanged = (dur) => {
            this.timeline.setDuration(dur);
            this.projectManager.currentProject.duration = dur;
            this.updateDurationDisplay(dur);
        };
        
        this.audioPlayer.onPlayStateChanged = (isPlaying) => {
            this.updatePlayButton(isPlaying);
        };
        
        this.audioPlayer.onError = (error) => {
            this.showError('音频播放错误: ' + error.message);
        };
        
        // 文本管理器事件
        this.textManager.onTextImported = (data) => {
            this.onTextImported(data);
        };
        
        this.textManager.onError = (error) => {
            this.showError('文本导入错误: ' + error.message);
        };
        
        // 项目管理器事件
        this.projectManager.onProjectSaved = (data) => {
            this.showSuccess('项目保存成功: ' + data.projectName);
        };
        
        this.projectManager.onProjectLoaded = (data) => {
            this.onProjectLoaded(data);
        };
        
        this.projectManager.onError = (error) => {
            this.showError('项目管理错误: ' + error.message);
        };
        
        // 键盘快捷键 - 对应桌面版keyPressEvent
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // 文件拖拽事件
        this.setupDragAndDrop();
    }
    
    // 设置事件回调
    setupCallbacks() {
        // 设置项目数据更新回调
        this.projectManager.onProjectChanged = (projectData) => {
            this.updateTimelineData(projectData);
            this.updateUI(projectData);
        };
    }
    
    // 初始化UI
    initUI() {
        // 初始化文件上传按钮
        this.initFileUploads();
        
        // 初始化播放控制按钮
        this.initPlaybackControls();
        
        // 初始化工具栏按钮
        this.initToolbarButtons();
        
        // 初始化语言切换
        this.initLanguageSwitcher();
        
        // 更新UI状态
        this.updateUI(this.projectManager.getCurrentProjectData());
    }
    
    // 初始化文件上传
    initFileUploads() {
        // 音频文件上传
        const audioUpload = document.getElementById('audio-upload');
        if (audioUpload) {
            audioUpload.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.loadAudioFile(file);
                }
            });
        }
        
        // 字幕文件上传
        const subtitleUpload = document.getElementById('subtitle-upload');
        if (subtitleUpload) {
            subtitleUpload.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.loadSubtitleFile(file);
                }
            });
        }
        
        // 文本文件上传
        const textUpload = document.getElementById('text-upload');
        if (textUpload) {
            textUpload.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.loadTextFile(file);
                }
            });
        }
    }
    
    // 初始化播放控制
    initPlaybackControls() {
        // 播放/暂停按钮
        const playButton = document.querySelector('.control-button.play');
        if (playButton) {
            playButton.addEventListener('click', () => {
                this.audioPlayer.playPause();
            });
        }
        
        // 停止按钮
        const stopButton = document.querySelector('.control-button');
        if (stopButton) {
            stopButton.addEventListener('click', () => {
                this.audioPlayer.stop();
            });
        }
        
        // 快进快退按钮
        const rewindButton = document.querySelector('.control-button:nth-child(3)');
        if (rewindButton) {
            rewindButton.addEventListener('click', () => {
                this.audioPlayer.skipTime(-5);
            });
        }
        
        const forwardButton = document.querySelector('.control-button:nth-child(4)');
        if (forwardButton) {
            forwardButton.addEventListener('click', () => {
                this.audioPlayer.skipTime(5);
            });
        }
        
        // 进度条
        const progressSlider = document.querySelector('.progress-slider');
        if (progressSlider) {
            progressSlider.addEventListener('input', (e) => {
                const time = parseFloat(e.target.value);
                this.audioPlayer.seekTo(time);
            });
        }
    }
    
    // 初始化工具栏按钮
    initToolbarButtons() {
        // 保存项目按钮
        const saveButton = document.querySelector('.toolbar-button:nth-child(5)');
        if (saveButton) {
            saveButton.addEventListener('click', () => {
                this.saveProject();
            });
        }
        
        // 加载项目按钮
        const loadButton = document.querySelector('.toolbar-button:nth-child(6)');
        if (loadButton) {
            loadButton.addEventListener('click', () => {
                this.showProjectList();
            });
        }
        
        // 导出SRT按钮
        const exportButton = document.querySelector('.toolbar-button.primary');
        if (exportButton) {
            exportButton.addEventListener('click', () => {
                this.exportSRT();
            });
        }
        
        // 清空字幕按钮
        const clearButton = document.querySelector('.toolbar-button:last-child');
        if (clearButton) {
            clearButton.addEventListener('click', () => {
                this.clearSubtitles();
            });
        }
    }
    
    // 初始化语言切换
    initLanguageSwitcher() {
        const languageSelect = document.querySelector('.language-select');
        if (languageSelect) {
            languageSelect.value = this.currentLanguage;
            languageSelect.addEventListener('change', (e) => {
                this.changeLanguage(e.target.value);
            });
        }
    }
    
    // 设置拖拽上传
    setupDragAndDrop() {
        const dropZone = document.body;
        
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            const files = Array.from(e.dataTransfer.files);
            
            files.forEach(file => {
                const fileName = file.name.toLowerCase();
                if (fileName.match(/\.(mp3|wav|m4a|ogg|aac)$/)) {
                    this.loadAudioFile(file);
                } else if (fileName.match(/\.(srt|txt)$/)) {
                    if (fileName.endsWith('.srt')) {
                        this.loadSubtitleFile(file);
                    } else {
                        this.loadTextFile(file);
                    }
                }
            });
        });
    }
    
    // 对应桌面版keyPressEvent
    handleKeyPress(event) {
        // 忽略输入框中的按键
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                this.audioPlayer.playPause();
                break;
                
            case 'ArrowLeft':
                event.preventDefault();
                this.audioPlayer.skipTime(-5);
                break;
                
            case 'ArrowRight':
                event.preventDefault();
                this.audioPlayer.skipTime(5);
                break;
                
            case 'KeyJ':
                event.preventDefault();
                this.audioPlayer.skipTime(-10);
                break;
                
            case 'KeyL':
                event.preventDefault();
                this.audioPlayer.skipTime(10);
                break;
                
            case 'Equal':
            case 'NumpadAdd':
                event.preventDefault();
                this.zoomIn();
                break;
                
            case 'Minus':
            case 'NumpadSubtract':
                event.preventDefault();
                this.zoomOut();
                break;
                
            case 'Delete':
                event.preventDefault();
                this.deleteSelectedSubtitle();
                break;
                
            case 'KeyS':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.saveProject();
                }
                break;
                
            case 'KeyO':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.showProjectList();
                }
                break;
                
            case 'KeyN':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.createNewProject();
                }
                break;
        }
    }
    
    // 加载音频文件
    async loadAudioFile(file) {
        try {
            this.showLoading('正在加载音频文件...');
            
            const url = await this.audioPlayer.loadAudio(file);
            
            // 更新项目数据
            this.projectManager.currentProject.setAudioFile(file, url);
            
            this.hideLoading();
            this.showSuccess(`音频文件加载成功: ${file.name}`);
            
        } catch (error) {
            this.hideLoading();
            this.showError('音频文件加载失败: ' + error.message);
        }
    }
    
    // 加载字幕文件
    async loadSubtitleFile(file) {
        try {
            this.showLoading('正在加载字幕文件...');
            
            const result = await this.textManager.importTextFile(file);
            
            // 如果是SRT文件，直接转换为字幕
            if (file.name.toLowerCase().endsWith('.srt')) {
                const subtitles = this.textManager.getAllTextLines().map(line => {
                    return new SubtitleItem(line.text, line.startTime, line.endTime);
                });
                
                this.projectManager.currentProject.subtitles = subtitles;
                this.timeline.setSubtitles(subtitles);
            }
            
            this.hideLoading();
            this.showSuccess(`字幕文件加载成功: ${file.name}`);
            
        } catch (error) {
            this.hideLoading();
            this.showError('字幕文件加载失败: ' + error.message);
        }
    }
    
    // 加载文本文件
    async loadTextFile(file) {
        try {
            this.showLoading('正在加载文本文件...');
            
            const result = await this.textManager.importTextFile(file);
            
            // 更新项目数据
            this.projectManager.currentProject.importTextLines(result.content.split('\n'));
            
            // 更新UI显示
            this.updateTextDisplay(result.content);
            
            this.hideLoading();
            this.showSuccess(`文本文件加载成功: ${file.name}`);
            
        } catch (error) {
            this.hideLoading();
            this.showError('文本文件加载失败: ' + error.message);
        }
    }
    
    // 字幕相关事件处理
    onSubtitleAdded(startTime, endTime) {
        const text = this.textManager.getNextTextLine();
        const subtitle = new SubtitleItem(text, startTime, endTime);
        
        this.projectManager.currentProject.addSubtitle(subtitle);
        this.timeline.setSubtitles(this.projectManager.currentProject.subtitles);
        
        this.updateSubtitleList();
    }
    
    onSubtitleSelected(index) {
        this.projectManager.currentProject.clearSelection();
        this.projectManager.currentProject.subtitles[index].selected = true;
        
        this.timeline.setSelectedSubtitle(index);
        this.updateSubtitleList();
    }
    
    onSubtitleChanged(index, startTime, endTime) {
        const subtitle = this.projectManager.currentProject.subtitles[index];
        subtitle.startTime = startTime;
        subtitle.endTime = endTime;
        
        this.updateSubtitleList();
    }
    
    onSubtitleDeleted(index) {
        this.projectManager.currentProject.removeSubtitle(index);
        this.timeline.setSubtitles(this.projectManager.currentProject.subtitles);
        
        this.updateSubtitleList();
    }
    
    // 文本导入事件处理
    onTextImported(data) {
        this.updateTextDisplay(data.content);
    }
    
    // 项目加载事件处理
    onProjectLoaded(data) {
        this.showSuccess(`项目加载成功: ${data.projectName}`);
        
        // 更新时间轴数据
        this.updateTimelineData(this.projectManager.currentProject);
        
        // 更新UI
        this.updateUI(this.projectManager.currentProject);
    }
    
    // 更新时间轴数据
    updateTimelineData(projectData) {
        this.timeline.setDuration(projectData.duration);
        this.timeline.setPosition(projectData.currentPosition);
        this.timeline.setSubtitles(projectData.subtitles);
    }
    
    // 更新UI
    updateUI(projectData) {
        this.updateTimeDisplay(projectData.currentPosition);
        this.updateDurationDisplay(projectData.duration);
        this.updateSubtitleList();
        this.updateTextDisplay(projectData.importedTextLines.join('\n'));
    }
    
    // 更新时间显示
    updateTimeDisplay(time) {
        const timeDisplay = document.querySelector('.time-display');
        if (timeDisplay) {
            const currentTime = this.formatTime(time);
            const duration = this.formatTime(this.projectManager.currentProject.duration);
            timeDisplay.textContent = `${currentTime} / ${duration}`;
        }
    }
    
    // 更新时长显示
    updateDurationDisplay(duration) {
        const progressSlider = document.querySelector('.progress-slider');
        if (progressSlider) {
            progressSlider.max = duration;
        }
    }
    
    // 更新播放按钮
    updatePlayButton(isPlaying) {
        const playButton = document.querySelector('.control-button.play');
        if (playButton) {
            playButton.textContent = isPlaying ? '⏸️ 暂停' : '▶️ 播放';
        }
    }
    
    // 更新字幕列表
    updateSubtitleList() {
        const subtitleList = document.querySelector('.subtitle-list');
        if (!subtitleList) return;
        
        const subtitles = this.projectManager.currentProject.subtitles;
        
        if (subtitles.length === 0) {
            subtitleList.innerHTML = '<div class="p-4 text-center text-gray-500">未加载字幕文件</div>';
            return;
        }
        
        subtitleList.innerHTML = subtitles.map((subtitle, index) => `
            <div class="subtitle-item ${subtitle.selected ? 'selected' : ''}" 
                 onclick="app.onSubtitleSelected(${index})">
                <div class="subtitle-info">
                    <div class="subtitle-number">#${index + 1}</div>
                    <div class="subtitle-time">
                        ${this.formatTime(subtitle.startTime)} - ${this.formatTime(subtitle.endTime)}
                    </div>
                    <div class="subtitle-text">
                        <input type="text" 
                               value="${subtitle.text}" 
                               onchange="app.updateSubtitleText(${index}, this.value)"
                               class="bg-transparent border-none outline-none w-full text-white"
                               placeholder="输入字幕文本...">
                    </div>
                </div>
                <div class="subtitle-actions">
                    <button onclick="app.deleteSubtitle(${index})" 
                            class="action-button danger">🗑️</button>
                </div>
            </div>
        `).join('');
    }
    
    // 更新文本显示
    updateTextDisplay(content) {
        const textDisplay = document.querySelector('.text-display');
        if (textDisplay) {
            if (content && content.trim()) {
                textDisplay.innerHTML = `<pre class="whitespace-pre-wrap">${content}</pre>`;
            } else {
                textDisplay.innerHTML = '<div class="text-gray-500 text-center mt-20">未加载文本内容</div>';
            }
        }
    }
    
    // 更新字幕文本
    updateSubtitleText(index, text) {
        if (index >= 0 && index < this.projectManager.currentProject.subtitles.length) {
            this.projectManager.currentProject.subtitles[index].text = text;
        }
    }
    
    // 删除字幕
    deleteSubtitle(index) {
        if (confirm('确定要删除这个字幕吗？')) {
            this.onSubtitleDeleted(index);
        }
    }
    
    // 清空字幕
    clearSubtitles() {
        if (confirm('确定要清空所有字幕吗？')) {
            this.projectManager.currentProject.subtitles = [];
            this.timeline.setSubtitles([]);
            this.updateSubtitleList();
        }
    }
    
    // 保存项目
    saveProject() {
        const projectName = prompt('请输入项目名称:', this.projectManager.currentProject.projectName);
        if (projectName) {
            const result = this.projectManager.saveProject(projectName);
            if (result.success) {
                this.showSuccess(result.message);
            } else {
                this.showError(result.error);
            }
        }
    }
    
    // 显示项目列表
    showProjectList() {
        const projects = this.projectManager.getAllProjects();
        
        if (projects.length === 0) {
            this.showInfo('没有保存的项目');
            return;
        }
        
        const projectList = projects.map(p => 
            `${p.name} (${p.subtitleCount} 字幕, ${this.formatTime(p.duration)})`
        ).join('\n');
        
        const projectName = prompt('选择要加载的项目:\n' + projectList);
        if (projectName) {
            const result = this.projectManager.loadProject(projectName);
            if (result.success) {
                this.showSuccess(result.message);
            } else {
                this.showError(result.error);
            }
        }
    }
    
    // 创建新项目
    createNewProject() {
        const projectName = prompt('请输入新项目名称:', '新项目');
        if (projectName) {
            const result = this.projectManager.createNewProject(projectName);
            if (result.success) {
                this.showSuccess(result.message);
            } else {
                this.showError(result.error);
            }
        }
    }
    
    // 导出SRT
    exportSRT() {
        const subtitles = this.projectManager.currentProject.subtitles;
        if (subtitles.length === 0) {
            this.showInfo('没有字幕可以导出');
            return;
        }
        
        const srtContent = this.projectManager.currentProject.exportToSRT();
        const blob = new Blob([srtContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'subtitles.srt';
        a.click();
        URL.revokeObjectURL(url);
        
        this.showSuccess('SRT文件导出成功');
    }
    
    // 缩放功能
    zoomIn() {
        // 实现缩放功能
        console.log('Zoom in');
    }
    
    zoomOut() {
        // 实现缩放功能
        console.log('Zoom out');
    }
    
    // 删除选中的字幕
    deleteSelectedSubtitle() {
        const selectedIndex = this.projectManager.currentProject.subtitles.findIndex(s => s.selected);
        if (selectedIndex >= 0) {
            this.deleteSubtitle(selectedIndex);
        }
    }
    
    // 语言切换
    changeLanguage(language) {
        this.currentLanguage = language;
        // 实现语言切换逻辑
        console.log('Language changed to:', language);
    }
    
    // 工具方法
    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes}:${secs.toString().padStart(2, '0')}`;
        }
    }
    
    // 消息显示方法
    showSuccess(message) {
        this.showMessage(message, 'success');
    }
    
    showError(message) {
        this.showMessage(message, 'error');
    }
    
    showInfo(message) {
        this.showMessage(message, 'info');
    }
    
    showMessage(message, type = 'info') {
        // 创建消息元素
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        
        // 添加到页面
        document.body.appendChild(messageDiv);
        
        // 自动移除
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 3000);
    }
    
    showLoading(message) {
        // 实现加载提示
        console.log('Loading:', message);
    }
    
    hideLoading() {
        // 隐藏加载提示
        console.log('Loading finished');
    }
    
    // 清理资源
    destroy() {
        if (this.timeline) {
            this.timeline.destroy();
        }
        
        if (this.audioPlayer) {
            this.audioPlayer.destroy();
        }
        
        // 移除事件监听器
        document.removeEventListener('keydown', this.handleKeyPress);
    }
}

// 创建全局应用实例
let app = null;

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    app = new SubtitleEditor();
});

// 导出类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SubtitleEditor;
}
