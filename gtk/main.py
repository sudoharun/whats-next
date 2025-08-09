import os
import backend
from ui.window import TitleBar, MainContainer
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gio, Gdk


class ToDoApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.sudoharun.tasker")
        self.connect("activate", self.on_activate)
        backend.get_or_create_db()

    def on_activate(self, app):
        self.load_css()
        window = Gtk.ApplicationWindow(application=app)
        window.set_child(MainContainer())
        window.set_titlebar(TitleBar(window.get_child().stack))
        window.present()

    def load_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_path(os.path.join(os.getcwd(), "styling", "styles.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


# ------------------ EOF ------------------ #

if __name__ == "__main__":
    app = ToDoApp()
    app.run()

# ------------------ EOF ------------------ #
