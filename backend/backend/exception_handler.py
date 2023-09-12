from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        custom_response = {
            "error": response.data  # 将原始异常数据包装在 "error" 字段内
        }
        response.data = custom_response
        response.data['status_code'] = response.status_code
    return response
