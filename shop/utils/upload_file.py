from qiniu import Auth, put_file, etag, put_data
from conf.env import QN_BASE_DIR_img, AccessKey, SecretKey, bucked_name, QN_BASE_DIR_video


def qiniu_token():
    q = Auth(access_key=AccessKey,
             secret_key=SecretKey)
    token = q.upload_token(bucked_name)
    return token


def upload_file(data, file_name):
    """
    收集本地信息到云服务器上
    参考地址：https://developer.qiniu.com/kodo/sdk/1242/python
    """
    # 指定上传空间，获取token
    token = qiniu_token()
    # 指定图片名称
    if 'mp4' in file_name:
        QN_BASE_DIR = QN_BASE_DIR_video
    else:
        QN_BASE_DIR = QN_BASE_DIR_img
    ret, info = put_data(token, file_name, data)
    img_url = QN_BASE_DIR + ret.get('key')
    return img_url

# if __name__ == '__main__':
#     bucked_name = 'h2002a'
#     file_path = '{}\\myutils\\123.png'.format(BASE_DIR)
#     domain_name = 'http://qj5ps2dbi.hb-bkt.clouddn.com/'
#     print(upload_img(bucked_name, file_path, domain_name))
