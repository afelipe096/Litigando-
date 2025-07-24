# Importa los módulos necesarios de SQLAlchemy para definir modelos y relaciones ORM
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Crea una clase base para los modelos ORM usando el sistema declarativo de SQLAlchemy
Base = declarative_base()

# Define una tabla intermedia para la relación muchos a muchos entre citas (quotes) y etiquetas (tags)
quote_tag = Table('quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quotes.id')),  # Clave foránea a la tabla de citas
    Column('tag_id', Integer, ForeignKey('tags.id'))        # Clave foránea a la tabla de etiquetas
)

# Modelo que representa una cita (Quote)
class Quote(Base):
    __tablename__ = 'quotes'  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True)           # Identificador único de la cita
    text = Column(String, unique=True)               # Texto de la cita, debe ser único
    author = Column(String)                          # Autor de la cita
    # Relación muchos a muchos con etiquetas, usando la tabla intermedia quote_tag
    tags = relationship('Tag', secondary=quote_tag, back_populates='quotes')

# Modelo que representa una etiqueta (Tag) 
class Tag(Base):
    __tablename__ = 'tags'  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True)           # Identificador único de la etiqueta
    name = Column(String, unique=True)               # Nombre de la etiqueta, debe ser único
    # Relación inversa muchos a muchos con citas
    quotes = relationship('Quote', secondary=quote_tag, back_populates='tags')

# Crea el motor de base de datos SQLite (archivo quotes.db en el directorio actual)
engine = create_engine('sqlite:///quotes.db')
# Crea todas las tablas definidas en los modelos si no existen
Base.metadata.create_all(engine)
# Crea una clase de sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
# Instancia una sesión para realizar operaciones (consultas, inserciones, etc.)
session = Session()
