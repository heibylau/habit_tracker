from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.clock import Clock
import json

class AppState():
    habits = [["Floss Teeth", True, 5],
              ["10000 Steps", False, 30],
              ["8 Hours Sleep", False, 20],
              ["2L of Water", False, 30]]
    score = 0
    for _, done, habbitScore in habits:
        if (done):
            score += habbitScore

class HabitWidget(Widget):
    pass

class HabitLayout(FloatLayout):
    pass

class HabitList(BoxLayout):
    def __init__(self, state, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.state = state  # Save reference to state
        for idx, habit in enumerate(state.habits):
            text, done, _ = habit
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Label(text=text, size_hint_x=.8)
            if done:
                toggle = ToggleButton(text='done', state='down', size_hint_x=.3)
            else:
                toggle = ToggleButton(text='not done', size_hint_x=.3)
            toggle.habit_index = idx  # Attach index to button

            toggle.bind(on_press=self.toggle_text)

            row.add_widget(label)
            row.add_widget(toggle)
            self.add_widget(row)

    def toggle_text(self, instance):
        idx = instance.habit_index
        # Update state
        self.state.habits[idx][1] = instance.state == 'down'
        self.state.score += self.state.habits[idx][2] * (1 if instance.state == 'down' else -1)
        instance.text = 'done' if instance.state == 'down' else 'not done'

class HabitApp(App):
    state = AppState()
    def save_state_to_json(self, dt):
        data = {
            "habits": self.state.habits,
            "score": self.state.score
        }
        with open("habit_state.json", "w") as f:
            json.dump(data, f)

    def update_score_label(self, dt):
        self.score_label.text = f"Score: {self.state.score}"

    def build(self):
        page = HabitLayout()
        habit_widget = HabitWidget()
        habit_list = HabitList(state=self.state, pos_hint={'x':0,'y':0.50})
        page.add_widget(habit_widget)
        self.score_label = Label(
            text=f"Score: {self.state.score}",
            size_hint_x=.8,
            size_hint_y=None,
            height=40,
            pos_hint={'x':0,'y':0}
        )
        page.add_widget(self.score_label)
        page.add_widget(habit_list)
        Window.size = (dp(187.5), dp(333.5))
        Clock.schedule_interval(self.save_state_to_json, 3)
        Clock.schedule_interval(self.update_score_label, 0.5)  # Update label every 0.5 seconds

        return page

if __name__ == '__main__':
    HabitApp().run()