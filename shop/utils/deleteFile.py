from qiniu import Auth, put_file, etag, put_data, BucketManager
from conf.env import  AccessKey, SecretKey, bucked_name





def deleteFile(file_name):
    """
    收集本地信息到云服务器上
    参考地址：https://developer.qiniu.com/kodo/sdk/1242/python
    """
    q = Auth(access_key=AccessKey,
             secret_key=SecretKey)
    bucket = BucketManager(q)
    ret, info = bucket.delete(bucked_name,file_name)
    return info
