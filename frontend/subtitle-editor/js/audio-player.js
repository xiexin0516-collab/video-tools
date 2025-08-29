// 音频播放器类 - 对应桌面版QMediaPlayer
class AudioPlayer {
    constructor() {
        this.audio = new Audio();
        this.isPlaying = false;
        this.duration = 0;
        this.currentTime = 0;
        this.positionUpdateTimer = null;
        this.seeking = false;
        
        // 事件回调
        this.onDurationChanged = null;
        this.onPositionChanged = null;
        this.onPlayStateChanged = null;
        this.onError = null;
        this.onLoaded = null;
        
        this.initEvents();
    }
    
    // 对应桌面版media_player事件
    initEvents() {
        this.audio.addEventListener('loadedmetadata', () => {
            this.duration = this.audio.duration;
            console.log('Audio loaded, duration:', this.duration);
            if (this.onDurationChanged) {
                this.onDurationChanged(this.duration);
            }
            if (this.onLoaded) {
                this.onLoaded();
            }
        });
        
        this.audio.addEventListener('timeupdate', () => {
            if (!this.seeking) {
                this.currentTime = this.audio.currentTime;
                if (this.onPositionChanged) {
                    this.onPositionChanged(this.currentTime);
                }
            }
        });
        
        this.audio.addEventListener('play', () => {
            this.isPlaying = true;
            this.startPositionTimer();
            if (this.onPlayStateChanged) {
                this.onPlayStateChanged(true);
            }
        });
        
        this.audio.addEventListener('pause', () => {
            this.isPlaying = false;
            this.stopPositionTimer();
            if (this.onPlayStateChanged) {
                this.onPlayStateChanged(false);
            }
        });
        
        this.audio.addEventListener('ended', () => {
            this.isPlaying = false;
            this.stopPositionTimer();
            if (this.onPlayStateChanged) {
                this.onPlayStateChanged(false);
            }
        });
        
        this.audio.addEventListener('error', (error) => {
            console.error('Audio error:', error);
            if (this.onError) {
                this.onError(error);
            }
        });
        
        this.audio.addEventListener('canplay', () => {
            console.log('Audio can play');
        });
        
        this.audio.addEventListener('loadstart', () => {
            console.log('Audio loading started');
        });
        
        this.audio.addEventListener('progress', () => {
            console.log('Audio loading progress');
        });
    }
    
    // 对应桌面版的平滑位置更新
    startPositionTimer() {
        this.stopPositionTimer(); // 确保只有一个定时器
        this.positionUpdateTimer = setInterval(() => {
            if (this.isPlaying && !this.seeking) {
                this.currentTime = this.audio.currentTime;
                if (this.onPositionChanged) {
                    this.onPositionChanged(this.currentTime);
                }
            }
        }, 50); // 50ms = 20fps，对应桌面版的更新频率
    }
    
    stopPositionTimer() {
        if (this.positionUpdateTimer) {
            clearInterval(this.positionUpdateTimer);
            this.positionUpdateTimer = null;
        }
    }
    
    // 加载音频文件
    loadAudio(file) {
        return new Promise((resolve, reject) => {
            if (!file) {
                reject(new Error('No file provided'));
                return;
            }
            
            // 验证文件类型
            const validTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/aac'];
            const validExtensions = ['.mp3', '.wav', '.m4a', '.ogg', '.aac'];
            
            const fileName = file.name.toLowerCase();
            const isValidType = validTypes.includes(file.type) || 
                              validExtensions.some(ext => fileName.endsWith(ext));
            
            if (!isValidType) {
                reject(new Error('Invalid audio file type'));
                return;
            }
            
            // 验证文件大小 (100MB限制)
            const maxSize = 100 * 1024 * 1024;
            if (file.size > maxSize) {
                reject(new Error('File too large (max 100MB)'));
                return;
            }
            
            // 创建对象URL
            const url = URL.createObjectURL(file);
            
            // 设置音频源
            this.audio.src = url;
            this.audio.load();
            
            // 监听加载完成
            const onLoaded = () => {
                this.audio.removeEventListener('loadedmetadata', onLoaded);
                this.audio.removeEventListener('error', onError);
                resolve(url);
            };
            
            const onError = (error) => {
                this.audio.removeEventListener('loadedmetadata', onLoaded);
                this.audio.removeEventListener('error', onError);
                URL.revokeObjectURL(url);
                reject(error);
            };
            
            this.audio.addEventListener('loadedmetadata', onLoaded);
            this.audio.addEventListener('error', onError);
        });
    }
    
