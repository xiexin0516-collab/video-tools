#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subtitle Parser Service
Handles parsing and exporting of subtitle files (SRT, TXT)
"""

import re
from datetime import timedelta
import json

class SubtitleParser:
    def __init__(self):
        self.supported_formats = ['srt', 'txt']
    
    def parse_time_string(self, time_str):
        """Parse time string in format HH:MM:SS,mmm or HH:MM:SS.mmm"""
        try:
            # Handle both comma and dot as milliseconds separator
            if ',' in time_str:
                time_str = time_str.replace(',', '.')
            
            # Parse time components
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds_parts = parts[2].split('.')
            seconds = int(seconds_parts[0])
            milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
            
            # Convert to total seconds
            total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
            return total_seconds
        except Exception as e:
            print(f"Error parsing time string '{time_str}': {e}")
            return 0.0
    
    def format_time_string(self, seconds):
        """Format seconds to time string HH:MM:SS,mmm"""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            milliseconds = int((seconds % 1) * 1000)
            
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
        except Exception as e:
            print(f"Error formatting time: {e}")
            return "00:00:00,000"
    
    def parse_srt_content(self, content):
        """Parse SRT format content"""
        subtitles = []
        
        # Split by subtitle blocks (double newlines)
        blocks = re.split(r'\n\s*\n', content.strip())
        
        for block in blocks:
            if not block.strip():
                continue
            
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue
            
            try:
                # Parse subtitle number
                subtitle_number = int(lines[0])
                
                # Parse time line
                time_line = lines[1]
                time_match = re.match(r'(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})', time_line)
                
                if not time_match:
                    continue
                
                start_time = self.parse_time_string(time_match.group(1))
                end_time = self.parse_time_string(time_match.group(2))
                
                # Parse subtitle text
                text_lines = lines[2:]
                text = '\n'.join(text_lines).strip()
                
                subtitle = {
                    'id': subtitle_number,
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': text,
                    'duration': end_time - start_time
                }
                
                subtitles.append(subtitle)
                
            except Exception as e:
                print(f"Error parsing SRT block: {e}")
                continue
        
        return subtitles
    
    def parse_txt_content(self, content):
        """Parse TXT format content (simple text with timestamps)"""
        subtitles = []
        lines = content.strip().split('\n')
        
        current_subtitle = None
        subtitle_id = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to match timestamp pattern [HH:MM:SS] or [HH:MM:SS.mmm]
            timestamp_match = re.match(r'\[(\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?)\]', line)
            
            if timestamp_match:
                # Save previous subtitle if exists
                if current_subtitle:
                    subtitles.append(current_subtitle)
                
                # Start new subtitle
                start_time = self.parse_time_string(timestamp_match.group(1))
                text = line[timestamp_match.end():].strip()
                
                current_subtitle = {
                    'id': subtitle_id,
                    'start_time': start_time,
                    'end_time': start_time + 2.0,  # Default 2 second duration
                    'text': text,
                    'duration': 2.0
                }
                subtitle_id += 1
            else:
                # Continue text for current subtitle
                if current_subtitle:
                    current_subtitle['text'] += '\n' + line
        
        # Add last subtitle
        if current_subtitle:
            subtitles.append(current_subtitle)
        
        return subtitles
    
    def parse_subtitle_file(self, content, filename):
        """Parse subtitle file based on extension"""
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'txt'
        
        if file_extension == 'srt':
            return self.parse_srt_content(content)
        elif file_extension == 'txt':
            return self.parse_txt_content(content)
        else:
            raise ValueError(f"Unsupported subtitle format: {file_extension}")
    
    def parse_subtitle_content(self, content, format_type='srt'):
        """Parse subtitle content based on format type"""
        if format_type.lower() == 'srt':
            return self.parse_srt_content(content)
        elif format_type.lower() == 'txt':
            return self.parse_txt_content(content)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def export_srt(self, subtitles):
        """Export subtitles to SRT format"""
        srt_content = []
        
        for i, subtitle in enumerate(subtitles, 1):
            start_time = self.format_time_string(subtitle['start_time'])
            end_time = self.format_time_string(subtitle['end_time'])
            text = subtitle['text']
            
            srt_block = f"{i}\n{start_time} --> {end_time}\n{text}\n"
            srt_content.append(srt_block)
        
        return '\n'.join(srt_content)
    
    def export_txt(self, subtitles):
        """Export subtitles to TXT format"""
        txt_content = []
        
        for subtitle in subtitles:
            start_time = self.format_time_string(subtitle['start_time'])
            text = subtitle['text']
            
            txt_line = f"[{start_time}] {text}"
            txt_content.append(txt_line)
        
        return '\n'.join(txt_content)
    
    def export_subtitles(self, subtitles, format_type='srt'):
        """Export subtitles to specified format"""
        if format_type.lower() == 'srt':
            return self.export_srt(subtitles)
        elif format_type.lower() == 'txt':
            return self.export_txt(subtitles)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def validate_subtitle(self, subtitle):
        """Validate subtitle data"""
        required_fields = ['start_time', 'end_time', 'text']
        
        for field in required_fields:
            if field not in subtitle:
                return False, f"Missing required field: {field}"
        
        if subtitle['start_time'] < 0 or subtitle['end_time'] < 0:
            return False, "Time values must be non-negative"
        
        if subtitle['start_time'] >= subtitle['end_time']:
            return False, "Start time must be less than end time"
        
        if not subtitle['text'].strip():
            return False, "Subtitle text cannot be empty"
        
        return True, "Valid"
    
    def validate_subtitles(self, subtitles):
        """Validate list of subtitles"""
        errors = []
        
        for i, subtitle in enumerate(subtitles):
            is_valid, message = self.validate_subtitle(subtitle)
            if not is_valid:
                errors.append(f"Subtitle {i+1}: {message}")
        
        return len(errors) == 0, errors
    
    def merge_subtitles(self, subtitles1, subtitles2):
        """Merge two subtitle lists"""
        merged = subtitles1 + subtitles2
        
        # Sort by start time
        merged.sort(key=lambda x: x['start_time'])
        
        # Reassign IDs
        for i, subtitle in enumerate(merged, 1):
            subtitle['id'] = i
        
        return merged
    
    def split_subtitle(self, subtitle, split_time):
        """Split a subtitle at specified time"""
        if split_time <= subtitle['start_time'] or split_time >= subtitle['end_time']:
            return [subtitle]
        
        subtitle1 = {
            'id': subtitle['id'],
            'start_time': subtitle['start_time'],
            'end_time': split_time,
            'text': subtitle['text'],
            'duration': split_time - subtitle['start_time']
        }
        
        subtitle2 = {
            'id': subtitle['id'] + 1,
            'start_time': split_time,
            'end_time': subtitle['end_time'],
            'text': subtitle['text'],
            'duration': subtitle['end_time'] - split_time
        }
        
        return [subtitle1, subtitle2]
