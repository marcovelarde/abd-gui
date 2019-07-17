#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSES/GPL-3.0

import os.path
import signal
import sys

import gi
gi.require_version("Gtk", "3.0")

import lmanager
from lmanager.defs import VERSION


if __name__ == '__main__':
    try:
        from lmanager.defs import VIEWS_DIR, DATA_DIR
        _defs_present = True
    except ImportError:
        VIEWS_DIR = DATA_DIR = ""
        _defs_present = False

    # the supplied prefix always beats the contents of defs
    if not _defs_present:
        _me = os.path.abspath(os.path.dirname(__file__))
        VIEWS_DIR = os.path.join(_me, "lmanager", "views")
        DATA_DIR = os.path.join(_me, "data")

    lmanager.VIEWS_DIR = VIEWS_DIR
    lmanager.DATA_DIR = DATA_DIR
    lmanager.APP_NAME = "log-manager"

    from lmanager.app import LogManager
    app = LogManager()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = app.run(None)
    sys.exit(exit_status)
