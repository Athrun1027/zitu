# -*- coding: utf-8 -*-

import xadmin

from .models import Mailbox, Friends, Message, Leader
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = u"自途网后台"
    site_footer = u"自途网后台管理系统"
    menu_style = "accordion"


class MailboxAdmin(object):
    model_icon = 'fa fa-envelope'
    pass


class FriendsAdmin(object):
    model_icon = 'fa fa-users'
    list_display = ['username', 'friend']
    search_fields = ['username__username', 'friend__username']
    list_filter = ['username', 'friend']


class LeaderAdmin(object):
    model_icon = 'fa fa-address-card-o'
    pass


class MessageAdmin(object):
    model_icon = 'fa fa-volume-up'
    pass


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Mailbox, MailboxAdmin)
xadmin.site.register(Leader, LeaderAdmin)
xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(Friends, FriendsAdmin)