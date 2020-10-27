from utils.serializers import BaseSerializer


class BaseImageSerializer(BaseSerializer):
    """图片信息封装"""
    def to_dict(self):
        image = self.obj
        return {
            'img':image.img.url,
            'summary':image.summary
        }


