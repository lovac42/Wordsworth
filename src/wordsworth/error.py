# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


class NoNoteError(Exception):
    """Raised when no note is selected"""
    def __str__(self): 
        return "Select some notes first"

class NoListError(Exception):
    """Raised when there is no list given"""
    def __str__(self): 
        return "Can't process list"
