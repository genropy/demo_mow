#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='Meals on wheels',sqlschema='mow',
                    name_short='MOW', name_long='Meals on wheels', name_full='Meals on wheels')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
