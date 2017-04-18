# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django import forms

from captcha.fields import CaptchaField

from USER_APP.models import MyUsers, Mailbox, Message, Leader
from OPR_APP.models import Carousel, UserMoney, UserClick
from PRO_APP.models import Projects
from CHO_APP.models import LeaderVote
from .utils.email_send import send_to
from .utils.login import LoginRequired

# Create your views here.


class CustomBackend(ModelBackend):
    '''
        重载认证方法
        '''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = MyUsers.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterForm(forms.Form):
    '''
        邮箱注册表单验证
        '''
    email = forms.EmailField(required=True, min_length=4,  max_length=20)
    password = forms.CharField(required=True, min_length=5, max_length=20, widget=forms.PasswordInput)
    captcha = CaptchaField(error_messages={'invalid': u"验证码错误"})


class ForgetForm(forms.Form):
    '''
        忘记密码表单验证
        '''
    email = forms.EmailField(required=True, min_length=4,  max_length=20)


class LoginForm(forms.Form):
    '''
        账户登录表单验证
        '''
    username = forms.CharField(required=True, min_length=2, max_length=20)
    password = forms.CharField(required=True, min_length=5, max_length=20, widget=forms.PasswordInput)


def IndexGetData(request):
    form = RegisterForm()
    carousel = Carousel.objects.all()[:3]
    leader = Leader.objects.all().order_by('-count')[:2]
    project1 = Projects.objects.filter(style=7).order_by('-num_admire')[:2]
    project2 = Projects.objects.filter(Q(style=1) | Q(style=6)).order_by('-num_admire')[:4]
    project3 = Projects.objects.all().order_by('-num_admire')[:8]
    project4 = Projects.objects.filter(status='6').order_by('-num_admire')[:4]
    message = Message.objects.filter(receive=request.user.id)
    message_no = message.filter(passed=0).count()
    user_count = MyUsers.objects.all().count()
    index_dict = {
        'form': form,
        'carousel': carousel,
        'leader': leader,
        'user_count': user_count,
        'project1': project1,
        'project2': project2,
        'project3': project3,
        'project4': project4,
        'message_no': message_no,
    }
    return index_dict


class IndexPage(View):
    '''
        首页
        '''
    def get(self, request):
        '''
            首页GET
            '''
        index_dict = IndexGetData(request)
        return render(request, 'index.html', index_dict)

    def post(self, request):
        '''
            首页登录POST
            '''
        login_form = LoginForm(request.POST)
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')

        if login_form.is_valid():
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    '''
                        登录成功重定向到GET首页
                        '''
                    return HttpResponseRedirect(reverse("index"))
                else:
                    index_dict = IndexGetData(request)
                    index_dict['info_login'] = "您的账户未激活，请查收邮件激活后再登录"
                    index_dict['username_login'] = user_name
                    return render(request, 'index.html', index_dict)
            else:
                index_dict = IndexGetData(request)
                index_dict['info_login'] = "账户密码错误!"
                index_dict['username_login'] = user_name
                return render(request, 'index.html', index_dict)
        else:
            form = RegisterForm()
            '''
                未通过表单验证，返回错误信息，数据重填
                '''
            index_dict = IndexGetData(request)
            index_dict['login_form'] = login_form
            index_dict['username_login'] = user_name
            return render(request, 'index.html', index_dict)


class RegisterPage(View):
    '''
        首页POST注册
        '''
    def get(self, request):
        '''
            首页GET（为了加强用户体验设立）
            '''
        index_dict = IndexGetData(request)
        return render(request, 'index.html', index_dict)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        pass_word = request.POST.get('password', '')
        user_email = request.POST.get('email', '')

        if register_form.is_valid():
            my_user = MyUsers()
            my_user.email = user_email
            my_user.username = user_email
            my_user.is_active = False
            my_user.password = make_password(pass_word)
            try:
                my_user.save()
            except Exception as e:
                if e[0] == 1062:
                    '''
                        邮箱已经存在，错误处理
                        '''
                    index_dict = IndexGetData(request)
                    index_dict['info_register'] = "账号已经存在"
                    index_dict['email_login'] = user_email
                    return render(request, 'index.html', index_dict)
                else:
                    index_dict = IndexGetData(request)
                    index_dict['info_register'] = "数据保存出错"
                    index_dict['email_login'] = user_email
                    return render(request, 'index.html', index_dict)
            status = send_to(user_email, "register")
            index_dict = IndexGetData(request)
            index_dict['info_register'] = "账户：{0}已经创建成功<br>请在邮箱中查收激活链接，激活账户后登录".format(status)
            return render(request, 'index.html', index_dict)
        else:
            '''
                表单验证错误，并返回错误信息，数据重填
                '''
            index_dict = IndexGetData(request)
            index_dict['register_form'] = register_form
            index_dict['email_register'] = user_email
            return render(request, 'index.html', index_dict)


def do_logout(request):
    '''
        账户注销处理
        '''
    logout(request)
    return HttpResponseRedirect(reverse("index"))


class ActiveView(View):
    '''
        账户激活处理
        '''
    def get(self, request, active_code):
        email_get = Mailbox.objects.get(code=active_code)
        if email_get.active == 0:
            email_get.active = 1
            email_get.save()
            email = email_get.email
            user = MyUsers.objects.get(email=email)
            user.is_active = True
            user_name = user.username
            user.save()
            index_dict = IndexGetData(request)
            index_dict['info_login'] = "账户已经激活，请登录！"
            index_dict['username_login'] = user_name
            return render(request, 'index.html', index_dict)
        else:
            index_dict = IndexGetData(request)
            index_dict['info_login'] = "激活码已经过期，请重试！"
            return render(request, 'index.html', index_dict)


