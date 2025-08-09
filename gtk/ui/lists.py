import gi
gi.require_version('Gtk', '4.0')

import backend
from .dialogs import (
    AddTaskOverlay,
    ModifyTaskOverlay
)
from gi.repository import Gtk, GObject


class BaseListItem(Gtk.Box):
    def __init__(self, content, index, list_name):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True,
            spacing=2,
        )
        self.label = content
        self.index = index
        self.get_style_context().add_class("list-item")
        self.append(Gtk.Label(label=self.label))


class BaseList(Gtk.Box):
    list_name = GObject.Property(type=str)

    def __init__(self, list_name):
        super().__init__(
            halign=Gtk.Align.CENTER,
            vexpand=True,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            list_name=list_name
        )

        self.list_items = []
        self.filler_text = Gtk.Label(
            label="No Tasks To See Here!",
            valign=Gtk.Align.CENTER,
            halign=Gtk.Align.CENTER
        )
        self.container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            hexpand=True,
            spacing=8,
        )

        self.get_style_context().add_class("stack-content")
        self.container.get_style_context().add_class("list")

    def create_list_item(self, li, index):
        return BaseListItem(li, index, self.list_name)

    def refresh_data(self):
        if self.container.get_parent() is not None:
            self.remove(self.container)

        child = self.container.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.container.remove(child)
            child = next_child

        self.list_items.clear()

        db = backend.get_or_create_db()

        index = 0
        for li in db[self.list_name]:
            self.list_items.append(self.create_list_item(li, index))
            index+=1

        if index == 0:
            self.container.append(self.filler_text)
        else:
            self.container.remove(self.filler_text)

        for li in self.list_items:
            self.container.append(li)

        self.append(self.container)

    def move_task(self, li_index, destination):
        db = backend.get_or_create_db()
        if li_index > len(db.keys()):
            raise IndexError("Invalid index")

        li = self.list_items[li_index]
        self.remove(self.list_items[li_index])
        self.list_items.pop(li_index)
        db[self.list_name].pop(li_index)
        db[destination].append(li.label)
        backend.sync_tasks(db)

    def edit_task(self, li_index, list_name):
        self.main_ancestor = self.get_parent().get_parent()
        self.main_ancestor.set_overlay(ModifyTaskOverlay(list_name, li_index))

    def delete_task(self, li_index):
        db = backend.get_or_create_db()
        if li_index > len(db.keys()):
            raise IndexError("Invalid index")

        self.remove(self.list_items[li_index])
        self.list_items.pop(li_index)
        db[self.list_name].pop(li_index)
        backend.sync_tasks(db)


class ToDoList(BaseList):
    def __init__(self):
        super().__init__(list_name="to-do")

        self.add_task_widget = Gtk.Box(spacing=8)
        self.add_task_widget.append(Gtk.Label(label="Add Task"))
        self.add_task_widget.append(Gtk.Box(hexpand=True))
        self.add_task_button = Gtk.Button()
        self.add_task_widget.append(self.add_task_button)
        self.add_task_widget.get_style_context().add_class("add-task-widget")

        self.add_task_button.set_child(Gtk.Image(icon_name="add", pixel_size=18))
        self.add_task_button.connect("clicked", self.add_task)

        self.append(self.add_task_widget)
        self.refresh_data()

    def add_task(self, widget):
        self.main_ancestor = self.get_parent().get_parent()
        self.main_ancestor.set_overlay(AddTaskOverlay("to-do"))

    def create_list_item(self, li, index):
        item = super().create_list_item(li, index)

        start_button = Gtk.Button(tooltip_text="Start task (moves to \"In Progress\")")
        start_button.set_child(Gtk.Image(icon_name="currenttrack_play", pixel_size=18))
        start_button.connect("clicked", lambda *_: self.move_task(index, "in-progress"))

        cancel_button = Gtk.Button(tooltip_text="Cancel task (moves to \"Cancelled\")")
        cancel_button.set_child(Gtk.Image(icon_name="cancel", pixel_size=18))
        cancel_button.connect("clicked", lambda *_: self.move_task(index, "cancelled"))

        done_button = Gtk.Button(tooltip_text="Mark task as done (moves to \"Done\")")
        done_button.set_child(Gtk.Image(icon_name="check-filled", pixel_size=18))
        done_button.connect("clicked", lambda *_: self.move_task(index, "done"))

        edit_button = Gtk.Button(tooltip_text="Edit task")
        edit_button.set_child(Gtk.Image(icon_name="edit", pixel_size=18))
        edit_button.connect("clicked", lambda *_: self.edit_task(index, "to-do"))

        delete_button = Gtk.Button(tooltip_text="Permanently delete task")
        delete_button.set_child(Gtk.Image(icon_name="delete", pixel_size=18))
        delete_button.connect("clicked", lambda *_: self.delete_task(index))

        # Empty space between text and buttons
        item.append(Gtk.Box(hexpand=True))

        item.append(start_button)
        item.append(cancel_button)
        item.append(done_button)
        item.append(edit_button)
        item.append(delete_button)
        return item


