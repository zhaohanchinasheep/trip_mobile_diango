from django.http import JsonResponse


class NotFoundJsonResponse(JsonResponse):
    """400对应的json响应"""
    status_code = 404

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "404000",
            "error_msg": "您访问的内容不存在或已被删除"
        }
        super().__init__(data, *args, **kwargs)


class BadJsonResponse(JsonResponse):
    """表单请求验证没有通过错误信息"""
    status_code = 400

    def __init__(self, err_list=[], *args, **kwargs):
        data = {
            "error_code": "400000",
            "error_msg": "参数格式不正确（表单请求验证没有通过）",
            'error_list': err_list
        }
        super().__init__(data, *args, **kwargs)


class MethodNotAllowResponse(JsonResponse):
    """请求方式不被允许"""
    status_code = 405

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "405000",
            "error_msg": "请求方式不正确"
        }
        super().__init__(data, *args, **kwargs)


class UnauthorizedJsonResponse(JsonResponse):
    status_code = 401

    def __init__(self, *args, **kwargs):
        data = {
            "error_code": "415000",
            "error_msg": "请登陆"
        }
        super().__init__(data, *args, **kwargs)

