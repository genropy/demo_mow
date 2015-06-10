#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('calendar', pkey='id', name_long='!!Calendar', name_plural='!!Calendar',
                        caption_field='date',order_by='$date')
        self.sysFields(tbl)
        tbl.column('date',dtype='D',name_long='!!Date',unique=True,indexed=True)
        tbl.column('notes',name_long='!!Notes')

        tbl.formulaColumn('starters',"array_to_string(ARRAY(#m),'<br/>')||'<br/><br/>'",
                            select_m=dict(table='mow.calendar_meal',where='$calendar_id=#THIS.id AND $meal_type=:ct',
                            ct='1',columns='$meal_name'),name_long='Starters')
        tbl.formulaColumn('main_courses',"array_to_string(ARRAY(#m),'<br/>')||'<br/><br/>'",
                            select_m=dict(table='mow.calendar_meal',where='$calendar_id=#THIS.id AND $meal_type=:ct',
                            ct='2',columns='$meal_name'),name_long='Main courses')
        tbl.formulaColumn('desserts',"array_to_string(ARRAY(#m),'<br/>') ||'<br/><br/>'",
                            select_m=dict(table='mow.calendar_meal',where='$calendar_id=#THIS.id AND $meal_type=:ct',
                            ct='2',columns='$meal_name'),name_long='Desserts')

    def trigger_onInserted(self,record):
        self.db.table('mow.recipient_calendar').alignCalendar(calendar_id=record['id'])

