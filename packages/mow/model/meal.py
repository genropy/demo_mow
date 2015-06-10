#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('meal', pkey='id', name_long='!!Meal', name_plural='!!Meals',caption_field='name')
        self.sysFields(tbl)
        tbl.column('name' ,size=':40',name_long='!!Name',indexed=True)
        tbl.column('type' ,size=':1',name_long='!!Type',values='1:Starter,2:Main Course,3:Dessert')
        tbl.column('description',name_long='!!Description')
        tbl.column('photo_url', dtype='P',name_long='!!Photo URL')
