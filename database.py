# Se importan los módulos necesarios de SQLAlchemy para definir los modelos y las relaciones ORM.
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Se crea una clase base para los modelos ORM utilizando el sistema declarativo de SQLAlchemy.
Base = declarative_base()

# Se define una tabla intermedia para establecer la relación muchos a muchos entre las citas (quotes) y las etiquetas (tags).
quote_tag = Table('quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quotes.id')),  # Clave foránea que referencia a la tabla de citas.
    Column('tag_id', Integer, ForeignKey('tags.id'))        # Clave foránea que referencia a la tabla de etiquetas.
)

# Se define el modelo que representa una cita (Quote).
class Quote(Base):
    __tablename__ = 'quotes'  # Nombre de la tabla en la base de datos.

    id = Column(Integer, primary_key=True)           # Identificador único de la cita.
    text = Column(String, unique=True)               # Texto de la cita, debe ser único para evitar duplicados.
    author = Column(String)                          # Nombre del autor de la cita.
    # Se establece la relación muchos a muchos con las etiquetas, utilizando la tabla intermedia quote_tag.
    tags = relationship('Tag', secondary=quote_tag, back_populates='quotes')

# Se define el modelo que representa una etiqueta (Tag).
class Tag(Base):
    __tablename__ = 'tags'  # Nombre de la tabla en la base de datos.

    id = Column(Integer, primary_key=True)           # Identificador único de la etiqueta.
    name = Column(String, unique=True)               # Nombre de la etiqueta, debe ser único.
    # Se establece la relación inversa muchos a muchos con las citas.
    quotes = relationship('Quote', secondary=quote_tag, back_populates='tags')

# Se crea el motor de base de datos SQLite, que almacenará los datos en el archivo quotes.db.
engine = create_engine('sqlite:///quotes.db')
# Se crean todas las tablas definidas en los modelos, si aún no existen en la base de datos.
Base.metadata.create_all(engine)
# Se crea una clase de sesión para interactuar con la base de datos.
Session = sessionmaker(bind=engine)
# Se instancia una sesión para realizar operaciones como consultas e inserciones.
session = Session()
