# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/5/11 9:59
@Author  : chen
前台蓝图文件：apps/front/views.py
"""
# 前台的蓝图文件  类视图函数写在这里
from flask import (
    Blueprint,
    render_template,
    views,
    make_response,                  # make_response生成response对象，用于返回前端模板
    request,
    session,
    g,
)

# 导入图像验证码生成文件
from utils.captcha import Captcha

# 图形验证码image是二进制数据，需要转换成字节流才能使用
from io import BytesIO

# 将图形验证码保存到Redis         restful输出信息弹窗
from utils import redis_captcha, restful

# 验证码表单信息验证
from .forms import (
    SignupForm,               # 注册的Form表单信息收集
    SigninForm,               # 登录的Form表单信息收集
    AddPostForm,              # 帖子提交表单信息
    AddCommentForm,           # 添加帖子评论
)

# 导入前台用户模型
from .models import (
    Front_User,
    PostModel,
    CommentModel,             # 评论模型
)

# 导入数据库连接 db
from exts import db

# 确保URL安全的文件：utils/safe_url.py
from utils import safe_url

from apps.cms.models import (
    BannerModel,                      # 导入后台轮播图模型BannerModel
    BoardModel,                       # 导入后台板块管理模型
    HighlightPostModel,               # 帖子加精模型
)
# 导入分页功能库
from flask_paginate import Pagination, get_page_parameter
# 导入前台界面权限验证装饰器
from .decorators import login_required
# 导入配置文件
import config
from sqlalchemy import func                      # 导入求和方法

front_bp = Blueprint("front", __name__)          # 前端不用前缀，直接在首页显示，front是蓝图，在front_signup.html调用生成图形验证码时候需要用

# 权限验证  需要在front_bp产生后，再导入
from .hooks import before_request


# BBS的首页界面路由
@front_bp.route("/")
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)   # 通过权重查询，每页显示4条
    boards = BoardModel.query.all()                                              # 查询板块中的所有
    board_id = request.args.get('board_id', type=int, default=None)              # get方法需要使用args，注意这里的数据类型需要改成int
    
    # 接收参数st的状态值，用于判断不同种类的排序
    sort = request.args.get('st', type=int, default=1)
    
    page = request.args.get(get_page_parameter(), type=int, default=1)           # 获取当前页码
    start = (page-1)*config.PER_PAGE                                             # 起始页码是(当前页码-1)*10
    end = start + config.PER_PAGE                                                # 每页都是起始页码+10
    
    # 接收参数st，根据sort的参数不同，判断不同种类的排序
    query_obj = None
    if sort == 1:                                                                # 用户选择最新帖子的顺序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())       # 帖子创建时间倒序
    elif sort == 2:                                                              # 用户选择精华帖子的顺序
        query_obj = db.session.query(PostModel).join(HighlightPostModel).order_by(  # 内关联PostModel,HighlightPostModel交集
            HighlightPostModel.create_time.desc()                                   # 根据创建时间倒序排序
        )                     # 帖子加精模型
    elif sort == 3:                                                              # 用户选择阅读最多的顺序
        query_obj = PostModel.query.order_by(PostModel.read_count.desc())        # 查询阅读数量
    elif sort == 4:                                                              # 用户选择评论最多的顺序
        query_obj = db.session.query(PostModel).join(CommentModel).group_by(
            PostModel.id                                                         # 先分组，根据不同帖子id进行分组再排序
        ).order_by(
            func.count(CommentModel.id).desc()                                   # 通过评论总数排序
        )
       
    # 实现根据不同board_id进行帖子分类显示，即用户选择不同板块，显示的帖子种类相对应
    if board_id:
        posts = query_obj.filter(PostModel.board_id == board_id).slice(start, end)        # slice(start, end)分页
        total = query_obj.filter(PostModel.board_id == board_id).count()                  # 计算该板块的总数
    else:
        posts = query_obj.slice(start, end)                                    # 帖子信息传输，如果用户不选择板块，查询所有
        total = query_obj.count()                                              # 计算帖子总数

    # pagination是一个对象,bs_version=3是bootstrap的版本为3,per_page参数添加，pagination.links正常显示所有
    pagination = Pagination(bs_version=3, page=page, total=total,
                            per_page=config.PER_PAGE,                          # config.py中的每页10条数据
                            inner_window=3, outer_window=1)                    # inner_window=3是内层显示页码的样式，默认为2，
    # print(pagination.links)                                                  # 当数据量小的时候，不显示，添加per_page参数就能解决
    
    context = {                                                                # 多种数据传输到前台界面
        "banners": banners,
        "boards": boards,
        "current_board_id": board_id,
        "posts": posts,
        "pagination": pagination,
        "current_sort": sort,
        
    }
    
    return render_template("front/front_index.html", **context)            # 渲染到首页界面,查询数据传输到前台界面


# 图形验证码路由
@front_bp.route("/captcha/")
def graph_captcha():
    try:                                                 # 异常处理
        # 图像验证码生成文件中返回两个参数   text, image
        text, image = Captcha.gene_graph_captcha()      # 生成图形验证码，image是二进制数据，需要转换成字节流才能使用
        print("发送的图形验证码是：{}".format(text))
        
        # 将图形验证码保存到Redis数据库中
        redis_captcha.redis_set(text.lower(), text.lower())  # redis_set中需要传参key和value，text没有唯一对应的key，只能都传参text
        
        # BytesIO是生成的字节流
        out = BytesIO()
        image.save(out, 'png')                          # 把图片image保存在字节流中，并指定为png格式
        # 文件流指针
        out.seek(0)                                     # 从字节流最初开始读取
        # 生成response对象，用于返回前端模板中
        resp = make_response(out.read())
        resp.content_type = 'image/png'                 # 指定数据类型
    except:
        return graph_captcha()                          # 没有生成验证码就再调用一次
        
    return resp                                         # 返回对象


# 测试referrer的跳转
@front_bp.route("/test/")
def test():
    return render_template("front/front_test.html")


# 用户注册类视图
class SingupView(views.MethodView):
    def get(self):
        # 图像验证码生成文件中返回两个参数   text, image
        # text, image = Captcha.gene_graph_captcha()
        # print(text)                      # 验证码
        # print(image)                     # 图形文件，图形类<PIL.Image.Image image mode=RGBA size=100x30 at 0x1EFC9000C88>

        # 从当前页面跳转过来就是None   从其他页面跳转过来输出就是上一个页面信息     referrer是页面的跳转
        # print(request.referrer)                           # http://127.0.0.1:9999/test/
        
        return_to = request.referrer
        # 确保URL安全的文件：utils/safe_url.py
        print(safe_url.is_safe_url(return_to))              # 判断return_to是否来自站内，是否是安全url，防爬虫
        
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):       # 跳转的url不能是当前页面，request.url是当前的url地址
            return render_template("front/front_signup.html", return_to=return_to)           # return_to渲染到前端界面
        else:
            return render_template("front/front_signup.html")                                # 如果没获取url,直接渲染注册界面
        
    # 验证码的form表单信息提交验证
    def post(self):
        form = SignupForm(request.form)                       # 收集表单信息
        
        # 表单验证通过
        if form.validate():
            # 保存到数据库
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data                    # forms表单信息
            
            # 前台用户模型数据添加到数据库
            user = Front_User(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()                                                   # 提交到数据库
            
            # 表单验证通过，提交到数据库成功
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())                  # 表单信息验证出错


# 用户登录的类视图
class SinginView(views.MethodView):
    def get(self):
        return_to = request.referrer                                                    # referrer是上一个url
    
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):  # 跳转的url不能是当前页面，判断url是否安全
            return render_template("front/front_signin.html", return_to=return_to)      # return_to渲染到前端界面
        else:
            return render_template("front/front_signin.html")                           # 如果没获取url,直接渲染注册界面
    
    def post(self):
        form = SigninForm(request.form)                                            # 登录界面的Form表单信息
        
        if form.validate():                                                        # 表单信息存在
            # 收集form表单信息
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            
            user = Front_User.query.filter_by(telephone=telephone).first()         # 通过手机号验证该用户是否存在数据库
            if user and user.check_password(password):                             # 判断密码和用户是否正确
                # 'front_user_id'命名防止与后台验证session相同，会产生覆盖情况bug
                session['front_user_id'] = user.id                                 # 用户的id存储到session中，用于登录验证
                if remember:                                                       # 如果remember状态是1
                    # session持久化
                    session.permanent = True
                return restful.success()                                           # 成功
            else:
                return restful.params_error(message="手机号或者密码错误")           # 密码是、用户不正确
        else:
            return restful.params_error(message=form.get_error())                  # 表单信息不存在，输出异常信息
        

#  帖子编辑提交  的类视图     富文本编辑
class PostView(views.MethodView):
    # 登录验证，实现帖子编辑前进行权限验证
    decorators = [login_required]
    # 表单信息收集，传输
    def get(self):
        # 查询boards数据进行传输
        boards = BoardModel.query.all()                                           # boards是list类型
        return render_template("front/front_apost.html", boards=boards)           # boards数据传输到前端front_apost.html页面
    
    # 帖子的Form表单信息收集查询
    def post(self):
        form = AddPostForm(request.form)                     # 查询帖子提交的Form表单信息
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data                    # 收集表单中提交的信息
            content = form.content.data
            
            # 查询用户信息是否在数据库中存在
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message="没有这个版块名称")           # 数据库中不存在，返回异常信息
            
            # 数据库中board信息存在，传输数据到数据库表中，并修改名称
            post = PostModel(title=title, board_id=board_id, content=content)
            post.board = board                                                   # 外键中的信息修改赋值
            post.author = g.front_user                                           # g对象

            db.session.add(post)
            db.session.commit()
            return restful.success()                                             # 提交成功，为json数据
        else:
            return restful.params_error(message=form.get_error())
            

# 前台 帖子详情 路由
@front_bp.route("/p/<post_id>")                  # 蹄子详情路由需要传参帖子id：post_id
def post_detail(post_id):
    post = PostModel.query.get(post_id)          # 通过post_id查找数据库中的帖子信息
    if not post:
        return restful.params_error(message="帖子不存在！")
    
    # 阅读数量计数
    post.read_count += 1
    db.session.commit()
    
    # 评论数量查询,先查询帖子模型中的id
    comment_count = db.session.query(PostModel).filter(PostModel.id == post_id).join(
        CommentModel                                                                     # 关联查询评论模型
    ).count()                                                                            # 再整体求和
    return render_template("front/front_detail.html", post=post, comment_count=comment_count)  # 查找到帖子信息，传输数据到帖子详情页渲染
 

# 添加评论  的路由
@front_bp.route("/acomment/", methods=['POST'])
@login_required                                      # 登录验证
def add_comment():
    form = AddCommentForm(request.form)              # 网页发送的request.form表单信息放入AddCommentForm进行验证
    if form.validate():
        content = form.content.data                  # form表单信息
        post_id = form.post_id.data
        
        post = PostModel.query.get(post_id)          # 通过post_id查询帖子信息
        if post:
            comment = CommentModel(content=content)  # 将AddCommentForm中验证后的content信息传给CommentModel模型
            # 外键关联，反向属性backref，从CommentModel中调用
            comment.post = post                      # 外键关联的是post表中的id字段
            comment.author = g.front_user            # 将apps/front/hooks.py中的g对象赋值外键的作者的id
            db.session.add(comment)                  # 添加对象信息到数据库
            db.session.commit()
            return restful.success()                 # 提交成功
        else:
            return restful.params_error(message="没有这篇帖子")  # 数据库中查询不到信息
    else:
        return restful.params_error(message=form.get_error())   # 表单验证失败
            
        
# 绑定类视图的路由
front_bp.add_url_rule("/signup/", view_func=SingupView.as_view("signup"))          # "signup"视图中不需要反斜线,决定了url_for的路由地址
front_bp.add_url_rule("/signin/", view_func=SinginView.as_view("signin"))          # "signin"视图中不需要反斜线
front_bp.add_url_rule("/apost/", view_func=PostView.as_view("apost"))              # 绑定帖子编辑提交路由
