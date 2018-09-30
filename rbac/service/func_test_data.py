#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/9/28 15:37
# @Author  : Cranezhou


import re

menu_list = [
    {'menu_id':1, 'menu_title':'菜单一','title':'用户列表','url':'/userinfo/','active':False},
    {'menu_id':1, 'menu_title':'菜单一','title':'订单列表','url':'/order/','active':False},
    {'menu_id':2, 'menu_title':'菜单二','title':'xxx列表','url':'/xxx/','active':False},
    {'menu_id':2, 'menu_title':'菜单二','title':'iii列表','url':'/uuu/','active':False},
]

current_url = '/userinfo/'

res = {}

for tem in menu_list:
    mid = tem['menu_id']
    mtitle = tem['menu_title']
    title = tem['title']
    url = tem['url']
    active = False

    if re.match(url,current_url):
        active = True

    if mid in res:
        res[mid]['children'].append({"title":title,"url":url,"active":active})
        if active:
            res[mid]['actvie'] = True
    else:
        res[mid] = {
            'menu_id':mid,
            'menu_title':mtitle,
            'active':active,
            'children':[
                {"title":title,"url":url,"active":active},
            ]
        }

print(res)