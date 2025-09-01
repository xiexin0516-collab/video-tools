// 时间轴编辑器类 - 对应桌面版TimelineEditor
class TimelineEditor {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // 基础属性 - 对应桌面版
        this.duration = 0;
        this.currentPosition = 0;
        this.subtitles = [];
        this.selectedSubtitle = -1;
        
        // 缩放相关 - 对应桌面版
        this.zoomStart = 0.0;
        this.zoomEnd = 0.0;
        this.isZoomed = false;
        this.pixelsPerSecond = 50;
        
        // 交互状态 - 对应桌面版
        this.dragMode = null; // 'move', 'resize-left', 'resize-right', 'create'
        this.dragging = false;
        this.dragStartPos = null;
        this.dragStartTime = 0;
        this.originalStartTime = 0;
        this.originalEndTime = 0;
        
        // 字幕块创建状态
        this.creatingSubtitle = false;
        this.createStartTime = 0;
        this.createEndTime = 0;
        
        // 吸附功能 - 对应桌面版
        this.snapEnabled = true;
        this.snapThreshold = 0.5;
        this.snapLines = [];
        
        // 渲染相关
        this.animationId = null;
        this.lastRenderTime = 0;
        
        // 事件回调
        this.onPositionChanged = null;
        this.onSubtitleAdded = null;
        this.onSubtitleSelected = null;
        this.onSubtitleChanged = null;
        this.onSubtitleDeleted = null;
        
