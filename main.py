from kivy.metrics import dp  # Import dp function
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ListProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel  # Added this import
from kivy.clock import Clock
import json
import os
import random

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.start_animation, 2)

    def start_animation(self, dt):
        self.manager.transition = NoTransition()
        self.manager.current = 'main'

class MainScreen(Screen):
    quote = StringProperty("")

    def on_enter(self):
        self.quote = random.choice(QUOTES)

class TaskListScreen(Screen):
    tasks = ListProperty([])

    def on_pre_enter(self):
        self.refresh_task_list()



    def refresh_task_list(self):
        task_list = self.ids.task_list  # Get the task list container
        task_list.clear_widgets()  # Clear previous widgets
        
        if not self.tasks:  # If there are no tasks
            # Create an empty label
            empty_label = MDLabel(
                text='List is empty. Add a task by pressing the "+" icon.',
                halign='center',
                size_hint_y=None,  # Allow height to be defined by content
                height=dp(50),  # Set a fixed height for the label
                valign='middle'  # Align text vertically to the middle of the label
            )
            # Ensure the label is centered in the task_list layout
            empty_label.bind(size=empty_label.setter('text_size'))  # Auto wrap text
            task_list.add_widget(empty_label)  # Add the empty label to the task list
        else:
            for task in self.tasks:
                self.add_task_widget(task)  # Method to add individual task widgets

    def add_task_widget(self, task):
        app = MDApp.get_running_app()
        task_item = OneLineIconListItem(
            text=task['task'],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1) if task['completed'] else (0, 0, 0, 1),
            bg_color=(0, 1, 0, 1) if task['completed'] else (0.9, 0.9, 0.9, 1)
        )

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Mark Completed" if not task['completed'] else "Mark Incomplete",
                "on_release": lambda x=task['task']: self.mark_complete_and_close(menu, x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Delete",
                "on_release": lambda x=task['task']: self.delete_and_close(menu, x)
            }
        ]

        menu = MDDropdownMenu(items=menu_items, width_mult=4)

        def open_menu(instance):
            menu.caller = instance
            menu.open()

        task_item.bind(on_release=open_menu)
        self.ids.task_list.add_widget(task_item)
    def mark_complete_and_close(self, menu, task):
        self.toggle_task_status(task)
        menu.dismiss()

    def delete_and_close(self, menu, task):
        self.delete_task(task)
        menu.dismiss()

    def toggle_task_status(self, task):
        app = MDApp.get_running_app()
        app.toggle_task_status(task)
        self.refresh_task_list()

    def delete_task(self, task):
        app = MDApp.get_running_app()
        app.delete_task(task)
        self.refresh_task_list()

class SettingsScreen(Screen):
    pass

class TaskManagerApp(MDApp):
    tasks = ListProperty([])

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        self.root = Builder.load_string(KV)
        self.load_tasks()
        return self.root

    def update_task_list_ui(self):
        list_screen = self.root.get_screen('list')
        list_screen.tasks = self.tasks
        list_screen.refresh_task_list()  

    def on_start(self):
        self.root.current = 'main'
        self.root.get_screen('main').on_enter()

    def change_screen(self, screen_name):
        # self.root.transition = SlideTransition()
        self.root.current = screen_name

    def on_stop(self):
        self.save_tasks()

    def add_task(self, task):
        if task and not any(t['task'] == task for t in self.tasks):
            self.tasks.append({'task': task, 'completed': False})
            self.root.get_screen('list').tasks = self.tasks
            self.root.get_screen('main').ids.task_input.text = ''
            self.save_tasks()

    def load_tasks(self):
        try:
            file_path = os.path.join(self.user_data_dir, 'tasks.json')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.tasks = json.load(f)
                self.update_task_list_ui()
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def save_tasks(self):
        try:
            file_path = os.path.join(self.user_data_dir, 'tasks.json')
            with open(file_path, 'w') as f:
                json.dump(self.tasks, f)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def update_task_list_ui(self):
        self.root.get_screen('list').tasks = self.tasks

    def toggle_task_status(self, task_name):
        for task in self.tasks:
            if task['task'] == task_name:
                task['completed'] = not task['completed']
                break
        self.save_tasks()
        self.root.get_screen('list').tasks = self.tasks

    def delete_task(self, task_name):
        self.tasks = [task for task in self.tasks if task['task'] != task_name]
        self.save_tasks()
        self.root.get_screen('list').tasks = self.tasks

QUOTES = [
    "The two most powerful warriors are patience and time.",
    "Time is a created thing. To say 'I don't have time' is to say 'I don't want to.'",
    "The past is a place of reference, not a place of residence.",
    "Yesterday is history, tomorrow is a mystery, today is a gift. That's why we call it 'The Present'.",
    "Time is free, but it's priceless. You can't own it, but you can use it. You can't keep it, but you can spend it.",
]

KV = '''
#:import MDLabel kivymd.uix.label.MDLabel

ScreenManager:
    SplashScreen:
    MainScreen:
    TaskListScreen:
    SettingsScreen:

<SplashScreen>:
    name: 'splash'
    MDFloatLayout:
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: 256, 256
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        MDLabel:
            text: "Task Manager"
            halign: "center"
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            font_style: "H4"

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "To-Do Application"
            elevation: 10
        
        MDTextField:
            id: task_input
            hint_text: "Enter Task"
            height: dp(200)  # Doubling the original height
            padding_y: [100, 100]  # Doubling the vertical padding
            pos_hint: {'center_y': 0.5}
            font_size: dp(24)  # Increase font size for better visibility
            on_text_validate:
                app.add_task(self.text)
                self.text = ''
        MDLabel:
            text: root.quote
            halign: "center"
            valign: 'center'
            height: dp(50)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        ScrollView:
            MDList:
                id: task_list
                on_kv_post:
                    self.clear_widgets()
                    if not self.children: self.add_widget(MDLabel(text='', halign='center', valign='center', height=dp(50), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            MDIconButton:
                icon: 'format-list-bulleted'
                on_release: app.change_screen('list')
            MDIconButton:
                icon: 'cog'
                on_release: app.change_screen('settings')

<TaskListScreen>:
    name: 'list'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Tasks"
            elevation: 10
        ScrollView:
            MDList:
                id: task_list

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            MDIconButton:
                icon: 'plus'
                on_release: app.change_screen('main')
            MDIconButton:
                icon: 'cog'
                on_release: app.change_screen('settings')

<SettingsScreen>:
    name: 'settings'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(100)  # Space between children

        MDTopAppBar:
            title: "Settings"
            elevation: 10
            # No need for padding since the app bar will occupy the top space

        MDLabel:
            text: "Wait for future updates."
            valign: "center"
            halign: 'center'
            height: dp(50)
            # No pos_hint needed since the label will just flow below the app bar

        # This box layout can also hold more UI components in the future
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            MDIconButton:
                icon: 'format-list-bulleted'
                on_release: app.change_screen('list')
            MDIconButton:
                icon: 'plus'
                on_release: app.change_screen('main')


'''

if __name__ == '__main__':
    TaskManagerApp().run()
