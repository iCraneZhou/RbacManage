# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from models import Menu,Group,Permission,User,Role

admin.site.register(Menu)
admin.site.register(Group)
admin.site.register(Permission)
admin.site.register(User)
admin.site.register(Role)
