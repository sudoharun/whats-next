import gi
gi.require_version('Gtk', '4.0')

import backend
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
        self.append(Gtk.Label(label="To do"))


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
