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
# Incluimos todas las dependencias detectadas en requirements.txt
requirements = python3,kivy==2.3.1,sqlalchemy,certifi,urllib3,idna,requests,python-dotenv

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# El PDF se guarda en el almacenamiento privado de la app, así que no hace falta pedir permisos de almacenamiento.
android.permissions = INTERNET

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1