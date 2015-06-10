#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('staff', pkey='id', name_long='!!Staff', name_plural='!!Staff',caption_field='name_full')
        self.sysFields(tbl)
        tbl.column('name_first' ,size=':40',name_long='!!Name first')
        tbl.column('name_second', size=':30',name_long='!!Middle name')
        tbl.column('name_last', size=':40',name_long='!!Last name', indexed=True)
        tbl.column('salutation', size=':10',name_long='!!Salutation',group='a_names.06',values='Mr:Mr,Ms:Ms,Miss:Miss,Mrs:Mrs,Dr:Dr,Prof:Prof') #use dbCombo
        tbl.column('dob','D',name_long='!!Date of Birth', name_short='DOB',group='x_other.01',wdg_pivotYear=1,_sendback=True)
        tbl.formulaColumn('age', "extract(YEAR FROM age($dob))", dtype='L', name_long='!!Age', group='x_other.02')
        tbl.column('gender', size='1',name_long='!!Gender', group='x_other.03',_sendback=True,values='M:Male,F:Female:U:Unknown')

        tbl.column('full_address',name_long='!!Geocoder Address',group='b_addresses.00')
        tbl.column('street',name_long='!!Street',group='b_addresses.01') #validate_regex='![?]{2,2}', validate_regex_error='!!Missing street number')
        tbl.column('suburb', size=':50',name_long='!!Suburb',group='b_addresses.02')
        tbl.column('state', name_long='!!State', indexed=True, group='b_addresses.03',validate_case='UPPER')
        tbl.column('postcode', name_long='!!Postcode',group='b_addresses.04')
        tbl.column('country', size=':2',name_long='!!Country',group='b_addresses.05',default='AU')
        tbl.column('geocoords', name_long='!!Geocoder coords',group='_')


        tbl.column('photo_url', dtype='P',name_long='!!Photo URL')

        tbl.formulaColumn('name_full',"""COALESCE($name_first,'') || ' ' || COALESCE($name_last,'')
                                         """,name_long='Full Name', group='a_names.01')
        tbl.formulaColumn('address_street',"""COALESCE($street,'')  ||' '|| COALESCE($suburb,'')  ||' '|| COALESCE($state,'') ||' '|| COALESCE($postcode,'')""",
                        name_long='!!Full address') 
        tbl.column('general_notes',name_long='!!General Notes')
        tbl.column('phone',indexed=True,name_long='!!Phone')
        tbl.column('mobile',indexed=True,name_long='!!Mobile')
        tbl.column('email',indexed=True,name_long='!!Email')