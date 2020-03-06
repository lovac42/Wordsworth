# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/Wordsworth
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.utils import ids2str


def fieldNamesForNotes(nids):
    fields = set()
    mids = mw.col.db.list("select distinct mid from notes where id in %s" % ids2str(nids))
    for mid in mids:
        model = mw.col.models.get(mid)
        for name in mw.col.models.fieldNames(model):
            if name not in fields: #slower w/o
                fields.add(name)
    return sorted(fields, key=lambda x: x.lower())
