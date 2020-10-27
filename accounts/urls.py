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

from django.urls import path

from accounts import views

urlpatterns = [
    # 3.1用户登陆
    path('user/login/', views.user_login, name='user_login'),
    # 3.2用户个人中心
    path('user/info/', views.user_info, name='user_info'),
    # 3.3退出登陆
    path('user/logout/', views.user_logout, name='user_logout'),

    # 用户登陆和退出接口
    path('user/api/logout/', views.user_api_logout, name='user_api_logout'),
    path('user/api/login/', views.user_api_login, name='user_api_login'),
    # 用户详情接口
    path('user/api/info/', views.UserDetailView.as_view(), name='user_api_info'),



]
