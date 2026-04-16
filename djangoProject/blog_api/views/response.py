from rest_framework.response import Response
from rest_framework import status


class ApiResponse:
    SUCCESS_CODE = 200
    CREATED_CODE = 201
    BAD_REQUEST_CODE = 400
    UNAUTHORIZED_CODE = 401
    FORBIDDEN_CODE = 403
    NOT_FOUND_CODE = 404
    ERROR_CODE = 500

    @staticmethod
    def success(data=None, msg="success", code=None):
        if code is None:
            code = ApiResponse.SUCCESS_CODE
        response_data = {
            "code": code,
            "msg": msg
        }
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status.HTTP_200_OK)

    @staticmethod
    def created(data=None, msg="创建成功", code=None):
        if code is None:
            code = ApiResponse.CREATED_CODE
        response_data = {
            "code": code,
            "msg": msg
        }
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status.HTTP_201_CREATED)

    @staticmethod
    def error(msg="操作失败", code=None, errors=None):
        if code is None:
            code = ApiResponse.ERROR_CODE
        response_data = {
            "code": code,
            "msg": msg
        }
        if errors is not None:
            response_data["errors"] = errors
        return Response(response_data, status=code)

    @staticmethod
    def bad_request(msg="请求错误", errors=None):
        return ApiResponse.error(
            msg=msg,
            code=ApiResponse.BAD_REQUEST_CODE,
            errors=errors
        )

    @staticmethod
    def unauthorized(msg="未授权"):
        return ApiResponse.error(
            msg=msg,
            code=ApiResponse.UNAUTHORIZED_CODE,
            http_status=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def forbidden(msg="禁止访问"):
        return ApiResponse.error(
            msg=msg,
            code=ApiResponse.FORBIDDEN_CODE,
            http_status=status.HTTP_403_FORBIDDEN
        )

    @staticmethod
    def not_found(msg="资源不存在"):
        return ApiResponse.error(
            msg=msg,
            code=ApiResponse.NOT_FOUND_CODE,
            http_status=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def no_content(msg="操作成功"):
        return Response({
            "code": ApiResponse.SUCCESS_CODE,
            "msg": msg
        }, status=status.HTTP_204_NO_CONTENT)
