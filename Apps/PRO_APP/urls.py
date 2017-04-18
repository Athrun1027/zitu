# -*- coding: utf-8 -*-
from django.conf.urls import url

from PRO_APP.views import AllProjectPage, StartProjectPage, ModelProjectPage, LoadingProjectPage

#查看所有景点
urlpatterns = [
    url(r'^all_pro/', AllProjectPage.as_view(), name='all_pro'),
    url(r'^start_pro/', StartProjectPage.as_view(), name='start_pro'),
    url(r'^model_pro/(?P<pro_id>.*)/$', ModelProjectPage.as_view(), name='model_pro'),
    url(r'^loading_pro/(?P<pro_id>.*)/$', LoadingProjectPage.as_view(), name='loading_pro'),
]
