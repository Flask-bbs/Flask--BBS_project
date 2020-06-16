# -*- encoding: utf-8 -*-
"""
@File    : send_telephone_msg.py
@Time    : 2020/5/22 16:18
@Author  : chen
发送验证码到手机的功能：utils/send_telephone_msg.py
"""
# 发送验证码到手机的功能
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient


# 封装成方法
def send_phone_msg(telephone, code):
    # 初始化client,apikey作为所有请求的默认值
    # clnt = YunpianClient('70b0eb56669841bbecff6c000c99d7e7')                                 # API key是云片账号中绑定的私有的
    clnt = YunpianClient('e8abe129a4e9f9a7c8c9adc8ece9ebc9')  # API key是云片账号中绑定的私有的
    
    param = {YC.MOBILE: telephone, YC.TEXT: '【于成令】您的验证码是{}'.format(code)}
    r = clnt.sms().single_send(param)
    return r.code()                                                                            # 返回发送状态码
    
    
# print(r.code())    # 0    代表发送成功
# print(r.msg())     # 发送成功
# print(r.data())    # {'code': 0, 'msg': '发送成功', 'count': 1, 'fee': 0.05, 'unit': 'RMB', 'mobile': '13316551764', 'sid': 54051316288}
# 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
# 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()