        this.initEvents();
        this.startRenderLoop();
    }
    
    // 初始化事件监听
    initEvents() {
        this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        this.canvas.addEventListener('wheel', (e) => this.handleWheel(e));
        this.canvas.addEventListener('mouseleave', (e) => this.handleMouseLeave(e));
        
        // 键盘事件
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
    }
    
    // 开始渲染循环
    startRenderLoop() {
        const render = (timestamp) => {
            if (timestamp - this.lastRenderTime > 16) { // 60fps
                this.paint();
                this.lastRenderTime = timestamp;
            }
            this.animationId = requestAnimationFrame(render);
        };
        this.animationId = requestAnimationFrame(render);
    }
    
    // 停止渲染循环
    stopRenderLoop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }
    
    // 完全对应桌面版paintEvent方法
    paint() {
        const width = this.canvas.width;
        const height = this.canvas.height;
        
        // 清空画布 - 深色背景
        this.ctx.fillStyle = '#1e1e1e';
        this.ctx.fillRect(0, 0, width, height);
        
        if (this.duration <= 0) {
            this.drawWelcomeMessage();
            return;
        }
        
        // 绘制时间刻度 - 对应桌面版智能自适应算法
        this.drawTimeRuler();
        
        // 绘制字幕轨道
        this.drawSubtitleTrack();
        
        // 绘制字幕块 - 对应桌面版颜色和渐变效果
        this.drawSubtitleBlocks();
        
        // 绘制播放位置红线 - 100%精确对应
        this.drawPlaybackLine();
        
        // 绘制吸附线
        this.drawSnapLines();
        
        // 绘制创建预览
        if (this.creatingSubtitle) {
            this.drawCreationPreview();
        }
    }
    
    // 绘制欢迎信息
    drawWelcomeMessage() {
        this.ctx.fillStyle = '#666666';
        this.ctx.font = '16px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('请导入音频文件开始编辑字幕', this.canvas.width / 2, this.canvas.height / 2);
    }
    
    // 智能时间刻度算法 - 完全对应桌面版
    drawTimeRuler() {
        const displayDuration = this.isZoomed ? (this.zoomEnd - this.zoomStart) : this.duration;
        let majorInterval, minorInterval;
        
        // 桌面版的智能自适应间隔算法
        if (displayDuration <= 10) {
            majorInterval = 1.0;   // 1秒
            minorInterval = 0.2;   // 0.2秒
        } else if (displayDuration <= 30) {
            majorInterval = 2.0;   // 2秒
            minorInterval = 0.5;   // 0.5秒
        } else if (displayDuration <= 60) {
            majorInterval = 5.0;   // 5秒
            minorInterval = 1.0;   // 1秒
        } else if (displayDuration <= 300) {
            majorInterval = 30.0;  // 30秒
            minorInterval = 5.0;   // 5秒
        } else if (displayDuration <= 600) {
            majorInterval = 60.0;  // 1分钟
            minorInterval = 10.0;  // 10秒
        } else {
            majorInterval = 300.0; // 5分钟
            minorInterval = 60.0;  // 1分钟
        }
        
        this.drawMajorTicks(majorInterval);
        this.drawMinorTicks(minorInterval, majorInterval);
    }
    
    // 绘制主刻度
    drawMajorTicks(interval) {
        const startTime = this.isZoomed ? this.zoomStart : 0;
        const endTime = this.isZoomed ? this.zoomEnd : this.duration;
        
        this.ctx.strokeStyle = '#404040';
        this.ctx.lineWidth = 1;
        this.ctx.fillStyle = '#9ca3af';
        this.ctx.font = 'bold 12px Arial';
        this.ctx.textAlign = 'center';
        
        for (let time = Math.floor(startTime / interval) * interval; time <= endTime; time += interval) {
            if (time >= startTime && time <= endTime) {
                const x = this.timeToX(time);
                
                // 主刻度线
                this.ctx.beginPath();
                this.ctx.moveTo(x, 0);
                this.ctx.lineTo(x, 50);
                this.ctx.stroke();
                
                // 时间标签
                this.ctx.fillText(this.formatTime(time), x, 25);
            }
        }
    }
    
    // 绘制次刻度
    drawMinorTicks(minorInterval, majorInterval) {
        const startTime = this.isZoomed ? this.zoomStart : 0;
        const endTime = this.isZoomed ? this.zoomEnd : this.duration;
        
        this.ctx.strokeStyle = '#2a2a2a';
        this.ctx.lineWidth = 1;
        
        for (let time = Math.floor(startTime / minorInterval) * minorInterval; time <= endTime; time += minorInterval) {
            if (time >= startTime && time <= endTime && time % majorInterval !== 0) {
                const x = this.timeToX(time);
                
                this.ctx.beginPath();
                this.ctx.moveTo(x, 0);
                this.ctx.lineTo(x, 20);
                this.ctx.stroke();
            }
        }
    }
    
    // 绘制字幕轨道
    drawSubtitleTrack() {
        const trackY = 60;
        const trackHeight = this.canvas.height - trackY - 20;
        
        // 轨道背景
        this.ctx.fillStyle = '#2a2a2a';
        this.ctx.fillRect(0, trackY, this.canvas.width, trackHeight);
        
        // 网格线
        this.ctx.strokeStyle = '#1a1a1a';
        this.ctx.lineWidth = 1;
        
        for (let y = trackY; y < trackY + trackHeight; y += 30) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }
    
    // 绘制字幕块
    drawSubtitleBlocks() {
        const trackY = 70;
        const blockHeight = 20;
        
        this.subtitles.forEach((subtitle, index) => {
            const startX = this.timeToX(subtitle.startTime);
            const endX = this.timeToX(subtitle.endTime);
            const width = endX - startX;
            
            if (width < 5) return; // 太小的块不绘制
            
            // 渐变背景 - 对应桌面版颜色效果
            const gradient = this.ctx.createLinearGradient(startX, trackY, endX, trackY + blockHeight);
            
            if (subtitle.selected) {
                gradient.addColorStop(0, '#3b82f6');
                gradient.addColorStop(1, '#1d4ed8');
            } else {
                gradient.addColorStop(0, '#4b5563');
                gradient.addColorStop(1, '#374151');
            }
            
            this.ctx.fillStyle = gradient;
            this.ctx.strokeStyle = subtitle.selected ? '#60a5fa' : '#6b7280';
            this.ctx.lineWidth = subtitle.selected ? 2 : 1;
            
            // 圆角矩形
            this.drawRoundedRect(startX, trackY, width, blockHeight, 4);
            this.ctx.fill();
            this.ctx.stroke();
            
            // 字幕文本
            if (width > 30) {
                this.ctx.fillStyle = '#ffffff';
                this.ctx.font = 'bold 11px Arial';
                this.ctx.textAlign = 'left';
                const displayText = subtitle.text.length > 10 ? subtitle.text.substring(0, 10) + '...' : subtitle.text;
                this.ctx.fillText(displayText, startX + 5, trackY + 13);
            }
            
            // 字幕编号
            this.ctx.fillStyle = '#fbbf24';
            this.ctx.font = 'bold 10px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(`#${index + 1}`, startX + width / 2, trackY + 13);
            
            // 选中时的调整手柄
            if (subtitle.selected) {
                this.ctx.fillStyle = '#ffffff';
                this.ctx.fillRect(startX - 2, trackY, 4, blockHeight);
                this.ctx.fillRect(endX - 2, trackY, 4, blockHeight);
            }
        });
    }
    
    // 绘制播放位置红线
    drawPlaybackLine() {
        const x = this.timeToX(this.currentPosition);
        
        // 红线
        this.ctx.strokeStyle = '#ef4444';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(x, 0);
        this.ctx.lineTo(x, this.canvas.height);
        this.ctx.stroke();
        
        // 三角形头部
        this.ctx.fillStyle = '#ef4444';
        this.ctx.beginPath();
        this.ctx.moveTo(x - 8, 0);
        this.ctx.lineTo(x + 8, 0);
        this.ctx.lineTo(x, 16);
        this.ctx.closePath();
        this.ctx.fill();
        
        // 阴影效果
        this.ctx.shadowColor = 'rgba(239, 68, 68, 0.5)';
        this.ctx.shadowBlur = 4;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;
        this.ctx.fill();
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
    }
    
    // 绘制吸附线
    drawSnapLines() {
        if (!this.snapEnabled || this.snapLines.length === 0) return;
        
        this.ctx.strokeStyle = 'rgba(59, 130, 246, 0.5)';
        this.ctx.lineWidth = 1;
        this.ctx.setLineDash([5, 5]);
        
        this.snapLines.forEach(line => {
            const x = this.timeToX(line);
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        });
        
        this.ctx.setLineDash([]);
    }
    
    // 绘制创建预览
    drawCreationPreview() {
        const startX = this.timeToX(this.createStartTime);
        const endX = this.timeToX(this.createEndTime);
        const width = endX - startX;
        const trackY = 70;
        const blockHeight = 20;
        
        if (width < 5) return;
        
        // 半透明预览块
        this.ctx.fillStyle = 'rgba(59, 130, 246, 0.3)';
        this.ctx.strokeStyle = '#3b82f6';
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([5, 5]);
        
        this.drawRoundedRect(startX, trackY, width, blockHeight, 4);
        this.ctx.fill();
        this.ctx.stroke();
        
        this.ctx.setLineDash([]);
        
        // 预览文本
        this.ctx.fillStyle = '#3b82f6';
        this.ctx.font = 'bold 12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('创建中...', startX + width / 2, trackY + 13);
    }
    
    // 绘制圆角矩形
    drawRoundedRect(x, y, width, height, radius) {
        this.ctx.beginPath();
        this.ctx.moveTo(x + radius, y);
        this.ctx.lineTo(x + width - radius, y);
        this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        this.ctx.lineTo(x + width, y + height - radius);
        this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        this.ctx.lineTo(x + radius, y + height);
        this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        this.ctx.lineTo(x, y + radius);
        this.ctx.quadraticCurveTo(x, y, x + radius, y);
        this.ctx.closePath();
    }
    
    // 完全对应桌面版的鼠标事件处理
    handleMouseDown(event) {
        const pos = this.getMousePos(event);
        
        // 时间轴区域点击跳转 - 对应桌面版
        if (pos.y <= 50) {
            const newTime = this.xToTime(pos.x);
            this.setPosition(Math.max(0, Math.min(this.duration, newTime)));
            if (this.onPositionChanged) {
                this.onPositionChanged(newTime);
            }
            return;
        }
        
        // 字幕块交互 - 对应桌面版逻辑
        const [subtitleIndex, dragType] = this.getSubtitleAtPos(pos);
        
        if (subtitleIndex >= 0) {
            this.selectedSubtitle = subtitleIndex;
            this.dragMode = dragType;
            this.dragging = true;
            this.dragStartPos = pos;
            this.dragStartTime = this.xToTime(pos.x);
            this.originalStartTime = this.subtitles[subtitleIndex].startTime;
            this.originalEndTime = this.subtitles[subtitleIndex].endTime;
            
            if (this.onSubtitleSelected) {
                this.onSubtitleSelected(subtitleIndex);
            }
        } else {
            // 开始创建字幕块 - 对应桌面版
            this.startSubtitleCreation(pos);
        }
    }
    
    // 鼠标移动处理
    handleMouseMove(event) {
        const pos = this.getMousePos(event);
        
        if (this.dragging) {
            this.handleDrag(pos);
        } else if (this.creatingSubtitle) {
            this.createEndTime = this.xToTime(pos.x);
        }
        
        // 更新鼠标样式
        this.updateCursor(pos);
    }
    
    // 鼠标释放处理
    handleMouseUp(event) {
        if (this.creatingSubtitle) {
            this.finishSubtitleCreation();
        }
        
        this.dragging = false;
        this.dragMode = null;
        this.creatingSubtitle = false;
    }
    
    // 对应桌面版的wheelEvent
    handleWheel(event) {
        event.preventDefault();
        const zoomFactor = event.deltaY > 0 ? 1.3 : 1/1.3;
        this.zoomAroundPosition(this.currentPosition, zoomFactor);
    }
    
    // 鼠标离开处理
    handleMouseLeave(event) {
        this.canvas.style.cursor = 'default';
    }
    
    // 键盘事件处理
    handleKeyDown(event) {
        if (event.code === 'Delete' && this.selectedSubtitle >= 0) {
            this.deleteSelectedSubtitle();
        }
    }
    
    // 开始创建字幕
    startSubtitleCreation(pos) {
        this.creatingSubtitle = true;
        this.createStartTime = this.xToTime(pos.x);
        this.createEndTime = this.createStartTime;
    }
    
    // 完成字幕创建
    finishSubtitleCreation() {
        const startTime = Math.min(this.createStartTime, this.createEndTime);
        const endTime = Math.max(this.createStartTime, this.createEndTime);
        
        if (endTime - startTime >= 0.1) { // 最小时长
            if (this.onSubtitleAdded) {
                this.onSubtitleAdded(startTime, endTime);
            }
        }
    }
    
    // 处理拖拽
    handleDrag(pos) {
        const currentTime = this.xToTime(pos.x);
        const deltaTime = currentTime - this.dragStartTime;
        
        if (this.selectedSubtitle >= 0) {
            const subtitle = this.subtitles[this.selectedSubtitle];
            
            switch (this.dragMode) {
                case 'move':
                    const newStartTime = Math.max(0, this.originalStartTime + deltaTime);
                    const newEndTime = Math.min(this.duration, this.originalEndTime + deltaTime);
                    subtitle.startTime = newStartTime;
                    subtitle.endTime = newEndTime;
                    break;
                    
                case 'resize-left':
                    subtitle.startTime = Math.max(0, Math.min(currentTime, subtitle.endTime - 0.5));
                    break;
                    
                case 'resize-right':
                    subtitle.endTime = Math.min(this.duration, Math.max(currentTime, subtitle.startTime + 0.5));
                    break;
            }
            
            if (this.onSubtitleChanged) {
                this.onSubtitleChanged(this.selectedSubtitle, subtitle.startTime, subtitle.endTime);
            }
        }
    }
    
    // 获取鼠标位置
    getMousePos(event) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };
    }
    
    // 获取指定位置的字幕
    getSubtitleAtPos(pos) {
        const trackY = 70;
        const blockHeight = 20;
        
        if (pos.y < trackY || pos.y > trackY + blockHeight) {
            return [-1, null];
        }
        
        const time = this.xToTime(pos.x);
        
        for (let i = this.subtitles.length - 1; i >= 0; i--) {
            const subtitle = this.subtitles[i];
            if (time >= subtitle.startTime && time <= subtitle.endTime) {
                const startX = this.timeToX(subtitle.startTime);
                const endX = this.timeToX(subtitle.endTime);
                
                // 检查是否点击在调整手柄上
                if (Math.abs(pos.x - startX) < 5) {
                    return [i, 'resize-left'];
                } else if (Math.abs(pos.x - endX) < 5) {
                    return [i, 'resize-right'];
                } else {
                    return [i, 'move'];
                }
            }
        }
        
        return [-1, null];
    }
    
    // 更新鼠标样式
    updateCursor(pos) {
        if (pos.y <= 50) {
            this.canvas.style.cursor = 'pointer';
        } else if (this.dragging) {
            this.canvas.style.cursor = 'grabbing';
        } else if (this.creatingSubtitle) {
            this.canvas.style.cursor = 'crosshair';
        } else {
            const [subtitleIndex, dragType] = this.getSubtitleAtPos(pos);
            if (subtitleIndex >= 0) {
                if (dragType === 'resize-left' || dragType === 'resize-right') {
                    this.canvas.style.cursor = 'ew-resize';
                } else {
                    this.canvas.style.cursor = 'grab';
                }
            } else {
                this.canvas.style.cursor = 'crosshair';
            }
        }
    }
    
    // 缩放功能
    zoomAroundPosition(centerTime, factor) {
        if (!this.isZoomed) {
            this.zoomStart = 0;
            this.zoomEnd = this.duration;
            this.isZoomed = true;
        }
        
        const centerX = this.timeToX(centerTime);
        const zoomCenter = centerX / this.canvas.width;
        
        const newDuration = (this.zoomEnd - this.zoomStart) / factor;
        const halfDuration = newDuration / 2;
        
        this.zoomStart = centerTime - halfDuration * zoomCenter;
        this.zoomEnd = centerTime + halfDuration * (1 - zoomCenter);
        
        // 限制缩放范围
        this.zoomStart = Math.max(0, this.zoomStart);
        this.zoomEnd = Math.min(this.duration, this.zoomEnd);
    }
    
    // 时间坐标转换
    timeToX(time) {
        if (this.isZoomed) {
            const zoomDuration = this.zoomEnd - this.zoomStart;
            return ((time - this.zoomStart) / zoomDuration) * this.canvas.width;
        } else {
            return (time / this.duration) * this.canvas.width;
        }
    }
    
    xToTime(x) {
        if (this.isZoomed) {
            const zoomDuration = this.zoomEnd - this.zoomStart;
            return this.zoomStart + (x / this.canvas.width) * zoomDuration;
        } else {
            return (x / this.canvas.width) * this.duration;
        }
    }
    
    // 格式化时间显示
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
    
    // 设置属性
    setDuration(duration) {
        this.duration = duration;
        if (!this.isZoomed) {
            this.zoomStart = 0;
            this.zoomEnd = duration;
        }
    }
    
    setPosition(position) {
        this.currentPosition = Math.max(0, Math.min(this.duration, position));
    }
    
    setSubtitles(subtitles) {
        this.subtitles = subtitles;
    }
    
    setSelectedSubtitle(index) {
        this.selectedSubtitle = index;
        this.subtitles.forEach((s, i) => s.selected = (i === index));
    }
    
    // 删除选中的字幕
    deleteSelectedSubtitle() {
        if (this.selectedSubtitle >= 0 && this.onSubtitleDeleted) {
            this.onSubtitleDeleted(this.selectedSubtitle);
        }
    }
    
    // 清理资源
    destroy() {
        this.stopRenderLoop();
        // 移除事件监听器
        this.canvas.removeEventListener('mousedown', this.handleMouseDown);
        this.canvas.removeEventListener('mousemove', this.handleMouseMove);
        this.canvas.removeEventListener('mouseup', this.handleMouseUp);
        this.canvas.removeEventListener('wheel', this.handleWheel);
        this.canvas.removeEventListener('mouseleave', this.handleMouseLeave);
    }
}

// 导出类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TimelineEditor;
}
