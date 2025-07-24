# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto por donde se accede al API
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "api.py"]
