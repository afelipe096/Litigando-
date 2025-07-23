# Importa Flask para crear la API web y los módulos necesarios para manejar peticiones y respuestas
from flask import Flask, request, jsonify
# Importa joinedload para cargar relaciones de manera eficiente
from sqlalchemy.orm import joinedload
# Importa los modelos y la sesión de la base de datos
from database import Quote, Tag, Session

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define una ruta para obtener citas (quotes) con filtros opcionales
@app.route('/quotes', methods=['GET'])
def get_quotes():
    # Crea una nueva sesión de base de datos para esta petición
    session = Session()
    # Prepara la consulta base, cargando también las etiquetas relacionadas
    query = session.query(Quote).options(joinedload(Quote.tags))

    # Obtiene los parámetros de la URL para filtrar resultados
    author = request.args.get("author")
    tag = request.args.get("tag")
    search = request.args.get("search")

    # Si se proporciona un autor, filtra las citas por autor (búsqueda parcial, insensible a mayúsculas)
    if author:
        query = query.filter(Quote.author.ilike(f"%{author}%"))
    # Si se proporciona un texto de búsqueda, filtra las citas cuyo texto contenga ese valor
    if search:
        query = query.filter(Quote.text.ilike(f"%{search}%"))
    # Si se proporciona una etiqueta, filtra las citas que tengan esa etiqueta (búsqueda parcial)
    if tag:
        query = query.join(Quote.tags).filter(Tag.name.ilike(f"%{tag}%"))

    # Ejecuta la consulta y obtiene todas las citas que cumplen los filtros
    quotes = query.all()
    result = []
    # Construye la respuesta en formato JSON
    for quote in quotes:
        result.append({
            "text": quote.text,  # Corrige el nombre del atributo (antes estaba mal escrito como 'trext')
            "author": quote.author,
            "tags": [t.name for t in quote.tags]  # Lista de nombres de etiquetas asociadas
        })

    # Devuelve la lista de citas como respuesta JSON
    return jsonify(result)

# Punto de entrada principal para ejecutar la aplicación Flask en modo debug
if __name__ == "__main__":
    app.run(debug=True)