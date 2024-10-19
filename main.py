import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform


class TaskRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(TaskRecycleView, self).__init__(**kwargs)
        self.data = []

    def update_view(self):
        self.data = [{'text': task, 'is_completed': False} for task in self.parent.app.load_tasks()]
        self.refresh_from_data()


class TaskItem(BoxLayout):
    def __init__(self, task_text, **kwargs):
        super(TaskItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.checkbox = CheckBox()
        self.label = Label(text=task_text, size_hint_x=0.8)
        self.remove_button = Button(text='Remove', size_hint_x=0.2)
        
        self.checkbox.bind(active=self.on_checkbox_active)
        self.remove_button.bind(on_press=self.on_remove)
        
        self.add_widget(self.checkbox)
        self.add_widget(self.label)
        self.add_widget(self.remove_button)

    def on_checkbox_active(self, checkbox, value):
        self.label.color = (0.5, 0.5, 0.5, 1) if value else (1, 1, 1, 1)

    def on_remove(self, instance):
        self.parent.remove_task(self.label.text)


class ToDoApp(App):
    def build(self):
        self.tasks_store = JsonStore(self.get_storage_path())
        self.layout = BoxLayout(orientation='vertical')
        self.task_input = TextInput(hint_text='Enter a task', size_hint_y=None, height=40)
        self.add_button = Button(text='Add Task', size_hint_y=None, height=40)
        
        self.task_list = TaskRecycleView()
        self.task_list.update_view()

        self.add_button.bind(on_press=self.add_task)

        self.layout.add_widget(self.task_input)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.task_list)

        return self.layout

    def get_storage_path(self):
        """Get the appropriate storage path based on the platform."""
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            return os.path.join(os.environ['HOME'], 'todo_tasks.json')
        else:
            return os.path.join(os.getcwd(), 'todo_tasks.json')

    def load_tasks(self):
        """Load tasks from storage."""
        if self.tasks_store.exists('tasks'):
            return self.tasks_store.get('tasks')['tasks']
        return []

    def save_tasks(self):
        """Save tasks to storage."""
        self.tasks_store.put('tasks', tasks=self.load_tasks())

    def add_task(self, instance):
        """Add a task to the list."""
        task = self.task_input.text.strip()
        if task:
            tasks = self.load_tasks()
            tasks.append(task)
            self.tasks_store.put('tasks', tasks=tasks)  # Save to storage
            self.task_list.update_view()  # Refresh the task list
            self.task_input.text = ''

    def remove_task(self, task_text):
        """Remove a task from the list."""
        tasks = self.load_tasks()
        tasks.remove(task_text)
        self.tasks_store.put('tasks', tasks=tasks)  # Save updated tasks
        self.task_list.update_view()  # Refresh the task list

    def on_stop(self):
        """Called when the app is closed; save tasks."""
        self.save_tasks()


if __name__ == '__main__':
    ToDoApp().run()
