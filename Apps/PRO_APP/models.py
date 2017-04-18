# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.


class Projects(models.Model):
    ID = models.AutoField(primary_key=True, verbose_name=u"项目ID")
    name = models.CharField(max_length=50, verbose_name=u"项目名", default=u"未命名")
    image = models.ImageField(
        upload_to="project/%Y/%m",
        verbose_name=u"项目首页图",
        default=u"image/project.jpg",
        max_length=100
    )
    description = models.CharField(verbose_name=u"项目描述", max_length=300, default=u"")
    something = models.TextField(verbose_name=u"项目详情", default=u"")
    last = models.IntegerField(default=0, verbose_name=u"项目耗时")
    style = models.CharField(
        verbose_name=u"类型",
        choices=(
            ("1", u"疆藏"),
            ("2", u"东北"),
            ("3", u"西北"),
            ("4", u"北方"),
            ("5", u"江浙沪"),
            ("6", u"南方"),
            ("7", u"欧洲"),
            ("8", u"非洲"),
            ("9", u"澳洲"),
            ("10", u"美洲"),
            ("11", u"亚洲"),
            ("12", u"异域风情")
        ),
        default="register",
        max_length=8
    )
    price = models.FloatField(default=0.0, verbose_name=u"价格")
    num_min = models.IntegerField(default=0, verbose_name=u"最低开团人数")
    num_max = models.IntegerField(default=0, verbose_name=u"最多人数")
    status = models.CharField(
        verbose_name=u"类型",
        choices=(
            ("0", u"模型团"),
            ("1", u"达到开团人数"),
            ("2", u"推荐导游中"),
            ("3", u"导游投票中"),
            ("4", u"投票结果确认"),
            ("5", u"正在旅游"),
            ("6", u"已经结束"),
        ),
        default=u"模型团",
        max_length=10
    )
    num_click = models.IntegerField(default=0, verbose_name=u"点击数")
    num_admire = models.IntegerField(default=0, verbose_name=u"关注数")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"项目基本信息表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.ID, self.name)


class Plan(models.Model):
    project = models.ForeignKey(Projects, verbose_name=u"项目名称", on_delete=models.CASCADE)
    day = models.IntegerField(default=0, verbose_name=u"第几天")
    place = models.CharField(max_length=100, verbose_name=u"地点", default=u"未命名")
    day_in = models.DateField(verbose_name=u"到达时间")
    day_out = models.DateField(verbose_name=u"离开时间")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"项目行程表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.project, self.day)


class TimeLimit(models.Model):
    style = models.CharField(
        verbose_name=u"时间类型",
        choices=(
            ("1", u"达到开团人数"),
            ("2", u"推荐导游中"),
            ("3", u"导游投票中"),
            ("4", u"投票结果确认"),
        ),
        default=u"模型团",
        max_length=10
    )
    time_start = models.DateTimeField(verbose_name=u"开始时间")
    time_end = models.DateTimeField(verbose_name=u"结束时间")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"项目截止日期表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.style


class Analysis(models.Model):
    project = models.ForeignKey(Projects, verbose_name=u"项目名称", on_delete=models.CASCADE)
    num_A = models.IntegerField(default=0, verbose_name=u"A人数")
    num_B = models.IntegerField(default=0, verbose_name=u"B人数")
    num_C = models.IntegerField(default=0, verbose_name=u"C人数")
    num_D = models.IntegerField(default=0, verbose_name=u"D人数")

    class Meta:
        verbose_name = u"项目分析表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project