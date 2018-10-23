# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from models import User,Role,Permission
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
        allUsers = User.objects.filter(flag = 0)
        print(allUsers)
        return render(request, 'rbac/member-list.html',locals())

    if request.method == 'POST':
        pass

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


def admin_list_views(request):
    if request.method == 'GET':
        allUsers = User.objects.filter(flag = 1)
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
        print(status)
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