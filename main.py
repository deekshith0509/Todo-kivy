from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
import random

class MainScreen(Screen):
    quote = StringProperty("")

    def on_enter(self):
        self.quote = random.choice(QUOTES)

class TaskListScreen(Screen):
    tasks = ListProperty([])
    def on_pre_enter(self, *args):
        self.ids.task_list.clear_widgets()
        for task in self.tasks:
            self.ids.task_list.add_widget(
                MDBoxLayout(
                    MDRaisedButton(
                        text=task,
                        size_hint_x=1,
                        on_release=lambda x: print(f"Task: {x.text}")
                    ),
                    size_hint_y=None,
                    height="48dp"
                )
            )

class SettingsScreen(Screen):
    pass

class TaskManagerApp(MDApp):
    tasks = ListProperty([])

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def add_task(self, task):
        if task:
            self.tasks.append(task)
            self.root.get_screen('list').tasks = self.tasks
            self.root.get_screen('main').ids.task_input.text = ''

QUOTES = [
    "The two most powerful warriors are patience and time.",
    "Time is a created thing. To say 'I don't have time' is to say 'I don't want to.'",
    "The past is a place of reference, not a place of residence.",
    "Yesterday is history, tomorrow is a mystery, today is a gift. That's why we call it 'The Present'.",
    "Time is free, but it's priceless. You can't own it, but you can use it. You can't keep it, but you can spend it.",
]

KV = '''
ScreenManager:
    MainScreen:
    TaskListScreen:
    SettingsScreen:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            MDLabel:
                text: "ToDo"
                halign: "center"
                valign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        MDTextField:
            id: task_input
            hint_text: "Enter Task"
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.9
            multiline: False
            on_text_validate: app.add_task(self.text)
        MDLabel:
            text: root.quote
            halign: 'center'
            valign: 'center'
            theme_text_color: "Secondary"
            size_hint_y: 1
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.add_task(root.ids.task_input.text)
            MDIconButton:
                icon: "format-list-bulleted"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('list')
            MDIconButton:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('settings')

<TaskListScreen>:
    name: 'list'
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('main')
            MDLabel:
                text: "Tasks"
                halign: "center"
                valign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        ScrollView:
            MDBoxLayout:
                id: task_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('main')
            MDIconButton:
                icon: "format-list-bulleted"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDIconButton:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('settings')

<SettingsScreen>:
    name: 'settings'
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('main')
            MDLabel:
                text: "Settings"
                halign: "center"
                valign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        MDLabel:
            text: "Settings go here"
            halign: 'center'
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('main')
            MDIconButton:
                icon: "format-list-bulleted"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                on_release: app.change_screen('list')
            MDIconButton:
                icon: "cog"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
'''

if __name__ == "__main__":
    TaskManagerApp().run()
