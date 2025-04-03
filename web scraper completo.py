import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
import json
import os

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]

BASE_URLS = {
    "tecnologia": "https://elpais.com/tecnologia/",
    "politica": "https://elpais.com/politica/"
}

HEADERS = {
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://www.google.com/"
}

DELAY = random.uniform(1, 3)
TIMEOUT = 10

def get_random_headers():
    return {
        **HEADERS,
        "User-Agent": random.choice(USER_AGENTS)
    }

def fetch_page(url):
    try:
        response = requests.get(url, headers=get_random_headers(), timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error al obtener {url}: {str(e)}")
        return None

def clean_text(text):
    return " ".join(text.strip().split()) if text else ""

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None

def parse_news(html, category):
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    
    # Selectores actualizados para El País
    for article in soup.select('article'):
        try:
            title_elem = article.select_one('h2 a')
            if not title_elem:
                continue
                
            title = clean_text(title_elem.get_text())
            url = title_elem['href']
            
            # Algunas URLs son relativas
            if url.startswith('/'):
                url = f"https://elpais.com{url}"
            
            date_elem = article.select_one('time')
            date = parse_date(date_elem['datetime']) if date_elem else None
            
            summary_elem = article.select_one('p')
            summary = clean_text(summary_elem.get_text()) if summary_elem else ""
            
            articles.append({
                "title": title,
                "url": url,
                "date": str(date) if date else "",
                "summary": summary,
                "category": category,
                "source": "El País"
            })
        except Exception as e:
            logger.error(f"Error procesando artículo: {str(e)}")
            continue
            
    return articles

def scrape_category(base_url, category):
    html = fetch_page(base_url)
    if not html:
        return []
    
    articles = parse_news(html, category)
    time.sleep(DELAY)
    return articles

def save_data(articles, filename="noticias"):
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(articles)
    
    # Guardar en CSV y JSON
    csv_path = f"data/{filename}.csv"
    json_path = f"data/{filename}.json"
    
    df.to_csv(csv_path, index=False, encoding='utf-8')
    df.to_json(json_path, orient='records', force_ascii=False, indent=2)
    
    logger.info(f"Datos guardados en {csv_path} y {json_path}")
    return csv_path, json_path

def main():
    logger.info("Iniciando scraper de El País...")
    
    all_articles = []
    for category, url in BASE_URLS.items():
        articles = scrape_category(url, category)
        all_articles.extend(articles)
        logger.info(f"Encontradas {len(articles)} noticias de {category}")
    
    if not all_articles:
        logger.error("No se encontraron artículos. Verifica:")
        logger.error("1. Selectores HTML en el código")
        logger.error("2. Conexión a internet")
        return
    
    save_data(all_articles, "elpais_noticias")

if __name__ == "__main__":
    main()