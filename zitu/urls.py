# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.static import serve

import xadmin
from captcha.urls import views

from USER_APP.views import IndexPage, TestPage
from django.conf import settings

#主页
urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index'),
    url(r'^test$', TestPage.as_view(), name='test'),
]

#后台管理
urlpatterns += [
    url(r'^admin/', xadmin.site.urls, name='root'),
]

# 验证码及其刷新
urlpatterns += [
    url(r'^captcha/', include('captcha.urls')),
    url(r'^refresh/$', views.captcha_refresh, name='refresh'),
]

# 各模块的划分
urlpatterns += [
    url(r'^user/', include('USER_APP.urls')),
    url(r'^project/', include('PRO_APP.urls')),
    url(r'^notice/', include('OPR_APP.urls')),
]

#错误页面处理
handler404 = 'USER_APP.views.page_not_found'
handler500 = 'USER_APP.views.server_errors'

#静态文件处理
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]
if not settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ]
