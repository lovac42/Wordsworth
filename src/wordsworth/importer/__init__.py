# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from .batch import BatchProcessor
from .line import LineNumberImporter
from .space import SpaceSeparatedImporter


Importers = (
    (_("Rank by line number (*.line)"), LineNumberImporter),
    (_("Text separated by space or tab (*.freq *.txt)"), SpaceSeparatedImporter),
    )

# TODO: add xml & sql support
