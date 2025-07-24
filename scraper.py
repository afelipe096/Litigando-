import requests  # Importa la librería requests para hacer peticiones HTTP
import sqlite3   # Importa sqlite3 para manejar la base de datos SQLite
from bs4 import BeautifulSoup  # Importa BeautifulSoup para parsear HTML

# URL base del sitio web de donde se van a extraer las citas
URL = "https://quotes.toscrape.com/"

def scrape_quote():
    """
    Función para extraer todas las citas de la página web.
    Retorna una lista de diccionarios, cada uno con el texto, autor y tags de una cita.
    """
    all_quotes = []  # Lista para almacenar todas las citas extraídas
    page = 1  # Contador de página para la paginación

    while True:
        print(f"Scraping page {page}...")  # Imprime la página que se está extrayendo

        # Realiza la petición HTTP a la página correspondiente
        response = requests.get(URL + f"page/{page}/")
        # Parsea el contenido HTML de la respuesta
        soup = BeautifulSoup(response.text, "html.parser")

        # Busca todos los divs con clase "quote" (cada cita)
        quotes = soup.find_all("div", class_="quote")
        if not quotes:
            # Si no encuentra más citas, termina el ciclo
            break

        # Itera sobre cada cita encontrada en la página
        for quote in quotes:
            # Extrae el texto de la cita
            text = quote.find("span", class_="text").get_text()
            # Extrae el autor de la cita
            author = quote.find("small", class_="author").get_text()
            # Extrae los tags asociados a la cita
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

            # Agrega la cita a la lista de todas las citas
            all_quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        page += 1  # Pasa a la siguiente página

    return all_quotes  # Retorna la lista de todas las citas

if __name__ == "__main__":
    # Si el script se ejecuta directamente, comienza la extracción de citas
    data = scrape_quote()
    print(f"Se extrajeron {len(data)} citas")  # Imprime cuántas citas se extrajeron

    # Conectar a la base de datos SQLite (crea el archivo si no existe)
    conn = sqlite3.connect("quotes.db")
    cursor = conn.cursor()

    # Crear la tabla 'quotes' si no existe, con columnas id, text y author
    cursor.execute('''
         Función para extraer todas las citas de la página web.
    Retorna una lista de diccionarios, cada uno con el texto, autor y etiquetas (tags) de una cita.
        )
    ''')

    # Insertar cada cita extraída en la base de datos
    for quote in data:
        cursor.execute(
            "INSERT INTO quotes (text, author) VALUES (?, ?)",
            (quote["text"], quote["author"])
        )

    # Guardar los cambios realizados en la base de datos
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()
    print("Citas guardadas en la base de datos.")  # Mensaje final de confirmación
