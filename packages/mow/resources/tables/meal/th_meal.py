#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):
    css_requires='mow'
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('type')
        r.fieldcell('name')
        r.fieldcell('description',width='40em')

    def th_order(self):
        return 'type,name'

    def th_view(self,view):
        view.grid.attributes.update(rowCustomClassesCb="""function(row){
                                                                    return {'1':'row_starter','2':'row_main_course','3':'row_dessert'}[row['type']]
                                                                }""")

    def th_query(self):
        return dict(column='name', op='contains', val='',runOnStart=True)

    def th_top_upperslotbar(self,top):
        top.slotToolbar('5,sections@type,*',sections_type_all_end=True,
                    childname='upper',_position='<bar',gradient_from='#999',gradient_to='#666')



class ViewPicker(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('id', hidden=True)
        r.fieldcell('type', hidden=True)
        r.fieldcell('name', width='100%')

    def th_order(self):
        return 'type,name'
        
    def th_top_upperslotbar(self,top):
        top.slotToolbar('5,sections@type,*',childname='upper',_position='<bar',gradient_from='#999',gradient_to='#666',
                                    sections_type_all_end=True)

    def th_view(self,view):
        view.grid.attributes.update(rowCustomClassesCb="""function(row){
                                                                    return {'1':'row_starter','2':'row_main_course','3':'row_dessert'}[row['type']]
                                                                }""")

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.mealTopForm(bc.borderContainer(region='top',height='180px'))
        self.mealCalendar(bc.borderContainer(region='center'))

    def mealCalendar(self,bc):
        left = bc.contentPane(region='left',width='280px')
        th = left.plainTableHandler(relation='@meal_calendars',viewResource='ViewFromMeal',
                                condition='$date>=:env_workdate',pbl_classes=True,margin='2px',
                                configurable=False)
        th.view.grid.dataFormula('#FORM.selectedCalendarId','calendar_id',calendar_id='^.selectedId?calendar_id')
        th = bc.contentPane(region='center').plainTableHandler(table='mow.recipient_calendar',viewResource='ViewFromMeal',
                                condition='$calendar_id=:cid AND (@starter_id.meal_id=:mid OR @main_course_id.meal_id=:mid OR @dessert_id.meal_id=:mid)',
                                condition_cid='^#FORM.selectedCalendarId',
                                condition_mid='=#FORM.record.id',
                                pbl_classes=True,margin='2px')
        th.view.grid.dataController('grid._current_type=type',
                                    type='^#FORM.record.type',grid=th.view.grid)

    def mealTopForm(self,bc):
        left = bc.roundedGroup(region='left',datapath='.record',title='Info',width='600px')
        fb =left.formbuilder(cols=2, border_spacing='4px')
        fb.field('type',width='10em')
        fb.field('name',width='20em')
        fb.field('description',tag='simpleTextArea',width='100%',colspan=2)
        bc.contentPane(region='center').inlineTableHandler(relation='@options',pbl_classes='*',viewResource='ViewEditable',
                                                                view_grid_selfDragRows=True,margin='2px',searchOn=False)
        bc.roundedGroup(region='right',title='Photo',width='180px').img(src='^#FORM.record.photo_url',crop_width='140px',crop_height='140px',
                        placeholder=self.getResourceUri('images/missing_image.png'),
                        upload_folder='site:img/card/avatar',edit=True,
                        upload_filename='=#FORM.record.id',crop_border='2px solid #ddd',crop_rounded=8,crop_margin='5px',
                        zoomWindow=True)
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

    @public_method
    def th_onLoading(self,record, newrecord, loadingParameters, recInfo):
        if newrecord:
            record['id'] = self.db.table('mow.staff').newPkeyValue()

