#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/9/27 17:31
# @Author  : Cranezhou

from django.conf import settings


def init_permission(user,request):
    """
    初始化权限信息，获取权限信息并放置到sesssion中。
    :param user:
    :param request:
    :return:
    """
    # data = {
    #     1: {
    #         'codes': ['list', 'add', 'edit', 'del'],
    #         'urls': [
    #             '/userinfo/',
    #             '/userinfo/add/',
    #             '/userinfo/edit/(\d+)/',
    #             '/userinfo/del/(\d+)/',
    #         ]
    #     },
    #     2: {
    #         'codes': ['list', 'add', 'edit', 'del'],
    #         'urls': [
    #             '/userinfo/',
    #             '/userinfo/add/',
    #             '/userinfo/edit/(\d+)/',
    #             '/userinfo/del/(\d+)/',
    #         ]
    #     },
    # }

    # permission_list = user.roles.values('permissions__title',       # 用户列表
    #                                     'permissions__url',
    #                                     'permissions__code',
    #                                     'permissions__is_menu',     # 是否是菜单
    #                                     'permissions__group_id',
    #                                     'permissions__group__menu_id', # 菜单ID
    #                                     'permissions__group__menu__title', # 菜单名称
    #                                     ).distinct()

    permission_list = user.roles.values('permissions__title',
                                        'permissions__code',
                                        'permissions__id',
                                        'permissions__url',
                                        'permissions__menu_gp_id',
                                        'permissions__group__id',
                                        'permissions__group__menu_id',
                                        'permissions__group__menu__title',
                                        ).distinct()

    # url_list = []
    # for item in permission_list:
    #     url_list.append(item['permisssions__url'])
    # print(url_list)
    # request.session['permission_url_list'] = url_list


    # menu_list= []
    # # 去掉不是菜单的URL
    # for item in permission_list:
    #     if not item['permissions__is_menu']:
    #         continue
    #     tpl = {
    #         'menu_id':item['permissions__group__menu_id'],
    #         'menu_title':item['permissions__group__menu__title'],
    #         'title':item['permissions__title'],
    #         'url':item['permissions__url'],
    #         'active':False,
    #     }
    #     menu_list.append(tpl)

    menu_list = []
    # 去掉不是菜单的URL
    for item in permission_list:
        tpl = {
            'id':item['permissions__id'],
            "title":item["permissions__title"],
            "menu_title":item["permissions__group__menu__title"],
            "url":item["permissions__url"],
            "menu_id":item["permissions__group__menu_id"],
            "menu_gp_id":item["permissions__menu_gp_id"],
        }
        menu_list.append(tpl)

    request.session[settings.PERMISSION_MENU_KEY] = menu_list


    #权限表
    result = {}
    for item in permission_list:
        groupid = item['permissions__group_id']
        code = item['permissions__code']
        url = item['permissions__url']

        if groupid in result:
            result[groupid]["codes"].append(code)
            result[groupid]["urls"].append(url)
        else:
            result[groupid] = {
                "codes":[code,],
                "urls":[url,]
            }

    # print(result)
    request.session[settings.PERMISSIONS_URL_DICT_KEY] = result


