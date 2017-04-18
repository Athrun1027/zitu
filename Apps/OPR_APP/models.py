# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from USER_APP.models import MyUsers
from PRO_APP.models import Projects
# Create your models here.


class LeaderFiles(models.Model):
    username = models.ForeignKey(MyUsers, verbose_name=u"导游", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"文件名")
    words = models.CharField(max_length=200, verbose_name=u"文件描述")
    file = models.FileField(
        upload_to="file/%Y/%m",
        verbose_name=u"文件",
        default=u"file/default.txt",
        max_length=100
    )
    done = models.BooleanField(default=0, verbose_name=u"是否通过")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"导游资料审核表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.username.username, self.name)


class UserMoney(models.Model):
    username = models.ForeignKey(MyUsers, verbose_name=u"导游", on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, verbose_name=u"项目", on_delete=models.CASCADE)
    money_part = models.FloatField(default=0.0, verbose_name=u"已缴纳金额")
    money_left = models.FloatField(default=0.0, verbose_name=u"未缴纳金额")
    done = models.BooleanField(default=0, verbose_name=u"是否完成支付")
    time_do = models.DateTimeField(default=datetime.now, verbose_name=u"完成支付时间")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户购买项目表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.username.username, self.money_left)


class UserClick(models.Model):
    username = models.ForeignKey(MyUsers, verbose_name=u"导游", on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, verbose_name=u"项目", on_delete=models.CASCADE)
    click = models.IntegerField(default=0, verbose_name=u"用户点击数")
    like = models.BooleanField(default=0, verbose_name=u"是否关注")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"触发时间")

    class Meta:
        verbose_name = u"用户浏览项目记录表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.username.username, self.project.name)


class UserAsk(models.Model):
    username = models.ForeignKey(MyUsers, verbose_name=u"导游", on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, verbose_name=u"类似项目", on_delete=models.CASCADE)
    words = models.TextField(default=u"", verbose_name=u"拉票内容")
    done = models.BooleanField(default=0, verbose_name=u"是否通过")
    time_do = models.DateTimeField(default=datetime.now, verbose_name=u"处理时间")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"推荐开设项目表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username.username


class Carousel(models.Model):
    project = models.CharField(default='#', verbose_name=u"轮播图URL", max_length=100)
    image = models.ImageField(
        upload_to="Carousel/%Y/%m",
        verbose_name=u"轮播图",
        default=u"image/carousel.jpg",
        max_length=100
    )
    title = models.CharField(verbose_name=u"公告标题", default=u"", max_length=50)
    content = models.TextField(verbose_name=u"公告内容", default=u"")
    index = models.IntegerField(default=0, verbose_name=u"序号")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"轮播图表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.project, self.index)

