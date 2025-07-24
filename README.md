 Descripción

Este proyecto realiza scraping de citas desde el sitio https://quotes.toscrape.com, almacena los datos en una base de datos SQLite utilizando SQLAlchemy y expone una API REST con Flask para consultar citas, autores y etiquetas.

Incluye scripts para scraping, definición de modelos con SQLAlchemy, y un servidor API local para pruebas o despliegue.

 Estructura del repositorio

rpa_quotes_project/
│
├── api.py                # API REST con Flask
├── database.py           # Modelos y configuración de la base de datos (SQLAlchemy)
├── scraper.py            # Script para extraer y guardar citas
├── requirements.txt      # Dependencias del proyecto
├── Dockerfile            # Archivo para crear imagen Docker
├── README.md             # Documentación del proyecto
└── quotes.db             # Base de datos SQLite (se genera automáticamente)

 Instalación

1. Clona el repositorio:
   git clone https://github.com/afelipe096/Litigando-.git
   cd rpa_quotes_project

2. Crea un entorno virtual (opcional pero recomendado):
   python -m venv venv
   En Linux/macOS: source venv/bin/activate
   En Windows: venv\Scripts\activate

3. Instala las dependencias:
   pip install -r requirements.txt

Uso del proyecto

1. Ejecutar el script de scraping:
   python scraper.py

   Esto descarga todas las citas y las guarda en quotes.db.

2. Levantar la API con Flask:
   python api.py

   Accede a la API en: http://127.0.0.1:5000/quotes

   Parámetros de consulta:
   - author: /quotes?author=Einstein
   - tag: /quotes?tag=inspirational
   - search: /quotes?search=life

3. Ejecutar con Docker (opcional):
   docker build -t rpa_quotes_project .
   docker run -p 5000:5000 rpa_quotes_project

   Asegúrate que el Dockerfile tenga al final:
   CMD ["python", "api.py"]

 Base de datos

La base de datos se crea automáticamente al ejecutar scraper.py.
Los modelos están en database.py usando SQLAlchemy.

Puedes abrir quotes.db con DB Browser for SQLite para consultar directamente.

 Dependencias

- Flask
- requests
- beautifulsoup4
- SQLAlchemy

Contacto

Autor: Andrés Felipe Currea
GitHub: https://github.com/afelipe096
