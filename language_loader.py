# language_loader.py
import json
import os

def load_language(lang_code='zh'):
    """Load specified language (zh/en), default Chinese"""
    base_path = os.path.dirname(__file__)
    lang_file = os.path.join(base_path, 'locales', f'lang_{lang_code}.json')

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

# Load current language
def reload_language():
    """Reload language based on current config"""
    global lang
    lang = load_language(get_saved_language())

# Initial load
lang = load_language(get_saved_language())
