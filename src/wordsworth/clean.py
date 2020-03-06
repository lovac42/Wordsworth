# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from .const import ANKI20

if ANKI20:
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser


class Cleaner(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()

    def reset(self):
        HTMLParser.reset(self)
        self.dat=[]

    def handle_data(self, txt):
        self.dat.append(txt)

    def toString(self):
        return ''.join(self.dat)
