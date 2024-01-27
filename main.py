from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.clock import Clock

import math

import kivy
from kivy.config import Config
from kivy.core.clipboard import ClipboardBase

# Ustaw Kivy, aby używał wewnętrznego schowka zamiast xclip/xsel
Config.set('kivy', 'clipboard', 'sdl2')  # Możesz również spróbować 'simple' zamiast 'sdl2'
ClipboardBase._obj = None



KV = '''
RelativeLayout:

    Image:
        source: 'tomato.png'
        size_hint: (1, 1)

    Label:
        id: timer_label
        text: "Timer"
        font_size: '50sp'
        color: 0, 1, 0, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}  # Ustawienie timera na wierzchu obrazu

    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(20)

        MDFillRoundFlatButton:
            text: 'Start'
            on_press: app.start_timer()
            md_bg_color: app.theme_cls.primary_color
            size_hint_x: 0.33  # Dostosowanie szerokości przycisku w zależności od szerokości okna

        MDFillRoundFlatButton:
            text: 'Pause'
            on_press: app.pause_timer()
            md_bg_color: app.theme_cls.primary_color
            size_hint_x: 0.33  # Dostosowanie szerokości przycisku w zależności od szerokości okna

        MDFillRoundFlatButton:
            text: 'Reset'
            on_press: app.reset_timer()
            md_bg_color: app.theme_cls.primary_color
            size_hint_x: 0.33  # Dostosowanie szerokości przycisku w zależności od szerokości okna

    Label:
        id: checkmark



'''

class PomodoroApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.reps = 0
        self.paused = False
        self.remaining_time = 0
        self.timer_interval = None

    def reset_timer(self):
        self.root.ids.timer_label.text = "Timer"
        self.root.ids.timer_label.color = (0, 1, 0, 1)

        if hasattr(self.root.ids, 'checkmark'):
            self.root.ids.checkmark.text = ""

        self.reps = 0
        self.paused = False
        self.remaining_time = 0
        if self.timer_interval:
            self.timer_interval.cancel()

    def start_timer(self):
        if not self.paused:
            self.reps += 1

            work_sec = 25 * 60
            short_break_sec = 5 * 60
            long_break_sec = 20 * 60

            if self.reps % 8 == 0:
                self.root.ids.timer_label.text = "Break"
                self.root.ids.timer_label.color = (1, 0, 0, 1)
                self.count_down(long_break_sec)

            elif self.reps % 2 == 0:
                self.root.ids.timer_label.text = "Break"
                self.root.ids.timer_label.color = (0.89, 0.59, 0.61, 1)
                self.count_down(short_break_sec)

            else:
                self.root.ids.timer_label.text = "Work"
                self.root.ids.timer_label.color = (0, 1, 0, 1)
                self.count_down(work_sec)
        else:
            self.paused = False
            self.count_down(self.remaining_time)

    def pause_timer(self):
        self.paused = not self.paused
        if self.timer_interval:
            self.timer_interval.cancel()

    def count_down(self, count):
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        self.root.ids.timer_label.text = f"{count_min}:{count_sec}"
        if count > 0:
            self.remaining_time = count
            self.timer_interval = Clock.schedule_once(lambda dt: self.count_down(count - 1), 1)
        else:
            self.start_timer()
            mark = "✓" * (self.reps // 2)
            if hasattr(self.root.ids, 'checkmark'):
                self.root.ids.checkmark.text = mark

if __name__ == '__main__':
    PomodoroApp().run()
