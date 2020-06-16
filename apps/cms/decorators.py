# -*- encoding: utf-8 -*-
"""
@File    : decorators.py
@Time    : 2020/5/12 22:38
@Author  : chen
验证后台登录信息装饰器：apps/cms/decorators.py
"""
# 装饰器方法实现另一种判定后台用户当前界面是否是登录界面，不是就重定向到登录界面
from flask import session, g
from flask import redirect, url_for
# 双层装饰器修饰
from functools import wraps


def login_required(func):                    # 验证是否登录，没有就重定向到后台登录页面
    def inner(*args, **kwargs):              # 内层函数
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))
    return inner


# 装饰器传参   判定用户不同模块的权限，进行验证显示
def permission_required(permission):
    def outter(func):
        # print(func)                                    # <function posts at 0x0000018950B76BF8>，views.py文件中的posts路由
        # print(type(func))                              # <class 'function'> 类
        @wraps(func)                                     # func需要传参，就需要用wraps
        def inner(*args, **kwargs):                      # 内层函数
            user = g.cms_user
            if user.has_permissions(permission):         # 判断g对象的权限
                return func(*args, **kwargs)             # 执行该方法
            else:
                return redirect(url_for('cms.index'))    # 跳转回首页/cms/index/
        return inner
    return outter
