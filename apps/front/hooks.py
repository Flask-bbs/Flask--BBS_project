# -*- encoding: utf-8 -*-
"""
@File    : hooks.py
@Time    : 2020/5/13 9:36
@Author  : chen
保存g对象文件：apps/front/hooks.py
"""
from flask import request, session, url_for, redirect, g   # g对象全局变量gloabl，方便调用
from .views import front_bp
from .models import Front_User


# 钩子函数 ,所有操作前执行该方法，判断当前界面是否是登录界面,不是就将url重定向到登录界面
@front_bp.before_request
def before_request():
    # 判断front_user_id是否登陆过，登录之后就返回用户名到前台页面
    if 'front_user_id' in session:
        user_id = session.get('front_user_id')        # 调用session中user_id
        user = Front_User.query.get(user_id)          # 通过user_id查询到用户对象，方便前端界面调用对象中的字段属性
        if user:
            g.front_user = user                       # 赋值给g对象，全局变量g.front_user用于渲染到前台界面
