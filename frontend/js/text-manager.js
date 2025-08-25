// 文本管理系统 - 对应桌面版文本导入功能
class TextManager {
    constructor() {
        this.importedTextLines = [];
        this.currentTextLineIndex = 0;
        this.textContent = '';
        this.fileName = '';
        
        // 事件回调
        this.onTextImported = null;
        this.onTextLineChanged = null;
        this.onError = null;
    }
    
    // 对应桌面版import_text方法
    importTextFile(file) {
        return new Promise((resolve, reject) => {
            if (!file) {
                const error = new Error('No file provided');
                if (this.onError) this.onError(error);
                reject(error);
                return;
            }
            
            // 验证文件类型
            const validExtensions = ['.txt', '.srt'];
            const fileName = file.name.toLowerCase();
            const isValidType = validExtensions.some(ext => fileName.endsWith(ext));
            
            if (!isValidType) {
                const error = new Error('Invalid file type. Please select .txt or .srt file');
                if (this.onError) this.onError(error);
                reject(error);
                return;
            }
            
            // 验证文件大小 (10MB限制)
            const maxSize = 10 * 1024 * 1024;
            if (file.size > maxSize) {
                const error = new Error('File too large (max 10MB)');
                if (this.onError) this.onError(error);
                reject(error);
                return;
            }
            
            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    const content = e.target.result;
                    this.textContent = content;
                    this.fileName = file.name;
                    
                    // 根据文件类型处理
                    if (fileName.endsWith('.srt')) {
                        this.parseSRTContent(content);
                    } else {
                        this.parseTXTContent(content);
                    }
                    
                    if (this.onTextImported) {
                        this.onTextImported({
                            fileName: this.fileName,
                            lineCount: this.importedTextLines.length,
                            content: this.textContent
                        });
                    }
                    
                    resolve({
                        fileName: this.fileName,
                        lineCount: this.importedTextLines.length,
                        content: this.textContent
                    });
                    
                } catch (error) {
                    if (this.onError) this.onError(error);
                    reject(error);
                }
            };
            
            reader.onerror = (error) => {
                if (this.onError) this.onError(error);
                reject(error);
            };
            
            reader.readAsText(file, 'utf-8');
        });
    }
    
    // 解析SRT文件内容
    parseSRTContent(content) {
        // 处理不同的换行符
        const normalizedContent = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const blocks = normalizedContent.trim().split('\n\n');
        
        this.importedTextLines = [];
        
        blocks.forEach((block, index) => {
            const lines = block.split('\n').filter(line => line.trim());
            
            if (lines.length >= 3) {
                const timeLine = lines[1];
                const text = lines.slice(2).join(' ').trim();
                
                // 验证时间格式
                const timeMatch = timeLine.match(/(\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})/);
                
                if (timeMatch && text) {
                    this.importedTextLines.push({
                        index: index + 1,
                        text: text,
                        startTime: this.parseTime(timeMatch[1]),
                        endTime: this.parseTime(timeMatch[2]),
                        originalBlock: block
                    });
                }
            }
        });
        
        this.currentTextLineIndex = 0;
    }
    
    // 解析TXT文件内容
    parseTXTContent(content) {
        // 处理不同的换行符
        const normalizedContent = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const lines = normalizedContent.split('\n').filter(line => line.trim());
        
        this.importedTextLines = lines.map((line, index) => ({
            index: index + 1,
            text: line.trim(),
            startTime: 0,
            endTime: 0,
            originalLine: line
        }));
        
        this.currentTextLineIndex = 0;
    }
    
    // 解析时间字符串
    parseTime(timeStr) {
        try {
            // 处理逗号和点作为毫秒分隔符
            const separator = timeStr.includes(',') ? ',' : '.';
            const [time, ms] = timeStr.split(separator);
            const [hours, minutes, seconds] = time.split(':').map(Number);
            
            // 验证时间组件
            if (isNaN(hours) || isNaN(minutes) || isNaN(seconds) || isNaN(ms)) {
                return 0;
            }
            
            return hours * 3600 + minutes * 60 + seconds + ms / 1000;
        } catch (error) {
            console.error('Error parsing time string:', timeStr, error);
            return 0;
        }
    }
    
    // 对应桌面版get_next_text_line方法
    getNextTextLine() {
        if (this.importedTextLines.length === 0) {
            return "新字幕";
        }
        
        if (this.currentTextLineIndex >= this.importedTextLines.length) {
            this.currentTextLineIndex = 0; // 循环使用
        }
        
        const textLine = this.importedTextLines[this.currentTextLineIndex];
        this.currentTextLineIndex++;
        
        if (this.onTextLineChanged) {
            this.onTextLineChanged(this.currentTextLineIndex, textLine);
        }
        
        return textLine.text;
    }
    
    // 获取当前文本行
    getCurrentTextLine() {
        if (this.importedTextLines.length === 0) {
            return null;
        }
        
        return this.importedTextLines[this.currentTextLineIndex - 1] || null;
    }
    
    // 设置当前文本行索引
    setCurrentTextLineIndex(index) {
        if (index >= 0 && index < this.importedTextLines.length) {
            this.currentTextLineIndex = index;
            if (this.onTextLineChanged) {
                this.onTextLineChanged(index, this.importedTextLines[index]);
            }
        }
    }
    
    // 获取所有文本行
    getAllTextLines() {
        return [...this.importedTextLines];
    }
    
    // 获取文本行数量
    getTextLineCount() {
        return this.importedTextLines.length;
    }
    
    // 获取当前索引
    getCurrentIndex() {
        return this.currentTextLineIndex;
    }
    
    // 重置索引到开始
    resetIndex() {
        this.currentTextLineIndex = 0;
        if (this.onTextLineChanged) {
            this.onTextLineChanged(0, this.importedTextLines[0] || null);
        }
    }
    
    // 获取指定索引的文本行
    getTextLineByIndex(index) {
        if (index >= 0 && index < this.importedTextLines.length) {
            return this.importedTextLines[index];
        }
        return null;
    }
    
    // 搜索文本
    searchText(query) {
        if (!query || query.trim() === '') {
            return [];
        }
        
        const results = [];
        const searchQuery = query.toLowerCase();
        
        this.importedTextLines.forEach((line, index) => {
            if (line.text.toLowerCase().includes(searchQuery)) {
                results.push({
                    index: index,
                    line: line,
                    matchIndex: line.text.toLowerCase().indexOf(searchQuery)
                });
            }
        });
        
        return results;
    }
    
    // 替换文本
    replaceText(searchQuery, replaceText) {
        let replaceCount = 0;
        
        this.importedTextLines.forEach(line => {
            if (line.text.includes(searchQuery)) {
                line.text = line.text.replace(new RegExp(searchQuery, 'g'), replaceText);
                replaceCount++;
            }
        });
        
        return replaceCount;
    }
    
    // 清空文本
    clearText() {
        this.importedTextLines = [];
        this.currentTextLineIndex = 0;
        this.textContent = '';
        this.fileName = '';
    }
    
    // 导出为TXT格式
    exportAsTXT() {
        return this.importedTextLines.map(line => line.text).join('\n');
    }
    
    // 导出为SRT格式
    exportAsSRT() {
        return this.importedTextLines.map((line, index) => {
            const startTime = this.formatTime(line.startTime);
            const endTime = this.formatTime(line.endTime);
            return `${index + 1}\n${startTime} --> ${endTime}\n${line.text}\n`;
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
    
    // 获取文本统计信息
    getTextStats() {
        const totalLines = this.importedTextLines.length;
        const totalCharacters = this.importedTextLines.reduce((sum, line) => sum + line.text.length, 0);
        const totalWords = this.importedTextLines.reduce((sum, line) => sum + line.text.split(/\s+/).length, 0);
        
        return {
            totalLines,
            totalCharacters,
            totalWords,
            averageWordsPerLine: totalLines > 0 ? Math.round(totalWords / totalLines) : 0,
            averageCharactersPerLine: totalLines > 0 ? Math.round(totalCharacters / totalLines) : 0
        };
    }
    
    // 验证文本内容
    validateText() {
        const errors = [];
        
        this.importedTextLines.forEach((line, index) => {
            if (!line.text || line.text.trim() === '') {
                errors.push({
                    type: 'empty_line',
                    index: index,
                    message: `Line ${index + 1} is empty`
                });
            }
            
            if (line.text.length > 100) {
                errors.push({
                    type: 'long_line',
                    index: index,
                    message: `Line ${index + 1} is too long (${line.text.length} characters)`
                });
            }
        });
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }
    
    // 获取文本预览
    getTextPreview(maxLines = 10) {
        return this.importedTextLines.slice(0, maxLines).map(line => line.text);
    }
    
    // 设置文本行的时间
    setTextLineTime(index, startTime, endTime) {
        if (index >= 0 && index < this.importedTextLines.length) {
            this.importedTextLines[index].startTime = startTime;
            this.importedTextLines[index].endTime = endTime;
        }
    }
    
    // 自动分配时间 (用于TXT文件)
    autoAssignTimes(duration) {
        if (this.importedTextLines.length === 0 || duration <= 0) {
            return;
        }
        
        const timePerLine = duration / this.importedTextLines.length;
        
        this.importedTextLines.forEach((line, index) => {
            line.startTime = index * timePerLine;
            line.endTime = (index + 1) * timePerLine;
        });
    }
}

// 导出类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TextManager;
}
