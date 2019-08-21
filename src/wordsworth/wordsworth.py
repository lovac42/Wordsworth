# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re
from aqt import mw
from aqt.qt import *
from aqt.utils import getFile, showInfo
from anki.lang import _

from .utils import fieldNamesForNotes
from .importer import *
from .const import *
from .error import *

if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


class Wordsworth():
    importer=None

    def __init__(self, browser):
        self.browser=browser

        #Must have some notes selected in browser
        try:
            self.setNotes()
        except NoNoteError as err:
            showInfo(str(err))
            return

        #Note in editor must be removed to update templates.
        if CCBC or ANKI20:
            self.browser.editor.saveNow()
            self.hideEditor()
        else:
            self.browser.editor.saveNow(self.hideEditor)

        self.showDialog()


    def setNotes(self):
        self.notes=self.browser.selectedNotes()
        if not self.notes:
            raise NoNoteError


    def hideEditor(self):
        self.browser.editor.setNote(None)
        self.browser.singleCard=False


    def showDialog(self):
        fields=fieldNamesForNotes(self.notes)

        r=0
        gridLayout=QtWidgets.QGridLayout()
        layout=QtWidgets.QVBoxLayout()
        layout.addLayout(gridLayout)

        self.btn_import=QPushButton('Import Word List')
        self.btn_import.clicked.connect(self.onImport)
        gridLayout.addWidget(self.btn_import,r,0,1,1)

        self.cb_casesense=QtWidgets.QCheckBox()
        self.cb_casesense.clicked.connect(self._import)
        self.cb_casesense.setText(_('Case Sen..'))
        gridLayout.addWidget(self.cb_casesense, r, 1, 1, 1)

        r+=1
        fieldLayout=QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel("Word Field (READ):")
        fieldLayout.addWidget(label)

        self.wordField=QComboBox()
        self.wordField.setMinimumWidth(250)
        self.wordField.addItems(fields)
        self.wordField.currentIndexChanged.connect(self.valueChange)
        fieldLayout.addWidget(self.wordField)
        gridLayout.addLayout(fieldLayout,r,0, 1, 1)

        self.cb_rm_html=QtWidgets.QCheckBox()
        self.cb_rm_html.clicked.connect(self._import)
        self.cb_rm_html.setText(_('Strip HTML'))
        gridLayout.addWidget(self.cb_rm_html, r, 1, 1, 1)

        r+=1
        fieldLayout=QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel("Rank Field (WRITE):")
        fieldLayout.addWidget(label)

        self.rankField=QComboBox()
        self.rankField.setMinimumWidth(250)
        self.rankField.addItems(fields)
        self.rankField.currentIndexChanged.connect(self.valueChange)
        fieldLayout.addWidget(self.rankField)
        gridLayout.addLayout(fieldLayout,r,0, 1, 1)

        self.cb_rm_space=QtWidgets.QCheckBox()
        self.cb_rm_space.clicked.connect(self._import)
        self.cb_rm_space.setText(_('Strip Space'))
        gridLayout.addWidget(self.cb_rm_space, r, 1, 1, 1)

        r+=1
        self.cb_overWrite=QtWidgets.QCheckBox()
        # self.cb_overWrite.setCheckState(2)
        self.cb_overWrite.setText(_('Overwrite rank field if not empty?'))
        gridLayout.addWidget(self.cb_overWrite, r, 0, 1, 1)

        r+=1
        lbl_help=QtWidgets.QLabel()
        lbl_help.setText(_("""<br><i>Exact matches only, 
                           beware of hidden html tags.</i><br>
                           <b>Make sure to backup first!</b>"""))
        gridLayout.addWidget(lbl_help,r,0,1,1)


        self.btn_save=QPushButton('Write')
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.onWrite)
        gridLayout.addWidget(self.btn_save,r,1,1,1)


        diag=QDialog(self.browser)
        diag.setLayout(layout)
        diag.setWindowTitle('Wordsworth: Word Frequency Ranker')
        diag.exec_()


    def valueChange(self):
        if not self.importer or not self.freq_file:
            self.btn_save.setEnabled(False)
            return

        wdf=self.wordField.currentText()
        rkf=self.rankField.currentText()
        if wdf==rkf:
            self.btn_save.setEnabled(False)
        else:
            self.btn_save.setEnabled(True)


    def getImporter(self, file):
        for im in Importers:
            for mext in re.findall("[( ]?\*\.(.+?)[) ]", im[0]):
                if file.endswith("." + mext):
                    return im[1]()
        return Importers[0][1]() #default importer


    def onImport(self):
        filt = ";;".join([x[0] for x in Importers])
        self.freq_file=getFile(
            self.browser, _("Choose File"), None,
            filter=filt, key="import"
        )
        if not self.freq_file:
            return
        self.importer=self.getImporter(self.freq_file)
        self._import()


    def _import(self):
        if not self.importer:
            return
        try:
            self.importer.setList(self.freq_file)
            self.importer.checkList()
            self.btn_import.setText("Frequency List Loaded")
            self.valueChange()

        except InvalidFormatError as e:
            self.btn_import.setText("Not the right format")
            self.btn_save.setEnabled(False)
            self.importer=None
            showInfo(e.message)

        # except:
            # self.btn_import.setText("Error Reading File")
            # self.btn_save.setEnabled(False)
            # self.importer=None


    def onWrite(self):
        if self.btn_save.isEnabled():
            mw.progress.start(immediate=True)
            mw.progress.update(_("Processing Dictionary..."))

            wdf=self.wordField.currentText()
            rkf=self.rankField.currentText()
            ow=self.cb_overWrite.checkState()
            cs=self.cb_casesense.checkState()
            sp=self.cb_rm_space.checkState()
            htm=self.cb_rm_html.checkState()

            self.importer.setFields(wdf,rkf)
            self.importer.setProperties(ow,cs,sp,htm)
            try:
                self.importer.process(self.notes)
                tot=len(self.notes)
                cnt=self.importer.count
                showInfo("Process complete (%d/%d)"%(cnt,tot))
            except NoListError as err:
                showInfo(str(err))
            finally:
                mw.progress.finish()
