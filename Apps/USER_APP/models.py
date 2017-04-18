# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

from datetime import datetime

# Create your models here.


class MyUsers(AbstractUser):
    objects = UserManager()
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default=u"")
    job = models.CharField(max_length=50, verbose_name=u"职业", default=u"")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(
        verbose_name=u"性别",
        choices=(("male", u"男"), ("female", u"女")),
        default="female",
        max_length=6
    )
    count = models.IntegerField(verbose_name=u"参团次数", default=0)
    identity = models.CharField(verbose_name=u"身份证", max_length=50, default=u"")
    address = models.CharField(max_length=100, verbose_name=u"地址", default=u"")
    mobile = models.CharField(max_length=11, verbose_name=u"联系方式", default=u"")
    baduser = models.BooleanField(default=0, verbose_name=u"是否拉黑")
    leader = models.BooleanField(default=0, verbose_name=u"是否导游")
    integral = models.IntegerField(default=0, verbose_name=u"积分")
    balance = models.IntegerField(default=0, verbose_name=u"余额")
    image = models.ImageField(
        upload_to="image/%Y/%m",
        verbose_name=u"头像",
        default=u"image/default.jpg",
        max_length=200
    )

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class Mailbox(models.Model):
    email = models.EmailField(verbose_name=u"邮箱")
    style = models.CharField(
        verbose_name=u"类型",
        choices=(("password", u"修改密码"), ("register", u"注册")),
        default="register",
        max_length=8
    )
    active = models.BooleanField(verbose_name=u"已经使用", default=0)
    code = models.CharField(verbose_name=u"验证码", max_length=50, default=u"")
    time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}--{1}--{2}'.format(self.email, self.style, self.time)


class Friends(models.Model):
    username = models.ForeignKey(
        MyUsers,
        verbose_name=u"用户名称",
        related_name="user_mine",
        on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        MyUsers,
        verbose_name=u"好友名称",
        related_name="user_friend",
        on_delete=models.CASCADE
    )
    time_get = models.DateTimeField(default=datetime.now, verbose_name=u"同意时间",)
    passed = models.BooleanField(default=0, verbose_name=u"是否通过")
    time_sent = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"用户好友资源表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}--{1}'.format(self.username, self.friend)


class Message(models.Model):
    sender = models.ForeignKey(MyUsers, verbose_name=u"发送者名称", related_name="user_sender", on_delete=models.CASCADE)
    receive = models.ForeignKey(MyUsers, verbose_name=u"接收者名称", related_name="user_receive", on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"消息内容", default=u"")
    time_sent = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")
    passed = models.BooleanField(default=0, verbose_name=u"是否查看")
    reply = models.BooleanField(default=0, verbose_name=u"是否回复")
    send_all = models.BooleanField(default=0, verbose_name=u"是否群发")

    class Meta:
        verbose_name = u"用户消息表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}--{1}'.format(self.sender, self.receive)


class Leader(models.Model):
    leader = models.ForeignKey(MyUsers, verbose_name=u"用户名称", related_name="user_leaders", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"成为导游时间")
    short = models.CharField(max_length=300, verbose_name=u"简介", default=u"")
    count = models.IntegerField(default=0, verbose_name=u"导游积分")
    times = models.IntegerField(default=0, verbose_name=u"开团次数")

    class Meta:
        verbose_name = u"导游信息表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.leader.username