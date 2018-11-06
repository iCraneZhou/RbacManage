# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from models import User,Role,Permission
from django.core.paginator import Paginator
import json

from django.shortcuts import render


# Create your views here.

def login_views(request):
    print request
    if request.method == 'GET':
        return render(request, 'rbac/login.html')

    if request.method == 'POST':
        pass


def index_views(request):
    if request.method == 'GET':
        return render(request, 'rbac/index.html',locals())

    if request.method == 'POST':
        pass


def welcome_views(request):
    if request.method == 'GET':
        return render(request, 'rbac/welcome.html')

    if request.method == 'POST':
        pass


def member_list_views(request):
    if request.method == 'GET':
        limit = 10
        allUsers = User.objects.filter(flag = 0,flag_delete=0)[:limit]
        countUser = User.objects.filter(flag = 0,flag_delete=0).count()
        print(allUsers)
        return render(request, 'rbac/member-list.html',locals())

    if request.method == 'POST':
        data = request.POST
        print(data)
        page_id = int(data['page_id'])
        limit = int(data['limit'])
        print(limit,page_id)
        status = {}

        try:
            countUser = User.objects.filter(flag=0, flag_delete=0).count()
            last_page_id = countUser // limit + 1 if limit * ( countUser // limit ) < countUser else countUser // limit

            if page_id == 1:
                allUsers = User.objects.filter(flag=0, flag_delete=0).order_by("id")[:limit]
            elif page_id == last_page_id:
                offset_start = ( page_id - 1 ) * limit
                allUsers = User.objects.filter(flag=0, flag_delete=0).order_by("id")[offset_start:]
            else:
                offset_start = ( page_id - 1 ) * limit
                offset_end = page_id * limit
                allUsers = User.objects.filter(flag=0, flag_delete=0).order_by("id")[offset_start:offset_end]

            print(allUsers)

            data = {}
            n = 1
            for U in allUsers:
                data[n] = {
                    'id':U.id,
                    'username':U.username,
                    'email':U.email,
                    'phone':U.phone,
                    'flag':U.flag,
                    'create_time':U.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status':U.status,
                    'flag_delete':U.flag_delete,
                    'roles': [ R for R in U.roles.filter(status=1,flag=0).values('title')],
                    #'roles':[ R.title for R in U.roles.filter(status=1,flag=0).all()]
                }
                n += 1
            print(data)

            status["data"] = data
            status["countUser"] = countUser
            status["status"] = 200
            status["message"] = "分页查询成功"
        except Exception as e:
            print(e)
            status["status"] = False
            status["message"] = "分页查询失败"

        print(status)
        return HttpResponse(json.dumps(status))


def member_add_views(request):
    if request.method == 'GET':
        allRoles = Role.objects.filter(flag = 0)
        return render(request, 'rbac/member-add.html',locals())

    if request.method == 'POST':
        data = request.POST
        print(data)
        username = data['username']
        phone = data['phone']
        password = data['password']
        email = data['email']
        role_ids = json.loads(request.POST.getlist('roles')[0])  # 处理ajax传递过来的JavaScript数组，方法1，须配置ajax传参对应写法
        print(role_ids)
        status = {}
        try:
            U = User.objects.create(username=username,phone=phone,password=password,email=email)
            for id in role_ids:
                U.roles.add(id)
            status["status"] = 200
            status["message"] = "添加用户成功"
        except:
            status["status"] = False
            status["message"] = "添加用户失败"
        print(status)
        return HttpResponse(json.dumps(status))


def member_edit_views(request):
    if request.method == 'GET':
        username_id = request.GET.get('username_id')
        if username_id:
            U = User.objects.get(id = username_id)
            U_roles = U.roles.values()
        allRoles = Role.objects.filter(flag = 0)
        return render(request, 'rbac/member-edit.html',locals())

    if request.method == 'POST':
        data = request.POST
        print(data)
        username_id = int(data['username_id'])
        username = data['username']
        phone = data['phone']
        email = data['email']
        roles_id = json.loads(request.POST.getlist('roles')[0])  # 处理ajax传递过来的JavaScript数组，方法1，须配置ajax传参对应写法
        print(roles_id)
        message = {}

        try:
            U = User.objects.get(id=username_id)
            U.username = username
            U.phone = phone
            U.email = email
            U.save()
            user_role_list = []

            for user_role in U.roles.values():
                user_role_list.append(user_role['id'])
            print(user_role_list)

            role_delete_list = [item for item in user_role_list if item not in roles_id]
            print(role_delete_list)

            role_add_list = [item for item in roles_id if item not in user_role_list]
            print(role_add_list)

            for role_id in role_delete_list:
                U = User.objects.get(id=username_id)
                U.roles.remove(role_id)

            for role_id in role_add_list:
                U = User.objects.get(id=username_id)
                U.roles.add(role_id)

            message["status"] = 200
            message["message"] = "更改用户信息成功"
        except Exception as e:
            print(e)
            message["status"] = False
            message["message"] = "更改用户信息失败"
        print(message)
        return HttpResponse(json.dumps(message))


def member_password_views(request):
    if request.method == 'GET':
        username_id = request.GET.get('username_id')
        print(username_id)
        if username_id:
            U = User.objects.get(id = username_id)
            print(U)
        return render(request, 'rbac/member-password.html',locals())

    if request.method == 'POST':
        data = request.POST
        print(data)
        username = data['username']
        oldpass = data['oldpass']
        newpass = data['newpass']
        message = {}
        try:
            U = User.objects.get(username=username,password=oldpass)
            if U:
                U.password = newpass
                U.save()
                message["status"] = 200
                message["message"] = "修改密码成功"
            else:
                message["status"] = False
                message["message"] = "修改密码失败1"
        except:
            message["status"] = False
            message["message"] = "修改密码失败2"
        print(message)
        return HttpResponse(json.dumps(message))


