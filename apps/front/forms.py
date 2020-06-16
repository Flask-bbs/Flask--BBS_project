# -*- encoding: utf-8 -*-
"""
@File    : forms.py
@Time    : 2020/5/11 10:00
@Author  : chen
前台表单信息：apps/front/forms.py
"""
# 前台form表单信息
from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import EqualTo, Email, InputRequired, Length, Regexp
from utils import random_captcha                                               # 随机生成验证码
from utils import redis_captcha                                                # 保存验证码到redis数据库中


# 表单信息的父类文件
class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]          # 错误信息的收集，字典类型数据信息提取
        return message


# 注册界面的Form表单类
class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确格式的手机号")])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message="请输入正确格式的验证码")])              # \w包含字母
    username = StringField(validators=[Length(min=2, max=15, message="请输入正确长度的用户名")])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{3,20}', message="请输入正确格式的密码")])
    password2 = StringField(validators=[EqualTo('password1', message="两次输入密码不一致")])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message="请输入正确格式的验证码")])
    
    # 验证手机验证码字段
    def validate_sms_captcha(self, field):
        telephone = self.telephone.data
        sms_captcha = self.sms_captcha.data                            # 获得表单信息
        
        sms_captcha_redis = redis_captcha.redis_get(telephone)         # redis数据库中根据手机号调验证码，进行判定是否相同
        
        # 判断用户输入的验证码和redis中取出的验证码是否相同
        if not sms_captcha_redis or sms_captcha_redis.lower() != sms_captcha.lower():
            raise ValidationError(message="手机验证码输入错误")
        
        # if sms_captcha or sms_captcha.lower() == sms_captcha_redis.lower():
        #     pass
        # else:
        #     raise ValidationError("验证码输入错误")
      
    # 图形验证码字段验证
    def validate_graph_captcha(self, field):
        graph_captcha = self.graph_captcha.data                                 # 表单信息收集

        graph_captcha_redis = redis_captcha.redis_get(graph_captcha)            # redis中是将验证码的text当做key来保存的，调用也是一样

        # 判定图形验证码是否一致
        if not graph_captcha_redis or graph_captcha_redis.lower() != graph_captcha.lower():
            # print("ceshi")
            raise ValidationError(message="图形验证码输入错误")


# 登录界面的Form表单信息收集
class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确格式的手机号")])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{3,20}', message="请输入正确格式的密码")])
    remember = StringField(IntegerField())
    

# 帖子的Form表单信息收集
class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入标题")])
    content = StringField(validators=[InputRequired(message="请输入内容")])
    board_id = StringField(validators=[InputRequired(message="请输入板块名称")])
    

# 评论的Form表单验证
class AddCommentForm(BaseForm):
    # 表单信息的收集根据网页端发送的参数名称和类型
    content = StringField(validators=[InputRequired(message="请输入评论内容")])
    post_id = IntegerField(validators=[InputRequired(message="请选择一篇帖子进行评论")])


