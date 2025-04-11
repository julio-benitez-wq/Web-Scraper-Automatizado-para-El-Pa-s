# 📰 Web Scraper de Noticias - El País

Este proyecto es un script en Python que extrae automáticamente las últimas noticias del sitio [elpais.com](https://elpais.com/ultimas-noticias/), y las guarda en formatos **CSV** y **JSON** para análisis posterior.

---

## 🚀 Características

- Extracción de títulos, fechas y enlaces de noticias.
- Limpieza automatizada de datos.
- Rotación de headers para evitar bloqueos por scraping.
- Guardado en `data/` en dos formatos: `.csv` y `.json`.
- Logging de errores y actividad en `scraper.log`.

---

## 📂 Estructura del proyecto

web-scraper-el-pais/ ├── scraper.py ├── utils.py ├── requirements.txt ├── README.md ├── scraper.log ├── scheduler.sh └── data/ ├── noticias_YYYY-MM-DD.csv └── noticias_YYYY-MM-DD.json

yaml
Copiar
Editar

---

## ⚙️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu_usuario/web-scraper-el-pais.git
cd web-scraper-el-pais
