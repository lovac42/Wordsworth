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


class SpaceSeparatedImporter(BatchProcessor):

    def checkList(self):
        for line in self.freq_list:
            if not line: continue #empty lines
            if not re.match(r'(?:^[^\s]+\s+\d+$)|^\s+$',line):
                self.freq_list=None
                raise TypeError


    def matchLine(self, note):
        for line in self.freq_list:
            word=note[self.word_field]
            if not word: continue
            word=self.parse(word)

            if word and line.find(word) > -1:
                wd,freq=line.split()
                if word==wd:
                    note[self.rank_field]=freq
                    note.flush()

