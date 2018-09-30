# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

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
        return render(request, 'rbac/index.html')

    if request.method == 'POST':
        pass