# -*- coding: utf-8 -*-
from django.conf.urls import url

from OPR_APP.views import NoticeView, InformView, FooterView, LeaderView, ProjectingView, BuyView

#查看所有景点
urlpatterns = [
    url(r'^inform/$', InformView.as_view(), name='inform'),
    url(r'^footer/$', FooterView.as_view(), name='footer'),
    url(r'^leader/$', LeaderView.as_view(), name='leader'),
    url(r'^projecting/$', ProjectingView.as_view(), name='projecting'),
    url(r'^buy/$', BuyView.as_view(), name='buy'),
    url(r'^$', NoticeView.as_view(), name='notice'),
]
