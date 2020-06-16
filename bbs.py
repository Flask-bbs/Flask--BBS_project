# -*- encoding: utf-8 -*-
"""
@File    : bbs.py
@Time    : 2020/5/11 9:46
@Author  : chen

"""
# 项目主文件，启动入口

# 前台  front    管理前端界面的逻辑
# 后台  cms      管理后端的操作
# 公有的文件 common

from flask import Flask
import config                              # 配置文件库
from exts import db, mail                  # 第三方库导入db,mail
from apps.cms.views import cms_bp          # 导入后端蓝图文件
from apps.front.views import front_bp      # 导入前端蓝图文件
from apps.common.views import common_bp    # 导入公有蓝图文件
from flask_wtf import CSRFProtect          # CSRF表单保护验证

app = Flask(__name__)

CSRFProtect(app)                           # CSRF保护app

app.config.from_object(config)             # 添加配置

db.init_app(app)                           # 绑定app
mail.init_app(app)                         # mail绑定app

app.register_blueprint(cms_bp)             # 后端蓝图文件注册
app.register_blueprint(front_bp)           # 前端蓝图文件注册
app.register_blueprint(common_bp)          # 公有蓝图文件注册


if __name__ == '__main__':
    app.run(debug=True, port=9999)