class ForgetView(View):
    '''
        首页密码重置
        '''
    def get(self, request):
        '''
            首页密码重置GET（为了加强用户体验设立）
            '''
        index_dict = IndexGetData(request)
        return render(request, 'index.html', index_dict)

    def post(self, request):
        reset_form = ForgetForm(request.POST)
        user_email = request.POST.get('email', '')
        if reset_form.is_valid():
            email_get = MyUsers.objects.filter(email=user_email)
            if email_get:
                status = send_to(user_email, "password")
                if status:
                    index_dict = IndexGetData(request)
                    index_dict['info_forget'] = "{0}重置信息已经发送到邮箱，请查收！".format(status)
                    return render(request, 'index.html', index_dict)
                else:
                    index_dict = IndexGetData(request)
                    index_dict['info_forget'] = "发送失败，请检查网络"
                    return render(request, 'index.html', index_dict)
            else:
                index_dict = IndexGetData(request)
                index_dict['info_forget'] = "该邮箱不存在，请重试！"
                return render(request, 'index.html', index_dict)
        else:
            index_dict = IndexGetData(request)
            index_dict['forget_form'] = reset_form
            index_dict['email_forget'] = user_email
            return render(request, 'index.html', index_dict)


class ResetView(View):
    '''
        忘记密码页面处理
        '''
    def get(self, request, reset_code):
        '''
            忘记密码GET
            '''
        email_get = Mailbox.objects.filter(code=reset_code)
        if email_get:
            email_get = email_get.get(code=reset_code)
            if email_get.active == 0:
                # email_get.active = 1
                email_get.save()
                email = email_get.email
                form = RegisterForm()
                return render(request, 'reset.html', {
                    'form': form,
                    'email_reset': email
                })
            else:
                index_dict = IndexGetData(request)
                index_dict['info_login'] = "重置密码链接过期，请重试"
                return render(request, 'index.html', index_dict)
        else:
            index_dict = IndexGetData(request)
            index_dict['info_login'] = "重置密码链接不存在，请重试"
            return render(request, 'index.html', index_dict)

    def post(self, request):
        '''
            忘记密码POST
            '''
        reset_form = RegisterForm(request.POST)
        pass_word = request.POST.get('password', '')
        user_email = request.POST.get('email', '')
        if reset_form.is_valid():
            email_get = MyUsers.objects.filter(email=user_email)
            if email_get:
                user = email_get.get(email=user_email)
                user.password = make_password(pass_word)
                try:
                    user.save()
                    logout(request)
                    index_dict = IndexGetData(request)
                    index_dict['info_login'] = "您的账户密码已经重置，请登录"
                    index_dict['username_login'] = user_email
                    return render(request, 'index.html', index_dict)
                except Exception as e:
                    print e
                    form = RegisterForm()
                    return render(request, 'reset.html', {
                        'form': form,
                        'info_reset': "重置密码发生错误，请重试！"
                    })
            else:
                form = RegisterForm()
                return render(request, 'reset.html', {
                    'form': form,
                    'info_reset': "邮箱不存在，请重试！"
                })
        else:
            form = RegisterForm()
            return render(request, 'reset.html', {
                'form': form,
                'reset_form': reset_form,
                'email_reset': user_email
            })


class PersonView(LoginRequired, View):

    def get(self,request):
        meg = Message.objects.filter(receive=request.user.id)
        form = RegisterForm()
        buy = UserMoney.objects.filter(username=request.user.id).order_by('-time_in')
        admire = UserClick.objects.filter(username=request.user.id).order_by('-time_in')
        mylead = LeaderVote.objects.filter(leader__leader=request.user.id)
        carousel = Carousel.objects.all().order_by('index')
        message = Message.objects.filter(receive=request.user.id).order_by('-time_sent')
        message_no = message.filter(passed=0).count()
        return render(request, 'person.html', {
            'megs': meg,
            'message_no': message_no,
            'form': form,
            'buy': buy,
            'admire': admire,
            'mylead': mylead,
            'carousel': carousel,
        })


class PeopleView(View):

    def get(self,request):
        meg = Message.objects.filter(receive=request.user.id)
        form = RegisterForm()
        buy = UserMoney.objects.filter(username=request.user.id)
        mylead = LeaderVote.objects.filter(leader__leader=request.user.id)
        message = Message.objects.filter(receive=request.user.id)
        message_no = message.filter(passed=0).count()
        return render(request, 'people.html', {
            'megs': meg,
            'message_no': message_no,
            'form': form,
            'buy': buy,
            'mylead': mylead,
        })


def page_not_found(request):
    '''
        全局页面404处理
        '''
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def server_errors(request):
    '''
        全局页面500处理
        '''
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


class TestPage(View):
    '''
        TestPage
        '''
    def get(self, request):
        '''
            TestPageGET
            '''
        index_dict = IndexGetData(request)
        return render(request, 'base.html', index_dict)


class NeedLogin(View):
    '''
        NeedLogin
        '''
    def get(self, request):
        '''
            NeedLogin
            '''
        index_dict = IndexGetData(request)
        index_dict['info_login'] = "您需要登录，才能使用此功能。"
        return render(request, 'index.html', index_dict)