# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from __future__ import unicode_literals
from aqt import mw
from aqt.utils import getFile, showInfo
from codecs import open
import os, re
from .const import *
from .error import *


class BatchProcessor:
    freq_list=None

    # def __init__(self):

    def setFields(self, word_field, rank_field, overwrite):
        self.word_field=word_field
        self.rank_field=rank_field
        self.overwrite=overwrite


    def setList(self, file):
        #file format: unix EOF & unicode
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                data=f.read()
            self.freq_list=re.split(r'\r?\n',data)


    def checkList(self):
        lineRank=False

        #Format: word (space) freq_num
        for line in self.freq_list:
            if not line: continue #empty lines
            if not re.match(r'(?:^[^\s]+\s+\d+$)|^\s+$',line):
                lineRank=True
                break

        #Format: freq by line number
        if lineRank:
            for line in self.freq_list:
                if not line: continue #empty lines
                if not re.match(r'^[^\s]+$|^\s+$',line):
                    self.freq_list=None
                    raise TypeError


    def process(self, nids):
        if not nids:
            raise NoNoteError
        if not self.freq_list:
            raise NoListError

        mw.checkpoint("Wordsworth")
        mw.progress.start()
        self.processNotes(nids)
        mw.progress.finish()
        showInfo("Process complete")
        mw.reset()


    def processNotes(self, nids):
        for nid in nids:
            note=mw.col.getNote(nid)

            if self.word_field not in note or \
               self.rank_field not in note or \
               not note[self.word_field]:
                continue

            if note[self.rank_field] and not self.overwrite:
                continue

            i=1
            for line in self.freq_list:
                if line.find(note[self.word_field]) > -1:
                    try:
                        wd,freq=line.split() #word-space-freq format
                    except ValueError: #sort by line number
                        wd=line
                        freq=str(i)

                    if wd==note[self.word_field].replace(" ", ""):
                        note[self.rank_field]=freq
                        note.flush()
                        break
                i+=1

