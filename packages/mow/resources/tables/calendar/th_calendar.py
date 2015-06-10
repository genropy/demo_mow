#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):
    css_requires='mow'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('date',width='8em')
        r.fieldcell('starters',width='20em',cellClasses='row_starter')
        r.fieldcell('main_courses',width='20em',cellClasses='row_main_course')
        r.fieldcell('desserts',width='20em',cellClasses='row_dessert')
        r.fieldcell('notes',width='20em')

    def th_order(self):
        return 'date'

    def th_query(self):
        return dict(column='main_courses', op='contains', val='',runOnStart=True)

    def th_sections_period(self):
        return [dict(code='past',caption='!!Past',condition="$date <:env_workdate",condition_p='past'),
                dict(code='week',caption='!!Week 1',condition="#PERIOD($date,:p)",condition_p='today;today+7',isDefault=True),
                dict(code='2_week',caption='!!Week 2',condition="#PERIOD($date,:p)",condition_p='today+8;today+14'),
                dict(code='next_month',caption='!!Week 3',condition="#PERIOD($date,:p)",condition_p='today+15;today+21'),
                dict(code='all',caption='!!All')]

    def th_top_upperslotbar(self,top):
        top.slotToolbar('5,sections@period,*',childname='upper',_position='<bar',gradient_from='#999',gradient_to='#666')

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top',datapath='.record').formbuilder(cols=2, border_spacing='4px')
        fb.field('date')
        fb.field('notes')
        self.mealGrid(bc.contentPane(region='center'))
        self.recipientCalendarGrid(bc.contentPane(region='bottom',height='50%',splitter=True))

    def mealGrid(self,pane):
        pane.plainTableHandler(relation='@calendar_meals',picker='meal_id',picker_viewResource='ViewPicker',
                                pbl_classes=True,margin='2px',
                                addrow=False,
                                view_grid_canSort=False,
                                grid_rowCustomClassesCb="""function(row){
                                                                    return {'1':'row_starter','2':'row_main_course','3':'row_dessert'}[row['meal_type']]
                                                                }""")


    def recipientCalendarGrid(self,pane):
        th = pane.inlineTableHandler(relation='@recipient_calendar_items',
                                condition='@recipient_id.assigned_to=:at',
                                condition_at='^#FORM.currentStaffId',
                                view_store__if='at',
                                pbl_classes=True,margin='2px',
                                viewResource='ViewFromStaffCalendar',
                                view_loadingHider=False,title='Recipients',
                                addrow=False,delrow=False,autoSave=True,export=True,
                                view_grid_canSort=False,
                                searchOn=False)
        bar = th.view.top.bar.replaceSlots('vtitle','vtitle,10,staffselector')
        fb = bar.staffselector.formbuilder(cols=1,border_spacing='0')
        fb.dbSelect(value='^#FORM.currentStaffId',lbl='Staff',hasDownArrow=True,dbtable='mow.staff')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormStaffRecipient(BaseComponent):
    def th_options(self):
        return dict(showtoolbar=False)

    def th_form(self, form):
        pane = form.center.contentPane()
        pane.inlineTableHandler(relation='@recipient_calendar_items',
                                condition='@recipient_id.assigned_to=:at',
                                condition_at='=#FORM/parent/#FORM.record.id',
                                pbl_classes=True,margin='2px',
                                viewResource='ViewFromStaffCalendar',
                                view_loadingHider=False,
                                addrow=False,delrow=False,autoSave=True)


