import sys
import os.path

from gi.repository import GLib, Gio, Gtk

import lmanager
from lmanager.abdview import Window

class LogManager(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self, application_id="me.gedzeppelin.logmanager")
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)

        assert(os.path.exists(lmanager.DATA_DIR))

        builder = Gtk.Builder()
        filename = os.path.join(lmanager.DATA_DIR, 'app-menu.glade')
        builder.add_from_file(filename)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = Window(self)

        self.window.present()

    def about_cb(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
