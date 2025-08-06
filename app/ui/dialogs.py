import gi
gi.require_version('Gtk', '4.0')

import backend
from gi.repository import Gtk


class AddTaskOverlay(Gtk.Box):
    def __init__(self, list_name):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=4,
            valign=Gtk.Align.CENTER,
            halign=Gtk.Align.CENTER
        )
        self.list_name = list_name

        self.entry = Gtk.Entry()

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect("clicked", self.on_save)
        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", self.on_cancel)

        self.buttons_container = Gtk.Box(halign=Gtk.Align.END, spacing=4)
        self.buttons_container.append(self.save_button)
        self.buttons_container.append(self.cancel_button)

        self.append(Gtk.Label(label="Add Task", hexpand=True, halign=Gtk.Align.START))
        self.append(self.entry)
        self.append(self.buttons_container)

    def on_save(self, *_):
        # Get text from entry
        # (Later) Confirm addition
        backend.sync_tasks(backend.create_task(self.list_name, self.entry.get_text()))
        # Save to DB
        # Sync DB to widgets
        # Remove overlay (if entry is filled from last time, clear entry before)
        self.get_parent().reset_overlay()

    def on_cancel(self, *_):
        self.get_parent().reset_overlay()


class ModifyTaskOverlay(Gtk.Box):
    def __init__(self, prev_list_name, new_list_name):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER,
            halign=Gtk.Align.CENTER
        )
        self.prev_list_name = prev_list_name
        self.new_list_name = new_list_name

class ConfirmationDialog(Gtk.Box):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
