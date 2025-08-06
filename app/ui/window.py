import gi
gi.require_version('Gtk', '4.0')

import os
from .lists import (
    ToDoList,
    InProgressList,
    DoneList,
    CancelledList
)
from gi.repository import Gtk, Gio


class TitleBar(Gtk.HeaderBar):
    def __init__(self, stack):
        super().__init__(
            title_widget=Gtk.Label(
                label="Tasker"
            ),
            show_title_buttons=True,
            hexpand=True
        )

        stack_switcher = Gtk.StackSwitcher(
            stack=stack
        )
        self.set_title_widget(stack_switcher)


class MainContainer(Gtk.Overlay):
    def __init__(self):
        super().__init__()

        # Set up listener for db file
        self.db_file = Gio.File.new_for_path(os.path.join(os.getcwd(), "db", "data.json"))
        self.db_file_monitor = self.db_file.monitor(Gio.FileMonitorFlags.NONE)
        self.db_file_monitor.connect("changed", self.sync_db_changes)

        self.overlay = None

        self.container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            hexpand=True
        )
        self.set_child(self.container)

        self.to_do_list = ToDoList()
        self.in_progress_list = InProgressList()
        self.done_list = DoneList()
        self.cancelled_list = CancelledList()

        self.stack = Gtk.Stack(
            vexpand=True,
            hexpand=True
        )
        self.stack.add_titled(self.to_do_list, "To Do", "To Do")
        self.stack.add_titled(self.in_progress_list, "In Progress", "In Progress")
        self.stack.add_titled(self.done_list, "Done", "Done")
        self.stack.add_titled(self.cancelled_list, "Cancelled", "Cancelled")

        self.container.append(TitleBar(self.stack))
        self.container.append(self.stack)

    def set_overlay(self, widget):
        if widget is not None and self.overlay is None:
            self.overlay = widget
            self.add_overlay(widget)

    def reset_overlay(self):
        if self.overlay is not None:
            self.remove_overlay(self.overlay)
            self.overlay = None

    def sync_db_changes(self, monitor, file, other_file, event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            self.to_do_list.refresh_data()
            self.in_progress_list.refresh_data()
            self.done_list.refresh_data()
            self.cancelled_list.refresh_data()


if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
