import gi
gi.require_version('Gtk', '4.0')

import backend
from .dialogs import (
    AddTaskOverlay,
    ModifyTaskOverlay
)
from gi.repository import Gtk, GObject


class BaseListItem(Gtk.Box):
    def __init__(self, content, list_name):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        self.label = content

        self.append(Gtk.Label(label=self.label))


class BaseList(Gtk.Box):
    list_name = GObject.Property(type=str)

    def __init__(self, list_name):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            list_name=list_name
        )
        self.list_items = []

    def refresh_data(self):
        for li in self.list_items:
            self.remove(li)
        self.list_items.clear()
        db = backend.get_or_create_db()
        for li in db[self.list_name]:
            self.list_items.append(BaseListItem(li, self.list_name))
        for li in self.list_items:
            self.append(li)

    def create_task(self):
        pass


class ToDoList(BaseList):
    def __init__(self):
        super().__init__(list_name="to-do")

        self.add_task_widget = Gtk.Box(halign=Gtk.Align.CENTER, spacing=8)
        self.add_task_widget.append(Gtk.Label(label="Add Task"))
        self.add_task_button = Gtk.Button()
        self.add_task_widget.append(self.add_task_button)

        self.add_task_button.set_child(Gtk.Image(icon_name="add", pixel_size=18))
        self.add_task_button.connect("clicked", self.add_task_func)

        self.append(self.add_task_widget)
        self.refresh_data()

    def add_task_func(self, widget):
        self.main_ancestor = self.get_parent().get_parent().get_parent()
        self.main_ancestor.set_overlay(AddTaskOverlay("to-do"))


class InProgressList(BaseList):
    def __init__(self):
        super().__init__(list_name="in-progress")
        self.append(Gtk.Label(label="In progress"))


class DoneList(BaseList):
    def __init__(self):
        super().__init__(list_name="done")
        self.append(Gtk.Label(label="Done"))


class CancelledList(BaseList):
    def __init__(self):
        super().__init__(list_name="cancelled")
        self.append(Gtk.Label(label="Cancelled"))


if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
