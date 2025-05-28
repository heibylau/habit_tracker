from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

class LabelWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, **kwargs)
        
        for i in range(10):  # Adjust number of items as needed
            lbl = Label(text=f"Item {i}", size_hint_y=None, height=40)
            self.add_widget(lbl)

class LabelApp(App):
    def build(self):
        return LabelWidget()

LabelApp().run()
