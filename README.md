# DonSights-App

## Для сборки бэкэнда
```sh
docker compose up --build
```

## Для сборки клиент-приложения под Android

### Настройка виртуального окружения и установка зависимостей (Производится один раз)

```sh
python -m venv venv
```
```sh
source venv/bin/activate
```
или
```sh
source venv/bin/activate.fish
```
```sh
cd client
pip install -r requirements.txt
```

### Запуск проекта

```sh
python main.py
```

### Сборка проекта под Android

```sh
buildozer android debug deploy
```