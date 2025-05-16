from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp

class HabitWidget(Widget):
    pass

class HabitApp(App):
    def build(self):
        Window.size = (dp(187.5), dp(333.5))
        return HabitWidget()

if __name__ == '__main__':
    HabitApp().run()