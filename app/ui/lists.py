import gi
gi.require_version('Gtk', '4.0')

import backend
from .dialogs import (
    AddTaskOverlay,
    ModifyTaskOverlay
)
from gi.repository import Gtk


class BaseListItem(Gtk.Box):
    def __init__(self, content, list_name):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )


class BaseList(Gtk.Box):
    def __init__(self, list_name):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
        )
        self.list = list_name

    def populate_data(self):
        db = backend.get_or_create_db()
        for list_item in db[self.list]:
            self.append(BaseListItem(list_item, self.list))

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

    def add_task_func(self, widget):
        self.get_parent().get_parent().get_parent().add_overlay(AddTaskOverlay("to-do"))


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
