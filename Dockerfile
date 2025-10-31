# Base con Python 3.12
FROM python:3.12-slim

# Evitar interacciones
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt update && apt install -y \
    build-essential git wget curl \
    libsqlcipher-dev sqlcipher libfuse2 \
    xz-utils zip unzip \
    python3-tk file \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar código y archivos de build
COPY . /app

# Instalar librerías Python necesarias
RUN pip install --upgrade pip setuptools wheel
RUN pip install pyinstaller pyinstaller-hooks-contrib customtkinter darkdetect sqlcipher3

# Copiar appimagetool y dar permisos
RUN chmod +x /app/build_tools/appimagetool-x86_64.AppImage

# Comando por defecto para generar AppImage
CMD ["bash", "/app/build_tools/build_appimage.sh"]
