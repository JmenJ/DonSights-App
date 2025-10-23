from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock

import requests

# Для GPS на мобильных устройствах
try:
    from plyer import gps
    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False


class SearchField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(0.9, None)
        self.height=dp(50)
        self.pos_hint={"center_x":0.5, "y":0.05}

        with self.canvas.before:
            Color(1, 1, 1, 0.9)  # белый фон
            self.rect = RoundedRectangle(radius=[dp(10)], pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.text_input = MDTextField(hint_text="Поиск...", mode="rectangle")
        self.add_widget(self.text_input)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MapScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "map"
        root = FloatLayout()
        self.add_widget(root)

        # Карта
        self.map_view = MapView(zoom=15, lat=0, lon=0)
        root.add_widget(self.map_view)

        # Маркер пользователя
        self.user_marker = None

        # Хедер сверху
        self.toolbar = MDTopAppBar(
            title="DonSights",
            right_action_items=[["login", lambda x: print("Войти")]],
            pos_hint={"top":1}
        )
        root.add_widget(self.toolbar)

       # Поиск снизу через кастомный SearchField
        self.search_input = SearchField()
        root.add_widget(self.search_input)


        # Определяем геопозицию GPS через Plyer (Android) и fallback на ПК
        if GPS_AVAILABLE:
            try:
                gps.configure(on_location=self.update_location)
                gps.start(minTime=1000, minDistance=1)
            except NotImplementedError:
                self.add_user_location_ip()
        else:
            self.add_user_location_ip()

    # ------------------- GPS на мобильных -------------------
    def start_gps(self):
        try:
            gps.configure(on_location=self.update_location)
            gps.start(minTime=1000, minDistance=1)
        except NotImplementedError:
            print("GPS не поддержируется, fallback через IP")
            self.add_user_location_ip()

    def update_location(self, **kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']
        if self.user_marker is None:
            self.user_marker = MapMarker(lat=lat, lon=lon)
            self.map_view.add_widget(self.user_marker)
        else:
            self.user_marker.lat = lat
            self.user_marker.lon = lon
        self.map_view.center_on(lat, lon)

    # ------------------- fallback через IP для ПК -------------------
    def add_user_location_ip(self):
        try:
            res = requests.get("https://ipinfo.io/json").json()
            loc = res['loc'].split(',')
            lat, lon = float(loc[0]), float(loc[1])
            self.user_marker = MapMarker(lat=lat, lon=lon)
            self.map_view.add_widget(self.user_marker)
            self.map_view.center_on(lat, lon)
        except Exception as e:
            print("Не удалось получить геопозицию через IP:", e)
