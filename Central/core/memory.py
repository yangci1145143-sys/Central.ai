import json
import os

MEMORY_FILE = "central_memory.json"
IMPORTANT_FILE = "central_important.json"
MAX_HISTORY = 40

def load_memory() -> list:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []

def save_memory(history: list):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)

def load_important() -> list:
    if os.path.exists(IMPORTANT_FILE):
        try:
            with open(IMPORTANT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []

def save_important(items: list):
    with open(IMPORTANT_FILE, 'w', encoding='utf-8') as f:
        json.dump(items[:5], f, ensure_ascii=False, indent=2)