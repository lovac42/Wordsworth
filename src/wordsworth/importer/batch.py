# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from __future__ import unicode_literals
from aqt import mw
from aqt.utils import showInfo
from codecs import open
import os, re
from ..error import *


class BatchProcessor:
    freq_list=None
    dict=None

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


    def process(self, nids):
        if not nids:
            raise NoNoteError
        if not self.freq_list:
            raise NoListError
        mw.checkpoint("Wordsworth")
        self.processNotes(nids)


    def processNotes(self, nids):
        for nid in nids:
            note=mw.col.getNote(nid)

            if self.word_field not in note or \
               self.rank_field not in note or \
               not note[self.word_field]:
                continue

            if note[self.rank_field] and not self.overwrite:
                continue

            self.matchWord(note)


    def parse(self, wd):
        return wd.replace(" ", "")
        #TODO: add option to strip html


    def matchWord(self, note):
        "abstract method for matching word to list"
        return


    def setDict(self):
        "abstract method for checking valid dict files"
        return
