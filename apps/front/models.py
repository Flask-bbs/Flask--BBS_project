# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/5/11 10:00
@Author  : chen
前台模型文件 apps/front/models.py
"""
# 前台管理的模型
from exts import db                   # 数据库连接
import shortuuid                      # 前台用户id加密
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash         # 导入密码加密，解密方法的库
import enum                           # 导入枚举
from markdown import markdown         # 导入帖子编辑的markdown显示功能库
import bleach        # 导入帖子编辑的markdown显示功能库


# 性别选择的类
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


#   前台用户模型类
class Front_User(db.Model):
    __tablename__ = "front_user"
    # id 类型不用db.Integer类型，使用String是为了防止爆破，同时使用shortuuid进行加密
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)             # 非空唯一
    username = db.Column(db.String(150), nullable=False)
    _password = db.Column(db.String(150), nullable=False)                         # 密码加密操作修改字段
    email = db.Column(db.String(50), unique=True)
    
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(150))                                            # 头像，二进制数据
    signatrue = db.Column(db.String(500))                                         # 签名
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)            # 性别枚举类，默认未知
    join_time = db.Column(db.DateTime, default=datetime.now)  # 默认当前时间
    
    # 修改密码加密操作，manage.py映射数据库时候，使用字段保持相同，由于字段太多，使用传参形式
    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:                       # 如果传参中包含有password
            self.password = kwargs.get('password')     # 获取该参数值赋值给password
            kwargs.pop('password')                     # 模型参数中是_password，不是password，弹出
        
        # super(FrontUser, self).__init__(*args, **kwargs)   # python2的写法
        super().__init__(*args, **kwargs)

    # 密码加密操作
    @property
    def password(self):             # 密码取值
        return self._password

    @password.setter                # 密码加密
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    # 用于验证前台登录密码是否和数据库一致，raw_password是前台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)  # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result
    
    
# 帖子编辑提交模型
class PostModel(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=True)                                      # 帖子标题
    content = db.Column(db.Text, nullable=True)                                           # 帖子内容
    content_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)                            # 默认当前时间
    
    # 阅读数量字段
    read_count = db.Column(db.Integer, default=0)
    
    # 外键，用于查询排序
    board_id = db.Column(db.Integer, db.ForeignKey('cms_board.id'))      # 'cms_board.id'中cms_board是cms/models.py的表名
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))# 这里的id使用String是因为上面定义前台用户id时，使用的就是Str类型shortuuid

    # 反向查询属性,posts.author
    board = db.relationship("BoardModel", backref="posts")              # posts变成cms/models/BoardModel的属性
    author = db.relationship("Front_User", backref="posts")             # posts变成Front_User的属性

    # 实现将用户输入的content文件text类型转换成content_html的html文件，再进行存储
    @staticmethod
    def content_to_content_html(target, value, oldvalue, initiator):
        # content_html文件中允许使用的标签集合
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'ol', 'pre',
                        'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe',
                        'p', 'br', 'span', 'hr', 'src', 'class']
        # content_html文件中允许使用的属性
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}
        # 目标文件content_html，由bleach库进行转换         markdown将源文件显示成html文件
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),                                # output_format='html'输出格式为html
            tags=allowed_tags, strip=True, attributes=allowed_attrs))             # strip=True去空格
        
        
# 监听PostModel.content文件如果调用了set方法，就调用content_to_content_html方法进行转换格式到html文件
db.event.listen(PostModel.content, 'set', PostModel.content_to_content_html)


# 添加评论  模型
class CommentModel(db.Model):
    __tablename__ = "comment"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)                             # 帖子内容
    create_time = db.Column(db.DateTime, default=datetime.now)              # 默认当前时间

    # 添加评论的作者
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))       # 外键关联front_user表中的id字段
    # 帖子id   外键关联post表中的id字段
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    # 反向属性backref命名任意，调用的时候需要一致
    post = db.relationship("PostModel", backref="comments")
    author = db.relationship("Front_User", backref="comments")