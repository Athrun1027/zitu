# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from PRO_APP.models import Projects, TimeLimit, Plan
from USER_APP.views import RegisterForm, Leader, Message, MyUsers
from CHO_APP.models import LeaderVote, LeadeWho, UserProject
from OPR_APP.models import UserClick
# Create your views here.


def ProjectGetData(request, status):
    range_id = request.GET.get('range', '')
    place_id = request.GET.get('place', '')
    message = Message.objects.filter(receive=request.user.id)
    message_no = message.filter(passed=0).count()
    sort_id = request.GET.get('sort', '-num_admire')
    if status == '0':
        project = Projects.objects.filter(status='0')
    else:
        project = Projects.objects.exclude(Q(status='0') | Q(status='6'))

    if range_id == '1':
        project = project.filter(style__in=[1, 2, 3, 4, 5, 6]).order_by(sort_id)
        if place_id:
            project = project.filter(style=int(place_id)).order_by(sort_id)
    elif range_id == '2':
        project = project.filter(style__in=[7, 8, 9, 10, 11, 12]).order_by(sort_id)
        if place_id:
            project = project.filter(style=int(place_id)).order_by(sort_id)
    else:
        project = project.all().order_by(sort_id)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(project, 8, request=request)
    project_page = p.page(page)
    form = RegisterForm()
    project_dict = {
        'form': form,
        'project': project_page,
        'project_no': project,
        'range_id': range_id,
        'place_id': place_id,
        'sort_id': sort_id,
        'message_no': message_no,
    }
    return project_dict


class AllProjectPage(View):

    def get(self, request):
        project_dict = ProjectGetData(request, '0')
        return render(request, 'projects.html', project_dict)


class StartProjectPage(View):

    def get(self, request):
        project_dict = ProjectGetData(request, '1')
        timelimit1 = TimeLimit.objects.get(style='1')
        project_dict['timelimit1'] = timelimit1
        timelimit2 = TimeLimit.objects.get(style='2')
        project_dict['timelimit2'] = timelimit2
        timelimit3 = TimeLimit.objects.get(style='3')
        project_dict['timelimit3'] = timelimit3
        timelimit4 = TimeLimit.objects.get(style='4')
        project_dict['timelimit4'] = timelimit4
        return render(request, 'projects_on.html', project_dict)


class ModelProjectPage(View):

    def get(self, request, pro_id):
        if request.user.id:
            print request.user
            project = Projects.objects.get(ID=pro_id)
            user = MyUsers.objects.get(id=request.user.id)
            user_pro = UserClick.objects.filter(username=user, project=project)
            if not user_pro:
                user_pro = UserClick()
                user_pro.username = user
                user_pro.project = project
                user_pro.save()
            else:
                user_pro = user_pro.get(username=user)
            player = UserProject.objects.filter(project=pro_id)
            leader = LeaderVote.objects.filter(project=project.ID).order_by('-counter')
            plan = Plan.objects.filter(project=project.ID)
            form = RegisterForm()
            message = Message.objects.filter(receive=request.user.id)
            message_no = message.filter(passed=0).count()
            return render(request, 'project.html', {
               'form': form,
               'message_no': message_no,
               'project': project,
               'leader': leader,
               'plan': plan,
               'player': player,
               'user_pro': user_pro,
            })
        else:
            project = Projects.objects.get(ID=pro_id)
            player = UserProject.objects.filter(project=pro_id)
            leader = LeaderVote.objects.filter(project=project.ID).order_by('-counter')
            plan = Plan.objects.filter(project=project.ID)
            form = RegisterForm()
            return render(request, 'project.html', {
                'form': form,
                'project': project,
                'leader': leader,
                'plan': plan,
                'player': player,
            })

    def post(self, request, pro_id):
        user_id = int(request.POST.get('user_id', '0'))
        pro_id = int(request.POST.get('pro_id', '0'))
        user_pro = UserClick.objects.filter(username=user_id, project=pro_id)
        if user_pro:
            user_pro = user_pro.get(username=user_id)
            if user_pro.like == 0:
                user_pro.like = 1
                user_pro.save()
                return HttpResponse('{"status": "success", "msg": "已关注"}', content_type="application/json")
            else:
                user_pro.like = 0
                user_pro.save()
                return HttpResponse('{"status": "success", "msg": "未关注"}', content_type="application/json")
        else:
            user_pro = UserClick()
            user = MyUsers.objects.get(id=user_id)
            pro = Projects.objects.get(ID=pro_id)
            user_pro.username = user
            user_pro.project = pro
            user_pro.like = 1
            user_pro.save()
            return HttpResponse('{"status": "success", "msg": "已关注"}', content_type="application/json")


