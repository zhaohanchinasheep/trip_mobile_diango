from django import http
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from sight.models import Sight, SightCommet, Tickets, SightInfo
from sight.serializers import SightListSerializer, SightDetailSerializers, SightCommentSerializers, \
    TicketListSerializer, SightInfoSerializer, ImageListSerializer
from system.models import ImageRelated
from utils.response import NotFoundJsonResponse


class SightListView(ListView):
    """景点列表
    目标：
    1.获取到分页的json格式数据：
    data={
    'meta':{}  # meta中存放元数据，比如总页数，当前页码，列表项总数
    'objects':[]  # objects存放数据库返回的数据
    }
    2.从景点列表中要筛选出热门和精选景点"""
    # 设置每页数据
    paginate_by = 5

    # 重写查询方法，查询分为：有效景点列表，热门景点和精选景点
    # 返回值：根据需求查询到的景点列表
    def get_queryset(self):
        # Q()函数用来设置查询条件
        query = Q(is_valid=True)
        # 1.热门景点
        # 如果用户/前端有传递此参数，说明用户要查询的是热门景点，返回热门景点列表
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            query = query & Q(is_hot=True)
        # 如果用户/前端有传递此参数，说明用户要查询的是精选景点，返回精选景点列表
        # 2.精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            query = query & Q(is_top=True)
        # 3.景点名称搜索
        name = self.request.GET.get('name', None)
        if name:
            # 景点名字模糊查询
            query = query & Q(name__icontains=name)
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        """自定义页面展示的数量"""
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    # ListView返回的是html模板，要让其返回的结果是json格式，就要重写render_to_response方法，处理返回的数据
    # 返回值：json格式的接口数据
    def render_to_response(self, context, **response_kwargs):
        """重写返回接口的方法
        最后的返回格式要求：
        data={
        'meta':{},
        'objects':[]}"""
        page_obj = context['page_obj']
        if page_obj:
            data = SightListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()
        # data = {
        #     'meta': {
        #         'total_count': page_obj.paginator.count,
        #         'pag_count': page_obj.paginator.num_pages,
        #         'current_page': page_obj.number
        #     },
        #     'objects': []
        # }
        # # 因为page_obj.object_list,不能直接序列化，所以需要经过处理，将里面的数据取出放入objects中
        # # page_obj.object_list里面是一项一项的列表数据
        # for item in page_obj.object_list:
        #     data['objects'].append({
        #         'id': item.id,
        #         'name': item.name,
        #         'main_img': item.main_img.url,
        #         'score': item.score,
        #         'min_price':item.min_price,
        #         'province': item.province,
        #         'city': item.city,
        #         'comment_count': 0
        #     })
        # return http.JsonResponse(data)


class SightDetailView(DetailView):
    """景点详细信息"""

    def get_queryset(self):
        queryset = Sight.objects.all()
        return queryset

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            data = SightDetailSerializers(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightCommentView(ListView):
    """景点评论列表"""
    # 每页10条数据
    paginate_by = 10

    def get_queryset(self):
        # kwargs用于查询url中指定的参数
        sight_id = self.kwargs.get('pk', None)
        # sight必须是单个结果，如果是结果集，没有办法筛选数据
        sight = Sight.objects.filter(pk=sight_id, is_valid=True).first()
        if sight:
            return sight.comments.filter(is_valid=True)
        return SightCommet.objects.none()

    def render_to_response(self, context, **response_kwargs):
        """重写响应返回"""
        page_obj = context['page_obj']
        if page_obj is not None:
            data = SightCommentSerializers(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class TicketListView(ListView):
    """景点下的门票列表"""
    paginate_by = 10

    def get_queryset(self):
        sight_id = self.kwargs.get('pk', None)
        return Tickets.objects.filter(is_valid=True, sight_id=sight_id)

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = TicketListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightInfoView(DetailView):
    """2.5景点介绍"""
    # 声明url传递过来的参数指代的字段
    slug_field = 'sight__pk'

    def get_queryset(self):
        print('info:', SightInfo.objects.all())
        return SightInfo.objects.all()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            data = SightInfoSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class ImageListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        # kwargs用于查询url中指定的参数
        sight_id = self.kwargs.get('pk', None)
        # sight必须是单个结果，如果是结果集，没有办法筛选数据
        sight = Sight.objects.filter(pk=sight_id, is_valid=True).first()
        if sight:
            print(sight.images.filter(is_valid=True))
            return sight.images.filter(is_valid=True)
        return ImageRelated.objects.none()

    def render_to_response(self, context, **response_kwargs):
        """重写响应返回"""
        page_obj = context['page_obj']
        if page_obj is not None:
            data = ImageListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()
