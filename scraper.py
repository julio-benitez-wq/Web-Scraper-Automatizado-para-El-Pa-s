import requests
from bs4 import BeautifulSoup
from utils import get_random_header, clean_text, save_to_csv, save_to_json
from datetime import datetime
import os
import logging

# Configuración de logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ruta para guardar los archivos
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

URL = "https://elpais.com/ultimas-noticias/"

def extraer_noticias():
    logging.info("Iniciando extracción de noticias de El País...")
    try:
        response = requests.get(URL, headers=get_random_header(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        noticias = []
        contenedores = soup.select("article")

        for art in contenedores:
            titulo_tag = art.find('h2')
            fecha_tag = art.find('time')
            enlace_tag = art.find('a')

            if titulo_tag and fecha_tag and enlace_tag:
                noticia = {
                    "titulo": clean_text(titulo_tag.text),
                    "fecha": clean_text(fecha_tag.get("datetime", "Sin fecha")),
                    "enlace": "https://elpais.com" + enlace_tag.get("href")
                }
                noticias.append(noticia)

        if noticias:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            save_to_csv(noticias, f"{DATA_DIR}/noticias_{fecha_hoy}.csv")
            save_to_json(noticias, f"{DATA_DIR}/noticias_{fecha_hoy}.json")
            logging.info(f"Se guardaron {len(noticias)} noticias en CSV y JSON.")
            print(f"✅ Se extrajeron y guardaron {len(noticias)} noticias correctamente.")
        else:
            logging.warning("No se encontraron noticias para extraer.")
            print("⚠️ No se encontraron noticias para guardar.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error de conexión: {e}")
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    extraer_noticias()
