# -*- encoding: utf-8 -*-
"""
@File    : config.py
@Time    : 2020/5/11 10:08
@Author  : chen
项目配置文件：config.py
"""
import os    # 导入随机字符串用于加密session

# 127.0.0.1
HOSTNAME = "localhost"
DATABASE = "demo_bbs"
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DB_URL = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

'''
# 创建引擎并生成Base类
engine = create_engine(DB_URL)
Base = declarative_base(engine)
'''
SQLALCHEMY_DATABASE_URI = DB_URL           # 数据库连接成功

# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
# Set it to True or False to suppress this warning.'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
# 这里是为了解决上面的警告
SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = os.urandom(15)        # 产生随机15位字符串

# flask-mail配置信息
MAIL_SERVER = 'smtp.qq.com'       # 发送邮箱的服务地址  这里设置为QQ邮箱服务器地址
MAIL_PORT = '587'                 # 发送端口为465或者587
MAIL_USE_TLS = True               # 端口为587对应的服务
# MAIL_USE_SSL = True             # 端口为465对应的服务  二选一即可

MAIL_USERNAME = '727506892@qq.com'   # 使用者的邮箱
MAIL_PASSWORD = 'lzpihkhrsbhqbajd'   # 不是QQ邮箱登录密码，是QQ邮箱授权码获取，用于第三方登录验证
MAIL_DEFAULT_SENDER = '727506892@qq.com'   # 默认发送者，暂时先设置为自己

TEMPLATES_AUTO_RELOAD = True         # 修改模板，ajax自动启动


# 每页显示数据数目
PER_PAGE = 10

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

