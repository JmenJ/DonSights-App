from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.mapview import MapView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
import urllib3
import requests
import json

# Отключим предупреждения от urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Получим DPI и определим масштаб интерфейса
dpi_scale = max(Window.dpi / 160.0, 1.0)

class ConnectScreen(BoxLayout):
    def __init__(self, switch_callback, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(16), padding=dp(20) * dpi_scale, **kwargs)
        self.switch_callback = switch_callback

        self.ip_input = TextInput(
            hint_text='IP адрес',
            text="localhost",
            size_hint=(1, None),
            height=dp(50) * dpi_scale,
            font_size=sp(18) * dpi_scale,
            multiline=False
        )
        self.add_widget(self.ip_input)

        self.port_input = TextInput(
            hint_text='Порт',
            text="4443",
            size_hint=(1, None),
            height=dp(50) * dpi_scale,
            font_size=sp(18) * dpi_scale,
            multiline=False
        )
        self.add_widget(self.port_input)

        self.status_label = Label(
            text='',
            size_hint=(1, None),
            height=dp(40) * dpi_scale,
            font_size=sp(16) * dpi_scale,
            color=(1, 0, 0, 1)
        )
        self.add_widget(self.status_label)

        self.connect_btn = Button(
            text='Подключиться',
            size_hint=(1, None),
            height=dp(60) * dpi_scale,
            font_size=sp(20) * dpi_scale,
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
        )
        self.connect_btn.bind(on_press=self.try_connect)
        self.add_widget(self.connect_btn)

    def try_connect(self, instance):
        ip = self.ip_input.text.strip()
        port = self.port_input.text.strip()
        if not ip or not port:
            self.status_label.text = 'Введите IP и порт.'
            return

        try:
            url = f"https://{ip}:{port}/ping"
            response = requests.get(url, verify=False, timeout=7)
            if response.ok:
                data = response.json()
                if any(str(v).lower() in ('ok', 'pong') for v in data.values()):
                    self.status_label.text = ''
                    self.switch_callback()  # Переход на карту
                    return
                self.status_label.text = json.dumps(data, ensure_ascii=False)
            else:
                self.status_label.text = f"Ошибка: статус {response.status_code}"
        except Exception as exc:
            self.status_label.text = f"Ошибка подключения: {exc}"

class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_view = MapView(zoom=18, lat=47.991551, lon=37.798513)  # Донецк
        self.add_widget(self.map_view)

class MainApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.connect_screen = Screen(name='connect')
        self.connect_screen.add_widget(ConnectScreen(switch_callback=self.show_map))

        self.map_screen = MapScreen(name='map')

        self.sm.add_widget(self.connect_screen)
        self.sm.add_widget(self.map_screen)

        return self.sm

    def show_map(self):
        self.sm.current = 'map'

if __name__ == '__main__':
    MainApp().run()