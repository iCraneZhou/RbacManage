# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Menu(models.Model):
    """
    菜单组
    """
    title = models.CharField(max_length=32)


class Group(models.Model):
    """
    权限组
    """
    caption = models.CharField(verbose_name='组名称',max_length=16)
    menu = models.ForeignKey(verbose_name='所属菜单',to='Menu')


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(verbose_name='含正则URL',max_length=64)
    # is_menu = models.BooleanField(verbose_name='是否是菜单')
    menu_gp = models.ForeignKey(verbose_name='组内菜单',to='Permission',null=True,blank=True)
    code = models.CharField(verbose_name='代码',max_length=16)
    group = models.ForeignKey(verbose_name='所属组',to='Group')

    class Meta:
        verbose_name_plural = '权限表'

    def __str__(self):
        return  self.title


class User(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    phone = models.BigIntegerField(verbose_name='手机号码',unique=True)
    email = models.CharField(verbose_name='邮箱',max_length=32,unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    status = models.IntegerField(default=1,help_text='默认1,0代表禁用,1代表启用')
    flag = models.IntegerField(default=0,help_text='默认0,0代表普通用户,1代表管理员')

    roles = models.ManyToManyField(verbose_name='具有的所有角色',to='Role',blank=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(verbose_name='具有的所有权限',to='Permission',blank=True)
    flag = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title

