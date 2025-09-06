# language_loader.py
import json
import os

def load_language(lang_code='zh'):
    """Load specified language (zh/en), default Chinese"""
    # 使用统一的docs/i18n系统
    base_path = os.path.dirname(os.path.dirname(__file__))  # 回到项目根目录
    lang_file = os.path.join(base_path, 'docs', 'i18n', f'{lang_code}.json')

    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Language file {lang_file} not found, using default Chinese.")
        return {}

def get_saved_language():
    """Get saved language setting"""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', 'zh')
        except:
            pass
    return 'zh'

def save_language(lang_code):
    """Save language setting to config file"""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            pass
    
    config['language'] = lang_code
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def switch_language(lang_code):
    """Switch language and reload"""
    global lang
    if save_language(lang_code):
        lang = load_language(lang_code)
        return True
    return False

# Load current language
def reload_language():
    """Reload language based on current config"""
    global lang
    lang = load_language(get_saved_language())

# Initial load
lang = load_language(get_saved_language())
