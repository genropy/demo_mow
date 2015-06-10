#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):
    def th_hiddencolumns(self):
        return '$meal_name'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('meal_type',width='8em')
        r.fieldcell('meal_id',width='30em')
        r.fieldcell('@meal_id.description',width='40em',name='Description')

    def th_order(self):
        return 'meal_type,meal_name'

class ViewFromMeal(BaseComponent):
    def th_hiddencolumns(self):
        return '$date,$calendar_id'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('date',width='8em')
        r.fieldcell('recipient_count',width='6em')

    def th_order(self):
        return 'date'