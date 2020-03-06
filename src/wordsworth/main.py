# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

from .config import Config
from .wordsworth import Wordsworth
from .utils import getMenu
from .const import *


conf=Config(ADDONNAME)

def setupMenu(bws):
    key=conf.get("hotkey", DEFAULT_HOTKEY) or QKeySequence()

    act=QAction(TITLE, bws)
    act.setShortcut(QKeySequence(key))
    act.triggered.connect(lambda:Wordsworth(bws,conf))

    menu=getMenu(bws,'&Tools')
    # menu.addSeparator()
    menu.addAction(act)

addHook("browser.setupMenus", setupMenu)
