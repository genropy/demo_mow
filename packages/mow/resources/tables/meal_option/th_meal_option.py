#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method


class View(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('option',width='100%')

    def th_order(self):
        return '_row_count'

class ViewEditable(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count',counter=True,hidden=True,edit=True)

        r.fieldcell('option',width='100%',edit=dict(tag='dbCombobox',dbtable='mow.option'))

    def th_order(self):
        return '_row_count'

class Form(BaseComponent):
    def th_form(self,form):
        form.record