    // 播放/暂停
    playPause() {
        if (this.audio.src) {
            if (this.isPlaying) {
                this.pause();
            } else {
                this.play();
            }
        }
    }
    
    // 播放
    play() {
        if (this.audio.src) {
            this.audio.play().catch(error => {
                console.error('Play failed:', error);
                if (this.onError) {
                    this.onError(error);
                }
            });
        }
    }
    
    // 暂停
    pause() {
        this.audio.pause();
    }
    
    // 停止
    stop() {
        this.audio.pause();
        this.seekTo(0);
    }
    
    // 跳转到指定时间
    seekTo(time) {
        if (this.audio.src) {
            this.seeking = true;
            const targetTime = Math.max(0, Math.min(this.duration, time));
            this.audio.currentTime = targetTime;
            
            // 短暂延迟后恢复位置更新
            setTimeout(() => {
                this.seeking = false;
                this.currentTime = this.audio.currentTime;
                if (this.onPositionChanged) {
                    this.onPositionChanged(this.currentTime);
                }
            }, 100);
        }
    }
    
    // 跳转指定秒数
    skipTime(seconds) {
        const newTime = this.currentTime + seconds;
        this.seekTo(newTime);
    }
    
    // 设置音量
    setVolume(volume) {
        this.audio.volume = Math.max(0, Math.min(1, volume));
    }
    
    // 获取音量
    getVolume() {
        return this.audio.volume;
    }
    
    // 设置播放速率
    setPlaybackRate(rate) {
        this.audio.playbackRate = Math.max(0.1, Math.min(4, rate));
    }
    
    // 获取播放速率
    getPlaybackRate() {
        return this.audio.playbackRate;
    }
    
    // 获取当前播放状态
    getPlayState() {
        return {
            isPlaying: this.isPlaying,
            currentTime: this.currentTime,
            duration: this.duration,
            volume: this.audio.volume,
            playbackRate: this.audio.playbackRate
        };
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
    
    // 获取音频波形数据 (用于可视化)
    async getWaveformData() {
        // 这里可以实现音频波形分析
        // 由于浏览器限制，需要Web Audio API
        return null;
    }
    
    // 清理资源
    destroy() {
        this.stopPositionTimer();
        this.audio.pause();
        this.audio.src = '';
        this.audio.load();
    }
    
    // 设置音频源
    setSource(url) {
        this.audio.src = url;
        this.audio.load();
    }
    
    // 获取音频源
    getSource() {
        return this.audio.src;
    }
    
    // 获取当前播放时间
    getCurrentTime() {
        return this.audio.currentTime;
    }
    
    // 检查是否已加载
    isLoaded() {
        return this.audio.readyState >= 2; // HAVE_CURRENT_DATA
    }
    
    // 检查是否可以播放
    canPlay() {
        return this.audio.readyState >= 3; // HAVE_FUTURE_DATA
    }
    
    // 获取缓冲进度
    getBuffered() {
        if (this.audio.buffered.length > 0) {
            return {
                start: this.audio.buffered.start(0),
                end: this.audio.buffered.end(0)
            };
        }
        return null;
    }
    
    // 监听缓冲进度
    onProgress(callback) {
        this.audio.addEventListener('progress', () => {
            const buffered = this.getBuffered();
            if (buffered && callback) {
                callback(buffered);
            }
        });
    }
    
    // 监听时间更新
    onTimeUpdate(callback) {
        this.audio.addEventListener('timeupdate', () => {
            if (callback) {
                callback(this.audio.currentTime);
            }
        });
    }
    
    // 监听播放状态变化
    onPlayStateChange(callback) {
        this.audio.addEventListener('play', () => callback(true));
        this.audio.addEventListener('pause', () => callback(false));
        this.audio.addEventListener('ended', () => callback(false));
    }
    
    // 监听错误
    onAudioError(callback) {
        this.audio.addEventListener('error', (error) => {
            if (callback) {
                callback(error);
            }
        });
    }
}

// 导出类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AudioPlayer;
}
