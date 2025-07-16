from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import json
import sqlite3
from datetime import datetime, timedelta
import uuid
import os

class Habit:
    def __init__(self, id=99999, name="uninitialized", score=99999):
        self.id = id
        self.name = name
        self.score = score
        self.doneToday = False

class AppState():
    # habits = [["Floss Teeth", True, 5],
    #           ["10000 Steps", False, 30],
    #           ["8 Hours Sleep", False, 20],
    #           ["2L of Water", False, 30]]
    # score = 0
    # for _, done, habbitScore in habits:
    #     if (done):
    #         score += habbitScore
    habits = []
    score = 0

class HabitWidget(Widget):
    pass

class HabitLayout(FloatLayout):
    pass

class HabitList(BoxLayout):
    def __init__(self, state, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.state = state  # Save reference to state
        state.habit_toggles = []
        for idx, habit in enumerate(state.habits):
            # text, done, _ = habit
            text = habit.name
            done = habit.doneToday
            score = habit.score
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Label(text=text, size_hint_x=.8)
            if done:
                toggle = ToggleButton(text='done', state='down', size_hint_x=.3)
            else:
                toggle = ToggleButton(text=f'+{score}', size_hint_x=.3)
            toggle.habit_index = idx  # Attach index to button
            state.habit_toggles.append(toggle)
            toggle.bind(on_press=self.toggle_text)

            row.add_widget(label)
            row.add_widget(toggle)
            self.add_widget(row)

    def toggle_text(self, instance):
        idx = instance.habit_index
        # Update state
        self.state.habits[idx].doneToday = instance.state == 'down'
        self.state.score += self.state.habits[idx].score * (1 if instance.state == 'down' else -1)
        self.state.cur.execute(f"update GameState set score = {self.state.score}")
        self.state.con.commit()
        instance.text = 'done' if instance.state == 'down' else f'+{self.state.habits[idx].score}'

        id=uuid.uuid1()
        date= self.state.viewDate.strftime('%Y-%m-%d')
        habitid=self.state.habits[idx].id
        cur=self.state.cur

        if instance.state=='down':
            cur.execute('insert into CompletedHabits (ID,HabitID,Date) values (?,?,?)',(str(id),habitid,date))
            self.state.con.commit()
        else:
            cur.execute('delete from completedHabits where HabitID=? and Date=?', (habitid,date))    
            self.state.con.commit()


class HabitApp(App):
    state = AppState()

    state.viewDate = datetime.now()

    dbinit = not os.path.exists('habitTracker.db')
    state.con = sqlite3.connect('habitTracker.db')
    state.cur = state.con.cursor()

    if dbinit:
        state.cur.execute('create table GameState (score integer)')
        state.cur.execute('create table Habit (id integer primary key, name text, score integer)')
        state.cur.execute('create table CompletedHabits (id text, habitid integer, date text)')
        state.cur.execute('insert into GameState (score) values (0)')
        state.cur.execute("insert into Habit (id, name, score) VALUES (1, 'Floss Teeth', 5),(2, '10,000 Steps', 30),(3, '8 Hours of Sleep', 20),(4, '2L of Water', 30)")
        state.con.commit()

    state.cur.execute("select score from gamestate")
    state.score = state.cur.fetchone()[0]
    _ = state.cur.fetchall()

    state.cur.execute("select id, name, score from Habit")
    for row in state.cur.fetchall():
        # state.habits.append([row[1], False, row[2]])
        habit = Habit(row[0], row[1], row[2])
        date = state.viewDate.strftime('%Y-%m-%d')
        habitID = habit.id
        state.cur.execute("select id from completedHabits WHERE habitid = ? and date = ?",(habitID, date))
        res = state.cur.fetchall()
        if len(res) > 0:
            habit.doneToday = True
            # state.score += habit.score
        state.habits.append(habit)
    def save_state_to_json(self, dt):
        data = {
            "habits": self.state.habits,
            "score": self.state.score
        }
        with open("habit_state.json", "w") as f:
            json.dump(data, f)

    def update_score_label(self, dt):
        self.score_label.text = f"Score: {self.state.score}"

    def date_change(self, instance):
        if instance.text == '<':
            dateChange = -1
        elif instance.text == '>': 
            dateChange = 1    
        else:
            return
        self.state.viewDate = self.state.viewDate + timedelta(days=dateChange)
        self.state.date_label.text = f"Date: {self.state.viewDate.strftime('%b %d, %Y')}"
        if self.state.viewDate.strftime('%Y-%m-%d') >= datetime.now().strftime('%Y-%m-%d'):
            self.state.datePlus.disabled = True
        else:
            self.state.datePlus.disabled = False

        for habit in self.state.habits:
            habitID = habit.id
            date = self.state.viewDate.strftime('%Y-%m-%d')
            self.state.cur.execute("select id from completedHabits WHERE habitid = ? and date = ?",(habitID, date))
            res = self.state.cur.fetchall()
            if len(res) > 0:
                habit.doneToday = True
            else:
                habit.doneToday = False
        for toggle in self.state.habit_toggles:
            if self.state.habits[toggle.habit_index].doneToday:
                toggle.text = 'done'
                toggle.state = 'down'
            else:
                toggle.text = f'+{self.state.habits[toggle.habit_index].score}'
                toggle.state = 'normal'

    def delete_habit(self, instance):
        self.state.cur.execute('DELETE FROM Habit WHERE id = ?', str(instance.hid))
        self.state.con.commit()

    def change_habits(self, instance):
        popuproot = BoxLayout(orientation='vertical')
        # popuproot = BoxLayout(size_hint=(None, None), size=(400,400))
        # popuproot.add_widget(Label(text='Hellow world')),
        # popup.add_widget(okbutton)
        grid = GridLayout(cols=3, row_force_default = True, row_default_height = 40, size_hint_y=0.8, size_hint_x=1)
        for habit in self.state.habits:
            grid.add_widget(TextInput(text=habit.name, multiline = False, size_hint_x=3))
            grid.add_widget(TextInput(text=str(habit.score), multiline = False))
            b = Button(text='x')
            b.hid = habit.id 
            b.bind(on_press=self.delete_habit)
            grid.add_widget(b)


        popuproot.add_widget(grid)
        okbutton = Button(text='Close', size_hint=(.4, .2))
        popuproot.add_widget(okbutton)

        popup = Popup(title = 'Change Habits', 
                    #   content=Label(text='Hellow world'),
                      content=popuproot,
                      size_hint=(None, None), size=(400, 400),
                      auto_dismiss=False)
        
        okbutton.bind(on_press=popup.dismiss)
        popup.open()

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
        self.state.date_label = Label(
            text=f"Date: {self.state.viewDate.strftime('%b %d, %Y')}",
            size_hint_x=1,
            size_hint_y=None,
            height=40,
            pos_hint={'x':0,'y':0.85}
        )
        self.dateMinus = Button(text="<", size_hint_x=.1, size_hint_y=.05, pos_hint={'x':0,'y':0.85})
        self.dateMinus.bind(on_press=self.date_change)
        self.state.datePlus = Button(text=">", size_hint_x=.1, size_hint_y=.05, pos_hint={'x':0.9,'y':0.85}, disabled = True )
        self.state.datePlus.bind(on_press=self.date_change)
        page.add_widget(self.dateMinus)
        page.add_widget(self.state.datePlus)


        self.state.editButton = Button(text="Edit Habits", size_hint_x=.4, size_hint_y=.05, pos_hint={'x':0.3,'y':0.15} )
        self.state.editButton.bind(on_press=self.change_habits)
        page.add_widget(self.state.editButton)
        
        page.add_widget(self.score_label)
        page.add_widget(self.state.date_label)
        page.add_widget(habit_list)
        Window.size = (dp(187.5), dp(333.5))
        # Clock.schedule_interval(self.save_state_to_json, 3)
        Clock.schedule_interval(self.update_score_label, 0.5)  # Update label every 0.5 seconds

        return page

if __name__ == '__main__':
    HabitApp().run()