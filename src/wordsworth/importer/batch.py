# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


# enable for anki 2.0 if needed
# from __future__ import unicode_literals

import os, re
import time
from aqt import mw
from aqt.utils import showInfo
from anki.lang import _
from codecs import open
from ..clean import Cleaner
from ..error import *


RE_NOSPACE=re.compile(r'\s')


class BatchProcessor:
    htmlCleaner=Cleaner()
    re_validate=re.compile(r'.*')
    freq_list=None
    dict=None
    startTime=0
    count=0

    # def __init__(self):

    def setFields(self, word_field, rank_field):
        self.word_field=word_field
        self.rank_field=rank_field

    def setProperties(self, overwrite, case_sensitive, no_space, no_html):
        self.overwrite=overwrite
        self.case_sensitive=case_sensitive
        self.no_space=no_space
        self.no_html=no_html

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

        self.parseList()

        mw.checkpoint("Wordsworth")
        return self.processNotes(nids)


    def processNotes(self, nids):
        self.startTime=0
        for nid in nids:
            note=mw.col.getNote(nid)

            if self.word_field not in note or \
               self.rank_field not in note or \
               not note[self.word_field]:
                continue

            if note[self.rank_field] and not self.overwrite:
                continue

            self.matchWord(note)


    def checkList(self):
        "method for validating word lists"
        line_num=1
        for line_txt in self.freq_list:
            if line_txt and not self.re_validate.match(line_txt):
                self.freq_list=None
                raise InvalidFormatError(line_num,line_txt)
            line_num+=1


    def matchWord(self, note):
        "match word to list"
        try:
            wd=note[self.word_field]
            wd=self.cleanWord(wd)
            rank=self.dict[wd]
            note[self.rank_field]=rank
            note.flush()
            self.count+=1
            self.updatePTimer(wd)
        except KeyError:
            print("ww: no %s in dict"%wd)


    def cleanWord(self, wd):
        if not self.case_sensitive:
            wd=wd.lower()

        if self.no_html:
            self.htmlCleaner.reset()
            self.htmlCleaner.feed(wd)
            wd=self.htmlCleaner.toString()

        if self.no_space: #space between words
            return RE_NOSPACE.sub("",wd)
        return wd.strip() #leading & trailing space


    def updatePTimer(self, labelText):
        now = time.time()
        if now-self.startTime >= 0.5:
            self.startTime=now
            mw.progress.update(_("%s"%labelText))


    def parseList(self):
        "abstract method for parsing word lists"
        return
