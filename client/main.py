from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens.connect_screen import ConnectScreen
from screens.map_screen import MapScreen

class MainApp(MDApp):
    def build(self):
        self.sm = MDScreenManager()
        self.connect_screen = ConnectScreen(switch_callback=self.show_map)
        self.map_screen = MapScreen()
        self.sm.add_widget(self.connect_screen)
        self.sm.add_widget(self.map_screen)
        return self.sm

    def show_map(self):
        self.sm.current = "map"

if __name__ == "__main__":
    MainApp().run()
