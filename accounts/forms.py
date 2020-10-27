import re

from django import forms
from django.contrib.auth import authenticate, login
from django.utils.timezone import now


class LoginForm(forms.Form):
    """用户登陆表单"""
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密码', max_length=128, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 当前登陆的用户
        self.user = None

    def clean_username(self):
        """自定义验证用户名
        验证用户名是否为手机号码"""
        pattern = r'^1[3|5|6|7|8][0-9]{9}$'
        username = self.cleaned_data['username']
        print('username:',username)
        if not username:
            raise forms.ValidationError('请输入用户名')
        if not re.search(pattern, username):
            raise forms.ValidationError('请输入正确的手机号码')
        return username

    def clean(self):
        """多个字段综合验证"""
        # 调用父类验证原规则，得到验证后的用户对象
        data = super().clean()
        print('data:',data)
        if self.errors:
            return
        username = data.get('username', None)
        password = data.get('password', None)
        # 用户和密码验证
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('用户名或密码有误')
        else:
            if not user.is_active:
                raise forms.ValidationError('该用户已被禁用')
            self.user = user
            return data

    def do_login(self, request):
        """执行用户登陆"""
        user = self.user
        # 调用登陆函数
        login(request, user=user)
        # 修改最后的登陆时间,now()表示当前时间
        user.last_login = now()
        # 保存用户登陆信息
        user.save()
        # TODO:保存登陆历史
        return user
