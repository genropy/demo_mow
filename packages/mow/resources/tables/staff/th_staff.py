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

    def th_order(self):
        return 'name_full'

    def th_query(self):
        return dict(column='name_full', op='contains', val='')

class Form(BaseComponent):
    def th_form(self, form):
        tc = form.center.tabContainer()
        self.personalData(tc.contentPane(title='Personal Data',datapath='.record'))
        self.recipientPane(tc.borderContainer(title='Assigned Recipients'))
        self.staff_calendarPane(tc.contentPane(title='Calendar'))

    def personalData(self,pane):                                            
        fb = pane.div(margin_right='20px').formbuilder(cols=4, border_spacing='4px',colswidth='auto',width='750px',fld_width='100%')
        fb.field('name_first',validate_case='c')
        fb.field('name_last',colspan=2,validate_case='c')
        fb.img(src='^.photo_url',crop_width='120px',crop_height='120px',
                        placeholder=self.getResourceUri('images/missing_photo.png'),
                        upload_folder='site:img/card/avatar',edit=True,
                        upload_filename='=#FORM.record.id',crop_border='2px solid #ddd',crop_rounded=8,crop_margin='5px',
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
        fb.field('email',colspan=3,width='100%')
        fb.field('general_notes',editor=True,height='150px',colspan=4)

    def recipientPane(self,bc):
        left = bc.contentPane(region='left',width='50%')
        th = left.dialogTableHandler(relation='@recipients',nodeId='recipientInStaff',
                            margin='2px',
                            viewResource='ViewFromStaff',
                            formResource='FormFromStaff',
                            view_grid_selfDragRows=True,
                            view_grid_canSort=False,
                            pbl_classes='*',configurable=False)
        center = bc.contentPane(region='center',overflow='hidden',_lazyBuild=True)
        m = center.GoogleMap(position='absolute',top=0,left=0,right=0,bottom=0,
                     map_type='roadmap',
                     nodeId='gma',
                     autoFit=True,
                     #map_zoom=15
                    # map_disableDefaultUI=True,
                     )
        url = self.getResourceUri('markerwithlabel','js',add_mtime=True)
        m.dataController("""genro.dom.loadJs(url,function(){
                m.gnr.addMarkerType('with_label',MarkerWithLabel);
            });""", url=url,_onBuilt=True,m=m)

        th.view.dataController("""if(!m.map){
                                        return;
                                    }
                              m.gnr.clearMarkers(m);
                              var that = this;
                               store.forEach(function(n){
                                    m.gnr.setMarker(m,n.attr._pkey,n.attr.geocoords,{title:n.attr.name_full,
                                                                                    marker_type:'with_label',
                                                                                    labelContent:n.attr._row_count,
                                                                                    labelAnchor: new google.maps.Point(15, 0),
                                                                                    labelClass: "markerlabel", // the CSS class for the label
                                                                                    
                                                                                    });
                              },'static');
                             """,m=m,store='=.store',
                                 _fired='^#FORM.refreshMap',_delay=100)
        th.view.dataController("""
            FIRE #FORM.refreshMap;
             """,store='^.store')
       
    @public_method
    def th_onLoading(self,record, newrecord, loadingParameters, recInfo):
        if newrecord:
            record['id'] = self.db.table('mow.staff').newPkeyValue()

    def staff_calendarPane(self,pane):
        pane.multiButtonForm(frameCode='calendar',datapath='#FORM.calendar',
                            table='mow.calendar',
                            caption='date',
                            formResource='FormStaffRecipient',
                            condition='#PERIOD($date,:p)',
                            condition_p='today;today+7',
                            multibutton_caption_dtype='D',
                            store__fired='^#FORM.controller.loaded',
                            store_liveUpdate=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
