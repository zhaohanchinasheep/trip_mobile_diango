from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from accounts.models import User
from sight.choices import TicketStatus, EntryWay, TicketTypes
from system.models import ImageRelated
from utils.models import CommonModel


# Create your models here.

class Sight(CommonModel):
    """景点基础信息"""
    name = models.CharField('名称', max_length=64)
    desc = models.CharField('描述', max_length=256)
    main_img = models.ImageField('主图', upload_to='%Y%m/sight', max_length=256)
    banner_img = models.ImageField('详情主图', upload_to='%Y%m/sight', max_length=256)
    content = models.TextField('详细')
    score = models.FloatField('评分', default=5)
    min_price = models.FloatField('最低价格', default=0)

    province = models.CharField('省份', max_length=32)
    city = models.CharField('市区', max_length=32)
    area = models.CharField('区/县', max_length=32, null=True, blank=True)
    town = models.CharField('乡镇', max_length=32, null=True, blank=True)
    # 由景点的基础信息查询到图片
    images = GenericRelation(ImageRelated, related_query_name="rel_sight_images",
                             verbose_name='关联的图片')

    is_top = models.BooleanField('是否为精选景点', default=False)
    is_hot = models.BooleanField('是否为热门景点', default=False)

    class Meta:
        db_table = 'sight'
        ordering = ['-updated_at']


class SightInfo(CommonModel):
    """景点详细信息模块"""

    # 与景点表建立一对一关联
    sight = models.OneToOneField(Sight, on_delete=models.CASCADE)
    entry_explain = models.TextField('入园参考', max_length=1024, null=True, blank=True)
    play_way = models.TextField('特色玩法', null=True, blank=True)
    traffic = models.TextField('交通到达', null=True, blank=True)
    tips = models.TextField('温馨提示', null=True, blank=True)

    # 图片关联表可以根据rel_sight_info_img查找到景点详细信息
    # 景点详细信息表根据images字段查找到所有景点的图片

    class Meta:
        db_table = 'sight_info'


class Tickets(CommonModel):
    """门票信息模型"""
    sight = models.ForeignKey(Sight, on_delete=models.PROTECT, related_name='ticket', verbose_name='景点门票')
    name = models.CharField("名称", max_length=128)
    desc = models.TextField('描述', null=True, blank=True)
    types = models.SmallIntegerField('类型', choices=TicketTypes.choices,
                                     default=TicketTypes.ADULT,
                                     help_text='默认成人票')
    price = models.FloatField('原价', default=0)
    discount = models.FloatField('折扣', default=10, null=True, blank=True)
    total_stock = models.PositiveIntegerField('总库存', default=0)
    remain_stock = models.PositiveIntegerField('剩余库存', default=0)
    expire_date = models.DateTimeField('有效期', default=1)
    return_policy = models.CharField("退改政策", max_length=1024, default='条件退')
    has_invoice = models.BooleanField('是否提供发票', default=True)
    enty_way = models.SmallIntegerField('入园方式', choices=EntryWay.choices,
                                        default=EntryWay.BY_CODE,
                                        help_text='默认凭借验证码入园')
    tips = models.CharField('预定须知', max_length=1024, null=True, blank=True)
    remark = models.CharField('其他说明', max_length=1024, null=True, blank=True)
    status = models.SmallIntegerField('状态', choices=TicketStatus.choices,
                                      default=TicketStatus.OPEN,
                                      help_text='默认开放')

    class Meta:
        db_table = 'sight_tickets'


class SightCommet(CommonModel):
    """景点评论表"""
    user = models.ForeignKey(User, on_delete=models.SET(None),
                             related_name='comments',
                             verbose_name='评论人')
    sight = models.ForeignKey(Sight, on_delete=models.SET(None),
                              related_name='comments',
                              verbose_name='景点')
    content = models.TextField('内容', blank=True, null=True)
    is_top = models.BooleanField('是否置顶', default=False)
    love_count = models.IntegerField('点赞的次数', default=0)
    score = models.FloatField('评分', default=5)
    ip_address = models.CharField('ip', max_length=128, null=True, blank=True)
    is_public = models.SmallIntegerField('是否公开', default=1)
    reply = models.ForeignKey('self', blank=True, null=True,
                              related_name='reply_comments',
                              on_delete=models.CASCADE,
                              verbose_name='回复id')
    images = GenericRelation(ImageRelated, related_query_name='rel_comment_images',
                             verbose_name='关联的图片')

    class Meta:
        db_table = 'sight_comment'
        ordering=['-love_count','-created_at']
