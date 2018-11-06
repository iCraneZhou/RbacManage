"""RbacManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from views import login_views,index_views,welcome_views
from views import *


urlpatterns = [
    url(r'^login/$', login_views),
    url(r'^index/$',index_views),
    url(r'^welcome/$',welcome_views),

    url(r'^member_list/$',member_list_views),
    url(r'^member_add/$',member_add_views),
    url(r'^member_edit/$',member_edit_views),
    url(r'^member_password/$',member_password_views),
    url(r'^member_search/$',member_search_views),

    url(r'^admin_list/$',admin_list_views),
    url(r'^admin_add/$',admin_add_views),
    url(r'^admin_edit/$',admin_edit_views),
    url(r'^user_change_status/$',user_change_status_views),
    url(r'^user_batch_delete/$',user_batch_delete_views),
    url(r'^order_list/$',order_list_views),
    url(r'^unicode/$',unicode_views),
    url(r'^admin_role/$',admin_role_views),
    url(r'^admin_rule/$',admin_rule_views)
]
