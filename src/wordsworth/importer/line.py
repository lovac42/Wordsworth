# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
import re
from .batch import BatchProcessor


class LineNumberImporter(BatchProcessor):
    re_validate=re.compile(r'^[^\s]+$')

    def parseList(self, offset):
        i=1
        self.dict={}
        self.startTime=0
        for line in self.freq_list[offset:offset+20000]:
            offset+=1
            if line:
                self.updatePTimer(line)
                wd=self.cleanWord(line)
                self.dict[wd]=str(i)
                i+=1
        return offset
