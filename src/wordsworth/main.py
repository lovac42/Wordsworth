# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

from .config import Config
from .wordsworth import Wordsworth
from .const import *


conf=Config(ADDONNAME)

def setupMenu(bws):
    act=QAction(TITLE, bws)

    key=conf.get("hotkey","Ctrl+Shift+W")
    if key:
        act.setShortcut(QKeySequence(key))

    act.triggered.connect(lambda:Wordsworth(bws,conf))
    bws.form.menuEdit.addSeparator()
    bws.form.menuEdit.addAction(act)

addHook("browser.setupMenus", setupMenu)
