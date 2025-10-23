from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import requests
import json

class ConnectScreen(MDScreen):
    def __init__(self, switch_callback, **kwargs):
        super().__init__(**kwargs)
        self.name = "connect"
        self.switch_callback = switch_callback

        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(16))
        self.add_widget(layout)

        self.ip_input = MDTextField(hint_text="IP адрес", text="localhost", size_hint_y=None, height=dp(50))
        layout.add_widget(self.ip_input)

        self.port_input = MDTextField(hint_text="Порт", text="4443", size_hint_y=None, height=dp(50))
        layout.add_widget(self.port_input)

        self.connect_btn = MDRectangleFlatButton(
            text="Подключиться",
            pos_hint={"center_x": 0.5},
            on_release=self.try_connect
        )
        layout.add_widget(self.connect_btn)

    def try_connect(self, instance):
        ip = self.ip_input.text.strip()
        port = self.port_input.text.strip()
        try:
            url = f"https://{ip}:{port}/ping"
            response = requests.get(url, verify=False, timeout=7)
            if response.ok:
                self.switch_callback()  # переход на карту
        except Exception as e:
            print("Ошибка подключения:", e)
