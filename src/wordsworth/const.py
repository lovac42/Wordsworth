# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw

from anki import version
CCBC = version.endswith("ccbc")
ANKI21 = not CCBC and version.startswith("2.1.")
ANKI20 = version.startswith("2.0.")

ADDONNAME = "Wordsworth"

