import gi
gi.require_version('Gtk', '4.0')

from .lists import (
    ToDoList,
    InProgressList,
    DoneList,
    CancelledList
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


class MainContainer(Gtk.Overlay):
    def __init__(self):
        super().__init__()

        self.container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            vexpand=True,
            hexpand=True
        )
        self.set_child(self.container)

        self.stack = Gtk.Stack(
            vexpand=True,
            hexpand=True
        )
        self.stack.add_titled(ToDoList(), "To Do", "To Do")
        self.stack.add_titled(InProgressList(), "In Progress", "In Progress")
        self.stack.add_titled(DoneList(), "Done", "Done")
        self.stack.add_titled(CancelledList(), "Cancelled", "Cancelled")

        self.container.append(TitleBar(self.stack))
        self.container.append(self.stack)


if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
