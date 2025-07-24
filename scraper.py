import requests  # Se importa la librería requests para realizar solicitudes HTTP a páginas web.
import sqlite3   # Se importa sqlite3 para gestionar la base de datos local SQLite.
from bs4 import BeautifulSoup  # Se importa BeautifulSoup para analizar y extraer información de documentos HTML.

# Se define la URL base del sitio web del cual se extraerán las citas.
URL = "https://quotes.toscrape.com/"

def scrape_quote():
    """
    Esta función se encarga de recorrer todas las páginas del sitio web de citas,
    extrayendo el texto, el autor y las etiquetas asociadas a cada cita.
    Devuelve una lista de diccionarios, donde cada diccionario representa una cita.
    """
    all_quotes = []  # Aquí se almacenarán todas las citas recolectadas.
    page = 1  # Se inicializa el contador de páginas para la navegación paginada.

    while True:
        print(f"Scraping page {page}...")  # Se indica en consola qué página se está procesando.

        response = requests.get(URL + f"page/{page}/")  # Se realiza la petición HTTP a la página correspondiente.
        soup = BeautifulSoup(response.text, "html.parser")  # Se parsea el HTML recibido.

        quotes = soup.find_all("div", class_="quote")  # Se buscan todos los bloques de citas en la página.
        if not quotes:
            break  # Si no se encuentran más citas, se termina el ciclo.

        for quote in quotes:
            text = quote.find("span", class_="text").get_text()  # Se extrae el texto de la cita.
            author = quote.find("small", class_="author").get_text()  # Se extrae el nombre del autor.
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]  # Se extraen todas las etiquetas asociadas.

            all_quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })  # Se agrega la cita extraída a la lista principal.

        page += 1  # Se avanza a la siguiente página.

    return all_quotes  # Se retorna la lista completa de citas extraídas.


# Punto de entrada principal del script.
if __name__ == "__main__":
    data = scrape_quote()  # Se llama a la función para extraer las citas y se almacena el resultado.
    print(f"Se extrajeron {len(data)} citas")  # Se muestra cuántas citas fueron extraídas.

    # Se establece la conexión con la base de datos SQLite (se crea el archivo si no existe).
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    # Se crea la tabla 'quotes' si aún no existe, incluyendo una columna para almacenar las etiquetas como texto.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author TEXT,
            tags TEXT
        )
    ''')

    # Se insertan todas las citas extraídas en la base de datos.
    for quote in data:
        cursor.execute(
            "INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (quote["text"], quote["author"], ", ".join(quote["tags"]))
        )

    # Se guardan los cambios realizados y se cierra la conexión con la base de datos.
    conn.commit()
    conn.close()
    print("Citas guardadas en la base de datos.")
