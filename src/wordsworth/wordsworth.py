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

    def __init__(self, browser, conf):
        self.browser=browser
        self.conf=conf

        #Must have some notes selected in browser
        try:
            self.setNotes()
        except NoNoteError as err:
            showInfo(str(err))
            return

        #Note in editor must be removed to update templates.
        if ANKI21:
            self.browser.editor.saveNow(self.hideEditor)
        else:
            self.browser.editor.saveNow()
            self.hideEditor()

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

        cbs=self.conf.get("case_sensitive",0)
        self.cb_casesense=QtWidgets.QCheckBox()
        self.cb_casesense.setCheckState(cbs)
        self.cb_casesense.clicked.connect(self.onChangedCB)
        self.cb_casesense.setText(_('Case Sen..'))
        self.cb_casesense.setToolTip(_('Case Sensitive Match'))
        gridLayout.addWidget(self.cb_casesense, r, 1, 1, 1)

        r+=1
        fieldLayout=QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel("Word Field (READ):")
        fieldLayout.addWidget(label)

        idx=self.conf.get("word_field",0)
        self.wordField=QComboBox()
        self.wordField.setMinimumWidth(250)
        self.wordField.addItems(fields)
        self.wordField.setCurrentIndex(idx)
        self.wordField.currentIndexChanged.connect(self.checkWritable)
        fieldLayout.addWidget(self.wordField)
        gridLayout.addLayout(fieldLayout,r,0, 1, 1)

        cbs=self.conf.get("strip_html",0)
        self.cb_rm_html=QtWidgets.QCheckBox()
        self.cb_rm_html.setCheckState(cbs)
        self.cb_rm_html.clicked.connect(self.onChangedCB)
        self.cb_rm_html.setText(_('No HTML'))
        self.cb_rm_html.setToolTip(_('Strip HTML during search'))
        gridLayout.addWidget(self.cb_rm_html, r, 1, 1, 1)

        r+=1
        fieldLayout=QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel("Rank Field (WRITE):")
        fieldLayout.addWidget(label)

        idx=self.conf.get("rank_field",0)
        self.rankField=QComboBox()
        self.rankField.setMinimumWidth(250)
        self.rankField.addItems(fields)
        self.rankField.setCurrentIndex(idx)
        self.rankField.currentIndexChanged.connect(self.checkWritable)
        fieldLayout.addWidget(self.rankField)
        gridLayout.addLayout(fieldLayout,r,0, 1, 1)

        cbs=self.conf.get("strip_space",0)
        self.cb_rm_space=QtWidgets.QCheckBox()
        self.cb_rm_space.setCheckState(cbs)
        self.cb_rm_space.clicked.connect(self.onChangedCB)
        self.cb_rm_space.setText(_('No Space'))
        self.cb_rm_space.setToolTip(_('Strip space during search'))
        gridLayout.addWidget(self.cb_rm_space, r, 1, 1, 1)

        r+=1
        self.cb_overWrite=QtWidgets.QCheckBox()
        self.cb_overWrite.setText(_('Overwrite rank field if not empty?'))
        self.cb_overWrite.setToolTip(_('Do you seriously need a tooltip for this?'))
        gridLayout.addWidget(self.cb_overWrite, r, 0, 1, 1)

        r+=1
        self.cb_normalize=QtWidgets.QCheckBox()
        self.cb_normalize.setTristate(True)
        self.cb_normalize.clicked.connect(self._stemmer)
        self.cb_normalize.setText(_('Apply English stemmer? (GIYF)'))
        self.cb_normalize.setToolTip(_('Strips suffix -s, -ed, -es, -ing, -tion, -sion, ...'))
        gridLayout.addWidget(self.cb_normalize, r, 0, 1, 1)

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
        diag.setWindowTitle(TITLE)
        diag.exec_()


    def onChangedCB(self):
        cs=self.cb_casesense.checkState()
        sp=self.cb_rm_space.checkState()
        htm=self.cb_rm_html.checkState()
        self.conf.set("case_sensitive",cs)
        self.conf.set("strip_html",htm)
        self.conf.set("strip_space",sp)


    def checkWritable(self):
        idx=self.wordField.currentIndex()
        self.conf.set("word_field",idx)
        idx=self.rankField.currentIndex()
        self.conf.set("rank_field",idx)

        if not self.importer or not self.freq_file:
            self.btn_save.setEnabled(False)
            return

        wdf=self.wordField.currentText()
        rkf=self.rankField.currentText()
        if not wdf or not rkf or wdf==rkf:
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
        file=getFile(
            self.browser, _("Choose File"), None,
            filter=filt, key="import"
        )
        if file:
            self.freq_file=file
            self.importer=self.getImporter(file)
            self._import()


    def _import(self):
        if not self.importer:
            return
        try:
            self.importer.setList(self.freq_file)
            self.importer.checkList()
            name=self.freq_file.split("/")[-1]
            self.btn_import.setText("Loaded: "+name)
            self.checkWritable()

        except InvalidFormatError as e:
            self.btn_import.setText("Not the right format")
            self.btn_save.setEnabled(False)
            self.importer=None
            showInfo(e.message)

        # except:
            # self.btn_import.setText("Error Reading File")
            # self.btn_save.setEnabled(False)
            # self.importer=None


    def _stemmer(self):
        checked=self.cb_normalize.checkState()
        if checked==2:
            msg='Stemmer: strip both word field and word list'
        elif checked==1:
            msg='Stemmer: strip word field only'
        else:
            msg='Apply English stemmer? (GIYF)'
        self.cb_normalize.setText(_(msg))


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
            norm=self.cb_normalize.checkState()

            self.importer.setFields(wdf,rkf)
            self.importer.setProperties(ow,cs,sp,htm,norm)
            try:
                self.importer.process(self.notes)
            except NoListError as err:
                showInfo(str(err))
            finally:
                mw.progress.finish()
            self.showStats()


    def showStats(self):
        tot=self.importer.stat["total"]
        w=self.importer.stat["written"]
        s=self.importer.stat["skipped"]
        ow=self.importer.stat["overwritten"]
        nf=self.importer.stat["notfound"]
        e=self.importer.stat["nofield"]
        showInfo("""Process completed!

SUMMARY:\t\t\t( %d / %d )
\tTotal Notes:\t\t%d
\tMatches:\t\t%d
\tWritten:\t\t%d
\tOverwritten:\t\t%d
\tNot overwr.:\t\t%d
\tNot in dict:\t\t%d
\tNo FieldName:\t\t%d
\tSkipped:\t\t%d
"""%(w,tot,tot,w+s,w,ow,s,nf,e,e+s+nf))
