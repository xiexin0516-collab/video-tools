#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Timeline-based subtitle editor - Completely avoids waveform sync issues
Uses timeline instead of waveform, ensures 100% synchronization
Redesigned interface layout
"""

import sys
import os
from datetime import timedelta

# Import internationalization support
from language_loader import lang

print(lang["msg.startup"])

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtMultimedia import *
    from PyQt5.QtCore import QDateTime
    # Ensure all required components are imported
    from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
                                 QToolButton, QMessageBox, QShortcut, QStyle)
    from PyQt5.QtGui import QKeySequence
    print(lang["msg.pyqt_success"])
except ImportError as e:
    print(lang["msg.pyqt_failed"].format(error=str(e)))
    print(lang["msg.install_pyqt"])
    input(lang["msg.press_enter"])
    sys.exit(1)

class SubtitleItem:
    def __init__(self, text=lang["msg.new_subtitle"], start_time=0.0, end_time=2.0):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.selected = False

class ProgressSlider(QSlider):
    """Custom progress slider"""
    
    position_changed = pyqtSignal(float)
    
    def __init__(self, orientation=Qt.Horizontal):
        super().__init__(orientation)
        self.setObjectName("progressSlider")  # Name the progress bar for precise global style control
        self.setRange(0, 10000)
        self.setValue(0)
        self.duration = 0.0
        self.is_dragging = False
        
        # Remove inline styles to inherit global QSlider styles
        # self.setStyleSheet(""" ... """)  # Comment out inline styles
        
        self.valueChanged.connect(self.on_value_changed)
    
    def set_duration(self, duration):
        self.duration = duration
    
    def set_position(self, position):
        if self.duration > 0 and not self.is_dragging:
            value = int((position / self.duration) * self.maximum())
            self.blockSignals(True)
            self.setValue(value)
            self.blockSignals(False)
    
    def on_value_changed(self, value):
        if self.duration > 0:
            position = (value / self.maximum()) * self.duration
            self.position_changed.emit(position)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            value = QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), 
                event.x(), self.width()
            )
            self.setValue(value)
            if self.duration > 0:
                position = (value / self.maximum()) * self.duration
                self.position_changed.emit(position)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.LeftButton:
            value = QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), 
                event.x(), self.width()
            )
            self.setValue(value)
            if self.duration > 0:
                position = (value / self.maximum()) * self.duration
                self.position_changed.emit(position)
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
        super().mouseReleaseEvent(event)

class TimeDisplay(QLabel):
    """Time display widget"""
    
    def __init__(self):
        super().__init__()
        self.current_time = 0.0
        self.total_time = 0.0
        self.setFixedWidth(120)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #2d2d30;
                color: #ffffff;
                border: 1px solid #3e3e42;
                padding: 4px 8px;
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }
        """)
        self.update_display()
    
    def set_time(self, current_time, total_time=None):
        self.current_time = current_time
        if total_time is not None:
            self.total_time = total_time
        self.update_display()
    
    def update_display(self):
        current_str = self.format_time(self.current_time)
        total_str = self.format_time(self.total_time)
        self.setText(f"{current_str} / {total_str}")
    
    def format_time(self, seconds):
        if seconds < 3600:  # Less than 1 hour
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes:02d}:{secs:02d}"
        else:  # Greater than or equal to 1 hour
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours:02d}:{minutes:02d}"

