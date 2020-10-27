from django import http
from django.shortcuts import render

# Create your views here.
from system.models import Slider


def slider_list(request):
    """轮播图接口
    数据类型：json
    data={
    'meta':{},
    'objects':[]   // 包括轮播图名称、地址等，从数据库获取
    }"""

    data = {
        'meta': {

        },
        'objects': []
    }
    queryset = Slider.objects.filter(is_valid=True)
    for item in queryset:
        data['objects'].append({
            'id': item.id,
            'name': item.name,
            'img_url': item.img.url,  # img.url是ImageField提供的一个属性
            'target_url': item.target_url
        })
    return http.JsonResponse(data)
