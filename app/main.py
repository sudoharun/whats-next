import os
import json
import backend
from ui.window import (
    TitleBar,
    MainContainer
)
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio


class ToDoApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.sudoharun.tasker")
        self.connect("activate", self.on_activate)
        backend.get_or_create_db()

    def on_activate(self, app):
        window = Gtk.ApplicationWindow(application=app)
        window.set_child(MainContainer())
        window.present()


# ------------------ EOF ------------------ #

if __name__ == "__main__":
    app = ToDoApp()
    app.run()

# ------------------ EOF ------------------ #
