# -*- encoding: utf-8 -*-
"""
@File    : upload_qiniuyun.py
@Time    : 2020/5/28 10:14
@Author  : chen
上传本地文件到七牛云功能：utils/upload_qiniuyun.py
"""
from qiniu import Auth, put_file, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'F6TFlLqmX4Jxi_OJ86xLVCB8mQ5KRsyzCjGVWPEh'
secret_key = 'zhCb8cNSR-lifyVCZLPjH3GhD4_W7P5Sgbh9mHah'

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
bucket_name = 'chen0406'

# 上传后保存的文件名
key = 'my-python-logo.png'

# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)                                          # 生成token，用于项目上传使用

# 要上传文件的本地路径
localfile = r'E:\ENV\flask项目-cBMOsSmb\Flask项目实战-BBS\static\common\images\logo.png'

ret, info = put_file(token, key, localfile)
# print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
