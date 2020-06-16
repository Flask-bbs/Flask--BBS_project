# -*- encoding: utf-8 -*-
"""
@File    : forms.py
@Time    : 2020/5/11 10:00
@Author  : chen
forms表单信息:apps/cms/forms.py
"""
# forms表单信息
from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo, URL  # EqualTo验证新密码是否相同,URL验证
from utils.redis_captcha import redis_get  # 导入验证码模块


# 创父类form表单，用于输出错误信息
class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]  # 错误信息的收集，字典类型数据信息提取
        return message


# 登录页面中的Form表单      继承父类form
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(3, 15, message='请输入正确长度的密码')])  # 长度可以先设置短的，方便项目测试
    remember = IntegerField()  # 记住cookie操作  赋值为0或1


# 修改密码页面中的form表单信息    继承父类form
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(3, 15, message="密码长度有误")])
    newpwd = StringField(validators=[Length(3, 15, message="密码长度有误")])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message="两次输入密码不一致")])


# 定义设置邮箱的表单信息，进行提交时候使用
class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱")])  # 名称email与cms_resetemail.html中的要相同
    captcha = StringField(
        validators=[Length(min=4, max=4, message="请输入正确长度的验证码")])  # 名称captcha与cms_resetemail.html中的要相同
    
    # 验证redis中的字段与数据库中的字段是否相同
    def validate_captcha(self, field):  # 方法命名规则是：validate_字段名()
        # 表单提交上来的验证码
        email = self.email.data
        captcha = self.captcha.data
        
        # 取redis中保存的验证码             第一个redis_captcha是新对象，第二个redis_captcha是redis_captcha.py文件
        redis_captcha = redis_get(email)
        if not redis_captcha or captcha.lower() != redis_captcha.lower():  # 不区分大小写
            raise ValidationError('邮箱验证码错误')


# 定义 添加轮播图 的表单信息
class AddBannerForm(BaseForm):
    # Form表单名称根据static/cms/js/banners.js中的ajax.post发送的data中
    name = StringField(validators=[InputRequired(message="请输入轮播图名称")])
    image_url = StringField(validators=[InputRequired(message="请输入轮播图片链接"), URL(message="图片链接有误")])
    link_url = StringField(validators=[InputRequired(message="请输入轮播图上跳转链接"), URL(message="跳转链接有误")])
    priority = IntegerField(validators=[InputRequired(message="请输入轮播图优先级")])


# 定义 修改轮播图 的表单信息
class UpdateBannerForm(AddBannerForm):        # 继承AddBannerForm,收集表单信息一样，只多出来一个查询字段banner_id
    # 根据banner_id查询 修改 轮播图
    banner_id = IntegerField(validators=[InputRequired(message="轮播图不存在")])
    

# 定义 增加板块管理 的表单信息
class AddBoardsForm(BaseForm):
    # 板块名称
    name = StringField(validators=[InputRequired(message="板块名称不存在")])
    

# 编辑 板块管理名称
class UpdateBoardsForm(AddBoardsForm):
    # 修改编辑板块名称的时候需要使用board_id进行查询，再修改
    board_id = IntegerField(validators=[InputRequired(message="请输入板块ID")])
