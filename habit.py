from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

class HabitWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, **kwargs)
        labels = ["Option A", "Option B", "Option C", "Option D"]
 
        for text in labels:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Label(text=text)  # Corrected size_hint_x
            toggle = ToggleButton(text='Off')
            toggle.bind(on_press=self.toggle_text)  # Better binding option
 
            row.add_widget(label)
            row.add_widget(toggle)
            self.add_widget(row)  # Add row instead of individual widgets

    def toggle_text(self, instance):
        instance.text = 'On' if instance.state == 'down' else 'Off'



class HabitApp(App):
    def build(self):
        Window.size = (dp(187.5), dp(333.5))
        return HabitWidget()

if __name__ == '__main__':
    HabitApp().run()