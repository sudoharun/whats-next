import gi
gi.require_version('Gtk', '4.0')

import backend
from gi.repository import Gtk


class AddTaskOverlay(Gtk.Box):
    def __init__(self, list_name):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER,
            halign=Gtk.Align.CENTER
        )
        self.list_name = list_name


class ModifyTaskOverlay(Gtk.Box):
    def __init__(self, prev_list_name, new_list_name):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER,
            halign=Gtk.Align.CENTER
        )
        self.prev_list_name = prev_list_name
        self.new_list_name = new_list_name


if __name__ == "__main__":
    raise NotImplementedError("This module is not meant to be run directly.")
