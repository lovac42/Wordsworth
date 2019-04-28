# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.hooks import addHook
from .wordsworth import *
from .const import *


def setupMenu(bws):
    act=QAction("Wordsworth: Word Frequency Ranker", bws)

    # ENABLE IF THERE IS NO SHORTCUT CONFLICT
    # act.setShortcut(QKeySequence("Ctrl+Shift+W"))

    act.triggered.connect(lambda:Wordsworth(bws))
    bws.form.menuEdit.addSeparator()
    bws.form.menuEdit.addAction(act)

addHook("browser.setupMenus", setupMenu)
