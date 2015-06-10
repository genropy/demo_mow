#!/usr/bin/env python
# encoding: utf-8
def config(root,application=None):
    main_menu = root.branch(u"Main Menu", tags="staff")
    main_menu.thpage(u"!!Calendar", table="mow.calendar")
    main_menu.thpage(u"!!Recipients", table="mow.recipient")
    main_menu.thpage(u"!!Staff", table="mow.staff")
    configuration = root.branch(u"Configuration", tags="staff")
    configuration.thpage(u"!!Meals", table="mow.meal")
    configuration.thpage(u"!!Options", lookup_manager="mow.option")
    administrator = configuration.branch(u"!!Administrator", tags="admin")
    administrator.webpage(u"!!Users", filepath="/adm/user_page")
    administrator.thpage(u"!!Tags", table="adm.htag")
