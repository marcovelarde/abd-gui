import sys
import os.path

from tensorflow.keras.models import load_model

import numpy as np
import pandas as pd
import pickle
from io import StringIO

from gi.repository import Gtk, Gdk
import lmanager

class SingleLog():
    scroll = Gtk.ScrolledWindow()
    entry = Gtk.Entry()

    def __init__(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.get_style_context().add_class("container")

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # First row
        hbox1 = Gtk.Box(spacing=15)

        lbl1 = Gtk.Label(label="Ingrese log:", xalign=0.0)
        self.entry.set_placeholder_text("Copie y pegue un log unitario completo.")

        # button1 = Gtk.Button.new_with_label("Analizar")
        # button1.connect("clicked", self.analyze_log)

        hbox1.pack_start(lbl1, False, False, 0)
        hbox1.pack_start(self.entry, True, True, 0)
        # hbox1.pack_end(button1, False, False, 0)

        # Second row
        hbox2 = Gtk.Box(spacing=10)
        hbox2.get_style_context().add_class("row-margin-top")

        button2_1 = Gtk.Button.new_with_label("Analizar")
        button2_1.connect("clicked", self.analyze_log)

        button2_2 = Gtk.Button.new_with_label("Limpiar entrada")
        button2_2.connect("clicked", self.clear_text)

        button2_3 = Gtk.Button.new_with_label("Pegar texto")
        button2_3.connect("clicked", self.paste_text)

        hbox2.pack_end(button2_1, False, False, 0)
        hbox2.pack_end(button2_2, False, False, 0)
        hbox2.pack_end(button2_3, False, False, 0)

        # Thrid row
        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.vbox3.set_no_show_all(True)

        lbl3_1 = Gtk.Label(label="Información de entrada:", xalign=0.0)
        self.lbl3_2 = Gtk.Label(xalign=0.0)
        lbl3_1.get_style_context().add_class("body-title")

        lbl3_3 = Gtk.Label(label="Información de entrada decodificada:", xalign=0.0)
        self.lbl3_4 = Gtk.Label(xalign=0.0)
        lbl3_3.get_style_context().add_class("body-title-mt")

        lbl3_5 = Gtk.Label(label="Parámetros en la url no considerados:", xalign=0.0)
        self.lbl3_6 = Gtk.Label(xalign=0.0)
        lbl3_5.get_style_context().add_class("body-title-mt")

        lbl_res_title = Gtk.Label(label="Resultado del análisis:", xalign=0.0)
        self.lbl_res = Gtk.Label(xalign=0.0)
        lbl_res_title.get_style_context().add_class("body-title-mt")

        self.vbox3.pack_start(lbl3_1, False, False, 0)
        self.vbox3.pack_start(self.lbl3_2, False, False, 0)
        self.vbox3.pack_start(lbl3_3, False, False, 0)
        self.vbox3.pack_start(self.lbl3_4, False, False, 0)
        self.vbox3.pack_start(lbl3_5, False, False, 0)
        self.vbox3.pack_start(self.lbl3_6, False, False, 0)
        self.vbox3.pack_start(lbl_res_title, False, False, 0)
        self.vbox3.pack_start(self.lbl_res, False, False, 0)

        # Error row
        self.lbl_err_title = Gtk.Label(label="Error:", xalign=0.0)
        self.lbl_err_title.set_no_show_all(True)
        self.lbl_err_title.get_style_context().add_class("body-title")
        self.lbl_err = Gtk.Label(label="Error: ", xalign=0.0)
        self.lbl_err.set_no_show_all(True)

        # Adding rows
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.get_style_context().add_class("sep-margins")

        vbox.pack_start(hbox1, False, False, 0)
        vbox.pack_start(hbox2, False, False, 0)
        vbox.pack_start(separator, False, False, 0)
        vbox.pack_start(self.lbl_err_title, False, False, 0)
        vbox.pack_start(self.lbl_err, False, False, 0)
        vbox.pack_start(self.vbox3, True, True, 0)

        self.scroll.add(vbox)

        self.model = load_model(os.path.join(lmanager.DATA_DIR, 'model.h5'))

        with open(os.path.join(lmanager.DATA_DIR, 'dict.pkl'), 'rb') as f:
            self.word_index, self.reverse_word_index = pickle.load(f)

    def get_scroll(self):
        return self.scroll

    def clear_text(self, button):
        self.entry.set_text('')

    def paste_text(self, button):
        text = self.clipboard.wait_for_text()
        if text is not None:
            self.entry.set_text(text)

    def analyze_log(self, button):
        test = StringIO(self.entry.get_text().strip())

        try:
            df_evaluate = pd.read_csv(test, sep=" ", header=None)
            df_evaluate[11], df_evaluate[12], df_evaluate[13] = df_evaluate[5].str.split(' ', 2).str
            df_evaluate.drop([0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 13], axis=1, inplace=True)
        except ValueError:
            self.vbox3.hide()
            self.lbl_err.set_text("Valores en el registro no esperados o url inválida.")
            self.lbl_err_title.show()
            self.lbl_err.show()
            return -1
        except KeyError:
            self.vbox3.hide()
            self.lbl_err.set_text("Registro incompleto o url con formato inválido.")
            self.lbl_err_title.show()
            self.lbl_err.show()
            return -1

        if df_evaluate.at[0,11] != 'GET' and df_evaluate.at[0,11] != 'POST':
            self.vbox3.hide()
            self.lbl_err.set_text("Error: Método de la petición HTTP inválido o no considerado en el proyecto.")
            self.lbl_err_title.show()
            self.lbl_err.show()
            return -1

        df_evaluate[12].replace({r'^/$': '<BASE_URL>'}, regex=True, inplace=True)
        df_evaluate[12].replace({r' \%[\%0-9A-Za-z]*': ' <PERCENT_URL> '},regex=True, inplace=True)
        df_evaluate[12].replace({r'\w+\d+\w+': ''},regex=True, inplace=True)
        df_evaluate[12].replace({r'\d{2,}': ''},regex=True, inplace=True)
        df_evaluate[12].replace({r'\[\d*\]': ' '},regex=True, inplace=True)
        df_evaluate[12].replace({'/': ' ', ':': ' ', '\.': ' ', '\?': ' ', '=': ' ', '\|': ' ', '&': ' '},regex=True, inplace=True)
        df_evaluate[11].replace({'GET': 2, 'POST': 3}, inplace=True)

        df_evaluate[12] = df_evaluate[12].str.lower()
        df_evaluate[12] = df_evaluate[12].apply(self.encode)
        df_evaluate[12] = df_evaluate[12].apply(self.insert_start)

        df_evaluate[6].replace({307: '<TEMPORARY_REDIRECT>', 400: '<BAD_REQUEST>', 404: '<NOT_FOUND>', 200: '<OK>', 301: '<MOVED_PERMANTLY>'}, inplace=True)
        df_evaluate[6] = df_evaluate[6].apply(self.encode_single)

        df_evaluate.columns = ['status', 'method', 'r_url']

        if len(df_evaluate.at[0, 'r_url']) < 11:
            for i in range (len(df_evaluate.at[0,'r_url']), 11):
                df_evaluate.at[0,'r_url'].append(0)

        for i in range(11):
            df_evaluate.at[0, 'r_url' + str(i)] = df_evaluate.at[0, 'r_url'][i]

        df_evaluate.drop(['r_url'], axis=1, inplace=True)

        single_evaluate = df_evaluate.values[0]

        self.lbl3_2.set_text('[' + ', '.join(str(int(x)) for x in single_evaluate) + ']')
        self.lbl3_4.set_text(self.decode(single_evaluate))

        single_evaluate = (np.expand_dims(single_evaluate, 0))

        predict = round(self.model.predict(single_evaluate)[0][0] * 100, 4)
        if predict > 0.55:
            self.lbl_res.set_text('Maligno' + '   (' + str(predict) + '%)')
        else:
            self.lbl_res.set_text('Benigno' + '   (' + str(predict) + '%)')

        self.lbl_err_title.hide()
        self.lbl_err.hide()
        self.vbox3.set_no_show_all(False)
        self.vbox3.show_all()

    # DATA MANAGEMENT

    def decode(self, ls):
        result = ''
        pad_count = 0

        for i in ls:
            if int(i) != 0:
                result += self.reverse_word_index.get(i, '?') + ' '
            else:
                pad_count += 1

        if pad_count > 0: result += '<PAD>' + '(x' + str(pad_count) + ')'
        # return ' '.join([self.reverse_word_index.get(i, '?') for i in ls])
        return result

    def encode(self, text):
        text_ls = []
        for i in text.split():
            try:
                text_ls.append(self.word_index[i])
            except KeyError:
                self.lbl3_6.set_text(self.lbl3_6.get_text() + i + ' ')
                print('Unhandled word \'' + i + '\'')
        return text_ls

    def decode_single(self, text):
        return self.reverse_word_index.get(text)

    def encode_single(self, text):
        return self.word_index.get(text)

    def insert_start(self, ls):
        ls.insert(0, 1)
        return ls
