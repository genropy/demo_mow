#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name_full',width='30em')
        r.fieldcell('age',width='4em')
        r.fieldcell('gender',width='4em')
        r.fieldcell('address_street',width='40em')
        r.fieldcell('phone',width='15em')
        r.fieldcell('mobile',width='15em')
        r.fieldcell('assigned_to',width='15em')

    def th_order(self):
        return 'name_full'

    def th_query(self):
        return dict(column='name_full', op='contains', val='')


class ViewFromStaff(BaseComponent):
    def th_hiddencolumns(self):
        return '$geocoords,$name_full'
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count',counter=True)
        r.fieldcell('template_recipient',width='40em')

    def th_order(self):
        return '_row_count'




class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()

        self.form_recipient(bc.contentPane(region='top',datapath='.record'),assigned_to=True)
        tc = bc.tabContainer(region='center',margin='2px')
        self.rec_calendarPane(tc.contentPane(title='Calendar'))
        self.notesPane(tc.contentPane(title='Notes'))

    def form_recipient(self,pane,assigned_to=None):
        fb = pane.div(margin_right='20px').formbuilder(cols=4, border_spacing='6px',colswidth='auto',width='600px',fld_width='100%')
        fb.field('name_first',validate_case='c')
        fb.field('name_last',colspan=2,validate_case='c')
        fb.img(src='^.photo_url',crop_width='120px',crop_height='120px',
                        placeholder=self.getResourceUri('images/missing_photo.png'),
                        upload_folder='site:img/card/avatar',edit=True,
                        upload_filename='=#FORM.record.id',
                        crop_border='2px solid #ddd',
                        crop_rounded=8,crop_margin='5px',
                        crop_margin_left='10px',
                        zoomWindow=True,
                        rowspan=7)
        fb.field('salutation',width='5em')
        fb.field('dob',width='7em')
        fb.field('gender',width='5em')
        fb.field('full_address', tag='geoCoderField',
                     colspan=3,
                     lbl='Geocoder',
                     selected_street_address_eng='.street',
                     selected_locality='.suburb',
                     selected_postal_code='.postcode',
                     selected_administrative_area_level_1 ='.state',
                     selected_country='.country',
                     selected_position='.geocoords',
                     country='=.country',
                     #selectedRecord='#FORM.record.addressbag',
                     ghost='Nr Street Suburb State Postcode',
                     speech=True)        
        fb.field('street',colspan=3)
        fb.field('suburb',cospan=2)
        fb.field('state')
        fb.field('postcode')
        fb.field('country',cospan=2)
        fb.field('phone')
        fb.field('mobile')
        fb.field('email',colspan=2 if assigned_to else 3)
        if assigned_to:
            fb.field('assigned_to',validate_notnull=True)

    def rec_calendarPane(self,pane):
        pane.inlineTableHandler(relation='@recipient_calendar_items',addrow=False,delrow=False)

    def notesPane(self,pane):
        pane.simpleTextArea('^.record.general_notes',editor=True)

    def th_options(self):
        return dict(dialog_height='500px', dialog_width='650px')

    @public_method
    def th_onLoading(self,record, newrecord, loadingParameters, recInfo):
        if newrecord:
            record['id'] = self.db.table('mow.staff').newPkeyValue()


class FormFromStaff(Form):
    def th_form(self, form):
        pane = form.record
        pane.div(height='20px')
        self.form_recipient(pane,assigned_to=False)


    def th_options(self):
        return dict(dialog_height='280px', dialog_width='650px')