class LoadingProjectPage(View):

    def get(self, request, pro_id):
        if request.user.id:
            print request.user
            project = Projects.objects.get(ID=pro_id)
            user = MyUsers.objects.get(id=request.user.id)
            user_pro = UserClick.objects.filter(username=user, project=project)
            if not user_pro:
                user_pro = UserClick()
                user_pro.username = user
                user_pro.project = project
                user_pro.save()
            else:
                user_pro = user_pro.get(username=user)
            player = UserProject.objects.filter(project=pro_id)
            leader = LeaderVote.objects.filter(project=project.ID).order_by('-counter')
            plan = Plan.objects.filter(project=project.ID)
            form = RegisterForm()
            message = Message.objects.filter(receive=request.user.id)
            message_no = message.filter(passed=0).count()
            timelimit1 = TimeLimit.objects.get(style='1')
            timelimit2 = TimeLimit.objects.get(style='2')
            timelimit3 = TimeLimit.objects.get(style='3')
            timelimit4 = TimeLimit.objects.get(style='4')
            return render(request, 'project_on.html', {
               'form': form,
               'message_no': message_no,
               'timelimit1': timelimit1,
               'timelimit2': timelimit2,
               'timelimit3': timelimit3,
               'timelimit4': timelimit4,
               'project': project,
               'leader': leader,
               'plan': plan,
               'player': player,
               'user_pro': user_pro,
            })
        else:
            project = Projects.objects.get(ID=pro_id)
            player = UserProject.objects.filter(project=pro_id)
            leader = LeaderVote.objects.filter(project=project.ID).order_by('-counter')
            plan = Plan.objects.filter(project=project.ID)
            form = RegisterForm()
            timelimit1 = TimeLimit.objects.get(style='1')
            timelimit2 = TimeLimit.objects.get(style='2')
            timelimit3 = TimeLimit.objects.get(style='3')
            timelimit4 = TimeLimit.objects.get(style='4')
            return render(request, 'project_on.html', {
                'form': form,
                'timelimit1': timelimit1,
                'timelimit2': timelimit2,
                'timelimit3': timelimit3,
                'timelimit4': timelimit4,
                'project': project,
                'leader': leader,
                'plan': plan,
                'player': player,
            })

    def post(self, request, pro_id):
        user_id = int(request.POST.get('user_id', '0'))
        pro_id = int(request.POST.get('pro_id', '0'))
        user_pro = UserClick.objects.filter(username=user_id, project=pro_id)
        if user_pro:
            user_pro = user_pro.get(username=user_id)
            if user_pro.like == 0:
                user_pro.like = 1
                user_pro.save()
                return HttpResponse('{"status": "success", "msg": "已关注"}', content_type="application/json")
            else:
                user_pro.like = 0
                user_pro.save()
                return HttpResponse('{"status": "success", "msg": "未关注"}', content_type="application/json")
        else:
            user_pro = UserClick()
            user = MyUsers.objects.get(id=user_id)
            pro = Projects.objects.get(ID=pro_id)
            user_pro.username = user
            user_pro.project = pro
            user_pro.like = 1
            user_pro.save()
            return HttpResponse('{"status": "success", "msg": "已关注"}', content_type="application/json")
