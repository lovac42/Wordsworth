# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re
from aqt import mw
from .batch import BatchProcessor


class CSVImporter(BatchProcessor):

    def checkList(self):
        for line in self.freq_list:
            if not re.match(r'^.+;.+$|^\s+$',line):
                self.freq_list=None
                raise TypeError


    def matchLine(self, note):
        for line in self.freq_list:
            if not line: continue
            word=note[self.word_field]
            if word and line.find(word) > -1:
                wd,freq=line.split(';')
                if word==wd:
                    note[self.rank_field]=freq
                    note.flush()

