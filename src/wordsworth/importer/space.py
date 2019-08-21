# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
import os, re
from .batch import BatchProcessor


class SpaceSeparatedImporter(BatchProcessor):
    re_validate=re.compile(r'(?:^[^\s]+\s+\d+$)')

    def parseList(self):
        self.dict={}
        self.startTime=0
        for line in self.freq_list:
            if line:
                self.updatePTimer(line)
                try:
                    wd,freq=line.split()
                except: #split errors
                    print("ww: dict split error, %s"%line)
                    continue
                wd=self.cleanWord(wd)
                self.dict[wd]=freq
        self.no_space=True
