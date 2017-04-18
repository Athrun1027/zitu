# -*- coding: utf-8 -*-

import xadmin

from .models import LeaderFiles, UserMoney, UserClick, UserAsk, Carousel


class LeaderFilesAdmin(object):
    pass


class UserMoneyAdmin(object):
    pass


class UserClickAdmin(object):
    pass


class UserAskAdmin(object):
    pass


class CarouselAdmin(object):
    model_icon = 'fa fa-gavel'
    pass

xadmin.site.register(LeaderFiles, LeaderFilesAdmin)
xadmin.site.register(UserMoney, UserMoneyAdmin)
xadmin.site.register(UserClick, UserClickAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Carousel, CarouselAdmin)
