# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/5/11 9:59
@Author  : chen
公共视图文件：apps/common/views.py
"""
# 导入手机验证码生成文件
from utils.send_telephone_msg import send_phone_msg

from utils import restful
from utils.captcha import Captcha
from flask import Blueprint, request, jsonify
from utils import redis_captcha                                 # 图形验证码存储到redis数据库中

# 导入form表单信息验证客户端sign2和服务端sign
from apps.common.forms import SMSCaptchaForm

# 导入七牛云上传文件的依赖库
from qiniu import Auth, put_file, etag
import qiniu.config

common_bp = Blueprint("common", __name__, url_prefix='/c')      # 视图common，url前缀c,在


# 手机验证码生成文件，这部分是只要调用当前路由请求，就会发送短信验证码，
# 需要利用sign = md5(timestamp+telephone+"q3423805gdflvbdfvhsdoa`#$%")，在front_signup.js文件中调用
# @common_bp.route("/sms_captcha/", methods=['POST'])
# def sms_captcha():
#     telephone = request.form.get('telephone')        # 表单信息收集
#
#     if not telephone:
#         return restful.params_error(message="请填写手机号")              # 手机信息不存在，输出错误
#
#     captcha = Captcha.gene_text(number=4)                               # 生成4位验证码,这里生成的是验证码，要发送到手机端的，不能是图形验证码
#     # captcha = get_random_captcha(num=4):                              # 或者使用utils/random_captcha.py文件中的随机生成验证码
#
#     # 调用send_telephone_msg.py中send_phone_msg方法发送4位验证码到手机中
#     if send_phone_msg(telephone, captcha) == 0:                         # 返回成功的状态码为 0
#         return restful.success()
#     else:
#         return restful.params_error("手机验证码发送失败")                 # 手机验证码发送失败


# 在front_signup.js文件中调用sign = md5()验证表单信息.

@common_bp.route("/sms_captcha/", methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)               # 收集form表单信息
    
    if form.validate():                               # 表单信息存在
        # 接收数据
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)         # 生成4位验证码,这里生成的是验证码，要发送到手机端的，不能是图形验证码
        print("发送的手机验证码是：{}".format(captcha))
        
        # 验证发送成功状态码
        if send_phone_msg(telephone, captcha) == 0:                          # 返回成功的状态码为 0
            redis_captcha.redis_set(telephone, captcha)                      # 将telephone对应的手机验证码保存在Redis数据库中
            
            return restful.success()                                         # 返回成功信息提示框
        else:
            return restful.params_error("手机验证码发送失败")                 # 手机验证码发送失败
    else:
        return restful.params_error(message="参数错误")
    

# 创建七牛云上传文件路由，前后台公有
@common_bp.route("/uptoken/")                               # 路由与static/cms/js/banners.js中上传文件路由相同
def uptoken():
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'F6TFlLqmX4Jxi_OJ86xLVCB8mQ5KRsyzCjGVWPEh'
    secret_key = 'zhCb8cNSR-lifyVCZLPjH3GhD4_W7P5Sgbh9mHah'
    
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    
    # 要上传的空间
    bucket_name = 'chen0406'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)  # 生成token，用于项目上传使用
    
    return jsonify({"uptoken": token})   # 键值对类型