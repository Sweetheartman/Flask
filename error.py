#!/user/bin/python3
# -*- codeing:utf-8 -*-
'''
  统一自定义异常处理
'''
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(message=message, **kwargs)
    return response,code


def invalid_token():
    response, code = api_abort(return_code.Unauthorized, message='invalid token')
    return response, code


def token_missing():
    response, code = api_abort(return_code.Unauthorized, message='token missed')
    return response, code


def token_expired():
    response, code = api_abort(return_code.Forbidden, message='token expired')
    return response, code


class ValidationError(ValueError):
    pass

# 简单列了一些，别的类型自己可以根据需要扩展补充

def validation_error(e):
    return api_abort(400, e.args[0])
