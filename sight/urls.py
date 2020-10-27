"""trip_mobile_diango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from sight import views

urlpatterns = [
    # 2.1景点列表
    path('sight/list/', views.SightListView.as_view(), name='sight_list'),
    # 2.2景点详细信息
    path('sight/detail/<int:pk>', views.SightDetailView.as_view(), name='sight_detail'),
    # 2.3景点评论列表
    path('comment/list/<int:pk>', views.SightCommentView.as_view(), name='sight_comment_list'),
    # 2.4门票列表
    path('ticket/list/<int:pk>', views.TicketListView.as_view(), name='ticket_list'),
    # 2.5景点介绍
    path('sight/info/<int:pk>', views.SightInfoView.as_view(), name='sight_info'),
    # 2.6图片展示
    path('image/list/<int:pk>', views.ImageListView.as_view(), name='image_list'),


]
