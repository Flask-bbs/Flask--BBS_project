# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/5/11 9:59
@Author  : chen
视图文件:apps/cms/views.py文件
"""
# 蓝图文件：实现模块化应用，应用可以分解成一系列的蓝图   后端的类视图函数写在这个文件
from flask import (
    request, redirect, url_for,                      # 页面跳转redirect   request请求收集
    Blueprint, render_template, views, session,      # 定义类视图，显示模板文件
    jsonify, g                                       # jsonify强制转换成json数据
)
from exts import db, mail                            # 数据库中更新密码、邮箱等使用

from apps.cms.forms import (
    LoginForm, ResetPwdForm,                        # ResetPwdForm修改密码的form信息
    ResetEmailForm,                                 # 导入forms.py文件中的邮箱验证的表单信息类
    AddBannerForm,                                  # 导入 添加轮播图 的表单信息
    UpdateBannerForm,                               # 导入 更新轮播图 的表单信息
    AddBoardsForm,                                  # 导入 增加板块管理 的表单信息
    UpdateBoardsForm,                               # 导入 编辑板块管理 的表单信息
)

from apps.cms.models import (
    CMS_User,                                       # 后台用户模型
    CMSPersmission,                                 # CMSPersmission验证用户不同模块权限
    CMSRole,                                        # 用户角色模型
    BannerModel,                                    # 导入 轮播图模型BannerModel
    BoardModel,                                     # 导入 板块管理模型
    HighlightPostModel,                             # 帖子加精模型
)
# 导入 帖子 模型文件
from apps.front.models import PostModel

from .decorators import permission_required            # 传参装饰器验证用户不同模块权限

# 导入装饰器：判断当前界面是否是登录界面,不是就将url重定向到登录界面,一般不用，使用的主要是钩子函数
from .decorators import login_required

# 导入restful.py中的访问网页状态码的函数          redis_captcha：redis存储、提取、删除验证码功能
from utils import restful, random_captcha, redis_captcha           # 随机生成验证码函数random_captcha()

# 导入flask-mail中的Message
from flask_mail import Message

# 导入clery的异步发送邮件模块
from task import send_mail

cms_bp = Blueprint("cms", __name__, url_prefix='/cms/')     # URL前缀url_prefix

# 钩子函数是在cms_bp创建之后才创建的，顺序在cms_bp创建之后
from .hooks import before_request


@cms_bp.route("/")                                          # 后台界面
# @login_required             # 装饰器判定当前界面是否是登录界面，但是需要每个路由函数都要加该装饰器，比较麻烦，推荐使用钩子函数
def index():
    # return "cms index：后端类视图文件"
    return render_template('cms/cms_index.html')  # 登陆之后进入CMS后台管理界面


# 用户注销登录
@cms_bp.route("/logout/")                              # 需要关联到cms/cms_index.html中的注销属性
def logout():
    # session清除user_id
    del session['user_id']
    # 重定向到登录界面
    return redirect(url_for('cms.login'))             # 重定向(redirec)为把url变为重定向的url


# 定义个人中心的路由
@cms_bp.route("/profile/")
def profile():
    return render_template("cms/cms_profile.html")   # 模板渲染(render_template)则不会改变url，模板渲染是用模板来渲染请求的url


# 定义类视图，显示模板文件   用户登录功能实现
class LoginView(views.MethodView):
    def get(self, message=None):                                         # message=None时候不传输信息到cms_login.html页面
        return render_template("cms/cms_login.html", message=message)    # 针对post方法中同样要返回到cms_login.html页面进行代码简化
    
    # 用户登录操作验证
    def post(self):
        # 收集表单信息
        login_form = LoginForm(request.form)
        if login_form.validate():
            # 数据库验证
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data
            
            # 查询数据库中的用户信息
            user = CMS_User.query.filter_by(email=email).first()    # 邮箱唯一，用于查询验证用户
            if user and user.check_password(password):              # 验证用户和密码是否都正确
                session['user_id'] = user.id                        # 查询到用户数据时，保存session的id到浏览器
                # session['user_name'] = user.username                # 将数据库中的user.username保存到session中，在hooks.py中判断
                # session['user_email'] = user.email                  # 将数据库中的email保存到session中,方便html调用信息
                # session['user_join_time'] = user.join_time          # 将数据库中的join_time保存到session中,方便html调用信息
                
                if remember:                                        # 如果用户点击了remember选择，在浏览器中进行数据持久化
                    session.permanent = True                        # 数据持久化，默认31天，需要设置session_key在config.py中
            
                # 登录成功，跳转到后台首页
                return redirect(url_for('cms.index'))               # 在蓝图中必须加cms   跳转到index方法
            else:
                # return "邮箱或密码错误"                              # 登录出错，返回结果
                # return render_template("cms/cms_login.html", message="邮箱或密码错误")  # 登录出错，返回结果渲染到cms_login.html页面
                return self.get(message="邮箱或密码错误")             # 传参到get方法中，多加一个传输错误信息的参数到方法中
        else:
            # print(login_form.errors)                                 # forms.py中的错误信息  字典类型数据
            # print(login_form.errors.popitem())                       # forms.py中的错误信息  元祖类型数据
            # return "表单验证错误"                                     # 错误信息需要渲染到cms_login.html页面
            # return self.get(message=login_form.errors.popitem()[1][0])  # 字典类型数据信息提取
            return self.get(message=login_form.get_error())            # login_form是收集到的表单信息，信息提取放置到forms.py的父类中实现
    
    
# 修改密码的类视图验证
class ResetPwd(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetpwd.html')         # 模板渲染到cms_resetpwd.html
    
    # post提交密码修改
    def post(self):
        # 先审查旧密码是否与数据库中的信息相同
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            # 对象
            user = g.cms_user
            # 将用户输入的密码进行加密检测是否与数据库中的相同
            if user.check_password(oldpwd):
                # 更新我的密码  将新密码赋值，此时的新密码已经经过验证二次密码是否一致
                user.password = newpwd         # user.password已经调用了models.py中的 @property装饰器进行密码加密
                # 数据库更新
                db.session.commit()
                # return jsonify({"code": 400, "message": "密码修改成功"})        # 代码改写为下面
                return restful.success("密码修改成功")             # 调用restful.py中定义的访问网页成功的函数
            else:
                # 当前用户输入的旧密码与数据库中的不符
                # return jsonify({"code": 400, "message": "旧密码输入错误"})
                return restful.params_error(message="旧密码输入错误")      # 参数错误
        else:
            # ajax 需要返回一个json类型的数据
            # message = form.errors.popitem()[1][0]                     # 收集错误信息
            # return jsonify({"code": 400, "message": message})         # 将数据转换成json类型
            return restful.params_error(message=form.get_error())       # 参数错误，信息的收集在forms.py的父类函数中实现  form是收集到的信息
        

# 定义修改邮箱的类视图 验证
class ResetEmail(views.MethodView):
    def get(self):
        return render_template("cms/cms_resetemail.html")      # 返回到修改邮箱页面url
    
    def post(self):
        form = ResetEmailForm(request.form)                    # 接收邮箱验证的form表单信息
        if form.validate():                                    # 验证表单信息是否通过
            email = form.email.data                            # 获取form表单中填写的邮箱地址
            
            # 查询数据库
            # CMS_User.query.filter_by(email=email).first()
            # CMS_User.query.filter(CMS_User.email == email).first()
            g.cms_user.email = email                           # 数据库中的查询在apps/cms/hooks.py文件中确定了该用户的数据库信息,用全局对象g.cms_user修改邮箱
            db.session.commit()
            return restful.success()                           # 邮箱修改成功
        else:
            return restful.params_error(form.get_error())      # form是这个类中的所有表单信息
        
        
# 发送测试邮件进行验证
@cms_bp.route("/send_email/")
def send_mail_1():                                                  # 防止与clery中异步发送邮件方法名相同
    message = Message('邮件发送', recipients=['727506892@qq.com'], body='测试邮件发送')   # 主题：邮件发送;收件人：recipients;邮件内容：测试邮件发送
    mail.send(message)                   # 发送邮件
    return "邮件已发送"


# 邮件发送
class EmailCaptcha(views.MethodView):
    def get(self):                                  # 根据resetemail.js中的ajax方法来写函数，不需要post请求
        email = request.args.get('email')           # 查询email参数是否存在
        if not email:
            return restful.params_error('请传递邮箱参数')
        
        # 发送邮件，内容为一个验证码：4、6位数字英文组合
        captcha = random_captcha.get_random_captcha(4)            # 生成4位验证码
        # message = Message('BBS论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
        
        # 异常处理
        try:
            send_mail.delay('BBS论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)   # 引用clery异步发送邮件
            # mail.send(message)
        except:
            return restful.server_error(message="服务器错误，邮件验证码未发送！")   # 发送异常，服务器错误
        
        # 验证码保存，一般有时效性，且频繁请求变化，所以保存在Redis中
        redis_captcha.redis_set(key=email, value=captcha)        # redis中都是键值对类型，存储验证码
        return restful.success("邮件验证码发送成功！")
    

# 轮播图管理路由
@cms_bp.route("/banners/")
def banners():
    # 通过模型中定义的权重priority的倒叙来排序
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template("cms/cms_banners.html", banners=banners)           # 传输banners数据到cms_banners.html界面渲染


# 添加轮播图功能路由，且方法需要与static/cms/js/banners.js中绑定的方法POST相同
@cms_bp.route("/abanner/", methods=['POST'])
def abanner():
    form = AddBannerForm(request.form)                  # 接收添加轮播图的form表单信息
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)     # 轮播图模型
        db.session.add(banner)                                                                         # 提交数据库
        db.session.commit()
        return restful.success()                                                                       # 轮播图信息提交成功
    else:
        return restful.params_error(message=form.get_error())                                          # 表单信息错误


# 修改 轮播图 路由，方法与static/cms/js/banners.js中绑定的方法POST相同
@cms_bp.route("/ubanner/", methods=['POST'])
def ubanner():
    # 修改根据banner_id查询再修改
    form = UpdateBannerForm(request.form)             # 表单信息UpdateBannerForm中的request
    if form.validate():                                # 先查询页面表单信息是否存在
        banner_id = form.banner_id.data               # 收集用户输入的表单信息
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        
        banner = BannerModel.query.get(banner_id)     # 通过轮播图的模型BannerModel的banner_id查询数据库中轮播图对象
        if banner:                                     # 再查询数据库对象数据是否存在
            banner.name = name                        # 将UpdateBannerForm中收集到的form信息命名给数据库中的banner对象
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            
            db.session.commit()                       # 数据库信息直接提交修改即可，不用添加新的对象
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())    # 表单信息错误
    

# 删除  轮播图路由，路由命名与banners.js绑定
@cms_bp.route("/dbanner/", methods=['POST'])
def dbanner():
    '''
    request.form.get("key", type=str, default=None)      获取表单数据
    request.args.get("key")                              获取get请求参数
    request.values.get("key")                            获取所有参数
    '''
    # 修改根据banner_id查询再修改，获取post请求参数         get请求方式使用request.args.get()
    banner_id = request.form.get('banner_id')            # 获取表单数据，这里没有单独创建删除的Form表单，使用之前创建的
    if not banner_id:
        return restful.params_error(message="轮播图不存在")
    
    banner = BannerModel.query.get(banner_id)           # 根据banner_id查询数据库
    if banner:
        db.session.delete(banner)                       # 删除该banner
        db.session.commit()
        return restful.success()                        # 返回成功
    else:
        return restful.params_error("轮播图不存在")      # 根据banner_id查询数据库信息不存在
    

# 帖子管理路由 ，需要和cms_base.js中命名的相同才可以
@cms_bp.route("/posts/")
@permission_required(CMSPersmission.POSTER)                # 传参装饰器验证不同用户不同模块权限
def posts():
    posts = PostModel.query.all()                          # 数据库查询帖子信息，进行传输到后端页面cms_posts.html渲染
    return render_template("cms/cms_posts.html", posts=posts)
    

# 帖子 加精的 后台管理，路由名称在static/cms/js/posts.js文件定义好了
@cms_bp.route("/hpost/", methods=['POST'])                # 方法确定为post方式，默认支持的是get方法
@permission_required(CMSPersmission.POSTER)                # 传参装饰器验证不同用户不同模块权限
def hpost():
    # 接收外键，post接收方式使用form
    post_id = request.form.get("post_id")                  # 接收post_id进行查询
    if not post_id:
        return restful.params_error(message="请输入帖子ID")
    
    post = PostModel.query.get(post_id)                    # 从帖子的数据表中查找该帖子对象
    if not post:
        return restful.params_error(message="没有这篇帖子")
    
    highlight = HighlightPostModel()                      # 创建模型
    highlight.post = post                                 # 外键关联，加精帖子补充到新的表中
    db.session.add(highlight)
    db.session.commit()                                   # 提交
    return restful.success()                              # 加精成功，视图函数必须有返回值


# 帖子 取消加精的 后台管理，路由名称在static/cms/js/posts.js文件定义好了
@cms_bp.route("/uhpost/", methods=["POST"])               # 方法确定为post方式，默认支持的是get方法
@permission_required(CMSPersmission.POSTER)                # 传参装饰器验证不同用户不同模块权限
def uhpost():
    # 接收外键，post接收方式使用form
    post_id = request.form.get("post_id")                  # 接收post_id进行查询
    if not post_id:
        return restful.params_error(message="请输入帖子ID")
    
    post = PostModel.query.get(post_id)                     # 从帖子的数据表中查找该帖子对象
    if not post:
        return restful.params_error(message="没有这篇帖子")
    
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()                                     # 提交
    return restful.success()                                # 视图函数必须有返回值


# 评论管理路由
@cms_bp.route("/comments/")
@permission_required(CMSPersmission.COMMENTER)             # 传参装饰器验证不同用户不同模块权限
def comments():
    return render_template("cms/cms_comments.html")


# 板块管理路由
@cms_bp.route("/boards/")
@permission_required(CMSPersmission.BOARDER)               # 传参装饰器验证不同用户不同模块权限
def boards():
    boards = BoardModel.query.all()                        # 数据库查询所有板块名称
    return render_template("cms/cms_boards.html", boards=boards)        # 数据渲染到cms_boards.html


# 增加 板块管理名称 路由,与static/cms/js/banners.js中绑定的方法、路由要相同
@cms_bp.route("/aboard/", methods=['POST'])
@permission_required(CMSPersmission.BOARDER)               # 传参装饰器验证不同用户不同模块权限
def aboards():
    form = AddBoardsForm(request.form)                     # 表单信息传输过来，方便修改调用
    if form.validate():
        name = form.name.data                              # 表单信息收集
        
        board = BoardModel(name=name)                      # 添加信息到板块模型中
        db.session.add(board)
        db.session.commit()                                # 提交数据库
        return restful.success()                           # 数据库添加成功
    else:
        return restful.params_error(message=form.get_error())    # 表单信息错误


# 编辑 板块管理名称 路由,与static/cms/js/banners.js中绑定的方法、路由要相同
@cms_bp.route("/uboard/", methods=['POST'])
@permission_required(CMSPersmission.BOARDER)             # 传参装饰器验证不同用户不同模块权限
def uboards():
    form = UpdateBoardsForm(request.form)                # 表单信息传输过来，方便修改调用
    if form.validate():
        board_id = form.board_id.data                    # 表单信息收集
        name = form.name.data
        
        board = BoardModel.query.get(board_id)           # 根据表单中提交的board_id查询数据库中对象信息
        if board:
            board.name = name                            # 表单中提交的name命名给数据库中对象的名字
            db.session.commit()                          # 修改数据后提交数据库
            return restful.success()                     # 数据库修改成功
        else:
            return restful.params_error(message="没有这个分类板块")  # 数据库中对象信息不存在
    else:
        return restful.params_error(message=form.get_error())  # 表单信息错误


# 删除 板块管理名称 路由,与static/cms/js/banners.js中绑定的方法、路由要相同
@cms_bp.route("/dboard/", methods=['POST'])
@permission_required(CMSPersmission.BOARDER)             # 传参装饰器验证不同用户不同模块权限
def dboards():
    board_id = request.form.get('board_id')                  # 查询表单信息中的board_id，这里没有单独创建删除的Form表单，使用之前创建的
    if not board_id:
        return restful.params_error(message="分类板块不存在")  # 表单信息不存在

    board = BoardModel.query.get(board_id)               # 根据表单中提交的board_id查询数据库中对象信息,注意.get
    if not board:
        return restful.params_error(message="分类板块不存在")  # 数据库中对象信息不存在
    
    db.session.delete(board)                             # 删除数据库中的信息
    db.session.commit()                                  # 提交数据库修改
    return restful.success()                             # 删除成功


# 前台用户管理路由
@cms_bp.route("/fusers/")
@permission_required(CMSPersmission.FRONTUSER)             # 传参装饰器验证不同用户不同模块权限
def fuser():
    return render_template("cms/cms_fuser.html")


# 后用户管理路由
@cms_bp.route("/cusers/")
@permission_required(CMSPersmission.CMSUSER)               # 传参装饰器验证不同用户不同模块权限
def cuser():
    return render_template("cms/cms_cuser.html")


# 添加登录路由
cms_bp.add_url_rule("/login/", view_func=LoginView.as_view('login'))    # view_func 命名操作名字，"/login/"路由地址

# 类视图函数添加绑定路由  注意类视图需要修改ResetPwd.as_view('resetpwd')
cms_bp.add_url_rule("/resetpwd/", view_func=ResetPwd.as_view('resetpwd'))  # view_func 命名操作名字，/resetpwd/路由地址

# 添加修改邮箱的类视图路由绑定，路由的命名和cms_base.js中的命名要相同，否则不关联，url=/resetemail/必须要和resetemail.js中的ajax绑定的路由相同
cms_bp.add_url_rule("/resetemail/", view_func=ResetEmail.as_view('resetemail'))

# 绑定路由，路由的命名和cms_base.js中的命名要相同，必须要和resetemail.js中的ajax绑定的路由相同
cms_bp.add_url_rule("/email_captcha/", view_func=EmailCaptcha.as_view('email_captcha'))
