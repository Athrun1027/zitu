# -*- coding: utf-8 -*-
from django.conf.urls import url

from USER_APP.views import RegisterPage, do_logout, ActiveView, ForgetView, ResetView, PersonView, PeopleView, NeedLogin

#注册及激活
urlpatterns = [
    url(r'^register/', RegisterPage.as_view(), name='register'),
    url(r'^active_get/(?P<active_code>.*)/$', ActiveView.as_view(), name='active_get'),
]

# 注销
urlpatterns += [
    url(r'^out/$', do_logout, name='logout'),
]

# 忘记密码及重置密码
urlpatterns += [
    url(r'^forget/$', ForgetView.as_view(), name='forget'),
    url(r'^reset_get/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_get'),
    url(r'^reset_post/$', ResetView.as_view(), name='reset_post'),
]

# 个人中心
urlpatterns += [
    url(r'^person/$', PersonView.as_view(), name='person'),
    url(r'^people/$', PeopleView.as_view(), name='people'),
    url(r'^needlogin/$', NeedLogin.as_view(), name='needlogin'),
]

