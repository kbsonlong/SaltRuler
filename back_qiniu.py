# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth
import qiniu.config, sys


class qiniuBackup:
    __qiniu = None
    __bucket_name = None
    __bucket_domain = None
    __error_msg = "ERROR: 无法连接到七牛云服务器，请检查[AK/SK/存储空间]设置是否正确!"

    def __init__(self):
        # 获取七牛秘钥
        fp = open('qiniuAs.conf', 'r');
        if not fp:
            print 'ERROR: 请检查qiniuAs.conf文件中是否有七牛Key相关信息!';
            return
        keys = fp.read().split('|');
        if len(keys) < 4:
            print 'ERROR: 请检查qiniuAs.conf文件中的七牛Key信息是否完整!';
            return

        self.__bucket_name = keys[2];
        self.__bucket_domain = keys[3];

        # 构建鉴权对象
        self.__qiniu = Auth(keys[0], keys[1]);

    # 上传文件
    def upload_file(self, filename):
        try:
            from qiniu import put_file, etag, urlsafe_base64_encode
            # 上传到七牛后保存的文件名
            key = filename.split('/')[-1];

            # 生成上传 Token，可以指定过期时间等
            token = self.__qiniu.upload_token(self.__bucket_name, key, 3600 * 2)
            result = put_file(token, key, filename)
            return result[0]
        except:
            print self.__error_msg
            return None

    # 取回文件信息
    def get_files(self, filename):
        try:
            from qiniu import BucketManager
            bucket = BucketManager(self.__qiniu)
            result = bucket.stat(self.__bucket_name, filename)
            return result[0]
        except:
            print self.__error_msg
            return None

    # 取回文件列表
    def get_list(self):
        try:
            from qiniu import BucketManager
            bucket = BucketManager(self.__qiniu)
            result = bucket.list(self.__bucket_name)
            if not len(result[0]['items']): return [
                {"mimeType": "application/test", "fsize": 0, "hash": "", "key": "没有文件", "putTime": 14845314157209192}];
            return result[0]['items']
        except:
            print self.__error_msg
            return None

    # 下载文件
    def download_file(self, filename):
        try:
            base_url = 'http://%s/%s' % (self.__bucket_domain, filename)
            private_url = self.__qiniu.private_download_url(base_url, expires=3600)
            return private_url
        except:
            print self.__error_msg
            return None

    # 删除文件
    def delete_file(self, filename):
        try:
            from qiniu import BucketManager
            bucket = BucketManager(self.__qiniu)
            result = bucket.delete(self.__bucket_name, filename)
            return result[0]
        except:
            print self.__error_msg
            return None


if __name__ == "__main__":
    import json

    data = None
    q = qiniuBackup();
    type = sys.argv[1];
    if type == 'upload':
        data = q.upload_file(sys.argv[2]);
    elif type == 'download':
        data = q.download_file(sys.argv[2]);
    elif type == 'get':
        data = q.get_files(sys.argv[2]);
    elif type == 'list':
        data = q.get_list();
    elif type == 'delete_file':
        data = q.delete_file(sys.argv[2]);
    else:
        data = 'ERROR: 参数不正确!';

    print json.dumps(data)

