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

"""
Обновлённый клиент на Kivy для отправки запроса на сервер.

В этой версии интерфейс был переработан: добавлены поля для ввода IP‑адреса и порта,
кнопка отправки запроса и базовое оформление в духе современных приложений.
Пользователь может указать адрес сервера и порт, после чего получить ответ
от эндпоинта `/ping`.  Результат запроса отображается во всплывающем окне.

Для корректной работы требуется установить зависимости из `requirements.txt`.
Если сервер использует самоподписанный сертификат, проверка SSL отключается
через `verify=False`.  В боевом окружении используйте реальный сертификат.
"""

import json
from typing import Optional

import requests
import urllib3

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Отключаем предупреждения об использовании самоподписанного сертификата.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MainWidget(BoxLayout):
    """Главный виджет приложения.

    Содержит два поля ввода (IP‑адрес и порт) и кнопку для отправки запроса.
    Отображает результат в модальном окне.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="vertical", padding=24, spacing=16, **kwargs)

        # Задаём нейтральный цвет фона и базовые размеры окна
        Window.clearcolor = (0.95, 0.95, 0.95, 1)

        # Поле для ввода IP‑адреса
        self.ip_input: TextInput = TextInput(
            hint_text="IP‑адрес сервера",
            text="",  # оставляем пустым — пользователь введёт сам
            multiline=False,
            size_hint=(1, None),
            height=48,
            padding=[12, 14, 12, 14],
            foreground_color=(0.1, 0.1, 0.1, 1),
            background_color=(1, 1, 1, 1),
            cursor_color=(0.2, 0.6, 0.9, 1),
            font_size=18,
        )
        self.add_widget(self.ip_input)

        # Поле для ввода порта. По умолчанию 4443
        self.port_input: TextInput = TextInput(
            hint_text="Порт (по умолчанию 4443)",
            text="4443",
            multiline=False,
            size_hint=(1, None),
            height=48,
            padding=[12, 14, 12, 14],
            foreground_color=(0.1, 0.1, 0.1, 1),
            background_color=(1, 1, 1, 1),
            cursor_color=(0.2, 0.6, 0.9, 1),
            font_size=18,
            input_filter="int",
        )
        self.add_widget(self.port_input)

        # Кнопка отправки запроса
        self.send_button: Button = Button(
            text="Отправить запрос",
            size_hint=(1, None),
            height=56,
            font_size=18,
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.25, 0.47, 0.8, 1),  # синий цвет в духе Material
        )
        self.send_button.bind(on_press=self.on_press)
        self.add_widget(self.send_button)

    def build_url(self) -> Optional[str]:
        """Формирует URL из значений полей.

        Returns:
            str | None: Полный URL для запроса. Если IP не указан, возвращает None.
        """
        ip = self.ip_input.text.strip()
        port = self.port_input.text.strip() or "4443"
        if not ip:
            return None
        return f"https://{ip}:{port}/ping"

    def on_press(self, instance: Button) -> None:
        """Обработчик нажатия на кнопку.

        Формирует URL, отправляет GET‑запрос и отображает результат.
        """
        url = self.build_url()
        if not url:
            self.show_popup("Ошибка", "Пожалуйста, введите IP‑адрес сервера.")
            return

        try:
            response = requests.get(url, verify=False, timeout=7)
            if response.ok:
                data = response.json()
                content = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                content = f"Код ответа: {response.status_code}"
        except Exception as exc:
            content = f"Ошибка: {exc}"
        self.show_popup("Ответ сервера", content)

    def show_popup(self, title: str, content: str) -> None:
        """Отображает модальное окно с заголовком и содержимым."""
        popup = Popup(
            title=title,
            content=Label(
                text=content,
                color=(0, 0, 0, 1),
                font_size=16,
                text_size=(0.9 * Window.width, None),
                halign="left",
                valign="top",
            ),
            size_hint=(0.9, 0.5),
        )
        popup.open()

class PingApp(App):
    """Класс приложения, инициализирующий основной виджет."""

    def build(self) -> MainWidget:
        return MainWidget()

if __name__ == "__main__":
    PingApp().run()