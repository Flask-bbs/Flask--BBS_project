# -*- encoding: utf-8 -*-
"""
@File    : task.py
@Time    : 2020/6/6 20:37
@Author  : chen
clery的任务执行文件：task.py
"""
from celery import Celery
from flask_mail import Message
from exts import mail
from flask import Flask
import config

app = Flask(__name__)                 # 新创建一个app用于执行clery异步发送，为了防止互相引用

mail.init_app(app)                    # 初始化


def make_celery(app):                 # 使用clery运行app
    celery = Celery(
        app.import_name,
        backend=config.CELERY_BROKER_URL,
        broker=config.CELERY_RESULT_BACKEND
        # backend=app.config['CELERY_RESULT_BACKEND'],
        # broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)              # 导入配置文件

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)

