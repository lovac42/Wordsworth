# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


# from __future__ import unicode_literals
from aqt import mw
# from aqt.utils import getFile, showInfo
# from codecs import open
import os, re
# from ..const import *
from ..error import *
from .batch import BatchProcessor


class LineNumberImporter(BatchProcessor):

    def checkList(self):
        for line in self.freq_list:
            if not line: continue #empty lines
            if not re.match(r'^[^\s]+$|^\s+$',line):
                self.freq_list=None
                raise TypeError


    def matchLine(self, note):
        i=1
        for line in self.freq_list:
            word=note[self.word_field]
            print "line=%s word=%s"%(line,word)

            if not word: return
            word=self.parse(word)
            if word==line:
                note[self.rank_field]=str(i)
                note.flush()
            i+=1