def member_search_views(request):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        data = request.POST
        print(data)
        start_time = data['start_time']
        end_time = data['end_time']
        username = data['username']
        print(start_time,end_time,username)
        status = {}

        try:

            allUsers = User.objects.filter(username__contains=username, flag=0, flag_delete=0,create_time__range=(start_time,end_time))

            data = {}
            n = 1
            for U in allUsers:
                data[n] = {
                    'id':U.id,
                    'username':U.username,
                    'email':U.email,
                    'phone':U.phone,
                    'flag':U.flag,
                    'create_time':U.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status':U.status,
                    'flag_delete':U.flag_delete,
                    'roles': [ R for R in U.roles.filter(status=1,flag=0).values('title')],
                    #'roles':[ R.title for R in U.roles.filter(status=1,flag=0).all()]
                }
                n += 1
            print(data)

            status["data"] = data
            status["status"] = 200
            status["message"] = "搜索查询成功"
        except Exception as e:
            print(e)
            status["status"] = False
            status["message"] = "搜索查询失败"

        print(status)
        return HttpResponse(json.dumps(status))


def admin_list_views(request):
    if request.method == 'GET':
        allUsers = User.objects.filter(flag = 1,flag_delete=0)
        countUser = User.objects.filter(flag = 1,flag_delete=0).count()
        print(allUsers)
        return render(request, 'rbac/admin-list.html',locals())

    if request.method == 'POST':
        pass

def admin_add_views(request):
    if request.method == 'GET':
        allRoles = Role.objects.filter(flag = 1)
        return render(request, 'rbac/admin-add.html',locals())

    if request.method == 'POST':
        data = request.POST
        print(data)
        username = data['username']
        phone = data['phone']
        password = data['password']
        email = data['email']
        roles_id = data['roles'].split(',')   # 处理ajax传递过来的JavaScript数组，方法2，须配置ajax传参对应写法
        flag = int(data['flag'])
        print(roles_id)
        status = {}
        try:
            U = User.objects.create(username=username, phone=phone, password=password, email=email, flag=flag)
            for id in roles_id:
                U.roles.add(id)
            status["status"] = 200
            status["message"] = "添加用户成功"
        except:
            status["status"] = False
            status["message"] = "添加用户失败"
        print(status)
        return HttpResponse(json.dumps(status))


def admin_edit_views(request):
    if request.method == 'GET':
        username_id = request.GET.get('username_id')
        if username_id:
            U = User.objects.get(id=username_id)
            U_roles = U.roles.values()
        allRoles = Role.objects.filter(flag=1)
        return render(request, 'rbac/admin-edit.html',locals())

    if request.method == 'POST':
        data = request.POST
        print(data)
        username_id = int(data['username_id'])
        username = data['username']
        phone = data['phone']
        email = data['email']
        roles_id = data['roles'].split(',')   # 处理ajax传递过来的JavaScript数组，方法2，须配置ajax传参对应写法
        print(roles_id)
        message = {}

        try:
            U = User.objects.get(id=username_id)
            U.username=username
            U.phone=phone
            U.email=email
            U.save()
            user_role_list = []

            for user_role in U.roles.values():
                user_role_list.append(user_role['id'])
            print(user_role_list)

            role_delete_list = [item for item in user_role_list if item not in roles_id]
            print(role_delete_list)

            role_add_list = [item for item in roles_id if item not in user_role_list]
            print(role_add_list)

            for role_id in role_delete_list:
                U = User.objects.get(id=username_id)
                U.roles.remove(role_id)

            for role_id in role_add_list:
                U = User.objects.get(id=username_id)
                U.roles.add(role_id)

            message["status"] = 200
            message["message"] = "更改用户信息成功"
        except Exception as e:
            print(e)
            message["status"] = False
            message["message"] = "更改用户信息失败"
        print(message)
        return HttpResponse(json.dumps(message))


def user_change_status_views(request):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        data = request.POST
        print(data)
        username_id = int(data['username_id'])
        status = int(data['status'])
        message = {}
        try:
            U = User.objects.filter(id=username_id)
            U.update(status=status)
            message["status"] = 200
            message["message"] = "更改用户状态成功"
        except:
            message["status"] = False
            message["message"] = "更改用户状态失败"
        print(message)
        return HttpResponse(json.dumps(message))


def user_batch_delete_views(request):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        data = request.POST
        print(data)
        username_ids = data.getlist('username_ids')
        message = {}
        try:
            for id in username_ids:
                U = User.objects.get(id=id)
                U.flag_delete = 1
                U.save()
            message["status"] = 200
            message["message"] = "册除用户成功"
        except:
            message["status"] = False
            message["message"] = "册除用户失败"
        print(message)
        return HttpResponse(json.dumps(message))


def order_list_views(request):
    if request.method == 'GET':
        return render(request, 'rbac/order-list.html')

    if request.method == 'POST':
        pass


def unicode_views(request):
    if request.method == 'GET':
        return render(request, 'rbac/unicode.html')

    if request.method == 'POST':
        pass


def admin_role_views(request):
    if request.method == 'GET':
        allRole = Role.objects.all()
        print(allRole)
        return render(request, 'rbac/admin-role.html',locals())

    if request.method == 'POST':
        pass


def admin_rule_views(request):
    if request.method == 'GET':
        allPermission = Permission.objects.all()
        print(allPermission)
        return render(request, 'rbac/admin-rule.html',locals())

    if request.method == 'POST':
        pass

