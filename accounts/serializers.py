from utils.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    """用户基础信息"""

    def to_dict(self):
        user = self.obj
        return {
            'nickname': user.nickname,
            'avatar': user.avatar.url
        }


class UserProfileSerializer(BaseSerializer):
    """用户详细信息返回"""

    def to_dict(self):
        profile = self.obj
        return {
            'real_name': profile.real_name,
            'sex': profile.sex,
            # 返回sex值的中文信息
            'sex_display': profile.get_sex_display()
        }
