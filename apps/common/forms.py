# -*- encoding: utf-8 -*-
"""
@File    : forms.py
@Time    : 2020/5/11 10:00
@Author  : chen
表单验证文件：apps/common/forms.py
"""
# 表单验证手机短信验证码
from wtforms import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp
import hashlib          # 哈希md5加密

''' 页面请求Form会有下面三个表单信息，利用他们进行验证当前页面的请求是否正常
telephone: 13316551764
timestamp: 1590218267779
sign: 3a94b6c107973b94e557d909fcea54cc
'''


# 调用front_signup.js中生成的sign进行Form验证当前页面的请求是否正常
class SMSCaptchaForm(Form):
    telephone = StringField(validators=[Regexp(r'1[2345789]\d{9}')])        # 正则表达式验证手机号码
    timestamp = StringField(validators=[Regexp(r'\d{13}')])                 # 正则表达式验证时间戳长度
    sign = StringField(validators=[InputRequired()])                        # 请求中需要有sign

    # 验证前端发送过来的sign和后端md5加密之后的sign是否一致
    def validate_sign(self, field):
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        
        # 服务端自己加密之后生成的sign，都是md5加密,加密的内容是通过front_signup.js中的加密内容相同
        # md5加密前需要转码才行.encode('utf-8');             .hexdigest()将加密后内容转换成字符串
        sign2 = hashlib.md5((timestamp+telephone+"q3423805gdflvbdfvhsdoa`#$%").encode('utf-8')).hexdigest()
        print("客户端sign %s" % sign)
        print("服务端sign2 %s" % sign2)
        
        # 验证客户端sign和服务端sign2是否相同
        if sign == sign2:
            return True
        else:
            return False