class InProgressList(BaseList):
    def __init__(self):
        super().__init__(list_name="in-progress")

        self.refresh_data()

    def create_list_item(self, li, index):
        item = super().create_list_item(li, index)

        to_do_button = Gtk.Button(tooltip_text="Reset task (moves to \"To Do\")")
        to_do_button.set_child(Gtk.Image(icon_name="vm-restart", pixel_size=18))
        to_do_button.connect("clicked", lambda *_: self.move_task(index, "to-do"))

        cancel_button = Gtk.Button(tooltip_text="Cancel task (moves to \"Cancelled\")")
        cancel_button.set_child(Gtk.Image(icon_name="cancel", pixel_size=18))
        cancel_button.connect("clicked", lambda *_: self.move_task(index, "cancelled"))

        done_button = Gtk.Button(tooltip_text="Mark task as done (moves to \"Done\")")
        done_button.set_child(Gtk.Image(icon_name="check-filled", pixel_size=18))
        done_button.connect("clicked", lambda *_: self.move_task(index, "done"))

        edit_button = Gtk.Button(tooltip_text="Edit task")
        edit_button.set_child(Gtk.Image(icon_name="edit", pixel_size=18))
        edit_button.connect("clicked", lambda *_: self.edit_task(index, "in-progress"))

        delete_button = Gtk.Button(tooltip_text="Permanently delete task")
        delete_button.set_child(Gtk.Image(icon_name="delete", pixel_size=18))
        delete_button.connect("clicked", lambda *_: self.delete_task(index))

        # Empty space between text and buttons
        item.append(Gtk.Box(hexpand=True))

        item.append(to_do_button)
        item.append(cancel_button)
        item.append(done_button)
        item.append(edit_button)
        item.append(delete_button)
        return item


class DoneList(BaseList):
    def __init__(self):
        super().__init__(list_name="done")

        self.refresh_data()

    def create_list_item(self, li, index):
        item = super().create_list_item(li, index)

        to_do_button = Gtk.Button(tooltip_text="Reset task (moves to \"To Do\")")
        to_do_button.set_child(Gtk.Image(icon_name="vm-restart", pixel_size=18))
        to_do_button.connect("clicked", lambda *_: self.move_task(index, "to-do"))

        delete_button = Gtk.Button(tooltip_text="Permanently delete task")
        delete_button.set_child(Gtk.Image(icon_name="delete", pixel_size=18))
        delete_button.connect("clicked", lambda *_: self.delete_task(index))

        # Empty space between text and buttons
        item.append(Gtk.Box(hexpand=True))

        item.append(to_do_button)
        item.append(delete_button)
        return item


class CancelledList(BaseList):
    def __init__(self):
        super().__init__(list_name="cancelled")

        self.refresh_data()

    def create_list_item(self, li, index):
        item = super().create_list_item(li, index)

        to_do_button = Gtk.Button(tooltip_text="Reset task (moves to \"To Do\")")
        to_do_button.set_child(Gtk.Image(icon_name="vm-restart", pixel_size=18))
        to_do_button.connect("clicked", lambda *_: self.move_task(index, "to-do"))

        start_button = Gtk.Button(tooltip_text="Start task (moves to \"In Progress\")")
        start_button.set_child(Gtk.Image(icon_name="currenttrack_play", pixel_size=18))
        start_button.connect("clicked", lambda *_: self.move_task(index, "in-progress"))

        done_button = Gtk.Button(tooltip_text="Mark task as done (moves to \"Done\")")
        done_button.set_child(Gtk.Image(icon_name="check-filled", pixel_size=18))
        done_button.connect("clicked", lambda *_: self.move_task(index, "done"))

        delete_button = Gtk.Button(tooltip_text="Permanently delete task")
        delete_button.set_child(Gtk.Image(icon_name="delete", pixel_size=18))
        delete_button.connect("clicked", lambda *_: self.delete_task(index))

        # Empty space between text and buttons
        item.append(Gtk.Box(hexpand=True))

        item.append(to_do_button)
        item.append(start_button)
        item.append(done_button)
        item.append(delete_button)
        return item


if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
