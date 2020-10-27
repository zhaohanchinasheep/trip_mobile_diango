from system.serializers import BaseImageSerializer
from utils.serializers import BaseListPageSerializer, BaseSerializer


class SightListSerializer(BaseListPageSerializer):
    """景点列表，需要重写get_objects"""

    def get_object(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'main_img': obj.main_img.url,
            'score': obj.score,
            'min_price': obj.min_price,
            'province': obj.province,
            'city': obj.city,
            'comment_count': 0
        }


class SightDetailSerializers(BaseSerializer):
    """景点详情，需要重写to_dict()函数"""

    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'img': obj.banner_img.url,
            'content': obj.content,
            'score': obj.score,
            'province': obj.province,
            'min_price': obj.min_price,
            'area': obj.area,
            'town': obj.town,
            'comment_count': 0

        }


class SightCommentSerializers(BaseListPageSerializer):
    """评论列表数据封装"""

    def get_object(self, obj):
        user = obj.user
        images = []
        for image in obj.images.filter(is_valid=True):
            images.append(BaseImageSerializer(image).to_dict())

        return {
            'user': {'pk': user.pk,
                     'nickname': user.nickname
                     },
            'pk': obj.pk,
            'content': obj.content,
            'is_top': obj.is_top,
            'love_count': obj.love_count,
            'score': obj.score,
            'images': images
        }


class TicketListSerializer(BaseListPageSerializer):
    """门票列表，需要重写get_objects"""

    def get_object(self, obj):
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.price,
            'discount': obj.discount,
            'total_stock': obj.total_stock,
            'remain_stock': obj.remain_stock
        }


class SightInfoSerializer(BaseSerializer):

    def to_dict(self):
        obj = self.obj
        return {'pk': obj.pk,
                'entry_explain': obj.entry_explain,
                'play_way': obj.play_way,
                'tips': obj.tips,
                'traffic': obj.traffic

                }


class ImageListSerializer(BaseListPageSerializer):
    def get_object(self, obj):
        return {
            'img': obj.img.url,
            'summary': obj.summary
        }
