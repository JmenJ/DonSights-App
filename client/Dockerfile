FROM python:3.10-bullseye

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    git zip unzip wget curl python3-pip libffi-dev libssl-dev \
    libjpeg-dev libfreetype6-dev zlib1g-dev liblcms2-dev libblas-dev liblapack-dev \
    pkg-config autoconf automake libtool build-essential libgl1-mesa-dev \
    openjdk-17-jdk ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Установка Android SDK
ENV ANDROID_HOME /opt/android-sdk
ENV PATH ${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/build-tools/33.0.2

RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    cd ${ANDROID_HOME}/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O tools.zip && \
    unzip tools.zip && \
    mkdir -p ${ANDROID_HOME}/cmdline-tools/latest && \
    mv cmdline-tools/* ${ANDROID_HOME}/cmdline-tools/latest/ && \
    rm tools.zip

# Установка SDK-компонентов
RUN yes | sdkmanager --sdk_root=${ANDROID_HOME} --licenses && \
    sdkmanager --sdk_root=${ANDROID_HOME} \
        "platform-tools" \
        "platforms;android-33" \
        "build-tools;33.0.2" \
        "ndk;25.2.9519653"

# Установка Python-пакетов
RUN pip install --upgrade pip Cython buildozer virtualenv

WORKDIR /app
