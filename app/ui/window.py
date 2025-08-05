import gi
gi.require_version('Gtk', '4.0')

from .lists import (
    ToDoList,
    InProgressList,
    DoneList,
    CancelledList
)
from .dialogs import (
    AddTaskOverlay,
    ModifyTaskOverlay
)
from gi.repository import Gtk


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


class MainContainer(Gtk.Box):
    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            hexpand=True
        )

        self.stack = Gtk.Stack(
            vexpand=True,
            hexpand=True
        )
        self.stack.add_titled(ToDoList(), "To Do", "To Do")
        self.stack.add_titled(InProgressList(), "In Progress", "In Progress")
        self.stack.add_titled(DoneList(), "Done", "Done")
        self.stack.add_titled(CancelledList(), "Cancelled", "Cancelled")

        self.overlay = Gtk.Overlay(
            vexpand=True,
            hexpand=True,
            child=self.stack
        )

        self.append(TitleBar(self.stack))
        self.append(self.overlay)


if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
