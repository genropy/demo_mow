#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('recipient_calendar', pkey='id', name_long='!!Recipient calendar', name_plural='!!Recipient calendar')
        self.sysFields(tbl)
        tbl.column('recipient_id',size='22' ,group='_',name_long='!!Recipient').relation('recipient.id',relation_name='recipient_calendar_items',mode='foreignkey',onDelete='cascade')
        tbl.column('calendar_id',size='22' ,group='_',name_long='!!Calendar').relation('calendar.id',relation_name='recipient_calendar_items',mode='foreignkey',onDelete='raise')
        tbl.column('starter_id',size='22' ,group='_',name_long='!!Starter').relation('meal_option.id',mode='foreignkey',onDelete='raise')
        tbl.column('main_course_id',size='22' ,group='_',name_long='!!Main course').relation('meal_option.id',mode='foreignkey',onDelete='raise')
        tbl.column('dessert_id',size='22' ,group='_',name_long='!!Dessert').relation('meal_option.id',mode='foreignkey',onDelete='raise')
        tbl.aliasColumn('date','@calendar_id.date',name_long='Date',dtype='D')
        tbl.aliasColumn('recipient_rcount','@recipient_id._row_count',name_long='N.',dtype='L')


    def alignCalendar(self,calendar_id=None,recipient_id=None):
        records = None
        if calendar_id:
            records = [{'recipient_id':r['id'],'calendar_id':calendar_id} for r in self.db.table('mow.recipient').query(columns='$id',addPkeyColumn=False).fetch()]
        elif recipient_id:
            records = [{'recipient_id':recipient_id,'calendar_id':r['id']} for r in self.db.table('mow.calendar').query(columns='$id',addPkeyColumn=False,where='$date>=:env_workdate').fetch()]
        if records:
            self.insertMany(records)