class TimelineEditor(QWidget):
    """Timeline-based subtitle editor - No waveform, fully synchronized"""
    
    position_changed = pyqtSignal(float)
    subtitle_added = pyqtSignal(float)
    subtitle_selected = pyqtSignal(int)
    subtitle_changed = pyqtSignal(int, float, float)
    subtitle_deleted = pyqtSignal(int)
    play_triggered = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Basic properties
        self.duration = 0
        self.current_position = 0
        
        # Subtitle related
        self.subtitles = []
        self.selected_subtitle = -1
        
        # Zoom related
        self.zoom_start = 0.0
        self.zoom_end = 0.0
        self.is_zoomed = False
        self.pixels_per_second = 50  # Pixels per second
        
        # Interactive states
        self.drag_mode = None
        self.dragging = False
        self.drag_start_pos = None
        self.drag_start_time = 0
        self.original_start_time = 0
        self.original_end_time = 0
        
        # Subtitle block creation state
        self.creating_subtitle = False
        self.create_start_time = 0
        self.create_end_time = 0
        
        # Snap functionality
        self.snap_enabled = True
        self.snap_threshold = 0.5  # Snap threshold (seconds)
        self.snap_lines = []  # Snap line list
        
        # Right-click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        self.setMinimumHeight(200)
        self.setMouseTracking(True)
        
        # Set focus policy to allow timeline to receive keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        
        print(lang["msg.timeline_init"])
    
    def load_from_player(self, media_player):
        """从播放器加载时长信息"""
        try:
            duration_ms = media_player.duration()
            if duration_ms <= 0:
                print(lang["msg.player_duration_invalid"])
                return False
            
            self.duration = duration_ms / 1000.0
            print(lang["msg.player_duration"].format(duration=self.duration))
            
            self.zoom_start = 0.0
            self.zoom_end = min(self.duration, 60.0)  # Default display first 60 seconds
            self.is_zoomed = (self.zoom_end < self.duration)
            
            print(lang["msg.timeline_init_success"])
            self.update()
            
            return True
            
        except Exception as e:
            print(lang["msg.timeline_init_failed"].format(error=str(e)))
            return False
    
    def set_position(self, position):
        """设置播放位置"""
        if abs(self.current_position - position) < 0.01:
            return
        self.current_position = position
        
        # Auto-adjust display range to follow playback position
        if self.is_zoomed:
            display_duration = self.zoom_end - self.zoom_start
            
            # If playback position exceeds display range, adjust display window
            if position < self.zoom_start or position > self.zoom_end:
                # Place playback position at 1/3 of display window
                new_start = max(0, position - display_duration * 0.3)
                new_end = min(self.duration, new_start + display_duration)
                
                # If right boundary reaches end, adjust left boundary
                if new_end == self.duration:
                    new_start = max(0, self.duration - display_duration)
                
                self.zoom_start = new_start
                self.zoom_end = new_end
        
        self.update()
    
    def time_to_x(self, time_seconds):
        """时间转换为x坐标"""
        if self.zoom_end <= self.zoom_start:
            return 0
        display_duration = self.zoom_end - self.zoom_start
        relative_time = time_seconds - self.zoom_start
        return (relative_time / display_duration) * self.width()
    
    def x_to_time(self, x):
        """x坐标转换为时间"""
        if self.width() <= 0:
            return 0
        display_duration = self.zoom_end - self.zoom_start
        relative_x = x / self.width()
        return self.zoom_start + relative_x * display_duration
    
    def get_subtitle_at_pos(self, pos):
        """获取鼠标位置下的字幕"""
        click_time = self.x_to_time(pos.x())
        subtitle_track_y = 60
        track_height = 60
        
        if not (subtitle_track_y <= pos.y() <= subtitle_track_y + track_height):
            return -1, None
        
        for i, subtitle in enumerate(self.subtitles):
            if subtitle.start_time <= click_time <= subtitle.end_time:
                start_x = self.time_to_x(subtitle.start_time)
                end_x = self.time_to_x(subtitle.end_time)
                
                edge_threshold = 8
                
                if pos.x() <= start_x + edge_threshold:
                    return i, 'resize_left'
                elif pos.x() >= end_x - edge_threshold:
                    return i, 'resize_right'
                else:
                    return i, 'move'
        
        return -1, None
    
    def add_subtitle_at_time(self, time_pos):
        """在指定时间位置添加新字幕"""
        default_duration = 3.0
        start_time = max(0, time_pos)
        end_time = min(self.duration, start_time + default_duration)
        
        # Check if overlaps with existing subtitles
        if self.check_subtitle_overlap(start_time, end_time, -1):
            print(lang["msg.subtitle_overlap"])
            return -1
        
        # Get text content
        text_content = self.get_next_text_line()
        
        new_subtitle = SubtitleItem(
            text=text_content,
            start_time=start_time,
            end_time=end_time
        )
        
        # Insert in chronological order
        insert_index = 0
        for i, subtitle in enumerate(self.subtitles):
            if subtitle.start_time > start_time:
                break
            insert_index = i + 1
        
        self.subtitles.insert(insert_index, new_subtitle)
        self.selected_subtitle = insert_index
        
        self.subtitle_added.emit(start_time)
        self.update()
        
        print(lang["msg.subtitle_created"].format(index=insert_index + 1))
        return insert_index
    
    def get_next_text_line(self):
        """获取下一句文本"""
        parent = self.parent()
        while parent and not hasattr(parent, 'imported_text_lines'):
            parent = parent.parent()
        
        if parent and hasattr(parent, 'imported_text_lines') and parent.imported_text_lines:
            if parent.current_text_line_index >= len(parent.imported_text_lines):
                parent.current_text_line_index = 0
            
            current_index = parent.current_text_line_index
            sentence = parent.imported_text_lines[current_index]
            parent.current_text_line_index += 1
            
            return str(sentence).strip()
        else:
            return lang["msg.timeline_subtitle"]
    
    def check_subtitle_overlap(self, start_time, end_time, exclude_index=-1):
        """检查字幕时间是否重叠"""
        for i, subtitle in enumerate(self.subtitles):
            if i == exclude_index:
                continue
            
            # Check overlap: new subtitle start time < existing subtitle end time AND new subtitle end time > existing subtitle start time
            if start_time < subtitle.end_time and end_time > subtitle.start_time:
                return True
        
        return False
    
    def get_snap_points(self, exclude_index=-1):
        """获取所有吸附点"""
        snap_points = []
        
        # Add time scale snap points - intelligent adaptive
        display_duration = self.zoom_end - self.zoom_start
        if display_duration <= 10:
            interval = 1.0  # 1秒
        elif display_duration <= 30:
            interval = 2.0  # 2秒
        elif display_duration <= 60:
            interval = 5.0  # 5秒
        elif display_duration <= 300:
            interval = 30.0  # 30秒
        elif display_duration <= 600:
            interval = 60.0  # 1分钟
        elif display_duration <= 1800:
            interval = 300.0  # 5分钟
        elif display_duration <= 3600:
            interval = 600.0  # 10分钟
        elif display_duration <= 7200:
            interval = 1200.0  # 20分钟
        else:
            interval = 1800.0  # 30分钟
        
        # Generate time scale snap points
        start_tick = int(self.zoom_start / interval) * interval
        current_tick = start_tick
        while current_tick <= self.zoom_end:
            if current_tick >= self.zoom_start:
                snap_points.append(current_tick)
            current_tick += interval
        
        # Add subtitle edge snap points - including start and end times of all subtitles
        for i, subtitle in enumerate(self.subtitles):
            if i != exclude_index:
                snap_points.append(subtitle.start_time)
                snap_points.append(subtitle.end_time)
        
        # Add intelligent subtitle block snap points
        subtitle_snap_points = self.get_subtitle_snap_points(exclude_index)
        snap_points.extend(subtitle_snap_points)
        
        # Only add playback position snap points when snap function is enabled
        if self.snap_enabled:
            snap_points.append(self.current_position)
        
        return sorted(list(set(snap_points)))  # Remove duplicates and sort
    
    def snap_time(self, time_value, snap_points):
        """吸附时间到最近的吸附点"""
        if not self.snap_enabled or not snap_points:
            return time_value
        
        min_distance = float('inf')
        snapped_time = time_value
        
        for snap_point in snap_points:
            distance = abs(time_value - snap_point)
            if distance < min_distance and distance <= self.snap_threshold:
                min_distance = distance
                snapped_time = snap_point
        
        return snapped_time
    
    def get_subtitle_snap_points(self, exclude_index=-1):
        """获取字幕块之间的智能吸附点"""
        snap_points = []
        
        if exclude_index >= 0 and exclude_index < len(self.subtitles):
            current_subtitle = self.subtitles[exclude_index]
            
            for i, subtitle in enumerate(self.subtitles):
                if i == exclude_index:
                    continue
                
                # Current subtitle end time snaps to other subtitle start time
                if abs(current_subtitle.end_time - subtitle.start_time) < 1.0:  # 1秒内的距离
                    snap_points.append(subtitle.start_time)
                
                # Current subtitle start time snaps to other subtitle end time
                if abs(current_subtitle.start_time - subtitle.end_time) < 1.0:  # 1秒内的距离
                    snap_points.append(subtitle.end_time)
                
                # Current subtitle start time snaps to other subtitle start time (left align)
                if abs(current_subtitle.start_time - subtitle.start_time) < 1.0:
                    snap_points.append(subtitle.start_time)
                
                # Current subtitle end time snaps to other subtitle end time (right align)
                if abs(current_subtitle.end_time - subtitle.end_time) < 1.0:
                    snap_points.append(subtitle.end_time)
        
        return snap_points
    
    def update_snap_lines(self, start_time, end_time, exclude_index=-1):
        """更新吸附线显示"""
        self.snap_lines = []
        
        if not self.snap_enabled:
            return
        
        snap_points = self.get_snap_points(exclude_index)
        
        # Check start time snap
        snapped_start = self.snap_time(start_time, snap_points)
        if snapped_start != start_time:
            self.snap_lines.append(('start', snapped_start))
        
        # Check end time snap
        snapped_end = self.snap_time(end_time, snap_points)
        if snapped_end != end_time:
            self.snap_lines.append(('end', snapped_end))
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # Use dark background to ensure consistency with overall interface
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        width = self.width()
        height = self.height()
        
        if self.duration <= 0:
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawText(self.rect(), Qt.AlignCenter, 
                lang["subtitle_editor_welcome"])
            return
        
        display_duration = self.zoom_end - self.zoom_start
        if display_duration <= 0:
            return
        
        # Draw timeline background
        ruler_height = 50
        painter.fillRect(0, 0, width, ruler_height, QColor(35, 35, 35))
        
        # Draw ruler border
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.drawRect(0, 0, width, ruler_height)
        
        # Draw time scale
        painter.setPen(QPen(QColor(180, 180, 180), 1))
        painter.setFont(QFont("Arial", 10))
        
        # Determine scale interval based on zoom level - intelligent adaptive
        if display_duration <= 10:
            major_interval = 1.0  # 1秒
            minor_interval = 0.2  # 0.2秒
        elif display_duration <= 30:
            major_interval = 2.0  # 2秒
            minor_interval = 0.5  # 0.5秒
        elif display_duration <= 60:
            major_interval = 5.0  # 5秒
            minor_interval = 1.0  # 1秒
        elif display_duration <= 300:
            major_interval = 30.0  # 30秒
            minor_interval = 5.0   # 5秒
        elif display_duration <= 600:
            major_interval = 60.0  # 1分钟
            minor_interval = 10.0  # 10秒
        elif display_duration <= 1800:
            major_interval = 300.0  # 5分钟
            minor_interval = 60.0   # 1分钟
        elif display_duration <= 3600:
            major_interval = 600.0  # 10分钟
            minor_interval = 120.0  # 2分钟
        elif display_duration <= 7200:
            major_interval = 1200.0  # 20分钟
            minor_interval = 300.0   # 5分钟
        else:
            major_interval = 1800.0  # 30分钟
            minor_interval = 600.0   # 10分钟
        
        # Draw major scales
        start_tick = int(self.zoom_start / major_interval) * major_interval
        current_tick = start_tick
        
        while current_tick <= self.zoom_end:
            if current_tick >= self.zoom_start:
                x = self.time_to_x(current_tick)
                if 0 <= x <= width:
                    # Major scale lines
                    painter.setPen(QPen(QColor(200, 200, 200), 2))
                    painter.drawLine(int(x), 0, int(x), ruler_height)
                    
                    # Time label
                    painter.setPen(QPen(QColor(255, 255, 255), 1))
                    painter.setFont(QFont("Arial", 11, QFont.Bold))
                    time_label = self.format_time_label(current_tick)
                    
                    # Ensure labels don't exceed boundaries
                    text_width = painter.fontMetrics().width(time_label)
                    label_x = max(3, min(int(x) + 3, width - text_width - 3))
                    painter.drawText(label_x, 15, time_label)
            current_tick += major_interval
        
        # Draw minor scales
        start_minor = int(self.zoom_start / minor_interval) * minor_interval
        current_minor = start_minor
        
        while current_minor <= self.zoom_end:
            if current_minor >= self.zoom_start and current_minor % major_interval != 0:
                x = self.time_to_x(current_minor)
                if 0 <= x <= width:
                    painter.setPen(QPen(QColor(120, 120, 120), 1))
                    painter.drawLine(int(x), ruler_height - 15, int(x), ruler_height)
            current_minor += minor_interval
        
        # Draw scale background grid lines
        painter.setPen(QPen(QColor(60, 60, 60), 1, Qt.DotLine))
        for i in range(0, width, 50):  # One grid line every 50 pixels
            painter.drawLine(i, ruler_height, i, height)
        
        # Draw subtitle track area - use more prominent colors
        subtitle_track_y = 60
        track_height = 60
        painter.fillRect(0, subtitle_track_y, width, track_height, QColor(50, 50, 50))  # Slightly brighter background
        
        # Draw track border
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawRect(0, subtitle_track_y, width, track_height)
        
        # Draw subtitle track label - use more prominent colors
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(10, subtitle_track_y - 10, lang["label.subtitle_track"])
        
        # Draw subtitle blocks
        for i, subtitle in enumerate(self.subtitles):
            if subtitle.end_time < self.zoom_start or subtitle.start_time > self.zoom_end:
                continue
            
            start_x = self.time_to_x(subtitle.start_time)
            end_x = self.time_to_x(subtitle.end_time)
            
            start_x = max(0, start_x)
            end_x = min(width, end_x)
            
            if end_x - start_x < 3:
                end_x = start_x + 3
            
            # Subtitle block colors - use more prominent colors
            if i == self.selected_subtitle:
                if self.dragging:
                    color = QColor(255, 180, 80)  # Orange
                    border_color = QColor(255, 120, 0)  # Dark orange
                else:
                    color = QColor(80, 220, 120)  # Bright green
                    border_color = QColor(0, 255, 100)  # Bright green边框
            else:
                color = QColor(100, 150, 220)  # Bright blue
                border_color = QColor(120, 180, 255)  # Bright blue边框
            
            # Draw subtitle blocks主体
            rect = QRect(int(start_x), subtitle_track_y + 8, int(end_x - start_x), track_height - 16)
            
            # Gradient effect
            gradient = QLinearGradient(0, rect.top(), 0, rect.bottom())
            gradient.setColorAt(0, color.lighter(120))
            gradient.setColorAt(1, color.darker(120))
            painter.fillRect(rect, QBrush(gradient))
            
            # Border
            painter.setPen(QPen(border_color, 2))
            painter.drawRect(rect)
            
            # Draw drag handles for selected state
            if i == self.selected_subtitle:
                handle_size = 12
                handle_y = subtitle_track_y + track_height // 2 - handle_size // 2
                
                # Left handle - use more coordinated colors
                left_handle = QRect(int(start_x) - handle_size//2, handle_y, handle_size, handle_size)
                # Dark gray background, more coordinated
                painter.fillRect(left_handle, QColor(60, 60, 60))
                # Bright border, echoing subtitle block colors
                painter.setPen(QPen(QColor(200, 200, 200), 2))
                painter.drawRect(left_handle)
                # Add internal indicator lines
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawLine(left_handle.center().x() - 2, left_handle.center().y(), 
                               left_handle.center().x() + 2, left_handle.center().y())
                
                # Right handle - use more coordinated colors
                right_handle = QRect(int(end_x) - handle_size//2, handle_y, handle_size, handle_size)
                # Dark gray background, more coordinated
                painter.fillRect(right_handle, QColor(60, 60, 60))
                # Bright border, echoing subtitle block colors
                painter.setPen(QPen(QColor(200, 200, 200), 2))
                painter.drawRect(right_handle)
                # Add internal indicator lines
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawLine(right_handle.center().x() - 2, right_handle.center().y(), 
                               right_handle.center().x() + 2, right_handle.center().y())
            
            # Draw subtitle number and text
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            
            # Number - increase width to support more digits
            number_rect = QRect(int(start_x) + 4, subtitle_track_y + 10, 35, 16)
            painter.drawText(number_rect, Qt.AlignLeft | Qt.AlignTop, f"#{i+1}")
            
            # Text content - align with number
            if end_x - start_x > 40:  # Increase minimum width requirement
                text_rect = QRect(int(start_x) + 39, subtitle_track_y + 28, int(end_x - start_x) - 43, 20)
                max_chars = max(3, int((end_x - start_x - 43) / 7))
                text = subtitle.text[:max_chars] + "..." if len(subtitle.text) > max_chars else subtitle.text
                painter.setFont(QFont("Arial", 9))
                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignTop, text)
        
        # Draw playback position line - 100% accurate
        if self.zoom_start <= self.current_position <= self.zoom_end:
            pos_x = self.time_to_x(self.current_position)
            
            # Playback line
            painter.setPen(QPen(QColor(255, 50, 50), 3))
            painter.drawLine(int(pos_x), 0, int(pos_x), height)
            
            # Playback head
            play_head = QPolygon([
                QPoint(int(pos_x) - 8, 0),
                QPoint(int(pos_x) + 8, 0),
                QPoint(int(pos_x), 16)
            ])
            painter.setBrush(QBrush(QColor(255, 50, 50)))
            painter.drawPolygon(play_head)
            
            # Time label
            painter.setPen(QPen(QColor(255, 255, 0), 1))
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            time_str = self.format_time_precise(self.current_position)
            
            # Background
            text_width = 80
            text_rect = QRect(int(pos_x) - text_width//2, height - 25, text_width, 20)
            painter.fillRect(text_rect, QColor(0, 0, 0, 180))
            painter.setPen(QPen(QColor(255, 255, 0), 1))
            painter.drawText(text_rect, Qt.AlignCenter, f"▶ {time_str}")
        
        # Draw subtitle block creation preview
        if self.creating_subtitle:
            start_x = self.time_to_x(self.create_start_time)
            end_x = self.time_to_x(self.create_end_time)
            
            start_x = max(0, start_x)
            end_x = min(width, end_x)
            
            if end_x - start_x < 3:
                end_x = start_x + 3
            
            preview_rect = QRect(int(start_x), subtitle_track_y + 8, int(end_x - start_x), track_height - 16)
            painter.fillRect(preview_rect, QColor(255, 200, 100, 150))
            painter.setPen(QPen(QColor(255, 150, 50), 2, Qt.DashLine))
            painter.drawRect(preview_rect)
            
            # Display time information
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            duration = self.create_end_time - self.create_start_time
            time_text = f"{duration:.1f}s"
            painter.drawText(preview_rect, Qt.AlignCenter, time_text)
        
        # Display sync status
        painter.setPen(QPen(QColor(0, 255, 0), 1))
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(10, height - 10, lang["label.timeline_mode"])
        
        # Draw snap lines
        if self.snap_enabled and self.snap_lines:
            painter.setPen(QPen(QColor(255, 255, 0), 2, Qt.DashLine))
            for snap_type, snap_time in self.snap_lines:
                if self.zoom_start <= snap_time <= self.zoom_end:
                    snap_x = self.time_to_x(snap_time)
                    painter.drawLine(int(snap_x), 0, int(snap_x), height)
        
        # Display zoom information
        if self.is_zoomed:
            zoom_info = f"📍 {self.format_time_label(self.zoom_start)} - {self.format_time_label(self.zoom_end)}"
            painter.setPen(QPen(QColor(150, 150, 150), 1))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(width - 150, height - 10, zoom_info)
        
        # Display snap status
        if self.snap_enabled:
            snap_info = lang["label.snap_enabled"]
            painter.setPen(QPen(QColor(0, 255, 0), 1))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(10, height - 30, snap_info)
    
    def format_time_label(self, seconds):
        """格式化时间标签 - 智能自适应"""
        if seconds < 3600:  # Less than 1 hour
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes:02d}:{secs:02d}"
        else:  # Greater than or equal to 1 hour
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours:02d}:{minutes:02d}"
    
    def format_time_precise(self, seconds):
        """格式化精确时间 - 智能自适应"""
        if seconds < 3600:  # Less than 1 hour
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes:02d}:{secs:05.2f}"
        else:  # Greater than or equal to 1 hour
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            # Gain focus to receive keyboard events
            self.setFocus()
            
            # Check if in timeline area (for jumping)
            if pos.y() <= 50:
                new_time = self.x_to_time(pos.x())
                new_time = max(0, min(self.duration, new_time))
                self.current_position = new_time
                self.position_changed.emit(new_time)
                # Trigger playback
                self.play_triggered.emit()
                self.update()
                return
            
            subtitle_index, drag_type = self.get_subtitle_at_pos(pos)
            
            if subtitle_index >= 0:
                # Select existing subtitle block
                self.selected_subtitle = subtitle_index
                self.drag_mode = drag_type
                self.dragging = True
                self.drag_start_pos = pos
                self.drag_start_time = self.x_to_time(pos.x())
                
                subtitle = self.subtitles[subtitle_index]
                self.original_start_time = subtitle.start_time
                self.original_end_time = subtitle.end_time
                
                if drag_type in ['resize_left', 'resize_right']:
                    self.setCursor(Qt.SizeHorCursor)
                else:
                    self.setCursor(Qt.ClosedHandCursor)
                
                self.subtitle_selected.emit(subtitle_index)
            else:
                subtitle_track_y = 60
                track_height = 60
                
                if subtitle_track_y <= pos.y() <= subtitle_track_y + track_height:
                    # Start creating new subtitle block in subtitle track area
                    self.creating_subtitle = True
                    self.create_start_time = self.x_to_time(pos.x())
                    self.create_end_time = self.create_start_time
                    self.setCursor(Qt.CrossCursor)
            
            self.update()
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        
        # Mouse hover effect
        if not self.dragging and not self.creating_subtitle:
            if pos.y() <= 50:
                self.setCursor(Qt.PointingHandCursor)
            else:
                subtitle_index, drag_type = self.get_subtitle_at_pos(pos)
                
                if subtitle_index >= 0:
                    if drag_type in ['resize_left', 'resize_right']:
                        self.setCursor(Qt.SizeHorCursor)
                    elif drag_type == 'move':
                        self.setCursor(Qt.OpenHandCursor)
                else:
                    subtitle_track_y = 60
                    track_height = 60
                    
                    if subtitle_track_y <= pos.y() <= subtitle_track_y + track_height:
                        self.setCursor(Qt.CrossCursor)
                    else:
                        self.setCursor(Qt.ArrowCursor)
        
        if self.creating_subtitle:
            # Creating subtitle block
            current_time = self.x_to_time(pos.x())
            
            # Apply snap
            snap_points = self.get_snap_points(-1)
            snapped_time = self.snap_time(current_time, snap_points)
            
            if snapped_time > self.create_start_time:
                self.create_end_time = snapped_time
            else:
                self.create_end_time = self.create_start_time
                self.create_start_time = snapped_time
            
            # Update snap line display
            self.update_snap_lines(self.create_start_time, self.create_end_time, -1)
            self.update()
            
        elif self.dragging and self.selected_subtitle >= 0:
            # Drag existing subtitle block
            current_time = self.x_to_time(pos.x())
            time_delta = current_time - self.drag_start_time
            
            subtitle = self.subtitles[self.selected_subtitle]
            
            if self.drag_mode == 'move':
                duration = self.original_end_time - self.original_start_time
                new_start = max(0, self.original_start_time + time_delta)
                new_end = min(self.duration, new_start + duration)
                
                # If hitting right boundary, adjust start time
                if new_end == self.duration:
                    new_start = max(0, self.duration - duration)
                    new_end = new_start + duration
                
                # Apply snap
                snap_points = self.get_snap_points(self.selected_subtitle)
                snapped_start = self.snap_time(new_start, snap_points)
                snapped_end = snapped_start + duration
                
                # Ensure not exceeding boundaries
                if snapped_end > self.duration:
                    snapped_end = self.duration
                    snapped_start = self.duration - duration
                
                # Check if overlapping after movement
                if not self.check_subtitle_overlap(snapped_start, snapped_end, self.selected_subtitle):
                    subtitle.start_time = snapped_start
                    subtitle.end_time = snapped_end
                    
                    # Update snap line display
                    self.update_snap_lines(snapped_start, snapped_end, self.selected_subtitle)
                
            elif self.drag_mode == 'resize_left':
                new_start = max(0, self.original_start_time + time_delta)
                new_start = min(new_start, subtitle.end_time - 0.1)
                
                # Apply snap
                snap_points = self.get_snap_points(self.selected_subtitle)
                snapped_start = self.snap_time(new_start, snap_points)
                snapped_start = min(snapped_start, subtitle.end_time - 0.1)
                
                # 检查调整后是否重叠
                if not self.check_subtitle_overlap(snapped_start, subtitle.end_time, self.selected_subtitle):
                    subtitle.start_time = snapped_start
                    # Update snap line display
                    self.update_snap_lines(snapped_start, subtitle.end_time, self.selected_subtitle)
                
            elif self.drag_mode == 'resize_right':
                new_end = min(self.duration, self.original_end_time + time_delta)
                new_end = max(new_end, subtitle.start_time + 0.1)
                
                # Apply snap
                snap_points = self.get_snap_points(self.selected_subtitle)
                snapped_end = self.snap_time(new_end, snap_points)
                snapped_end = max(snapped_end, subtitle.start_time + 0.1)
                
                # 检查调整后是否重叠
                if not self.check_subtitle_overlap(subtitle.start_time, snapped_end, self.selected_subtitle):
                    subtitle.end_time = snapped_end
                    # Update snap line display
                    self.update_snap_lines(subtitle.start_time, snapped_end, self.selected_subtitle)
            
            self.subtitle_changed.emit(self.selected_subtitle, subtitle.start_time, subtitle.end_time)
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.creating_subtitle:
                # 完成创建字幕块
                if abs(self.create_end_time - self.create_start_time) >= 0.5:  # 最小0.5秒
                    # 确保时间顺序正确
                    start_time = min(self.create_start_time, self.create_end_time)
                    end_time = max(self.create_start_time, self.create_end_time)
                    
                    # 先检查是否可创建（不重叠等）
                    if not self.check_subtitle_overlap(start_time, end_time, -1):
                        # ✅ 只有确认能创建时，才取下一句并推进索引
                        subtitle_text = self.get_next_text_line()
                        
                        new_subtitle = SubtitleItem(
                            text=str(subtitle_text),
                            start_time=start_time,
                            end_time=end_time
                        )
                        
                        insert_index = 0
                        for i, subtitle in enumerate(self.subtitles):
                            if subtitle.start_time > start_time:
                                break
                            insert_index = i + 1
                        
                        self.subtitles.insert(insert_index, new_subtitle)
                        self.selected_subtitle = insert_index
                        self.subtitle_added.emit(start_time)
                    else:
                        print(lang["msg.subtitle_overlap"])
                else:
                    print(lang["msg.duration_short"])
                
                self.creating_subtitle = False
                self.create_start_time = 0
                self.create_end_time = 0
                
            elif self.dragging:
                # 完成拖拽
                self.dragging = False
                self.drag_mode = None
                # 清除吸附线
                self.snap_lines = []
            
            self.setCursor(Qt.ArrowCursor)
            self.update()

    def wheelEvent(self, event):
        """鼠标滚轮缩放时间轴 - 跟随播放位置"""
        if self.duration <= 0:
            print(lang["msg.skip_zoom"])
            return

        # 缩放因子
        zoom_factor = 1.3 if event.angleDelta().y() > 0 else 1 / 1.3

        # 计算新的显示范围
        display_duration = self.zoom_end - self.zoom_start
        new_duration = display_duration / zoom_factor

        # 限制最小和最大显示范围
        min_duration = 1.0   # 最小显示1秒
        max_duration = max(self.duration, 1.0)  # 防止0

        new_duration = max(min_duration, min(max_duration, new_duration))

        # 以当前播放位置为中心进行缩放
        center = self.current_position
        new_start = center - new_duration / 2
        new_end = center + new_duration / 2

        # 边界处理
        if new_start < 0:
            new_start = 0
            new_end = new_duration
        if new_end > self.duration:
            new_end = self.duration
            new_start = self.duration - new_duration

        self.zoom_start = max(0, new_start)
        self.zoom_end = min(self.duration, new_end)
        self.is_zoomed = (self.zoom_start > 0 or self.zoom_end < self.duration)

        print(lang["msg.zoom_info"].format(start=self.zoom_start, end=self.zoom_end, duration=self.duration))

        self.update()

    def show_context_menu(self, pos):
        """右键菜单"""
        menu = QMenu(self)
        
        subtitle_index, _ = self.get_subtitle_at_pos(pos)
        
        if subtitle_index >= 0:
            menu.addAction(lang["context.edit_text"], lambda: self.subtitle_selected.emit(subtitle_index))
            menu.addAction(lang["context.delete_subtitle"], lambda: self.delete_subtitle(subtitle_index))
            menu.addSeparator()
        
        # 添加字幕
        add_action = menu.addAction(lang["context.add_subtitle_here"])
        add_action.triggered.connect(lambda: self.add_subtitle_at_time(self.x_to_time(pos.x())))
        
        menu.addSeparator()
        
        # 视图操作
        menu.addAction(lang["context.fit_all"], self.reset_zoom)
        menu.addAction(lang["context.zoom_to_selection"], self.zoom_to_selection)
        
        menu.exec_(self.mapToGlobal(pos))

    def delete_subtitle(self, index):
        """删除字幕"""
        if 0 <= index < len(self.subtitles):
            del self.subtitles[index]
            
            if self.selected_subtitle == index:
                self.selected_subtitle = -1
            elif self.selected_subtitle > index:
                self.selected_subtitle -= 1
            
            self.subtitle_deleted.emit(index)
            self.update()

    def reset_zoom(self):
        """重置缩放，显示全部"""
        self.zoom_start = 0.0
        self.zoom_end = self.duration
        self.is_zoomed = False
        self.update()

    def zoom_to_selection(self):
        """缩放到选中的字幕"""
        if 0 <= self.selected_subtitle < len(self.subtitles):
            subtitle = self.subtitles[self.selected_subtitle]
            
            # 在字幕前后留一些空间
            padding = max(2.0, (subtitle.end_time - subtitle.start_time) * 0.5)
            
            self.zoom_start = max(0, subtitle.start_time - padding)
            self.zoom_end = min(self.duration, subtitle.end_time + padding)
            self.is_zoomed = True
            
            self.update()

