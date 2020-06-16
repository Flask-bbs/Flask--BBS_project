# -*- encoding: utf-8 -*-
"""
@File    : manage.py
@Time    : 2020/5/10 17:36
@Author  : chen
映射模型到数据库中文件： manage.py
"""
from flask_script import Manager
from bbs import app                                         # 需要将当前文件夹设置为当前根目录，才不会报错
from flask_migrate import Migrate, MigrateCommand             # 映射数据库
from exts import db
import random

# 导入后台模型 才能映射到数据库 ，导入轮播图和文章的管理模块
from apps.cms.models import (
    BannerModel,                      # 轮播图模型
    BoardModel,                       # 后台板块模型
    HighlightPostModel,               # 后台帖子加精模型
    CMS_User,                         # 导入后端的模型
    CMSRole,                          # 角色模型
    CMSPersmission,                   # 角色权限定义
)

# 导入前台模型 才能映射到数据库
from apps.front.models import (
    Front_User,                       # 前台用户模型
    PostModel,                        # 帖子模型
    CommentModel                      # 添加评论模型
)

manage = Manager(app)

Migrate(app, db)
manage.add_command('db', MigrateCommand)


# 命令行添加后台用户
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
@manage.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMS_User(username=username, password=password, email=email)
    # 添加映射到数据库，提交至数据库
    db.session.add(user)
    db.session.commit()
    print("cms后台用户添加成功")


# 命令行添加前台用户
@manage.option('-t', '--telephone', dest='telephone')
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = Front_User(telephone=telephone, username=username, password=password)
    # 添加映射到数据库，提交至数据库
    db.session.add(user)
    db.session.commit()
    print("front前台用户添加成功")


# 添加角色  不传参用command
@manage.command
def create_role():
    # 访问者
    visitor = CMSRole(name="访问者", desc="只能查看数据，不能修改数据")
    visitor.permission = CMSPersmission.VISITOR                         # 权限
    
    # 运营人员
    operator = CMSRole(name="运营人员", desc="管理评论、帖子、管理前台用户")
    # 权限或运算，代表包含有运算中的所有权限     二进制的运算 001|010=011
    operator.permission = CMSPersmission.VISITOR | CMSPersmission.POSTER | CMSPersmission.CMSUSER | \
                          CMSPersmission.COMMENTER | CMSPersmission.FRONTUSER
    
    # 管理员
    admin = CMSRole(name="管理员", desc="拥有本系统大部分权限")
    admin.permission = CMSPersmission.VISITOR | CMSPersmission.POSTER | CMSPersmission.CMSUSER | \
                          CMSPersmission.COMMENTER | CMSPersmission.FRONTUSER | CMSPersmission.BOARDER

    # 开发人员
    developer = CMSRole(name="开发人员", desc="拥有本系统所有权限")
    developer.permission = CMSPersmission.ALL_PERMISSION
    
    # 提交数据库   添加身份字段到数据库中的表,
    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()
    return "创建角色成功"


# 测试用户权限
@manage.command
def test_permission():
    # user = CMS_User.query.first()                          # 查询第一个用户，当时创建的用户还没有关联权限，所以应该是没有权限
    user = CMS_User.query.get(3)
    print(user)                                              # 显示用户信息
    if user.has_permissions(CMSPersmission.VISITOR):         # has_permissions方法判定是否具有该权限
        print("这个用户有访问者的权限！")
    else:
        print("这个用户有访问者的权限！")


# 添加用户到角色里面
@manage.option("-e", "--email", dest="email")
@manage.option("-n", "--name", dest="name")
def add_user_to_role(email, name):
    user = CMS_User.query.filter_by(email=email).first()                   # 通过邮箱查询用户
    if user:
        role = CMSRole.query.filter_by(name=name).first()                  # 邮箱存在的前提下，通过name查询角色
        if role:
            role.users.append(user)                                        # 将用户添加到角色中，list类型数据，role.users是CMSRole中的外键
            db.session.commit()                                            # 映射到数据库
            print("用户添加到角色成功")
        else:
            print("该角色不存在")
    else:
        print("邮箱不存在")


# 数据库添加多条帖子信息，进行验证分页功能
@manage.command
def create_test_post():
    for i in range(1, 200):                                  # 循环产生200篇帖子信息
        title = "标题%s" % i
        content = "内容%s" % i
        author = Front_User.query.first()                    # 查询数据库中所有的用户信息
        
        post = PostModel(title=title, content=content)       # 循环的标题内容信息添加给PostModel
        post.author = author
        post.board_id = random.randint(2, 7)                # 随机选择cms_board表中的id的值为2-7
        db.session.add(post)
        db.session.commit()
    print("测试帖子添加成功！")
    

if __name__ == '__main__':
    manage.run()
