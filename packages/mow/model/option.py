#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('option', pkey='name', name_long='!!Option', 
                        name_plural='!!Options',caption_field='name',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('name' ,size=':40',name_long='!!Name')