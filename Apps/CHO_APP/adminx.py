# -*- coding: utf-8 -*-

import xadmin

from .models import UserProject, LeadeWho, VoteWho, LeaderVote


class UserProjectAdmin(object):
    pass


class LeadeWhoAdmin(object):
    pass


class VoteWhoAdmin(object):
    pass


class LeaderVoteAdmin(object):
    model_icon = 'fa fa-tachometer'
    pass

xadmin.site.register(UserProject, UserProjectAdmin)
xadmin.site.register(LeadeWho, LeadeWhoAdmin)
xadmin.site.register(VoteWho, VoteWhoAdmin)
xadmin.site.register(LeaderVote, LeaderVoteAdmin)
