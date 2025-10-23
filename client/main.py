from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.metrics import dp
import requests
import json

# ----------------- Экран подключения -----------------
class ConnectScreen(MDScreen):
    def __init__(self, switch_callback, **kwargs):
        super().__init__(**kwargs)
        self.name = "connect"  # <-- имя экрана для ScreenManager
        self.switch_callback = switch_callback

        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(16))
        self.add_widget(layout)

        self.ip_input = MDTextField(
            hint_text="IP адрес",
            text="localhost",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(self.ip_input)

        self.port_input = MDTextField(
            hint_text="Порт",
            text="4443",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(self.port_input)

        self.status_label = BoxLayout(size_hint_y=None, height=dp(30))
        layout.add_widget(self.status_label)

        self.connect_btn = MDRectangleFlatButton(
            text="Подключиться",
            pos_hint={"center_x": 0.5},
            on_release=self.try_connect
        )
        layout.add_widget(self.connect_btn)

    def try_connect(self, instance):
        ip = self.ip_input.text.strip()
        port = self.port_input.text.strip()
        if not ip or not port:
            self.status_label.clear_widgets()
            self.status_label.add_widget(MDTextField(text="Введите IP и порт"))
            return
        try:
            url = f"https://{ip}:{port}/ping"
            response = requests.get(url, verify=False, timeout=7)
            if response.ok:
                data = response.json()
                if any(str(v).lower() in ('ok', 'pong') for v in data.values()):
                    self.status_label.clear_widgets()
                    self.switch_callback()  # Переход на карту
                    return
                self.status_label.clear_widgets()
                self.status_label.add_widget(MDTextField(text=json.dumps(data, ensure_ascii=False)))
            else:
                self.status_label.clear_widgets()
                self.status_label.add_widget(MDTextField(text=f"Ошибка: статус {response.status_code}"))
        except Exception as exc:
            self.status_label.clear_widgets()
            self.status_label.add_widget(MDTextField(text=f"Ошибка подключения: {exc}"))

# ----------------- Экран карты -----------------
class MapScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "map"
        root = FloatLayout()
        self.add_widget(root)

        # Карта
        self.map_view = MapView(zoom=15, lat=0, lon=0)
        root.add_widget(self.map_view)

        # Хедер сверху
        self.toolbar = MDTopAppBar(
            title="DonSights",
            right_action_items=[["login", lambda x: print("Войти")]],
            pos_hint={"top": 1}
        )
        root.add_widget(self.toolbar)

        # Поиск снизу
        self.search_input = MDTextField(
            hint_text="Поиск...",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "y": 0.05},
            mode="rectangle"
        )
        root.add_widget(self.search_input)

        # Теперь вызываем метод после того, как self.map_view создан
        self.add_user_location()

    def add_user_location(self):
        try:
            res = requests.get("https://ipinfo.io/json").json()
            loc = res['loc'].split(',')
            lat, lon = float(loc[0]), float(loc[1])
            self.map_view.center_on(lat, lon)
            marker = MapMarker(lat=lat, lon=lon)
            self.map_view.add_widget(marker)
        except Exception as e:
            print("Не удалось получить геопозицию:", e)


# ----------------- Основное приложение -----------------
class MainApp(MDApp):
    def build(self):
        self.sm = MDScreenManager()

        self.connect_screen = ConnectScreen(switch_callback=self.show_map)
        self.map_screen = MapScreen()

        self.sm.add_widget(self.connect_screen)
        self.sm.add_widget(self.map_screen)

        return self.sm

    def show_map(self):
        self.sm.current = "map"  # <-- теперь переключение работает

if __name__ == "__main__":
    MainApp().run()
