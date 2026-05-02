[app]
# (str) Title of your application
title = Estadistica Maranatha

# (str) Package name
package.name = estadistica_maranatha

# (str) Package domain (needed for android/ios packaging)
package.domain = org.maranatha

# (str) Application versioning (method 1)
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db,json

# (list) Application requirements
# Solo incluimos reportlab que es lo único necesario para los gráficos en PDF
# matplotlib, numpy y pillow NO son necesarios ya que reportlab tiene su propia implementación de gráficos
requirements = python3,kivy==2.3.0,sqlalchemy,certifi,urllib3,idna,requests,python-dotenv,reportlab

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# El PDF se guarda en el almacenamiento privado de la app, así que no hace falta pedir permisos de almacenamiento.
# Se agrega ACCESS_NETWORK_STATE para verificar conectividad antes de sincronizar con Firebase
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Android API to use (Android 14 - requerido para dispositivos modernos)
android.api = 34

# (int) Minimum API your APK will support (Android 8.0 - necesario para Python 3.8+ y compatibilidad con Android 14)
android.minapi = 26

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# Importante: incluir ambas arquitecturas para mayor compatibilidad
android.archs = arm64-v8a, armeabi-v7a

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1

# (int) Build version (incrementa con cada build)
build.version = 1

# (list) Extra arguments to pass to the build
# Importante para Android 14: forzar el uso de la última versión de build tools y habilitar backup
android.build_extra_args = --allow-backup=true

# (bool) Whether to use Gradle daemon or not
android.gradle_build_daemon = True