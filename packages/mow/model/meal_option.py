#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('meal_option', pkey='id', name_long='!!Meal option', name_plural='!!Meal options',
                        caption_field='meal_fullname',order_by='$meal_name,$_row_count')
        self.sysFields(tbl,counter='meal_id')
        tbl.column('meal_id',size='22' ,group='_',name_long='!!Meal').relation('meal.id',relation_name='options',
                                                                                mode='foreignkey',onDelete='cascade')
        tbl.column('option' ,size=':40',name_long='!!Option')
        tbl.aliasColumn('meal_type','@meal_id.type',name_long='Meal type')
        tbl.aliasColumn('meal_name','@meal_id.name',name_long='Meal name')
        tbl.formulaColumn('meal_fullname',"($meal_name || '-' || $option)")
        tbl.formulaColumn('selector_sorter',"$meal_fullname ||'_'||CAST(COALESCE($_row_count,0) as TEXT)")