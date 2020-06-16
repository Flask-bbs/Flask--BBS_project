# -*- encoding: utf-8 -*-
"""
@File    : restful.py
@Time    : 2020/5/16 22:04
@Author  : chen

"""
# 此文件是定义项目中使用到的各种代称和规范
from flask import jsonify


class HttpCode(object):
    ok = 200                # 网页访问成功
    unautherror = 401       # 用户需要验证
    paramserror = 400       # 参数错误
    servererror = 500       # 服务器错误
    
    
# 定义访问网页状态的的函数
def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data})


# 网页访问成功   状态码200
def success(message="", data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)


# 网页访问缺少权限 用户需要验证   状态码401
def unauth_error(message, data=None):
    return restful_result(code=HttpCode.unautherror, message=message, data=data)


# 网页访问参数错误   状态码400
def params_error(message, data=None):
    return restful_result(code=HttpCode.paramserror, message=message, data=data)


# 网页访问服务器错误  状态码500
def server_error(message, data=None):
    return restful_result(code=HttpCode.servererror, message=message, data=data)
