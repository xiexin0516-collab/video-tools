// 字幕项目类 - 对应桌面版SubtitleItem
class SubtitleItem {
    constructor(text = "新字幕", startTime = 0.0, endTime = 2.0) {
        this.id = Date.now() + Math.random(); // 唯一标识符
        this.text = text;
        this.startTime = startTime;
        this.endTime = endTime;
        this.selected = false;
    }
    
    // 获取字幕时长
    getDuration() {
        return this.endTime - this.startTime;
    }
    
    // 检查时间点是否在字幕范围内
    containsTime(time) {
        return time >= this.startTime && time <= this.endTime;
    }
    
    // 移动字幕
    move(deltaTime) {
        this.startTime += deltaTime;
        this.endTime += deltaTime;
    }
    
    // 调整开始时间
    setStartTime(time) {
        if (time < this.endTime) {
            this.startTime = time;
        }
    }
    
    // 调整结束时间
    setEndTime(time) {
        if (time > this.startTime) {
            this.endTime = time;
        }
    }
}

// 项目数据管理类
class ProjectData {
    constructor() {
        this.audioFile = null;
        this.audioUrl = null;
        this.subtitles = [];
        this.importedTextLines = [];
        this.currentTextLineIndex = 0;
        this.duration = 0;
        this.currentPosition = 0;
        this.projectName = "未命名项目";
        this.lastModified = new Date();
    }
    
    // 添加字幕
    addSubtitle(subtitle) {
        this.subtitles.push(subtitle);
        this.lastModified = new Date();
    }
    
    // 删除字幕
    removeSubtitle(index) {
        if (index >= 0 && index < this.subtitles.length) {
            this.subtitles.splice(index, 1);
            this.lastModified = new Date();
        }
    }
    
    // 获取选中的字幕
    getSelectedSubtitle() {
        return this.subtitles.find(s => s.selected);
    }
    
    // 清除所有选中状态
    clearSelection() {
        this.subtitles.forEach(s => s.selected = false);
    }
    
    // 设置音频文件
    setAudioFile(file, url) {
        this.audioFile = file;
        this.audioUrl = url;
        this.lastModified = new Date();
    }
    
    // 导入文本行
    importTextLines(lines) {
        this.importedTextLines = lines;
        this.currentTextLineIndex = 0;
        this.lastModified = new Date();
    }
    
    // 获取下一行文本
    getNextTextLine() {
        if (this.importedTextLines.length === 0) {
            return "新字幕";
        }
        
        if (this.currentTextLineIndex >= this.importedTextLines.length) {
            this.currentTextLineIndex = 0; // 循环使用
        }
        
        const text = this.importedTextLines[this.currentTextLineIndex];
        this.currentTextLineIndex++;
        return text;
    }
    
    // 导出为SRT格式
    exportToSRT() {
        return this.subtitles.map((subtitle, index) => {
            const startTime = this.formatTime(subtitle.startTime);
            const endTime = this.formatTime(subtitle.endTime);
            return `${index + 1}\n${startTime} --> ${endTime}\n${subtitle.text}\n`;
        }).join('\n');
    }
    
    // 格式化时间为SRT格式
    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const ms = Math.floor((seconds % 1) * 1000);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${ms.toString().padStart(3, '0')}`;
    }
    
    // 验证项目数据
    validate() {
        // 检查字幕时间重叠
        for (let i = 0; i < this.subtitles.length; i++) {
            for (let j = i + 1; j < this.subtitles.length; j++) {
                const s1 = this.subtitles[i];
                const s2 = this.subtitles[j];
                if (s1.startTime < s2.endTime && s1.endTime > s2.startTime) {
                    return false; // 时间重叠
                }
            }
        }
        return true;
    }
}

// 导出类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SubtitleItem, ProjectData };
}
