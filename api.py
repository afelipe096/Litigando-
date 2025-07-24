# Se importa Flask para crear la API web, junto con los módulos necesarios para manejar peticiones y respuestas.
from flask import Flask, request, jsonify
# Se importa joinedload para optimizar la carga de relaciones entre tablas al hacer consultas.
from sqlalchemy.orm import joinedload
# Se importan los modelos y la clase de sesión desde el módulo de base de datos.
from database import Quote, Tag, Session

# Se crea una instancia de la aplicación Flask.
app = Flask(__name__)

# Se define una ruta para obtener citas (quotes) mediante el método GET.
@app.route('/quotes', methods=['GET'])
def get_quotes():
    # Se crea una nueva sesión de base de datos para manejar la petición actual.
    session = Session()
    # Se prepara la consulta base, incluyendo la carga de las etiquetas asociadas a cada cita.
    query = session.query(Quote).options(joinedload(Quote.tags))

    # Se obtienen los parámetros de la URL para permitir el filtrado de resultados.
    author = request.args.get("author")
    tag = request.args.get("tag")
    search = request.args.get("search")

    # Si se especifica un autor, se filtran las citas por autor (búsqueda parcial, sin distinguir mayúsculas).
    if author:
        query = query.filter(Quote.author.ilike(f"%{author}%"))
    # Si se especifica un texto de búsqueda, se filtran las citas cuyo texto contenga ese valor.
    if search:
        query = query.filter(Quote.text.ilike(f"%{search}%"))
    # Si se especifica una etiqueta, se filtran las citas que tengan esa etiqueta (búsqueda parcial).
    if tag:
        query = query.join(Quote.tags).filter(Tag.name.ilike(f"%{tag}%"))

    # Se ejecuta la consulta y se obtienen todas las citas que cumplen con los filtros.
    quotes = query.all()
    result = []
    # Se construye la respuesta en formato JSON, incluyendo texto, autor y etiquetas de cada cita.
    for quote in quotes:
        result.append({
            "text": quote.text,  # Texto de la cita.
            "author": quote.author, # Autor de la cita.
            "tags": [t.name for t in quote.tags]  # Lista de nombres de etiquetas asociadas.
        })

    # Se devuelve la lista de citas como respuesta en formato JSON.
    return jsonify(result)

# Punto de entrada principal para ejecutar la aplicación Flask en modo debug.
if __name__ == "__main__":
    app.run(debug=True)