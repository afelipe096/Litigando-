# rpa_quotes_project

## Descripción

Este proyecto realiza la extracción (scraping) de citas desde [quotes.toscrape.com](https://quotes.toscrape.com/), almacena los datos en una base de datos SQLite y expone una API REST para consultar las citas, autores y etiquetas. Incluye scripts para scraping, modelos de base de datos con SQLAlchemy y una API desarrollada con Flask.

## Estructura del repositorio

```
rpa_quotes_project/
│
├── api.py                # API REST con Flask
├── database.py           # Modelos y configuración de la base de datos (SQLAlchemy)
├── scraper.py            # Script para extraer y guardar citas
├── requirements.txt      # Dependencias del proyecto
├── Dockerfile            # (Opcional) Archivo para crear imagen Docker
├── README.md             # Este archivo
└── quotes.db             # Base de datos SQLite (se genera al ejecutar los scripts)
```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/afelipe096/Litigando-.git
   cd rpa_quotes_project
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### 1. Extraer las citas y poblar la base de datos

Ejecuta el script de scraping:
```bash
python scraper.py
```
Esto descargará todas las citas y las almacenará en `quotes.db`.

### 2. Ejecutar la API

Inicia el servidor Flask:
```bash
python api.py
```
Por defecto, la API estará disponible en `http://127.0.0.1:5000/quotes`.

#### Parámetros de consulta disponibles:
- `author`: filtra por autor (ejemplo: `/quotes?author=Einstein`)
- `tag`: filtra por etiqueta (ejemplo: `/quotes?tag=inspirational`)
- `search`: busca texto en la cita (ejemplo: `/quotes?search=life`)

### 3. (Opcional) Ejecutar con Docker

Si tienes Docker instalado, puedes construir y correr el contenedor:
```bash
docker build -t rpa_quotes_project .
docker run -p 8000:8000 rpa_quotes_project
```
> Nota: El Dockerfile está preparado para aplicaciones FastAPI/Uvicorn. Si usas Flask, modifica el CMD en el Dockerfile o crea uno específico para Flask.

## Scripts de base de datos

La base de datos se crea automáticamente al ejecutar `scraper.py` o `database.py`. Los modelos están definidos en `database.py`.

## Dependencias

- Flask
- requests
- beautifulsoup4
- SQLAlchemy

Todas las dependencias están listadas en `requirements.txt`.

