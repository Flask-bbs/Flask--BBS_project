# -*- encoding: utf-8 -*-
"""
@File    : decorators.py
@Time    : 2020/5/12 22:38
@Author  : chen
验证前台登录信息装饰器：apps/front/decorators.py
"""
# 装饰器方法实现另一种判定后台用户当前界面是否是登录界面，不是就重定向到登录界面
from flask import session, g
from flask import redirect, url_for
# 双层装饰器修饰
from functools import wraps


def login_required(func):
    @wraps(func)                                              # 没传参的时候，可以省略wraps修饰
    def inner(*args, **kwargs):                               # 内层函数
        if 'front_user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("front.signin"))           # 重定向到前台登录界面
    return inner

