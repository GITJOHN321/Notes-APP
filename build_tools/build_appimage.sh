#!/bin/bash
set -e

# Limpiar builds anteriores
rm -rf build dist build_tools/MiApp.AppDir NotasPy-x86_64.AppImage

# Empaquetar con PyInstaller
pyinstaller --noconfirm --onefile --noconsole \
    --name MiApp \
    main.py

# Crear estructura AppDir
mkdir -p build_tools/MiApp.AppDir/usr/bin
mkdir -p build_tools/MiApp.AppDir/usr/share/applications
mkdir -p build_tools/MiApp.AppDir/usr/share/icons/hicolor/512x512/apps
mkdir -p build_tools/MiApp.AppDir/usr/lib

# Copiar binario e icono
cp dist/MiApp build_tools/MiApp.AppDir/usr/bin/
cp build_tools/icons/MiApp.png build_tools/MiApp.AppDir/usr/share/icons/hicolor/512x512/apps/
cp build_tools/desktop/MiApp.desktop build_tools/MiApp.AppDir/usr/share/applications/
cp build_tools/desktop/MiApp.desktop build_tools/MiApp.AppDir/
cp build_tools/icons/MiApp.png build_tools/MiApp.AppDir/

# Copiar librería SQLCipher (ajusta ruta si es diferente)
cp /usr/lib/x86_64-linux-gnu/libsqlcipher.so.1.8.0 build_tools/MiApp.AppDir/usr/lib/

# Crear enlaces simbólicos dentro del AppDir
cd build_tools/MiApp.AppDir/usr/lib
ln -s libsqlcipher.so.1.8.0 libsqlcipher.so.1
ln -s libsqlcipher.so.1.8.0 libsqlcipher.so
cd ../../../../  # volver al directorio original

# Copiar AppRun
cp build_tools/AppRun build_tools/MiApp.AppDir/
chmod +x build_tools/MiApp.AppDir/AppRun

# Crear AppImage
./build_tools/appimagetool-x86_64.AppImage --appimage-extract-and-run build_tools/MiApp.AppDir

echo "✅ AppImage generado: NotasPy-x86_64.AppImage"

#Copiar archivo
mkdir -p /output
cp NotasPy-x86_64.AppImage /output/
echo "📦 Copiado NotasPy-x86_64.AppImage a /output/"