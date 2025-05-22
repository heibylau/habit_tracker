from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

class HabitWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        labels = ["Option A", "Option B", "Option C", "Option D"]
 
        for text in labels:
            row = BoxLayout(orientation='horizontal', size_hint_y=80, height=40)
            label = Label(text=text, size_hint_x=30)
            toggle = ToggleButton(text='Off', size_hint_x=30)
 
            # Optional: Change text on toggle
            toggle.bind(on_press=self.toggle_text)
 
            row.add_widget(label)
            row.add_widget(toggle)
            self.add_widget(row)
    def toggle_text(self, instance):
        instance.text = 'on' if instance.state=='down' else 'off'



class HabitApp(App):
    def build(self):
        Window.size = (dp(187.5), dp(333.5))
        return HabitWidget()

if __name__ == '__main__':
    HabitApp().run()