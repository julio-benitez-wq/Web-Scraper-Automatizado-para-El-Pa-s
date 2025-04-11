import random
import json
import csv

# Lista de headers simulando navegadores reales
HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)..."},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)..."},
]

def get_random_header():
    """Devuelve un header HTTP aleatorio para evitar bloqueos por scraping."""
    return random.choice(HEADERS_LIST)

def clean_text(text):
    """Limpia texto eliminando saltos, espacios y caracteres especiales."""
    return ' '.join(text.strip().replace('\n', '').split())

def save_to_csv(data, filepath):
    """Guarda datos en formato CSV."""
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def save_to_json(data, filepath):
    """Guarda datos en formato JSON."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
