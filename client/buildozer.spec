[app]
title = DonSights
package.name = donsights
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,kivymd,plyer,requests,geopy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0

# 👇 указываем путь к уже клонированному python-for-android
p4a.source_dir = /root/.buildozer/android/platform/python-for-android

android.api = 33
android.minapi = 27
android.sdk = 33
android.ndk = 25b
android.ndk_path = /opt/android-sdk/ndk/25.2.9519653
android.sdk_path = /opt/android-sdk
android.build_tools = 33.0.2
