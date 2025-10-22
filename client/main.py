"""
Простой клиент на Kivy для взаимодействия с сервером, который
прослушивает эндпоинт https://localhost:4443/ping.  По нажатию на кнопку
отправляется HTTPS‑запрос и результат отображается в всплывающем окне.

Kivy — это кроссплатформенный фреймворк для создания GUI
приложений на Python.  Для работы этого примера понадобится
установить зависимости из requirements.txt.

Сервер, к которому обращается клиент, работает на самоподписанном
сертификате.  Поэтому параметр `verify=False` отключает проверку
сертификата.  В продакшене следует использовать корректный сертификат
и убрать этот параметр.
"""

import json
import requests
import urllib3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://localhost:4443/ping"  # адрес backend‑сервиса


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.button = Button(
            text="Проверить соединение", size_hint=(1, None), height=50
        )
        self.button.bind(on_press=self.on_press)
        self.add_widget(self.button)

    def on_press(self, instance):
        try:
            response = requests.get(API_URL, verify=False, timeout=5)
            if response.ok:
                data = response.json()
                content = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                content = f"Код ответа: {response.status_code}"
        except Exception as exc:
            content = f"Ошибка: {exc}"
        popup = Popup(
            title="Ответ сервера",
            content=Label(text=content),
            size_hint=(0.8, 0.4),
        )
        popup.open()


class PingApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    PingApp().run()