# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.base import View

from .models import Carousel
from USER_APP.views import RegisterForm
from USER_APP.models import Message, Friends, Leader, MyUsers
from PRO_APP.models import Projects
from OPR_APP.models import UserMoney

# Create your views here.


class NoticeView(View):

    def get(self, request):
        index = request.GET.get('index', '1')
        carousel = Carousel.objects.all().order_by('index')
        carousel_on = carousel.get(index=int(index))
        message = Message.objects.filter(receive=request.user.id)
        message_no = message.filter(passed=0).count()
        form = RegisterForm()
        return render(request, 'notice.html', {
            'carousel': carousel,
            'carousel_on': carousel_on,
            'form': form,
            'message_no': message_no,
        })


class InformView(View):

    def get(self, request):
        message = Message.objects.filter(receive=request.user.id)
        friends = Friends.objects.filter(username=request.user.id)
        friends_no = friends.filter(passed=0)
        message_no = message.filter(passed=0).count()
        form = RegisterForm()
        return render(request, 'inform.html', {
            'form': form,
            'message': message[:3],
            'message_no': message_no,
            'friends': friends,
            'friends_no': friends_no,
        })

    def post(self, request):
        user_id = int(request.POST.get('user_id', '0'))
        message = Message.objects.filter(receive=user_id)
        if not message:
            return HttpResponse('{"status": "fail", "msg": "没有发送给您的消息"}', content_type="application/json")
        else:
            for mes in message:
                mes.passed = 1
                mes.save()
            return HttpResponse('{"status": "success", "msg": "已经将所有消息置为已读"}', content_type="application/json")


class FooterView(View):

    def get(self, request):
        message = Message.objects.filter(receive=request.user.id)
        message_no = message.filter(passed=0).count()
        form = RegisterForm()
        return render(request, 'footer.html', {
            'form': form,
            'message': message,
            'message_no': message_no,
        })


class LeaderView(View):

    def get(self, request):
        leader = Leader.objects.all()[:3]
        message = Message.objects.filter(receive=request.user.id)
        message_no = message.filter(passed=0).count()
        form = RegisterForm()
        return render(request, 'leader.html', {
            'form': form,
            'leader': leader,
            'message': message,
            'message_no': message_no,
        })


class ProjectingView(View):

    def get(self, request):
        leader = Leader.objects.all()[:3]
        project = Projects.objects.get(ID=2)
        message = Message.objects.filter(receive=request.user.id)
        message_no = message.filter(passed=0).count()
        form = RegisterForm()
        return render(request, 'projecting.html', {
            'form': form,
            'leader': leader,
            'project': project,
            'message': message,
            'message_no': message_no,
        })


class BuyView(View):

    def post(self, request):
        user_id = int(request.POST.get('user_id', '0'))
        pro_id = int(request.POST.get('pro_id', '0'))
        user_pro = UserMoney.objects.filter(username=user_id, project=pro_id)
        if not user_pro:
            user_pro = UserMoney()
            project = Projects.objects.get(ID=pro_id)
            user = MyUsers.objects.get(id=user_id)
            user_pro.username = user
            user_pro.project = project
            user_pro.save()
            return HttpResponse('{"status": "success", "msg": "购买成功"}', content_type="application/json")
        else:
            user_pro = user_pro.get(username=user_id, project=pro_id)
            return HttpResponse('{"status": "fail", "msg": "不要重复购买"}', content_type="application/json")