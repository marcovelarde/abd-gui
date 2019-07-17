import sys
import os.path

from tensorflow.keras.models import load_model

import numpy as np
import pandas as pd
import pickle
from io import StringIO

from gi.repository import Gtk, Gdk
import lmanager

class MultiLog():
    scroll = Gtk.ScrolledWindow()

    def __init__(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.get_style_context().add_class("container")

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # First row
        hbox1 = Gtk.Box(spacing=15)

        lbl1 = Gtk.Label(label="Seleccione un archivo:", xalign=0.0)
        self.file_chooser = Gtk.FileChooserButton()

        button_a = Gtk.Button.new_with_label("Analizar")
        button_a.connect("clicked", self.analyze_log)

        # button1 = Gtk.Button.new_with_label("Analizar")
        # button1.connect("clicked", self.analyze_log)

        hbox1.pack_start(lbl1, False, False, 0)
        hbox1.pack_end(button_a, False, False, 0)
        hbox1.pack_end(self.file_chooser, False, False, 0)
        # hbox1.pack_end(button1, False, False, 0)

        vbox.pack_start(hbox1, False, False, 0)

        self.scroll.add(vbox)

        self.model = load_model(os.path.join(lmanager.DATA_DIR, 'model.h5'))

        with open(os.path.join(lmanager.DATA_DIR, 'dict.pkl'), 'rb') as f:
            self.word_index, self.reverse_word_index = pickle.load(f)

    def get_scroll(self):
        return self.scroll

    def analyze_log(self, button):
        try:
            path = self.file_chooser.get_file().get_path()
        catch AttributeError:
