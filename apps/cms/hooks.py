# -*- encoding: utf-8 -*-
"""
@File    : hooks.py
@Time    : 2020/5/13 9:36
@Author  : chen
后台钩子函数文件：apps/cms/hooks.py
"""
from flask import request, session, url_for, redirect, g   # g对象全局变量gloabl，方便调用
from .views import cms_bp
from .models import CMS_User
from .models import CMSPersmission                         # 导入CMSPersmission到上下文管理器中，方便全局调用


# 钩子函数 ,所有操作前执行该方法，判断当前界面是否是登录界面,不是就将url重定向到登录界面
@cms_bp.before_request
def before_request():
    # print(request.path)                                       # 输出的是网页url的后缀，即/cms/login/
    if not request.path.endswith(url_for('cms.login')):         # 判断当前所在url是否是/cms/login/，不是代表不在后台登录界面
        user_id = session.get('user_id')                        # 登陆之后，获取登录时候记录的session中的user_id
        if not user_id:                                         # 若没有user_id，说明登录不成功
            return redirect(url_for('cms.login'))               # 重定向到后台登录界面

    # 判断user_id是否登陆过，登录之后就返回用户名到CMS后台管理系统
    if 'user_id' in session:
        user_id = session.get('user_id')                        # 调用session中user_id
        user = CMS_User.query.get(user_id)                      # 通过user_id查询到用户对象，方便前端界面调用对象中的字段属性
        if user:
            g.cms_user = user                                   # 赋值给g对象，全局变量g.cms_user用于渲染到后台管理界面cms_index.html

# 上面的代码相对于下面的来说比较简单，下面的是将对象中的字段属性单独来调用并修改为全局变量，上面只是将完整的一个对象变成全局变量
'''
    # 判断user_id是否登陆过，登录之后就返回用户名到CMS后台管理系统
    if 'user_id' in session:                              # user_id在session中，说明cms用户已经登录了
        user_name = session.get('user_name')              # 从session中调用user_username
        user_email = session.get('user_email')            # 从session中调用user_email,用于设置为全局变量，渲染到cms_profile.html中
        user_join_time = session.get('user_join_time')    # 从session中调用user_join_time,用于设置为全局变量，渲染到cms_profile.html中

        if user_name:
            g.cms_user = user_name                        # 赋值给g对象，全局变量g.cms_user用于渲染到后台管理界面cms_index.html
            g.cms_email = user_email                      # 设置为全局变量，渲染到cms_profile.html中
            g.cms_join_time = user_join_time              # 设置为全局变量，渲染到cms_profile.html中
'''

# 上下文处理器,返回的字典中的键可以在模板上下文中使用。
@cms_bp.context_processor
def cms_context_processor():
    return {"CMSPersmission": CMSPersmission}             # 模板上下文中使用 cms_base.html中使用
