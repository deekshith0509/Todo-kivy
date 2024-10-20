from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ListProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
import json
import os
import random

# For Android functionality
from kivy.utils import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path

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
        self.ids.task_list.clear_widgets()
        for task in self.tasks:
            self.add_task_widget(task)

    def add_task_widget(self, task):
        app = MDApp.get_running_app()
        task_item = OneLineIconListItem(
            text=task['task'],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1) if task['completed'] else (0, 0, 0, 1),
            bg_color=(0, 1, 0, 1) if task['completed'] else (0.9, 0.9, 0.9, 1)  # Green for completed tasks
        )

        menu_items = [
            {"viewclass": "OneLineListItem",
             "text": "Mark Completed" if not task['completed'] else "Mark Incomplete",
             "on_release": lambda x=task['task']: self.toggle_task_status(x)},
            {"viewclass": "OneLineListItem",
             "text": "Delete",
             "on_release": lambda x=task['task']: self.delete_task(x)}
        ]
        menu = MDDropdownMenu(items=menu_items, width_mult=4)

        def open_menu(instance):
            menu.caller = instance
            menu.open()

        task_item.bind(on_release=open_menu)
        self.ids.task_list.add_widget(task_item)

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
    screen_stack = []

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        self.root = Builder.load_string(KV)
        self.load_tasks()
        return self.root

    def on_start(self):
        self.root.current = 'main'  # Start at the main screen
        self.root.get_screen('main').on_enter()  # Set the quote on startup

    def change_screen(self, screen_name):
        # Check if the requested screen is already the current screen
        if self.root.current == screen_name:
            # Set the current tab to the selected screen's tab
            self.root.get_screen(screen_name).ids.bottom_nav.current = screen_name
        else:
            self.root.transition = NoTransition()
            self.root.current = screen_name
            # Also set the current tab to the selected screen's tab
            self.root.get_screen(screen_name).ids.bottom_nav.current = screen_name

    def on_stop(self):
        self.save_tasks()

    def add_task(self, task):
        if task and not any(t['task'] == task for t in self.tasks):
            self.tasks.append({'task': task, 'completed': False})
            self.root.get_screen('list').tasks = self.tasks
            self.root.get_screen('main').ids.task_input.text = ''
            self.save_tasks()

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

    def load_tasks(self):
        try:
            if platform == "android":
                file_path = os.path.join(primary_external_storage_path(), 'tasks.json')
            else:
                file_path = 'tasks.json'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.tasks = json.load(f)
                self.root.get_screen('list').tasks = self.tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def save_tasks(self):
        try:
            if platform == "android":
                file_path = os.path.join(primary_external_storage_path(), 'tasks.json')
            else:
                file_path = 'tasks.json'
            with open(file_path, 'w') as f:
                json.dump(self.tasks, f)
        except Exception as e:
            print(f"Error saving tasks: {e}")

QUOTES = [
    "The two most powerful warriors are patience and time.",
    "Time is a created thing. To say 'I don't have time' is to say 'I don't want to.'",
    "The past is a place of reference, not a place of residence.",
    "Yesterday is history, tomorrow is a mystery, today is a gift. That's why we call it 'The Present'.",
    "Time is free, but it's priceless. You can't own it, but you can use it. You can't keep it, but you can spend it.",
]

KV = '''
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
            size_hint_y: None
            height: dp(50)
            on_text_validate:
                app.add_task(self.text)
                self.text = ''
        MDLabel:
            text: root.quote
            halign: "center"
            size_hint_y: None
            height: dp(50)
        MDBottomNavigation:
            id: bottom_nav  # Added ID to the bottom navigation
            panel_color: app.theme_cls.primary_color
            selected_color_background: app.theme_cls.accent_color
            text_color_active: app.theme_cls.accent_color
            MDBottomNavigationItem:
                name: 'add'
                text: 'Add'
                icon: 'plus'
                on_tab_press: app.add_task(root.ids.task_input.text)  # Adding task directly here
            MDBottomNavigationItem:
                name: 'list'
                text: 'Tasks'
                icon: 'format-list-bulleted'
                on_tab_press: app.change_screen('list')
            MDBottomNavigationItem:
                name: 'settings'
                text: 'Settings'
                icon: 'cog'
                on_tab_press: app.change_screen('settings')

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
        MDBottomNavigation:
            id: bottom_nav  # Added ID to the bottom navigation
            panel_color: app.theme_cls.primary_color
            selected_color_background: app.theme_cls.accent_color
            text_color_active: app.theme_cls.accent_color
            MDBottomNavigationItem:
                name: 'add'
                text: 'Add'
                icon: 'plus'
                on_tab_press: app.change_screen('main')
            MDBottomNavigationItem:
                name: 'list'
                text: 'Tasks'
                icon: 'format-list-bulleted'
                on_tab_press: app.change_screen('list')
            MDBottomNavigationItem:
                name: 'settings'
                text: 'Settings'
                icon: 'cog'
                on_tab_press: app.change_screen('settings')

<SettingsScreen>:
    name: 'settings'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Settings"
            elevation: 10
        # You can add your settings UI components here
        MDBottomNavigation:
            id: bottom_nav  # Added ID to the bottom navigation
            panel_color: app.theme_cls.primary_color
            selected_color_background: app.theme_cls.accent_color
            text_color_active: app.theme_cls.accent_color
            MDBottomNavigationItem:
                name: 'add'
                text: 'Add'
                icon: 'plus'
                on_tab_press: app.change_screen('main')
            MDBottomNavigationItem:
                name: 'list'
                text: 'Tasks'
                icon: 'format-list-bulleted'
                on_tab_press: app.change_screen('list')
            MDBottomNavigationItem:
                name: 'settings'
                text: 'Settings'
                icon: 'cog'
                on_tab_press: app.change_screen('settings')
'''

if __name__ == '__main__':
    TaskManagerApp().run()
