# DonSights-App

## Для сборки бэкэнда
```sh
docker compose up --build
```

## Для сборки клиент-приложения под Android

### Настройка виртуального окружения и установка зависимостей (Производится один раз)

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd client
```

### Запуск проекта

```sh
python main.py
```
