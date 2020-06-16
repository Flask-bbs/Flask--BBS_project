# -*- encoding: utf-8 -*-
"""
@File    : exts.py
@Time    : 2020/5/11 9:51
@Author  : chen

"""
# 第三方引用文件，防止互相引用报错
from flask_sqlalchemy import SQLAlchemy

# 引用flask-mail
from flask_mail import Mail

db = SQLAlchemy()
# 引入Mail()
mail = Mail()