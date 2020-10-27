# 将接口数据配置成可重用的数据
class BaseSerializer(object):
    """基类：单个对象返回为字典类型
    :param:obj
    :return:dict"""

    def __init__(self, obj):
        self.obj = obj

    def to_dict(self):
        """所有继承这个类的子类，都需要重写此方法"""
        return {}


class MetaSerializer(object):
    """元数据基类：分页列表中的元数据"""

    def __init__(self, page, page_count, total_count):
        """
        :param page: 当前页码
        :param page_count: 总页数
        :param total_count: 总记录数
        """
        self.page = page
        self.page_count = page_count
        self.total_count = total_count

    def to_dict(self):
        """将传入的数据变成字典形式输出"""
        return {
            'total_count': self.total_count,
            'pag_count': self.page_count,
            'current_page': self.page
        }


class BaseListPageSerializer(object):
    """分页封装"""

    def __init__(self, page_obj, paginator=None, object_list=[]):
        self.page_obj = page_obj
        self.paginator = paginator if paginator else page_obj.paginator
        self.object_list = object_list if object_list else page_obj.object_list

    def get_object(self, obj):
        """用于获取objects中的内容，由子类重写"""
        return {}

    def to_dict(self):
        page = self.page_obj.number
        page_count = self.paginator.num_pages
        total_count = self.paginator.count
        # meta用于接收MetaSerializer类中to_dict返回的字典
        meta = MetaSerializer(page=page, page_count=page_count, total_count=total_count).to_dict()
        objects = []
        for obj in self.object_list:
            objects.append(self.get_object(obj))
        return {"meta": meta,
                "objects": objects}
