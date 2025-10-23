from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.metrics import dp
import requests

class MapScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "map"
        root = FloatLayout()
        self.add_widget(root)

        self.map_view = MapView(zoom=15, lat=0, lon=0)
        root.add_widget(self.map_view)
        self.add_user_location()

        self.toolbar = MDTopAppBar(title="DonSights", right_action_items=[["login", lambda x: print("Войти")]], pos_hint={"top":1})
        root.add_widget(self.toolbar)

        self.search_input = MDTextField(
            hint_text="Поиск...",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x":0.5, "y":0.05},
            mode="rectangle"
        )
        root.add_widget(self.search_input)

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
