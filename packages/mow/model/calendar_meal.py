#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('calendar_meal', pkey='id', name_long='!!Calendar meal', name_plural='!!Calendar meals')
        self.sysFields(tbl)
        tbl.column('calendar_id',size='22' ,group='_',name_long='!!Calendar').relation('calendar.id',relation_name='calendar_meals',mode='foreignkey',onDelete='cascade')
        tbl.column('meal_id',size='22' ,group='_',name_long='!!Meal').relation('meal.id',relation_name='meal_calendars',mode='foreignkey',onDelete='cascade')
        tbl.aliasColumn('meal_type','@meal_id.type',name_long='Meal type')
        tbl.aliasColumn('meal_name','@meal_id.name',name_long='Meal name')
        tbl.formulaColumn('recipient_count',select=dict(columns='COUNT(*)',
                                                        table='mow.recipient_calendar',
                                                        where="""$calendar_id=#THIS.calendar_id AND 
                                                                (@starter_id.meal_id=#THIS.meal_id OR 
                                                                @main_course_id.meal_id=#THIS.meal_id OR
                                                                @dessert_id.meal_id=#THIS.meal_id)"""),
                        dtype='I',name_long='Rec.Count')
        tbl.aliasColumn('date','@calendar_id.date',name_long='Date',dtype='D')
