#
# Buildozer specification file for the Donetsk interactive maps app.
#
# This file contains the minimal configuration required to package the
# Kivy client into an Android APK. You can run `buildozer android debug`
# (or `buildozer android debug deploy run` to push it to a connected
# device) from the `client_kivy` directory. Buildozer will install all
# dependencies, fetch the Android SDK/NDK and python-for-android, and
# assemble your APK automatically.

[app]
# (str) Title of your application
title = DonSights

# (str) Package name
package.name = donsights

# (str) Package domain (unique, can be reversed domain-style)
package.domain = com.donsights

# (str) Source code directory (relative to this spec file)
source.dir = .

# (list) Additional source file extensions to include in the APK
source.include_exts = py,kv,png,jpg,jpeg

# (str) Application version
version = 0.1

# (list) Application requirements
# The Kivy client uses the standard library plus the Kivy framework and
# third‑party HTTP libraries. The `legacy‑cgi` requirement is only
# necessary if you build with Python ≥3.13; you can add
# "legacy‑cgi; python_version >= '3.13'" here to avoid import errors.
requirements = python3,kivy,kivy-garden,requests
garden_requirements = mapview

# (str) Supported orientation (one of landscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should run in fullscreen
fullscreen = 1

# (str) Android API level to use (comment to use the default API
# available with python‑for‑android). You can adjust this to match
# your installed SDK version.
android.api = 33

[android]
# (list) Permissions required by your app
android.permissions = INTERNET

# (str) Entry point of your app (default: main.py)
# This is not required unless your entry point differs from `main.py`.
# entrypoint = main.py

[buildozer]
# (int) Buildozer log level (0 = error only, 2 = debug)
log_level = 2

# (bool) Copy the Android APK to the current directory after build
copy_to_current_dir = 1