# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
import re
from ..error import *
from .batch import BatchProcessor


class LineNumberImporter(BatchProcessor):

    def setDict(self, case_sensitive):
        self.dict={}
        i=1
        for line in self.freq_list:
            if not line: continue #empty lines
            if not re.match(r'^[^\s]+$',line):
                self.freq_list=None
                raise TypeError
            else:
                if not case_sensitive:
                    line=line.lower()
                self.dict[line]=str(i)
            i+=1


    def matchWord(self, note):
        "space is allowed"
        try:
            wd=note[self.word_field]
            if not self.case_sensitive:
                wd=wd.lower()
            rank=self.dict[wd]
            note[self.rank_field]=rank
            note.flush()
        except KeyError:
            print("no %s in dict"%wd)
            return
