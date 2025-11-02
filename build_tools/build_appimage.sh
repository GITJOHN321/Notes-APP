#!/bin/bash
set -e


# -----------------------------
# 1️⃣ Limpiar builds anteriores
# -----------------------------
rm -rf build dist MiApp.AppDir NotasPy-x86_64.AppImage

# -----------------------------
# 2️⃣ Empaquetar con PyInstaller
# -----------------------------
# Nota: No usamos --add-binary para la librería SQLCipher
pyinstaller --noconfirm --onefile --noconsole \
    --name MiApp \
    main.py

# -----------------------------
# 3️⃣ Crear estructura AppDir
# -----------------------------
mkdir -p MiApp.AppDir/usr/bin
mkdir -p MiApp.AppDir/usr/lib
mkdir -p MiApp.AppDir/usr/share/applications
mkdir -p MiApp.AppDir/usr/share/icons/hicolor/512x512/apps

# -----------------------------
# 4️⃣ Copiar binario, icono y desktop
# -----------------------------

cp dist/MiApp MiApp.AppDir/usr/bin/
cp build_tools/libs/libsqlcipher.so.1.8.0 MiApp.AppDir/usr/lib/
cp build_tools/desktop/MiApp.desktop MiApp.AppDir/usr/share/applications/
cp build_tools/desktop/MiApp.desktop MiApp.AppDir/
cp build_tools/icons/MiApp.png MiApp.AppDir/usr/share/icons/hicolor/512x512/apps/
cp build_tools/icons/MiApp.png MiApp.AppDir/

# Copiar fuentes al AppDir
mkdir -p MiApp.AppDir/usr/share/fonts/truetype/fontawesome
cp build_tools/fonts/*.otf MiApp.AppDir/usr/share/fonts/truetype/fontawesome/

# Regenerar caché de fuentes dentro del AppImage
fc-cache -f -v MiApp.AppDir/usr/share/fonts/truetype/fontawesome/


# Crear enlaces simbólicos dentro del AppDir
ln -sf /app/MiApp.AppDir/usr/lib/libsqlcipher.so.1.8.0 /app/MiApp.AppDir/usr/lib/libsqlcipher.so.1
ln -sf /app/MiApp.AppDir/usr/lib/libsqlcipher.so.1.8.0 /app/MiApp.AppDir/usr/lib/libsqlcipher.so

# Tk
ln -sf libtk8.6.so libtk.so

# Tcl
ln -sf libtcl8.6.so libtcl.so

# -----------------------------
# 6️⃣ Copiar AppRun y dar permisos
# -----------------------------
cp build_tools/AppRun MiApp.AppDir/
chmod +x MiApp.AppDir/AppRun

# Crear AppImage
./build_tools/appimagetool-x86_64.AppImage --appimage-extract-and-run MiApp.AppDir

echo "✅ AppImage generado: NotasPy-x86_64.AppImage"

#Copiar archivo
mkdir -p /output
cp NotasPy-x86_64.AppImage /output/
echo "📦 Copiado NotasPy-x86_64.AppImage a /output/"