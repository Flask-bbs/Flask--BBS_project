# -*- encoding: utf-8 -*-
"""
@File    : safe_url.py
@Time    : 2020/5/26 14:33
@Author  : chen
确保URL安全的文件：utils/safe_url.py
"""
'''
确保URL安全的关键是判断URL是否属于程序内部，可以通过判断url的host、协议等信息是否和程序内部的url一致，如果一致则认识是可信的url
代码中is_safe_url()方法接受目标URL作为参数，通过request.host_url获取程序内部的主机URL，然后使用urljoin()函数将目标URL转为绝对URL。
接着，分别使用urlparse模块提供的urlparse()解析两个url，最后对目标url的url模式和主机地址进行验证，确保只属于程序内部的url才会被返回。
在执行重定向会上一个页面的redirect_back()函数中，使用is_safe_url()验证next和referer的值
'''

from urllib.parse import urlparse, urljoin  # python3从urllib.parse导入
from flask import request


def is_safe_url(target):
    ref_url = urlparse(request.host_url)                                                      # 获取当前页面url
    test_url = urlparse(urljoin(request.host_url, target))                                    # 获取目标的页面的url
    # 对比两个url
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc         # 返回True代表是安全的url

    # print("request.host_url:", request.host_url)                    # 当前的url地址
    # print("ref_url:", ref_url)                                      # 跳转至的页面url
    # print("target:", target)                                        # 跳转目标
    # print("test_url:", test_url)                                    # 测试页面url
    # print("ref_url.netloc:", ref_url.netloc)
    # print("test_url.netloc:", test_url.netloc)
    # print("test_url.scheme:", test_url.scheme)                      # http
