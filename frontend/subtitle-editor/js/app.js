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
            
            // 加载示例字幕数据
            this.loadDemoSubtitles();
            
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
        const audioFileInput = document.getElementById('audioFileInput');
        const fileUpload = document.getElementById('fileUpload');
        
        if (audioFileInput && fileUpload) {
            fileUpload.addEventListener('click', () => {
                audioFileInput.click();
            });
            
            audioFileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.loadAudioFile(file);
                }
            });
        }
    }
    
    // 初始化播放控制
    initPlaybackControls() {
        // 播放/暂停按钮
        const playBtn = document.getElementById('playBtn');
        if (playBtn) {
            playBtn.addEventListener('click', () => {
                this.audioPlayer.playPause();
            });
        }
        
        // 停止按钮
        const stopBtn = document.getElementById('stopBtn');
        if (stopBtn) {
            stopBtn.addEventListener('click', () => {
                this.audioPlayer.stop();
            });
        }
        
        // 添加字幕按钮
        const addSubtitleBtn = document.getElementById('addSubtitleBtn');
        if (addSubtitleBtn) {
            addSubtitleBtn.addEventListener('click', () => {
                this.addNewSubtitle();
            });
        }
        
        // 删除字幕按钮
        const deleteSubtitleBtn = document.getElementById('deleteSubtitleBtn');
        if (deleteSubtitleBtn) {
            deleteSubtitleBtn.addEventListener('click', () => {
                this.deleteSelectedSubtitle();
            });
        }
    }
    
    // 初始化工具栏按钮
    initToolbarButtons() {
        // 保存项目按钮
        const saveBtn = document.getElementById('saveBtn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                this.saveProject();
            });
        }
        
        // 导出字幕按钮
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportSubtitles();
            });
        }
        
        // 登录按钮
        const authBtn = document.getElementById('authBtn');
        if (authBtn) {
            authBtn.addEventListener('click', () => {
                this.handleAuth();
            });
        }
    }
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
            this.projectManager.currentProject.importedTextLines = result.content.split('\n');
            this.projectManager.currentProject.currentTextLineIndex = 0;
            
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
        
        this.projectManager.currentProject.subtitles.push(subtitle);
        this.timeline.setSubtitles(this.projectManager.currentProject.subtitles);
        
        this.updateSubtitleList();
    }
    
    onSubtitleSelected(index) {
        // 清除所有选中状态
        this.projectManager.currentProject.subtitles.forEach(s => s.selected = false);
        // 设置当前选中
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
        if (index >= 0 && index < this.projectManager.currentProject.subtitles.length) {
            this.projectManager.currentProject.subtitles.splice(index, 1);
            this.timeline.setSubtitles(this.projectManager.currentProject.subtitles);
            this.updateSubtitleList();
        }
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
        const timeDisplay = document.getElementById('currentTime');
        if (timeDisplay) {
            const currentTime = this.formatTime(time);
            timeDisplay.textContent = currentTime;
        }
    }
    
    // 更新时长显示
    updateDurationDisplay(duration) {
        // 这里可以添加更新音频播放器时长的逻辑
        console.log('Duration updated:', duration);
    }
    
    // 更新播放按钮
    updatePlayButton(isPlaying) {
        const playButton = document.getElementById('playBtn');
        if (playButton) {
            playButton.textContent = isPlaying ? '⏸️ 暂停' : '▶️ 播放';
        }
    }
    
    // 更新字幕列表
    updateSubtitleList() {
        const subtitleList = document.getElementById('subtitleList');
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
        const textDisplay = document.getElementById('textDisplay');
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
    
    // 添加新字幕
    addNewSubtitle() {
        const currentTime = this.audioPlayer.getCurrentTime() || 0;
        const startTime = currentTime;
        const endTime = currentTime + 3; // 默认3秒长度
        
        const newSubtitle = {
            text: "[点击编辑字幕文本]",
            startTime: startTime,
            endTime: endTime,
            selected: false
        };
        
        this.projectManager.currentProject.subtitles.push(newSubtitle);
        this.timeline.setSubtitles(this.projectManager.currentProject.subtitles);
        this.updateSubtitleList();
        
        console.log('新字幕已添加');
    }
    
    // 删除选中的字幕
    deleteSelectedSubtitle() {
        const selectedIndex = this.projectManager.currentProject.subtitles.findIndex(s => s.selected);
        if (selectedIndex >= 0) {
            this.deleteSubtitle(selectedIndex);
        }
    }
    
    // 导出字幕
    exportSubtitles() {
        const subtitles = this.projectManager.currentProject.subtitles;
        if (subtitles.length === 0) {
            this.showInfo('没有字幕可以导出');
            return;
        }
        
        let srtContent = '';
        subtitles.forEach((subtitle, index) => {
            const startTime = this.formatTimeForSRT(subtitle.startTime);
            const endTime = this.formatTimeForSRT(subtitle.endTime);
            srtContent += `${index + 1}\n${startTime} --> ${endTime}\n${subtitle.text}\n\n`;
        });
        
        // 创建下载链接
        const blob = new Blob([srtContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'subtitles.srt';
        a.click();
        URL.revokeObjectURL(url);
        
        this.showSuccess('字幕已导出为SRT文件');
    }
    
    // 处理认证
    handleAuth() {
        // 这里可以添加登录逻辑
        console.log('处理认证');
    }
    
    // 格式化时间为SRT格式
    formatTimeForSRT(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const ms = Math.floor((seconds % 1) * 1000);
        
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${ms.toString().padStart(3, '0')}`;
    }
    
    // 语言切换
    changeLanguage(language) {
        this.currentLanguage = language;
        // 实现语言切换逻辑
        console.log('Language changed to:', language);
    }
    
    // 加载示例字幕数据
    loadDemoSubtitles() {
        const demoSubtitles = [
            { text: "欢迎使用字幕编辑器网页版", startTime: 0, endTime: 3, selected: false },
            { text: "这是一个多语言视频工具平台", startTime: 3, endTime: 6, selected: false },
            { text: "支持中英文双语界面", startTime: 6, endTime: 9, selected: false },
            { text: "您可以上传音频文件和字幕文件", startTime: 9, endTime: 12, selected: false },
            { text: "进行实时编辑和同步", startTime: 12, endTime: 15, selected: false },
            { text: "导出为SRT或TXT格式", startTime: 15, endTime: 18, selected: false },
            { text: "开始您的字幕编辑之旅吧！", startTime: 18, endTime: 21, selected: false },
            { text: "Welcome to SubtitleEditor Web", startTime: 21, endTime: 24, selected: false },
            { text: "A multi-language video tool platform", startTime: 24, endTime: 27, selected: false },
            { text: "Supporting Chinese and English interfaces", startTime: 27, endTime: 30, selected: false }
        ];
        
        // 设置项目数据
        this.projectManager.currentProject.subtitles = demoSubtitles;
        this.projectManager.currentProject.duration = 30;
        this.projectManager.currentProject.projectName = "示例项目";
        
        // 更新时间轴
        this.timeline.setSubtitles(demoSubtitles);
        this.timeline.setDuration(30);
        
        // 更新UI
        this.updateSubtitleList();
        this.updateTextDisplay("欢迎使用字幕编辑器网页版\n\n这是一个多语言视频工具平台，支持中英文双语界面。您可以上传音频文件和字幕文件，进行实时编辑和同步，导出为SRT或TXT格式。\n\n开始您的字幕编辑之旅吧！");
        
        console.log('示例字幕数据已加载');
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
