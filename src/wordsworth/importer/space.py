# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
import os, re
from ..error import *
from .batch import BatchProcessor


class SpaceSeparatedImporter(BatchProcessor):

    def setDict(self, case_sensitive):
        self.dict={}
        for line in self.freq_list:
            if not line: continue #empty lines
            if not re.match(r'(?:^[^\s]+\s+\d+$)',line):
                self.freq_list=None
                raise TypeError
            else:
                try:
                    wd,freq=line.split()
                    if not case_sensitive:
                        wd=wd.lower()
                    self.dict[wd]=freq
                except: #split errors
                    continue

    def matchWord(self, note):
        "no space allowed"
        try:
            wd=self.parse(note[self.word_field])
            if not self.case_sensitive:
                wd=wd.lower()
            rank=self.dict[wd]
            note[self.rank_field]=rank
            note.flush()
        except KeyError:
            print("no %s in dict"%wd)
            return
