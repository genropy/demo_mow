#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):
    css_requires='mow'

    def th_hiddencolumns(self):
        return '$date'

    def th_struct(self,struct):
        r = struct.view().rows()
        columns='$meal_name,$option,$_row_count'
        r.fieldcell('calendar_id',edit=dict(condition='$date>=:env_workdate',hasDownArrow=True),width='10em')
        r.fieldcell('starter_id',edit=dict(condition='@meal_id.@meal_calendars.calendar_id=:c_id AND $meal_type=:t',
                                        condition_c_id='=.calendar_id',condition_t='1',hiddenColumns=columns),width='30em',cellClasses='row_starter')
        r.fieldcell('main_course_id',edit=dict(condition='@meal_id.@meal_calendars.calendar_id=:c_id AND $meal_type=:t',
                                        condition_c_id='=.calendar_id',condition_t='2',hiddenColumns=columns),width='30em',cellClasses='row_main_course')
        r.fieldcell('dessert_id',edit=dict(condition='@meal_id.@meal_calendars.calendar_id=:c_id AND $meal_type=:t',
                                        condition_c_id='=.calendar_id',condition_t='3',hiddenColumns=columns),width='30em',cellClasses='row_dessert')

    def th_order(self):
        return 'date'

    def th_top_upperslotbar(self,top):
        top.bar.replaceSlots('vtitle','sections@period')
    
    def th_sections_period(self):
        return [dict(code='past',caption='!!Past',condition="$date <:env_workdate",condition_p='past'),
                dict(code='week',caption='!!Week 1',condition="#PERIOD($date,:p)",condition_p='today;today+7',isDefault=True),
                dict(code='2_week',caption='!!Week 2',condition="#PERIOD($date,:p)",condition_p='today+8;today+14'),
                dict(code='all',caption='!!All')]


class ViewFromStaffCalendar(BaseComponent):
    css_requires='mow'
   
    def th_hiddencolumns(self):
        return '$date,$recipient_rcount'

    def th_order(self):
        return 'recipient_rcount'

    def th_struct(self,struct):
        r = struct.view().rows()
        columns='$meal_name,$option,$_row_count'
        r.fieldcell('recipient_rcount',width='3em')
        r.fieldcell('recipient_id',width='15em')
        r.fieldcell('starter_id',edit=dict(condition='@meal_id.@meal_calendars.calendar_id=:c_id AND $meal_type=:t',
                                        condition_c_id='=#FORM.record.id',condition_t='1',hasDownArrow=True,hiddenColumns=columns),width='30em',
                                        cellClasses='row_starter')
        r.fieldcell('main_course_id',edit=dict(condition='@meal_id.@meal_calendars.calendar_id=:c_id AND $meal_type=:t',
                                        condition_c_id='=#FORM.record.id',condition_t='2',hasDownArrow=True,hiddenColumns=columns),width='30em',cellClasses='row_main_course')
        r.fieldcell('dessert_id',edit=dict(condition='@meal_id.@meal_calendars.calendar_id=:c_id AND $meal_type=:t',
                                        condition_c_id='=#FORM.record.id',condition_t='3',hiddenColumns=columns,
                                        hasDownArrow=True),width='30em',cellClasses='row_dessert')

class ViewFromMeal(BaseComponent):
    css_requires='mow'
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('recipient_id',width='20em')
        r.fieldcell('@recipient_id.address_street',width='30em',name='Address')
        r.fieldcell('@starter_id.option',width='20em',name='Option',hidden=True)
        r.fieldcell('@main_course_id.option',width='20em',name='Option',hidden=True)
        r.fieldcell('@dessert_id.option',width='20em',name='Option',hidden=True)
        
        r.cell('_option',width='20em',name='Option',calculated=True,
                _customGetter="""function(row,idx){
                    genro.bp(true);
                    var ct = this.grid.sourceNode._current_type;
                    if(ct=='1'){
                        return row['_starter_id_option']
                    }else if(ct=='2'){
                        return row['_main_course_id_option']
                    }else{
                        return row['_dessert_id_option']
                    }
                }""")


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('recipient_id')
        fb.field('calendar_id')
        fb.field('starter_id')
        fb.field('main_course_id')
        fb.field('dessert_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