class TimelineSubtitleTool(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.audio_file = None
        self.subtitles = []
        self.current_subtitle_index = -1
        
        # 文本管理
        self.imported_text_lines = []
        self.current_text_line_index = 0
        
        # 音频播放器
        self.media_player = QMediaPlayer()
        self.media_player.positionChanged.connect(self.on_position_changed)
        self.media_player.stateChanged.connect(self.on_player_state_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        
        # 播放状态
        self.is_playing = False
        self.current_playback_position = 0.0
        self.is_seeking = False
        
        # 平滑播放位置更新定时器
        self.position_update_timer = QTimer()
        self.position_update_timer.timeout.connect(self.update_smooth_position)
        self.position_update_timer.setInterval(50)
        
        self.init_ui()
        print(lang["msg.timeline_init"])
    
    def init_ui(self):
        self.setWindowTitle(lang["app.title"])
        self.setGeometry(100, 100, 1600, 900)
        
        # 深色主题
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QPushButton { 
                background-color: #2d2d30; color: #ffffff; border: 1px solid #3e3e42;
                padding: 8px 16px; border-radius: 3px; font-size: 13px;
            }
            QPushButton:hover { background-color: #3e3e42; }
            QPushButton:pressed { background-color: #007acc; }
            QLabel { color: #cccccc; font-size: 13px; }
            QTextEdit { 
                background-color: #252526; color: #cccccc; 
                border: 1px solid #ffffff; font-size: 14px; 
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QListWidget { 
                background-color: #252526; color: #cccccc; 
                border: 1px solid #ffffff; font-size: 13px;
            }
            QListWidget::item:selected { background-color: #094771; }
            QStatusBar { background-color: #007acc; color: #ffffff; font-size: 13px; }
            QLineEdit { 
                background-color: #252526; color: #cccccc; 
                border: 1px solid #3e3e42; padding: 4px; 
            }
            
            /* ===== Scrollbar（文本显示区 / 文本列表）===== */
            QScrollBar:vertical {
                background: #2b2b2b;
                width: 12px;
                margin: 2px 2px 2px 2px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #5e5e5e;
                min-height: 28px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover  { background: #7a7a7a; }
            QScrollBar::handle:vertical:pressed{ background: #4a4a4a; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

            QScrollBar:horizontal {
                background: #2b2b2b;
                height: 12px;
                margin: 2px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: #5e5e5e;
                min-width: 28px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover  { background: #7a7a7a; }
            QScrollBar::handle:horizontal:pressed{ background: #4a4a4a; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }

                            /* ===== Slider（播放器进度条 / 音量条等）===== */
                QSlider::groove:horizontal {
                    background: #2b2b2b;  /* 统一浅黑背景 */
                    height: 12px;
                    border-radius: 6px;
                    margin: 0 6px;
                    border: none;
                }
                QSlider::handle:horizontal {
                    background: #5e5e5e;  /* 统一滚动条颜色 */
                    width: 20px; height: 20px;
                    margin: -4px 0;                 /* 让手柄垂直居中到槽里 */
                    border-radius: 2px;  /* 方形，接近滚动条 */
                    border: none;
                }
                QSlider::handle:horizontal:hover  { background: #7a7a7a; }
                QSlider::handle:horizontal:pressed{ background: #4a4a4a; }

                QSlider::groove:vertical {
                    background: #2b2b2b;  /* 统一浅黑背景 */
                    width: 12px;
                    border-radius: 6px;
                    margin: 6px 0;
                    border: none;
                }
                QSlider::handle:vertical {
                    background: #5e5e5e;  /* 统一滚动条颜色 */
                    width: 20px; height: 20px;
                    margin: 0 -4px;
                    border-radius: 2px;  /* 方形，接近滚动条 */
                    border: none;
                }
                QSlider::handle:vertical:hover  { background: #7a7a7a; }
                QSlider::handle:vertical:pressed{ background: #4a4a4a; }

                            /* ===== 进度条专属样式（统一深色主题）===== */
                #progressSlider::groove:horizontal {
                    background: #2b2b2b;  /* 浅黑背景 */
                    height: 12px;
                    margin: 0 6px;
                    border-radius: 6px;
                    border: none;
                }
                #progressSlider::handle:horizontal {
                    background: #5e5e5e;  /* 统一滚动条颜色 */
                    width: 20px;
                    height: 20px;
                    margin: -4px 0;      /* 让手柄居中到槽里 */
                    border-radius: 2px;  /* 方形，接近滚动条 */
                    border: none;
                }
                #progressSlider::handle:horizontal:hover {
                    background: #7a7a7a;  /* 统一滚动条悬停色 */
                }
                #progressSlider::handle:horizontal:pressed {
                    background: #4a4a4a;  /* 统一滚动条按下色 */
                }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # 菜单栏
        self.create_menu_bar()
        
        # 工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 播放控制栏
        playback_control = self.create_playback_control()
        layout.addWidget(playback_control)
        
        # 时间轴编辑器
        self.timeline = TimelineEditor()
        self.timeline.position_changed.connect(self.seek_to_position)
        self.timeline.play_triggered.connect(self.play_pause)
        self.timeline.subtitle_added.connect(self.on_subtitle_added)
        self.timeline.subtitle_selected.connect(self.on_subtitle_selected)
        self.timeline.subtitle_changed.connect(self.on_subtitle_changed)
        self.timeline.subtitle_deleted.connect(self.on_subtitle_deleted)
        
        self.timeline_label = QLabel(lang["label.timeline"])
        self.timeline_label.setStyleSheet("color: #00ff00; font-weight: bold; padding: 5px;")
        layout.addWidget(self.timeline_label)
        layout.addWidget(self.timeline, 1)
        
        # 字幕块区域 - 缩小高度
        self.subtitle_blocks_label = QLabel(lang["label.subtitle_blocks"])
        self.subtitle_blocks_label.setStyleSheet("color: #ffffff; font-weight: bold; padding: 5px;")
        layout.addWidget(self.subtitle_blocks_label)
        
        # 字幕块显示区域 - 减小高度
        subtitle_blocks_widget = QWidget()
        subtitle_blocks_widget.setFixedHeight(40)  # 从80改为40
        subtitle_blocks_widget.setStyleSheet("background-color: #2d2d30; border: 1px solid #3e3e42;")
        layout.addWidget(subtitle_blocks_widget)
        
        # 底部分为两部分：文本显示区 和 文本列表 - 增加权重
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：文本显示区
        text_display_panel = self.create_text_display_panel()
        
        # 右侧：文本列表
        text_list_panel = self.create_text_list_panel()
        
        bottom_splitter.addWidget(text_display_panel)
        bottom_splitter.addWidget(text_list_panel)
        bottom_splitter.setSizes([600, 400])
        
        # 给底部更多空间 - 增加权重
        layout.addWidget(bottom_splitter, 2)  # 添加权重2，让底部区域占更多空间
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(lang["msg.timeline_mode"])
        
        # 同步状态显示
        self.sync_status_label = QLabel(lang["label.sync_status"])
        self.sync_status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.status_bar.addPermanentWidget(self.sync_status_label)
        
        # 设置焦点策略，使窗口可以接收键盘事件
        self.setFocusPolicy(Qt.StrongFocus)
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu(lang["menu.file"])
        file_menu.addAction(f'📁 {lang["btn.import_audio"]}', self.import_audio)
        file_menu.addAction(f'📝 {lang["btn.import_text"]}', self.import_text)
        file_menu.addSeparator()
        file_menu.addAction(f'💾 {lang["btn.save_project"]}', self.save_project)
        file_menu.addAction(f'📂 {lang["btn.open_project"]}', self.open_project)
        file_menu.addSeparator()
        file_menu.addAction(f'📤 {lang["btn.export_srt"]}', self.export_subtitle)
        
        # 编辑菜单
        edit_menu = menubar.addMenu(lang["menu.edit"])
        
        # 语言菜单
        language_menu = menubar.addMenu(lang["menu.language"])
        zh_action = language_menu.addAction(lang["lang.zh"])
        en_action = language_menu.addAction(lang["lang.en"])
        zh_action.triggered.connect(lambda: self.change_language('zh'))
        en_action.triggered.connect(lambda: self.change_language('en'))
        edit_menu.addAction(f'🗑️ {lang["btn.delete"]}', self.delete_current_subtitle)
        edit_menu.addAction(f'🔄 {lang["btn.reset"]}', self.reset_text_index)
        
        # 视图菜单
        view_menu = menubar.addMenu(lang["menu.view"])
        view_menu.addAction(f'🔍 {lang["btn.fit_all"]}', self.fit_all)
        view_menu.addAction(f'🔍+ {lang["btn.zoom_in"]}', self.zoom_in)
        view_menu.addAction(f'🔍- {lang["btn.zoom_out"]}', self.zoom_out)
        view_menu.addSeparator()
        
        # 吸附菜单项
        snap_action = QAction(f'🔗 {lang["btn.snap"]}', self)
        snap_action.setCheckable(True)
        snap_action.setChecked(True)
        snap_action.triggered.connect(self.toggle_snap)
        view_menu.addAction(snap_action)
        self.snap_action = snap_action
        
        # 帮助菜单
        help_menu = menubar.addMenu(lang["menu.help"])
        help_menu.addAction(f'💡 {lang["btn.operation_help"]}', self.show_help)
        help_menu.addAction(f'ℹ️ {lang["btn.about"]}', self.show_about)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        
        # 文件操作
        self.btn_import_audio = QPushButton(f"📁 {lang['btn.import_audio']}")
        self.btn_import_text = QPushButton(f"📝 {lang['btn.import_text']}")
        self.btn_save_project = QPushButton(f"💾 {lang['btn.save_project']}")
        self.btn_open_project = QPushButton(f"📂 {lang['btn.open_project']}")
        self.btn_export = QPushButton(f"📤 {lang['btn.export_srt']}")
        
        self.btn_import_audio.clicked.connect(self.import_audio)
        self.btn_import_text.clicked.connect(self.import_text)
        self.btn_save_project.clicked.connect(self.save_project)
        self.btn_open_project.clicked.connect(self.open_project)
        self.btn_export.clicked.connect(self.export_subtitle)
        
        # 字幕操作
        self.btn_delete_subtitle = QPushButton(f"🗑️ {lang['btn.delete']}")
        self.btn_delete_subtitle.clicked.connect(self.delete_current_subtitle)
        
        # 视图操作
        self.btn_fit_all = QPushButton(f"🔍 {lang['btn.fit_all']}")
        self.btn_fit_all.clicked.connect(self.fit_all)
        
        self.btn_zoom_in = QPushButton(f"🔍+ {lang['btn.zoom_in']}")
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        
        self.btn_zoom_out = QPushButton(f"🔍- {lang['btn.zoom_out']}")
        self.btn_zoom_out.clicked.connect(self.zoom_out)
        
        # Snap functionality
        self.btn_toggle_snap = QPushButton(f"🔗 {lang['btn.snap']}")
        self.btn_toggle_snap.setCheckable(True)
        self.btn_toggle_snap.setChecked(True)
        self.btn_toggle_snap.clicked.connect(self.toggle_snap)
        # 设置切换按钮样式
        self.btn_toggle_snap.setStyleSheet("""
            QPushButton {
                background-color: #2d2d30; 
                color: #ffffff; 
                border: 1px solid #3e3e42;
                padding: 8px 16px; 
                border-radius: 3px; 
                font-size: 13px;
            }
            QPushButton:hover { 
                background-color: #3e3e42; 
            }
            QPushButton:pressed { 
                background-color: #007acc; 
            }
            QPushButton:checked {
                background-color: #4CAF50;
                border: 1px solid #45a049;
                color: #ffffff;
            }
            QPushButton:checked:hover {
                background-color: #45a049;
            }
            QPushButton:!checked {
                background-color: #666666;
                border: 1px solid #555555;
                color: #cccccc;
            }
            QPushButton:!checked:hover {
                background-color: #777777;
            }
        """)
        
        # 文本操作
        self.btn_reset_text_index = QPushButton(f"🔄 {lang['btn.reset']}")
        self.btn_reset_text_index.clicked.connect(self.reset_text_index)
        
        # 布局
        toolbar_layout.addWidget(self.btn_import_audio)
        toolbar_layout.addWidget(self.btn_import_text)
        toolbar_layout.addWidget(QLabel(lang["label.separator"]))
        toolbar_layout.addWidget(self.btn_save_project)
        toolbar_layout.addWidget(self.btn_open_project)
        toolbar_layout.addWidget(QLabel(lang["label.separator"]))
        toolbar_layout.addWidget(self.btn_delete_subtitle)
        toolbar_layout.addWidget(QLabel(lang["label.separator"]))
        toolbar_layout.addWidget(self.btn_fit_all)
        toolbar_layout.addWidget(self.btn_zoom_in)
        toolbar_layout.addWidget(self.btn_zoom_out)
        toolbar_layout.addWidget(QLabel(lang["label.separator"]))
        toolbar_layout.addWidget(self.btn_toggle_snap)
        toolbar_layout.addWidget(QLabel(lang["label.separator"]))
        toolbar_layout.addWidget(self.btn_reset_text_index)
        toolbar_layout.addWidget(QLabel(lang["label.separator"]))
        toolbar_layout.addWidget(self.btn_export)
        toolbar_layout.addStretch()
        
        return toolbar_widget
    
    def create_playback_control(self):
        """创建播放控制栏"""
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(0, 5, 0, 5)
        
        # 播放控制按钮
        self.btn_play_pause = QPushButton("▶️")
        self.btn_play_pause.setFixedSize(50, 40)
        self.btn_play_pause.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.btn_play_pause.clicked.connect(self.play_pause)
        
        self.btn_stop = QPushButton("⏹️")
        self.btn_stop.setFixedSize(50, 40)
        self.btn_stop.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.btn_stop.clicked.connect(self.stop_playback)
        
        # 快进快退按钮
        self.btn_backward = QPushButton("⏪")
        self.btn_backward.setFixedSize(40, 40)
        self.btn_backward.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.btn_backward.clicked.connect(lambda: self.skip_time(-5))
        
        self.btn_forward = QPushButton("⏩")
        self.btn_forward.setFixedSize(40, 40)
        self.btn_forward.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.btn_forward.clicked.connect(lambda: self.skip_time(5))
        
        # 时间显示
        self.time_display = TimeDisplay()
        
        # 进度滑块
        self.progress_slider = ProgressSlider()
        self.progress_slider.position_changed.connect(self.on_progress_slider_changed)
        
        # 音量控制
        volume_label = QLabel(lang["label.volume"])
        volume_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.valueChanged.connect(lambda v: self.media_player.setVolume(v))
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #3e3e42; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #007acc; width: 12px; border-radius: 6px; }
        """)
        
        # 布局
        control_layout.addWidget(self.btn_backward)
        control_layout.addWidget(self.btn_play_pause)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_forward)
        control_layout.addWidget(QLabel(lang["label.separator"]))
        control_layout.addWidget(self.time_display)
        control_layout.addWidget(self.progress_slider, 1)
        control_layout.addWidget(volume_label)
        control_layout.addWidget(self.volume_slider)
        
        return control_widget
    
    def create_text_display_panel(self):
        """创建文本显示区"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 0, 5, 0)
        
        # ====== 新的文本编辑UI实现 ======
        self.text_group = QGroupBox(lang["group.text_area"], self)
        # 文本显示区 样式
        self.text_group.setStyleSheet("""
            QGroupBox {
                background-color: #2b2b2b;
                color: lightgray;
                font: 10pt "Consolas";
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        
        # 顶部工具栏（右侧靠齐）
        tool_row = QHBoxLayout()
        tool_row.addStretch(1)
        
        def std_icon(name):
            # 统一取标准图标（不同平台样式一致）
            return self.style().standardIcon(name)
        
        btn_edit   = QToolButton(self); btn_edit.setIcon(std_icon(QStyle.SP_FileDialogDetailedView))
        btn_save   = QToolButton(self); btn_save.setIcon(std_icon(QStyle.SP_DialogSaveButton))
        btn_cancel = QToolButton(self); btn_cancel.setIcon(std_icon(QStyle.SP_DialogCancelButton))
        
        btn_edit.setToolTip(f"{lang['btn.edit']} (Ctrl+E)")
        btn_save.setToolTip(f"{lang['btn.save_done']} (Ctrl+S)")
        btn_cancel.setToolTip(f"{lang['btn.cancel']} (Esc)")
        
        # 初始只显示"编辑"，保存/取消隐藏
        btn_save.setVisible(False)
        btn_cancel.setVisible(False)
        
        tool_row.addWidget(btn_cancel)
        tool_row.addWidget(btn_save)
        tool_row.addWidget(btn_edit)
        
        # 文本区
        self.text_display = QPlainTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setPlainText("\n".join(getattr(self, "imported_text_lines", [])))
        
        # 设置浅黑背景 + 浅灰文字
        self.text_display.setStyleSheet("""
            QPlainTextEdit {
                background-color: #2b2b2b;   /* 浅黑背景 */
                color: #f0f0f0;              /* 浅灰文字 */
                border: 1px solid #ffffff;   /* 白色边框 */
            }
        """)
        
        # 设置字体和大小（老版本用的是 Consolas 12pt）
        font = QFont("Consolas", 12)
        self.text_display.setFont(font)
        
        # 组装
        box = QVBoxLayout(self.text_group)
        box.addLayout(tool_row)
        box.addWidget(self.text_display)
        
        # ====== 逻辑与快捷键 ======
        self._original_text = None  # 用于取消恢复
        
        def enter_edit_mode():
            if not self.text_display.isReadOnly():
                return
            self._original_text = self.text_display.toPlainText()
            self.text_display.setReadOnly(False)
            btn_edit.setVisible(False)
            btn_save.setVisible(True)
            btn_cancel.setVisible(True)
            self.text_display.setFocus()
        
        def save_and_exit():
            if self.text_display.isReadOnly():
                return
            raw = self.text_display.toPlainText().replace("\r\n","\n").replace("\r","\n")
            lines = [ln.strip() for ln in raw.split("\n") if ln.strip()]
            # 二次确认清空
            if not lines:
                ret = QMessageBox.question(self, lang["msg.confirm"],
                                           lang["msg.confirm_clear"],
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if ret != QMessageBox.Yes:
                    return
            # 写回与重置索引
            self.imported_text_lines = lines
            self.current_text_line_index = 0
            # 同步显示与退出编辑
            self.text_display.setPlainText("\n".join(self.imported_text_lines))
            self.text_display.setReadOnly(True)
            btn_edit.setVisible(True)
            btn_save.setVisible(False)
            btn_cancel.setVisible(False)
            QMessageBox.information(self, lang["msg.success"], lang["msg.saved"].format(n=len(lines)))
        
        def cancel_edit():
            if self.text_display.isReadOnly():
                return
            # 恢复原文并退出编辑
            if self._original_text is not None:
                self.text_display.setPlainText(self._original_text)
            self.text_display.setReadOnly(True)
            btn_edit.setVisible(True)
            btn_save.setVisible(False)
            btn_cancel.setVisible(False)
        
        btn_edit.clicked.connect(enter_edit_mode)
        btn_save.clicked.connect(save_and_exit)
        btn_cancel.clicked.connect(cancel_edit)
        
        # 快捷键：Ctrl+E 编辑，Ctrl+S 保存，Esc 取消
        QShortcut(QKeySequence("Ctrl+E"), self, activated=enter_edit_mode)
        QShortcut(QKeySequence("Ctrl+S"), self, activated=save_and_exit)
        QShortcut(QKeySequence("Esc"),    self, activated=cancel_edit)
        
        # 时间调整
        time_group = QWidget()
        time_layout = QVBoxLayout(time_group)
        time_layout.setContentsMargins(0, 10, 0, 0)
        
        self.time_adjust_label = QLabel(lang["label.time_adjust"])
        time_layout.addWidget(self.time_adjust_label)
        
        # 开始时间
        start_layout = QHBoxLayout()
        self.start_label = QLabel(lang["label.start"])
        start_layout.addWidget(self.start_label)
        self.start_time_edit = QLineEdit()
        self.start_time_edit.setPlaceholderText("00:00.000")
        self.start_time_edit.returnPressed.connect(self.update_times_from_input)
        start_layout.addWidget(self.start_time_edit)
        time_layout.addLayout(start_layout)
        
        # 结束时间
        end_layout = QHBoxLayout()
        self.end_label = QLabel(lang["label.end"])
        end_layout.addWidget(self.end_label)
        self.end_time_edit = QLineEdit()
        self.end_time_edit.setPlaceholderText("00:02.000")
        self.end_time_edit.returnPressed.connect(self.update_times_from_input)
        end_layout.addWidget(self.end_time_edit)
        time_layout.addLayout(end_layout)
        
        # 时长显示
        self.duration_label = QLabel(lang["label.duration"])
        time_layout.addWidget(self.duration_label)
        
        # 确保文本显示区正确添加到布局中
        layout.addWidget(self.text_group)
        layout.addWidget(time_group)
        layout.addStretch()
        
        return panel
    
    def create_text_list_panel(self):
        """创建文本列表区"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 0, 0, 0)
        
        # 文本列表 GroupBox
        self.text_list_group = QGroupBox(lang["group.text_list"], self)
        
        # 文本列表 样式（保持一致）
        self.text_list_group.setStyleSheet("""
            QGroupBox {
                background-color: #2b2b2b;
                color: lightgray;
                font: 10pt "Consolas";
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        
        # 字幕列表 - 增加高度以显示更多字幕
        self.subtitle_list = QListWidget()
        self.subtitle_list.setMinimumHeight(250)  # 最小高度250像素
        self.subtitle_list.setMaximumHeight(350)  # 最大高度350像素
        self.subtitle_list.itemClicked.connect(self.on_subtitle_list_clicked)
        # 设置字体大小，提高可读性
        font = QFont("Arial", 9)
        self.subtitle_list.setFont(font)
        # 设置项目高度，让每个字幕条目更清晰
        self.subtitle_list.setSpacing(2)
        # 设置项目高度，支持多行文本显示
        self.subtitle_list.setUniformItemSizes(False)  # 允许不同高度的项目
        
        # 将字幕列表添加到GroupBox中
        group_layout = QVBoxLayout(self.text_list_group)
        group_layout.addWidget(self.subtitle_list)
        
        # 将GroupBox添加到主布局
        layout.addWidget(self.text_list_group)
        
        return panel
    
    def show_help(self):
        """显示操作说明"""
        help_text = f"""
{lang["help.title"]}

{lang["help.mouse"]}
{lang["help.mouse.click"]}
{lang["help.mouse.drag"]}
{lang["help.mouse.move"]}
{lang["help.mouse.resize"]}
{lang["help.mouse.right"]}
{lang["help.mouse.wheel"]}

{lang["help.snap"]}
{lang["help.snap.auto"]}
{lang["help.snap.align"]}
{lang["help.snap.toggle"]}

{lang["help.shortcuts"]}
{lang["help.shortcuts.space"]}
{lang["help.shortcuts.arrows"]}

{lang["help.project"]}
{lang["help.project.auto"]}
{lang["help.project.detect"]}
{lang["help.project.save"]}
{lang["help.project.edit"]}

{lang["help.sync"]}
        """
        
        QMessageBox.information(self, lang["msg.operation_help"], help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = f"""
{lang["about.title"]}

{lang["about.version"]}
{lang["about.feature"]}

{lang["about.advantage"]}
{lang["about.advantage.no_wave"]}
{lang["about.advantage.timeline"]}
{lang["about.advantage.intuitive"]}
{lang["about.advantage.professional"]}

{lang["about.features"]}
{lang["about.features.click"]}
{lang["about.features.drag"]}
{lang["about.features.visual"]}
{lang["about.features.zoom"]}
{lang["about.features.track"]}
{lang["about.features.edit"]}

{lang["about.development"]}
        """
        
        QMessageBox.about(self, lang["msg.about"], about_text)
    
    def import_audio(self):
        """导入音频文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, lang["dialog.select_audio"], "", 
            f"{lang['dialog.audio_files']};;{lang['dialog.all_files']}"
        )
        
        if file_path:
            print(lang["msg.importing_audio"].format(file=file_path))
            self.status_bar.showMessage(lang["msg.audio_loading"])
            
            self.audio_file = file_path
            
            # 设置播放器
            url = QUrl.fromLocalFile(file_path)
            self.media_player.setMedia(QMediaContent(url))
            self.media_player.setVolume(self.volume_slider.value())
            
            # 立即重置播放条状态
            print(lang["msg.reset_progress"])
            self.is_seeking = False
            self.progress_slider.is_dragging = False
            self.progress_slider.set_position(0)
            self.time_display.set_time(0, 0)
            
            # 等待媒体加载完成后初始化时间轴
            QTimer.singleShot(1000, self.init_timeline)
    
    def init_timeline(self):
        """初始化时间轴"""
        if self.media_player.duration() > 0:
            # 让时间轴基于播放器
            if self.timeline.load_from_player(self.media_player):
                # 设置进度条和时间显示
                duration_seconds = self.media_player.duration() / 1000.0
                self.progress_slider.set_duration(duration_seconds)
                self.time_display.set_time(0, duration_seconds)
                
                self.status_bar.showMessage(lang["msg.audio_load_success"].format(file=os.path.basename(self.audio_file)))
                print(lang["msg.timeline_init_success_full"])
                self.update_ui_state()
                
                # 检查是否存在对应的工程文件
                QTimer.singleShot(500, self.check_existing_project)
            else:
                self.status_bar.showMessage(lang["msg.audio_load_failed"])
        else:
            QTimer.singleShot(500, self.init_timeline)
        
        # ✅ 强制修正播放条拖动状态
        print(lang["msg.fix_progress"])

        # 确保 duration 正确
        if self.timeline.duration > 0:
            self.progress_slider.set_duration(self.timeline.duration)
            print(lang["msg.set_progress_duration"].format(duration=self.timeline.duration))
        else:
            print(lang["msg.progress_duration_invalid"])
            self.timeline.duration = 100  # 防止为0
            self.progress_slider.set_duration(100)

        # 确保 is_seeking 清除
        self.is_seeking = False
        print(lang["msg.reset_seeking"])

        # 确保 progress_slider 不处于拖动状态
        self.progress_slider.is_dragging = False
        print(lang["msg.reset_dragging"])

        # 重置进度条和时间显示到 0
        self.progress_slider.set_position(0)
        self.time_display.set_time(0, self.timeline.duration)
        print(lang["msg.reset_progress_position"])
    
    def import_text(self):
        """导入文本文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, lang["dialog.select_text"], "", 
            f"{lang['dialog.text_files']};;{lang['dialog.all_files']}"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 按行分割文本
                self.imported_text_lines = []
                lines = content.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        self.imported_text_lines.append(line)
                
                self.current_text_line_index = 0
                
                # 清除现有字幕
                self.subtitles.clear()
                self.timeline.subtitles.clear()
                self.current_subtitle_index = -1
                self.update_subtitle_display()
                
                # 更新文本编辑器显示完整文本
                self.text_display.setPlainText('\n'.join(self.imported_text_lines))
                self.update_text_editor_display()
                
                # 🎯 设置滚动条位置 - 优化用户体验
                # 左侧文本显示区：滚动到顶部，显示待处理的文本
                self.text_display.verticalScrollBar().setValue(0)
                print(lang["msg.scroll_text_top"])
                
                # 右侧文本列表：滚动到底部，显示最新完成的字幕
                if self.subtitle_list.count() > 0:
                    self.subtitle_list.scrollToBottom()
                    print(lang["msg.scroll_list_bottom"].format(count=self.subtitle_list.count()))
                else:
                    print(lang["msg.list_empty"])
                
                self.status_bar.showMessage(lang["msg.text_import_success"].format(file=os.path.basename(file_path), lines=len(self.imported_text_lines)))
                self.update_ui_state()
                
            except Exception as e:
                QMessageBox.warning(self, lang["msg.error"], lang["msg.text_import_failed"].format(error=str(e)))
    
    def update_smooth_position(self):
        """平滑更新播放位置"""
        if self.is_playing and not self.is_seeking and not self.progress_slider.is_dragging:
            player_position = self.media_player.position() / 1000.0
            
            if abs(player_position - self.current_playback_position) > 0.01:
                self.current_playback_position = player_position
                
                # 更新时间轴显示
                self.timeline.set_position(self.current_playback_position)
                
                # 更新进度条和时间显示
                self.progress_slider.blockSignals(True)
                self.progress_slider.set_position(self.current_playback_position)
                self.progress_slider.blockSignals(False)
                
                self.time_display.set_time(self.current_playback_position)
    
    def skip_time(self, seconds):
        """快进/快退"""
        if self.timeline.duration > 0:
            new_position = self.current_playback_position + seconds
            new_position = max(0, min(self.timeline.duration, new_position))
            self.seek_to_position(new_position)
    
    def on_progress_slider_changed(self, position):
        """进度滑块变化"""
        if not self.is_seeking:
            self.is_seeking = True
            self.seek_to_position(position)
            QTimer.singleShot(100, lambda: setattr(self, 'is_seeking', False))
    
    def play_pause(self):
        """播放/暂停"""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.btn_play_pause.setText("▶️")
            self.status_bar.showMessage(lang["msg.paused"])
        else:
            self.media_player.play()
            self.btn_play_pause.setText("⏸️")
            self.status_bar.showMessage(lang["msg.playing"])
    
    def stop_playback(self):
        """停止播放"""
        self.media_player.stop()
        self.btn_play_pause.setText("▶️")
        self.status_bar.showMessage(lang["msg.stopped"])
        self.position_update_timer.stop()
    
    def seek_to_position(self, position):
        """跳转到指定位置"""
        if self.timeline.duration > 0:
            position = max(0, min(self.timeline.duration, position))
            ms_position = int(position * 1000)
            
            self.media_player.setPosition(ms_position)
            self.current_playback_position = position
            self.timeline.set_position(position)
            self.time_display.set_time(position)
            
            if not self.progress_slider.is_dragging:
                self.progress_slider.blockSignals(True)
                self.progress_slider.set_position(position)
                self.progress_slider.blockSignals(False)
    
    def on_player_state_changed(self, state):
        """播放器状态变化"""
        was_playing = self.is_playing
        self.is_playing = (state == QMediaPlayer.PlayingState)
        
        if self.is_playing and not was_playing:
            self.position_update_timer.start()
        elif not self.is_playing and was_playing:
            self.position_update_timer.stop()
    
    def on_position_changed(self, position):
        """播放位置变化"""
        if not self.is_seeking and not self.progress_slider.is_dragging and not self.is_playing:
            self.current_playback_position = position / 1000.0
            self.timeline.set_position(self.current_playback_position)
            
            self.progress_slider.blockSignals(True)
            self.progress_slider.set_position(self.current_playback_position)
            self.progress_slider.blockSignals(False)
            
            self.time_display.set_time(self.current_playback_position)
    
    def on_duration_changed(self, duration):
        """播放器时长变化"""
        if duration > 0:
            duration_seconds = duration / 1000.0
            self.progress_slider.set_duration(duration_seconds)
            self.time_display.set_time(self.current_playback_position, duration_seconds)
    
    # 字幕事件处理方法
    def on_subtitle_added(self, start_time):
        """处理添加字幕事件"""
        self.subtitles = self.timeline.subtitles[:]
        self.update_subtitle_display()
        self.update_ui_state()
        
        for i, subtitle in enumerate(self.subtitles):
            if abs(subtitle.start_time - start_time) < 0.1:
                self.current_subtitle_index = i
                break
        
        self.update_subtitle_details()
    
    def on_subtitle_selected(self, index):
        """处理字幕选中事件"""
        self.current_subtitle_index = index
        self.timeline.selected_subtitle = index
        self.timeline.update()
        self.update_subtitle_details()
        self.update_ui_state()
    
    def on_subtitle_changed(self, index, start_time, end_time):
        """处理字幕时间变化事件"""
        if 0 <= index < len(self.subtitles):
            self.subtitles[index].start_time = start_time
            self.subtitles[index].end_time = end_time
            self.update_subtitle_display()
            
            if index == self.current_subtitle_index:
                self.update_subtitle_details()
    
    def on_subtitle_deleted(self, index):
        """处理字幕删除事件"""
        self.subtitles = self.timeline.subtitles[:]
        
        if self.current_subtitle_index == index:
            self.current_subtitle_index = -1
        elif self.current_subtitle_index > index:
            self.current_subtitle_index -= 1
        
        self.update_subtitle_display()
        self.update_subtitle_details()
        self.update_ui_state()
    
    def update_subtitle_details(self):
        """更新字幕详情"""
        if 0 <= self.current_subtitle_index < len(self.subtitles):
            subtitle = self.subtitles[self.current_subtitle_index]
            
            self.start_time_edit.setText(self.format_time_input(subtitle.start_time))
            self.end_time_edit.setText(self.format_time_input(subtitle.end_time))
            
            duration = subtitle.end_time - subtitle.start_time
            self.duration_label.setText(lang["msg.duration_with_seconds"].format(duration=duration))
        else:
            self.start_time_edit.clear()
            self.end_time_edit.clear()
            self.duration_label.setText(lang["msg.duration_placeholder"])
        
        self.update_text_editor_display()
    
    def update_text_editor_display(self):
        """更新文本编辑器显示"""
        if hasattr(self, 'imported_text_lines') and self.imported_text_lines:
            remaining_lines = self.imported_text_lines[self.current_text_line_index:]
            remaining_text = '\n'.join(remaining_lines)
            self.text_display.blockSignals(True)
            self.text_display.setPlainText(remaining_text)
            self.text_display.blockSignals(False)
            
            remaining_count = len(remaining_lines)
            if remaining_count == 0:
                self.text_display.setPlaceholderText(lang["msg.all_text_used"])
            else:
                self.text_display.setPlaceholderText(lang["msg.remaining_text"].format(count=remaining_count))
        else:
            self.text_display.setPlainText("")
            self.text_display.setPlaceholderText(lang["msg.please_import_text"])
    
    def update_subtitle_display(self):
        """更新字幕列表显示"""
        self.subtitle_list.clear()
        
        for i, subtitle in enumerate(self.subtitles):
            start_str = self.format_time_display(subtitle.start_time)
            end_str = self.format_time_display(subtitle.end_time)
            
            text_content = str(subtitle.text).strip()
            # 增加文本显示长度，从30字符增加到50字符
            if len(text_content) > 50:
                text_preview = text_content[:50] + "..."
            else:
                text_preview = text_content
            
            # 优化显示格式，使用多行显示，支持更多位数
            duration = subtitle.end_time - subtitle.start_time
            item_text = f"{i+1:04d}  {start_str} → {end_str} ({duration:.1f}s)\n{text_preview}"
            self.subtitle_list.addItem(item_text)
    
    def format_time_display(self, seconds):
        """格式化时间显示"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{minutes:02d}:{secs:02d}.{milliseconds:03d}"
    
    def format_time_input(self, seconds):
        """格式化时间输入"""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:06.3f}"
    
    def parse_time_input(self, time_str):
        """解析时间输入"""
        try:
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = float(parts[1])
                    return minutes * 60 + seconds
            else:
                return float(time_str)
        except:
            return None
    
    def update_times_from_input(self):
        """从输入框更新时间"""
        if 0 <= self.current_subtitle_index < len(self.subtitles):
            start_time = self.parse_time_input(self.start_time_edit.text())
            end_time = self.parse_time_input(self.end_time_edit.text())
            
            if start_time is not None and end_time is not None:
                if 0 <= start_time < end_time <= self.timeline.duration:
                    subtitle = self.subtitles[self.current_subtitle_index]
                    subtitle.start_time = start_time
                    subtitle.end_time = end_time
                    
                    self.timeline.subtitles[self.current_subtitle_index].start_time = start_time
                    self.timeline.subtitles[self.current_subtitle_index].end_time = end_time
                    
                    self.update_subtitle_display()
                    self.update_subtitle_details()
                    self.timeline.update()
                else:
                    QMessageBox.warning(self, lang["msg.error"], lang["msg.time_format_error"])
                    self.update_subtitle_details()
    
    def on_subtitle_list_clicked(self, item):
        """字幕列表点击处理"""
        row = self.subtitle_list.row(item)
        if 0 <= row < len(self.subtitles):
            self.current_subtitle_index = row
            self.timeline.selected_subtitle = row
            self.timeline.update()
            self.update_subtitle_details()
            
            # 跳转到字幕位置
            subtitle = self.subtitles[row]
            self.seek_to_position(subtitle.start_time)
    
    def delete_current_subtitle(self):
        """删除当前选中字幕"""
        if 0 <= self.current_subtitle_index < len(self.subtitles):
            self.timeline.delete_subtitle(self.current_subtitle_index)
    
    def fit_all(self):
        """适合全部"""
        self.timeline.reset_zoom()
    
    def zoom_in(self):
        """放大时间轴 - 跟随播放位置"""
        if self.timeline.duration > 0:
            display_duration = self.timeline.zoom_end - self.timeline.zoom_start
            new_duration = display_duration / 1.5
            
            # 最小显示1秒
            if new_duration >= 1.0:
                # 以当前播放位置为中心进行缩放
                center = self.current_playback_position
                new_start = center - new_duration / 2
                new_end = center + new_duration / 2
                
                # 边界处理
                if new_start < 0:
                    new_start = 0
                    new_end = new_duration
                if new_end > self.timeline.duration:
                    new_end = self.timeline.duration
                    new_start = self.timeline.duration - new_duration
                
                self.timeline.zoom_start = max(0, new_start)
                self.timeline.zoom_end = min(self.timeline.duration, new_end)
                self.timeline.is_zoomed = True
                self.timeline.update()
    
    def zoom_out(self):
        """缩小时间轴 - 跟随播放位置"""
        if self.timeline.duration > 0:
            display_duration = self.timeline.zoom_end - self.timeline.zoom_start
            new_duration = min(display_duration * 1.5, self.timeline.duration)
            
            # 以当前播放位置为中心进行缩放
            center = self.current_playback_position
            new_start = center - new_duration / 2
            new_end = center + new_duration / 2
            
            # 边界处理
            if new_start < 0:
                new_start = 0
                new_end = new_duration
            if new_end > self.timeline.duration:
                new_end = self.timeline.duration
                new_start = self.timeline.duration - new_duration
            
            self.timeline.zoom_start = max(0, new_start)
            self.timeline.zoom_end = min(self.timeline.duration, new_end)
            self.timeline.is_zoomed = (new_start > 0 or new_end < self.timeline.duration)
            self.timeline.update()
    
    def reset_text_index(self):
        """重置文本索引"""
        if hasattr(self, 'imported_text_lines') and self.imported_text_lines:
            self.current_text_line_index = 0
            
            # 清除所有字幕
            self.subtitles.clear()
            self.timeline.subtitles.clear()
            self.current_subtitle_index = -1
            
            self.update_subtitle_display()
            self.update_subtitle_details()
            self.timeline.update()
            self.update_ui_state()
            
            self.status_bar.showMessage(lang["msg.text_reset"].format(lines=len(self.imported_text_lines)))
        else:
            QMessageBox.information(self, lang["msg.info"], lang["msg.please_import_text_first"])
    
    def change_language(self, lang_code):
        """切换语言"""
        try:
            # 保存当前语言设置
            import json
            config_file = os.path.join(os.path.dirname(__file__), 'config.json')
            config = {}
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            config['language'] = lang_code
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            # 重新加载语言文件
            from language_loader import load_language
            global lang
            lang = load_language(lang_code)
            
            # 刷新所有UI文本
            self.reload_ui_texts()
            
            QMessageBox.information(self, lang["msg.language_changed"], lang["msg.language_switched"].format(lang=lang_code.upper()))
            
        except Exception as e:
            QMessageBox.warning(self, lang["msg.error"], lang["msg.language_error"].format(error=str(e)))
    
    def reload_ui_texts(self):
        """重新加载所有UI文本"""
        try:
            # 更新窗口标题
            self.setWindowTitle(lang["app.title"])
            
            # 更新菜单栏
            menubar = self.menuBar()
            for i, menu in enumerate(menubar.findChildren(QMenu)):
                if i == 0:  # 文件菜单
                    menu.setTitle(lang["menu.file"])
                elif i == 1:  # 编辑菜单
                    menu.setTitle(lang["menu.edit"])
                elif i == 2:  # 语言菜单
                    menu.setTitle(lang["menu.language"])
                elif i == 3:  # 视图菜单
                    menu.setTitle(lang["menu.view"])
                elif i == 4:  # 帮助菜单
                    menu.setTitle(lang["menu.help"])
            
            # 更新工具栏按钮
            self.btn_import_audio.setText(f"📁 {lang['btn.import_audio']}")
            self.btn_import_text.setText(f"📝 {lang['btn.import_text']}")
            self.btn_save_project.setText(f"💾 {lang['btn.save_project']}")
            self.btn_open_project.setText(f"📂 {lang['btn.open_project']}")
            self.btn_export.setText(f"📤 {lang['btn.export_srt']}")
            self.btn_delete_subtitle.setText(f"🗑️ {lang['btn.delete']}")
            self.btn_fit_all.setText(f"🔍 {lang['btn.fit_all']}")
            self.btn_zoom_in.setText(f"🔍+ {lang['btn.zoom_in']}")
            self.btn_zoom_out.setText(f"🔍- {lang['btn.zoom_out']}")
            self.btn_toggle_snap.setText(f"🔗 {lang['btn.snap']}")
            self.btn_reset_text_index.setText(f"🔄 {lang['btn.reset']}")
            
            # 更新标签
            self.timeline_label.setText(lang["label.timeline"])
            self.sync_status_label.setText(lang["label.sync_status"])
            
            # 更新字幕块标签
            if hasattr(self, 'subtitle_blocks_label'):
                self.subtitle_blocks_label.setText(lang["label.subtitle_blocks"])
            
            # 更新GroupBox标题
            self.text_group.setTitle(lang["group.text_area"])
            self.text_list_group.setTitle(lang["group.text_list"])
            
            # 更新时间调整区域标签
            self.time_adjust_label.setText(lang["label.time_adjust"])
            self.start_label.setText(lang["label.start"])
            self.end_label.setText(lang["label.end"])
            self.duration_label.setText(lang["label.duration"])
            
            # 更新状态栏
            self.status_bar.showMessage(lang["msg.timeline_mode"])
            
            # 更新工具提示
            for widget in self.findChildren(QToolButton):
                if "编辑" in widget.toolTip():
                    widget.setToolTip(f"{lang['btn.edit']} (Ctrl+E)")
                elif "完成并保存" in widget.toolTip():
                    widget.setToolTip(f"{lang['btn.save_done']} (Ctrl+S)")
                elif "取消修改" in widget.toolTip():
                    widget.setToolTip(f"{lang['btn.cancel']} (Esc)")
            
            # 更新占位符文本
            self.start_time_edit.setPlaceholderText("00:00.000")
            self.end_time_edit.setPlaceholderText("00:02.000")
            
            # 更新文本显示区的占位符
            self.update_text_editor_display()
            
            print(f"✅ UI文本刷新完成")
            
        except Exception as e:
            print(f"⚠️ UI文本刷新失败: {e}")
            QMessageBox.warning(self, lang["msg.error"], f"UI刷新失败: {str(e)}")
    
    def toggle_snap(self):
        """切换吸附功能"""
        self.timeline.snap_enabled = not self.timeline.snap_enabled
        self.btn_toggle_snap.setChecked(self.timeline.snap_enabled)
        self.snap_action.setChecked(self.timeline.snap_enabled)
        
        if self.timeline.snap_enabled:
            self.status_bar.showMessage(lang["msg.snap_enabled"])
        else:
            self.timeline.snap_lines = []  # 清除吸附线
            self.status_bar.showMessage(lang["msg.snap_disabled"])
        
        self.timeline.update()
    
    def update_ui_state(self):
        """更新UI状态"""
        has_audio = self.audio_file is not None
        has_subtitles = len(self.subtitles) > 0
        has_selection = 0 <= self.current_subtitle_index < len(self.subtitles)
        has_text = hasattr(self, 'imported_text_lines') and bool(self.imported_text_lines)
        
        # 工具栏按钮
        self.btn_delete_subtitle.setEnabled(has_selection)
        self.btn_reset_text_index.setEnabled(has_text)
        self.btn_save_project.setEnabled(has_audio)  # 有音频就可以保存工程
        self.btn_export.setEnabled(has_subtitles)
        self.btn_fit_all.setEnabled(has_audio)
        self.btn_zoom_in.setEnabled(has_audio)
        self.btn_zoom_out.setEnabled(has_audio)
        
        # 播放控制
        self.btn_play_pause.setEnabled(has_audio)
        self.btn_stop.setEnabled(has_audio)
        self.btn_backward.setEnabled(has_audio)
        self.btn_forward.setEnabled(has_audio)
        self.progress_slider.setEnabled(has_audio)
        
        # 属性面板
        self.start_time_edit.setEnabled(has_selection)
        self.end_time_edit.setEnabled(has_selection)
    
    def export_subtitle(self):
        """导出字幕文件"""
        if not self.subtitles:
            QMessageBox.warning(self, lang["msg.warning"], lang["msg.no_subtitles"])
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, lang["dialog.export_srt"], "", 
            f"{lang['dialog.srt_files']};;{lang['dialog.all_files']}"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for i, subtitle in enumerate(self.subtitles, 1):
                        start_time = self.format_srt_time(subtitle.start_time)
                        end_time = self.format_srt_time(subtitle.end_time)
                        
                        f.write(f"{i}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{subtitle.text}\n\n")
                
                self.status_bar.showMessage(lang["msg.subtitle_export_success"].format(file=os.path.basename(file_path)))
                QMessageBox.information(self, lang["msg.success"], lang["msg.export_success"].format(path=file_path))
                
            except Exception as e:
                QMessageBox.critical(self, lang["msg.error"], lang["msg.export_error"].format(error=str(e)))
    
    def format_srt_time(self, seconds):
        """格式化SRT时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def save_project(self):
        """保存工程文件"""
        if not self.audio_file:
            QMessageBox.warning(self, lang["msg.warning"], lang["msg.please_import_audio_first"])
            return
        
        # 生成工程文件路径 - 与音频文件路径一致
        audio_path = self.audio_file
        project_path = os.path.splitext(audio_path)[0] + ".srtproj"
        
        try:
            project_data = {
                "version": "1.0",
                "audio_file": audio_path,
                "text_lines": self.imported_text_lines,
                "current_text_index": self.current_text_line_index,
                "subtitles": [],
                "timeline_settings": {
                    "zoom_start": self.timeline.zoom_start,
                    "zoom_end": self.timeline.zoom_end,
                    "is_zoomed": self.timeline.is_zoomed,
                    "snap_enabled": self.timeline.snap_enabled
                },
                "playback_position": self.current_playback_position,
                "save_time": QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            }
            
            # 转换字幕数据
            for subtitle in self.subtitles:
                project_data["subtitles"].append({
                    "text": subtitle.text,
                    "start_time": subtitle.start_time,
                    "end_time": subtitle.end_time
                })
            
            # 保存为JSON格式
            import json
            with open(project_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            
            self.status_bar.showMessage(lang["msg.project_save_success"].format(file=os.path.basename(project_path)))
            QMessageBox.information(self, lang["msg.success"], lang["msg.project_saved"].format(path=project_path))
            
        except Exception as e:
            QMessageBox.critical(self, lang["msg.error"], lang["msg.save_error"].format(error=str(e)))
    
    def open_project(self):
        """打开工程文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, lang["dialog.open_project"], "", 
            f"{lang['dialog.project_files']};;{lang['dialog.all_files']}"
        )
        
        if file_path:
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                
                # 加载文本数据
                self.imported_text_lines = project_data.get('text_lines', [])
                self.current_text_line_index = project_data.get('current_text_index', 0)
                print(lang["msg.loaded_text"].format(lines=len(self.imported_text_lines), index=self.current_text_line_index))
                
                # 加载字幕
                subtitles = project_data.get('subtitles', [])
                self.subtitles.clear()
                self.timeline.subtitles.clear()
                for item in subtitles:
                    subtitle = SubtitleItem(
                        text=item.get('text', ''),
                        start_time=item.get('start_time', 0.0),
                        end_time=item.get('end_time', 2.0)
                    )
                    self.subtitles.append(subtitle)
                    self.timeline.subtitles.append(subtitle)
                
                # 加载音频文件（如果有保存）
                audio_file = project_data.get('audio_file', None)
                if audio_file and os.path.exists(audio_file):
                    self.audio_file = audio_file
                    self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
                    self.media_player.setVolume(self.volume_slider.value())
                    print(lang["msg.loaded_audio"].format(file=self.audio_file))
                else:
                    print(lang["msg.no_audio_path"])
                
                # 设置时长
                loaded_duration = project_data.get('duration', None)
                if loaded_duration:
                    self.timeline.duration = loaded_duration
                    self.progress_slider.set_duration(loaded_duration)
                    self.time_display.set_time(0, loaded_duration)
                    print(lang["msg.set_duration"].format(duration=loaded_duration))
                else:
                    # 从字幕数据中计算最大时长
                    max_end_time = 0.0
                    for subtitle in subtitles:
                        max_end_time = max(max_end_time, subtitle.get('end_time', 0.0))
                    
                    # 如果音频文件存在，尝试从播放器获取时长
                    if audio_file and os.path.exists(audio_file):
                        # 临时设置音频文件以获取时长
                        temp_player = QMediaPlayer()
                        temp_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file)))
                        
                        # 等待音频加载完成
                        for _ in range(20):  # 最多等待10秒
                            if temp_player.duration() > 0:
                                break
                            QApplication.processEvents()
                            QThread.msleep(500)
                        
                        if temp_player.duration() > 0:
                            calculated_duration = temp_player.duration() / 1000.0
                            print(lang["msg.audio_duration"].format(duration=calculated_duration))
                        else:
                            calculated_duration = max(max_end_time + 30.0, 600.0)  # 至少10分钟
                            print(lang["msg.calc_duration"].format(duration=calculated_duration))
                    else:
                        calculated_duration = max(max_end_time + 30.0, 600.0)  # 至少10分钟
                        print(lang["msg.no_audio_calc"].format(duration=calculated_duration))
                    
                    self.timeline.duration = calculated_duration
                    self.progress_slider.set_duration(calculated_duration)
                    self.time_display.set_time(0, calculated_duration)

                # 恢复时间轴缩放设置
                timeline_settings = project_data.get('timeline_settings', {})
                if timeline_settings:
                    # 恢复保存的缩放设置
                    self.timeline.zoom_start = timeline_settings.get('zoom_start', 0.0)
                    self.timeline.zoom_end = timeline_settings.get('zoom_end', min(self.timeline.duration, 60.0))
                    self.timeline.is_zoomed = timeline_settings.get('is_zoomed', False)
                    self.timeline.snap_enabled = timeline_settings.get('snap_enabled', True)
                    print(lang["msg.restore_zoom"].format(start=self.timeline.zoom_start, end=self.timeline.zoom_end))
                else:
                    # 设置默认缩放范围
                    self.timeline.zoom_start = 0.0
                    self.timeline.zoom_end = min(self.timeline.duration, 60.0)  # Default display first 60 seconds
                    self.timeline.is_zoomed = (self.timeline.zoom_end < self.timeline.duration)
                    self.timeline.snap_enabled = True
                    print(lang["msg.default_zoom"].format(start=self.timeline.zoom_start, end=self.timeline.zoom_end))

                # 重置文本索引
                self.current_subtitle_index = -1
                self.update_subtitle_display()
                self.update_text_editor_display()
                self.update_subtitle_details()
                self.update_ui_state()
                self.timeline.update()
                
                # ✅ 修正播放条状态
                self.is_seeking = False
                self.progress_slider.is_dragging = False
                self.progress_slider.set_position(0)
                print(lang["msg.fix_progress_state"])
                
                # 🎯 设置滚动条位置 - 优化用户体验
                # 左侧文本显示区：滚动到顶部，显示待处理的文本
                self.text_display.verticalScrollBar().setValue(0)
                print(lang["msg.scroll_text_top"])
                
                # 右侧文本列表：滚动到底部，显示最新完成的字幕
                if self.subtitle_list.count() > 0:
                    self.subtitle_list.scrollToBottom()
                    print(lang["msg.scroll_list_bottom"].format(count=self.subtitle_list.count()))
                else:
                    print(lang["msg.list_empty"])
                
                self.status_bar.showMessage(lang["msg.project_load_success"].format(path=os.path.basename(file_path)))
            
            except Exception as e:
                QMessageBox.warning(self, lang["msg.error"], lang["msg.project_load_failed"].format(error=str(e)))
    

    

    

    

    

    

    
    def auto_save_project(self):
        """自动保存工程文件"""
        if self.audio_file and self.subtitles:
            self.save_project()
    
    def check_existing_project(self):
        """检查是否存在对应的工程文件"""
        if not self.audio_file:
            return
        
        project_path = os.path.splitext(self.audio_file)[0] + ".srtproj"
        
        if os.path.exists(project_path):
            # 使用QTimer延迟显示对话框，避免阻塞UI
            QTimer.singleShot(500, lambda: self._show_project_dialog(project_path))
    
    def _show_project_dialog(self, project_path):
        """显示工程文件对话框"""
        try:
            reply = QMessageBox.question(
                self, lang["msg.project_found"], 
                lang["msg.project_found_question"].format(file=os.path.basename(project_path)),
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 直接加载工程文件
                try:
                    import json
                    with open(project_path, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                    
                    # 加载文本数据
                    self.imported_text_lines = project_data.get('text_lines', [])
                    self.current_text_line_index = project_data.get('current_text_index', 0)
                    print(lang["msg.loaded_text"].format(lines=len(self.imported_text_lines), index=self.current_text_line_index))
                    
                    # 加载字幕
                    subtitles = project_data.get('subtitles', [])
                    self.subtitles.clear()
                    self.timeline.subtitles.clear()
                    for item in subtitles:
                        subtitle = SubtitleItem(
                            text=item.get('text', ''),
                            start_time=item.get('start_time', 0.0),
                            end_time=item.get('end_time', 2.0)
                        )
                        self.subtitles.append(subtitle)
                        self.timeline.subtitles.append(subtitle)
                    
                    # 加载音频文件（如果有保存）
                    audio_file = project_data.get('audio_file', None)
                    if audio_file and os.path.exists(audio_file):
                        self.audio_file = audio_file
                        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_file)))
                        self.media_player.setVolume(self.volume_slider.value())
                        print(lang["msg.loaded_audio"].format(file=self.audio_file))
                    
                    # 设置时长
                    loaded_duration = project_data.get('duration', None)
                    if loaded_duration:
                        self.timeline.duration = loaded_duration
                        self.progress_slider.set_duration(loaded_duration)
                        self.time_display.set_time(0, loaded_duration)
                    else:
                        # 从字幕数据中计算最大时长
                        max_end_time = 0.0
                        for subtitle in subtitles:
                            max_end_time = max(max_end_time, subtitle.get('end_time', 0.0))
                        calculated_duration = max(max_end_time + 30.0, 600.0)
                        self.timeline.duration = calculated_duration
                        self.progress_slider.set_duration(calculated_duration)
                        self.time_display.set_time(0, calculated_duration)

                    # 恢复时间轴缩放设置
                    timeline_settings = project_data.get('timeline_settings', {})
                    if timeline_settings:
                        self.timeline.zoom_start = timeline_settings.get('zoom_start', 0.0)
                        self.timeline.zoom_end = timeline_settings.get('zoom_end', min(self.timeline.duration, 60.0))
                        self.timeline.is_zoomed = timeline_settings.get('is_zoomed', False)
                        self.timeline.snap_enabled = timeline_settings.get('snap_enabled', True)
                    else:
                        self.timeline.zoom_start = 0.0
                        self.timeline.zoom_end = min(self.timeline.duration, 60.0)
                        self.timeline.is_zoomed = (self.timeline.zoom_end < self.timeline.duration)
                        self.timeline.snap_enabled = True

                    # 重置文本索引
                    self.current_subtitle_index = -1
                    self.update_subtitle_display()
                    self.update_text_editor_display()
                    self.update_subtitle_details()
                    self.update_ui_state()
                    self.timeline.update()
                    
                    # ✅ 修正播放条状态
                    self.is_seeking = False
                    self.progress_slider.is_dragging = False
                    self.progress_slider.set_position(0)
                    
                    # 🎯 设置滚动条位置 - 优化用户体验
                    # 左侧文本显示区：滚动到顶部，显示待处理的文本
                    self.text_display.verticalScrollBar().setValue(0)
                    print(lang["msg.scroll_text_top"])
                    
                    # 右侧文本列表：滚动到底部，显示最新完成的字幕
                    if self.subtitle_list.count() > 0:
                        self.subtitle_list.scrollToBottom()
                        print(lang["msg.scroll_list_bottom"].format(count=self.subtitle_list.count()))
                    else:
                        print(lang["msg.list_empty"])
                    
                    self.status_bar.showMessage(lang["msg.project_load_success"].format(path=os.path.basename(project_path)))
                    
                except Exception as e:
                    QMessageBox.warning(self, lang["msg.error"], lang["msg.project_load_failed"].format(error=str(e)))
                
        except Exception as e:
            self.status_bar.showMessage(lang["msg.dialog_failed"].format(error=str(e)))
    

    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Space:
            # 空格键控制播放/停止
            self.play_pause()
            event.accept()
        elif event.key() == Qt.Key_Left:
            # 左箭头键快退5秒
            self.skip_time(-5)
            event.accept()
        elif event.key() == Qt.Key_Right:
            # 右箭头键快进5秒
            self.skip_time(5)
            event.accept()
        else:
            super().keyPressEvent(event)

def main():
    try:
        print(lang["msg.creating_timeline"])
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        print(lang["msg.creating_window"])
        window = TimelineSubtitleTool()
        window.show()
        
        print(lang["msg.startup_success"])
        print("=" * 60)
        print(lang["msg.timeline_features"])
        print(lang["msg.no_wave_sync"])
        print(lang["msg.time_ruler"])
        print(lang["msg.sync_100"])
        print(lang["msg.intuitive_ui"])
        print(lang["msg.professional_edit"])
        print(lang["msg.core_advantages"])
        print(lang["msg.click_jump"])
        print(lang["msg.drag_create"])
        print(lang["msg.visual_scale"])
        print(lang["msg.multi_zoom"])
        print(lang["msg.real_time_track"])
        print(lang["msg.consumption_edit"])
        print(lang["msg.operation_mode"])
        print(lang["msg.click_timeline"])
        print(lang["msg.drag_subtitle"])
        print(lang["msg.drag_adjust"])
        print(lang["msg.wheel_zoom"])
        print(lang["msg.play_sync"])
        print("=" * 60)
        print(lang["msg.timeline_100_sync"])
        print(lang["msg.new_layout"])
        print(lang["msg.top_menu"])
        print(lang["msg.middle_timeline"])
        print(lang["msg.bottom_subtitle"])
        print(lang["msg.bottom_text"])
        print(lang["msg.help_menu"])
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(lang["msg.startup_failed"].format(error=str(e)))
        import traceback
        traceback.print_exc()
        input(lang["msg.press_enter"])

if __name__ == "__main__":
    main()