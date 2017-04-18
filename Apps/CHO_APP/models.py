# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from USER_APP.models import MyUsers, Leader
from PRO_APP.models import Projects
# Create your models here.


class UserProject(models.Model):
    username = models.ForeignKey(MyUsers, verbose_name=u"用户", on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, verbose_name=u"项目", on_delete=models.CASCADE)
    done = models.BooleanField(default=0, verbose_name=u"是否完成")
    feel = models.IntegerField(default=0, verbose_name=u"用户游玩感受级别")
    words = models.TextField(verbose_name=u"用户游玩感受内容")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户项目参与表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.username.username, self.project.name)


class LeadeWho(models.Model):
    project = models.ForeignKey(Projects, verbose_name=u"项目", on_delete=models.CASCADE)
    username = models.ForeignKey(MyUsers, verbose_name=u"导游", on_delete=models.CASCADE)
    done = models.BooleanField(default=0, verbose_name=u"是否接受")
    time_do = models.DateTimeField(verbose_name=u"接受时间")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"参团推荐导游表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.project.name, self.abc.username)


class VoteWho(models.Model):
    username = models.ForeignKey(
        MyUsers,
        verbose_name=u"用户",
        related_name="user_username",
        on_delete=models.CASCADE
    )
    leader = models.ForeignKey(
        MyUsers,
        verbose_name=u"导游",
        related_name="user_leader",
        on_delete=models.CASCADE
    )
    done = models.BooleanField(default=0, verbose_name=u"是否接受投票结果")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"投票时间")

    class Meta:
        verbose_name = u"游客投票表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.username.username, self.leader.username)


class LeaderVote(models.Model):
    leader = models.ForeignKey(Leader, verbose_name=u"导游", on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, verbose_name=u"项目", on_delete=models.CASCADE)
    counter = models.IntegerField(default=0, verbose_name=u"票数")
    words = models.TextField(default=u"", verbose_name=u"拉票内容")
    done_one = models.BooleanField(default=0, verbose_name=u"是否为最终导游")
    done_two = models.BooleanField(default=0, verbose_name=u"是否为后备导游")
    time_in = models.DateTimeField(default=datetime.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"导游计票表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}---{1}'.format(self.leader.leader.username, self.counter)

