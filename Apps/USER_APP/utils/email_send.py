#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# __author__ = "Athrun Xu"
# __date__ = "2017/3/6 下午11:51"
from random import Random
from ..models import Mailbox
from django.core.mail import send_mail
from zitu.settings import EMAIL_FROM


def random_code(random_length=8):
    '''
        生成随机验证码
        '''
    str_string = ''
    chars = "ABCDEFGHIJKLMNOPQRSTUYWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    length = len(chars)-1
    random = Random()

    for i in range(random_length):
        str_string += chars[random.randint(0, length)]
    return str_string


def send_to(email, send_type="register"):
    '''
        发送邮件处理，默认16位的随机数
        '''
    random_email = Mailbox()
    random_email.email = email
    random_email.style = send_type
    code = random_code(16)
    random_email.code = code
    random_email.save()

    if send_type == "register":
        '''
            注册激活验证
            '''
        email_title = "自途网注册激活链接"
        email_body = "请点击下面的链接完成注册：http://zitu.athrun.org/user/active_get/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status == 1:
            return email
        else:
            return None
    else:
        '''
            修改密码验证
            '''
        email_title = "自途网密码重置链接"
        email_body = "请点击下面的链接完成重置：http://zitu.athrun.org/user/reset_get/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status == 1:
            return email
        else:
            return None
