# -*- coding: utf-8 -*-

import xadmin

from .models import Projects, Plan, TimeLimit, Analysis


class PlanInline(object):
    model = Plan
    extra = 0


class ProjectsAdmin(object):
    inlines = [PlanInline]
    list_display = ['ID', 'name', 'status', 'num_click', 'price', 'style']
    list_editable = ['price', 'style', 'status']
    refresh_times = [3, 5]
    pass


class PlanAdmin(object):
    pass


class TimeLimitAdmin(object):
    list_display = ['style', 'time_end']
    list_editable = ['time_end']
    pass


class AnalysisAdmin(object):
    model_icon = 'fa fa-globe'
    pass

xadmin.site.register(Projects, ProjectsAdmin)
xadmin.site.register(Plan, PlanAdmin)
xadmin.site.register(TimeLimit, TimeLimitAdmin)
xadmin.site.register(Analysis, AnalysisAdmin)