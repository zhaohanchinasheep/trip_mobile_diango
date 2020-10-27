import json

from django import http
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from accounts.forms import LoginForm
from accounts.serializers import UserSerializer, UserProfileSerializer
from utils.response import BadJsonResponse, MethodNotAllowResponse, UnauthorizedJsonResponse


def user_login(request):
    """用户登陆页面"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            form.do_login(request)
            print('表单信息验证成功')
            return redirect('/accounts/user/info/')
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {'form': form})


@login_required
def user_info(request):
    """用户个人中心"""
    print(request.user)
    return render(request, 'user_info.html')


def user_logout(request):
    """退出登陆"""
    # 调用logout()函数实现
    logout(request)
    return redirect('/accounts/user/login/')


def user_api_login(request):
    """用户登陆接口"""
    # 1.获取用户输入信息
    if request.method == 'POST':
        # 2.表单验证
        form = LoginForm(data=request.POST)
        print(form)
        # 3.如果表单验证通过，执行登陆
        if form.is_valid():

            user = form.do_login(request)
            profile = user.profile
            # 4.返回用户的基本信息和详细信息
            data = {
                'user': UserSerializer(user).to_dict(),
                'profile': UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data)
        # 5.如果表单验证不通过，返回用户登陆的错误信息
        else:
            err = json.loads(form.errors.as_json())
            return BadJsonResponse(err)
    # 6.如果当前的请求不是post而是get 则返回获取方式错误的信息
    else:
        return MethodNotAllowResponse()


def user_api_logout(request):
    """用户退出接口"""
    logout(request)
    # 通过状态码判断用户状态，如果是201表示成功退出
    return http.HttpResponse(status=201)


class UserDetailView(View):
    """查询用户详细信息接口"""
    def get(self, request):
        # 获取用户
        user = request.user
        # 用户是否未游客
        if not user.is_authenticated:
            # 返回401状态码，表示用户未登陆
            return UnauthorizedJsonResponse()
        else:
            profile = user.profile
            # 4.返回用户的基本信息和详细信息
            data = {
                'user': UserSerializer(user).to_dict(),
                'profile': UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data)
