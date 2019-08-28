# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
import os, re
from .batch import BatchProcessor


class SpaceSeparatedImporter(BatchProcessor):
    re_validate=re.compile(r'(?:^[^\s]+\s+\d+$)')

    def parseList(self, offset):
        self.dict={}
        self.startTime=0
        self.no_space=True
        for line in self.freq_list[offset:offset+20000]:
            offset+=1
            if line:
                self.updatePTimer(line)
                try:
                    wd,freq=line.split()
                    wd=self.cleanWord(wd)
                    wd=self.normalize(wd,type=2)
                    if not self.dict.get(wd):
                        self.dict[wd]=freq
                except: #split errors
                    print("ww: dict split error, %s"%line)
        return offset
