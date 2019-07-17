from gi.repository import Gdk, Gio, Gtk, GLib
import os.path

import lmanager
from lmanager.views.single_log import SingleLog
from lmanager.views.multi_log import MultiLog

class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app)
        self.set_size_request(950, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title('Log manager')

        self.hsize_group = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL)

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        left_box = self.sidebar()
        right_box = self.main_content()
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

        main_box.pack_start(left_box, False, False, 0)
        main_box.pack_start(separator, False, False, 0)
        main_box.pack_start(right_box, True, True, 0)

        self.load_css()
        self.load_model_data()

        self.add(main_box)
        main_box.show_all()

    def sidebar(self):
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.listbox = Gtk.ListBox()
        self.listbox.set_size_request(200, -1)
        self.listbox.connect("row-selected", self._on_select_row)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER,
                          Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.listbox)

        left_box.pack_start(scroll, True, True, 0)

        # self.hsize_group.add_widget(left_box)

        return left_box

    def main_content(self):
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.stack = Gtk.Stack()
        self.stack.get_style_context().add_class("main-container")

        right_box.pack_start(self.stack, True, True, 0)

        return right_box

    def _on_select_row(self, listbox, row):
        if row:
            if row.get_index() == 0:
                print(row.get_index())
                self.stack.set_visible_child_name('multi')
            elif row.get_index() == 1:
                print(row.get_index())
                self.stack.set_visible_child_name('single')
            else:
                print(row.get_index())
            # self.stack.set_visible_child_name(group)

    def load_model_data(self):
        def _make_items_listbox(text):
            lbl = Gtk.Label(label=text, xalign=0.0)
            lbl.set_name('row')
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("sidebar-category")
            row.add(lbl)
            return row

        groups = ['Análisis unitario', 'Análisis grupal', 'Estadísticas']
        groups = sorted(groups)
        # "General" needs to be first item in sidebar

        for g in groups:
            row = _make_items_listbox(g)
            self.listbox.add(row)


        self.stack.add_named(SingleLog().get_scroll(), 'single')
        self.stack.add_named(MultiLog().get_scroll(), 'multi')

        widget = self.listbox.get_row_at_index(0)
        self.listbox.select_row(widget)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(
            os.path.join(lmanager.DATA_DIR, 'app.css'))
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_USER)
