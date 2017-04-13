# -*- coding: utf8 -*-

import docker
import os.path, json, requests

class BASE_REGISTRY_API:
    def __init__(self, timeout=2, verify=False):
        self.timeout  = timeout
        self.verify   = verify
    def checkStatus(self, url, version=1):
        """ 返回私有仓状态 """
        if url:
            url = url.strip("/") + "/v1/_ping" if version == 1 else url.strip("/") + "/v2/"
            try:
                req = requests.head(url, timeout=self.timeout, verify=self.verify)
            except Exception,e:
                return e
            else:
                return req.ok
        return False

    def search_all_repository(self, url, version=1, q=""):
        """ 搜索私有仓所有镜像 """
        res = {"msg": None, "data": []}
        if url:
            ReqUrl = url.strip("/") + "/v1/search" if version == 1 else url.strip("/") + "/v2/_catalog"

            try:
                Images = requests.get(ReqUrl, timeout=self.timeout, verify=self.verify, params={"q": q}).json()
            except Exception,e:

                res.update(msg=e)
            else:
                if version == 1:
                    res.update(data=Images["results"])
                else:
                    res.update(data=[ {"name": _, "description": None} for _ in Images["repositories"] if q in _ ])

        return res

    def list_image_tags(self, ImageName, url, version=1):
        """ 列出某个镜像所有标签 """

        res = {"msg": None, "data": {}}
        if url and ImageName:
            ReqUrl = url.strip("/") + "/v1/repositories/{}/tags".format(ImageName) if version == 1 else url.strip("/") + "/v2/{}/tags/list".format(ImageName)

            try:
                Tags = requests.get(ReqUrl, timeout=self.timeout, verify=self.verify).json()
            except Exception,e:
                res.update(msg=e)
            else:
                if version == 1:
                    res.update(data=Tags)
                else:
                    L=[]
                    for tag in Tags['tags']:
                        L.append({tag:self.from_image_tag_getId(ImageName, tag, url, version)})
                    res.update(data=L)
        return res

    def delete_image(self, ImageName, url, version=1):
        """ 删除一个镜像 """

        res = {"msg": None, "success": False}
        if url:
            ReqUrl = url.strip("/") + "/v1/repositories/{}/".format(ImageName) if version == 1 else ""

            try:
                delete_repo_result = requests.delete(ReqUrl, timeout=self.timeout, verify=self.verify).json()
            except Exception,e:

                if version == 1:
                    res.update(msg=e)
                else:
                    res.update(msg="The operation is unsupported.", code=-1)
            else:
                res.update(success=delete_repo_result)

        return res

    def from_image_tag_getId(self, ImageName, tag, url, version=1):
        """ 查询某个镜像tag的imageId/digest """

        if url:
            ReqUrl = url.strip("/") + "/v1/repositories/{}/tags/{}".format(ImageName, tag) if version == 1 else url.strip("/") + "/v2/{}/manifests/{}".format(ImageName, tag)

            try:
                if version == 1:
                    r = requests.get(ReqUrl, timeout=self.timeout, verify=self.verify)
                else:
                    r = requests.head(ReqUrl, timeout=self.timeout, verify=self.verify, allow_redirects=True, headers={"Content-Type": "application/vnd.docker.distribution.manifest.v2+json"})
            except Exception,e:
                print e
            else:
                if version == 1:
                    return r.json()
                else:
                    return r.headers.get("Docker-Content-Digest", "")
        return ""

    def get_imageId_info(self, ImageId, url, version=1,tag=None, ImageName=None):
        """ 查询某个镜像的信息(v2时必须定义ImageName), ImageId/Tag(v2) """
        res = {"msg": None, "data": {}}
        if url:
            ReqUrl = url.strip("/") + "/v1/images/{}/json".format(ImageId) if version == 1 else url.strip("/") + "/v2/{}/manifests/{}".format(ImageName, tag)

            try:
                ImageInfo = requests.get(ReqUrl, timeout=self.timeout, verify=self.verify).json()
            except Exception,e:

                res.update(msg=e)
            else:

                if "errors" in ImageInfo or "error" in ImageInfo:
                    res.update(msg="get tag detail info error")
                else:
                    res.update(data=ImageInfo)

        return res

    def delete_imageTag(self, ImageName, tag, url, version=1):
        """ 删除一个镜像标签 """

        res = {"msg": None, "success": False}
        if url:
            ReqUrl = url.strip("/") + "/v1/repositories/{}/tags/{}".format(ImageName, tag) if version == 1 else url.strip("/") + "/v2/{}/manifests/{}".format(ImageName, self.from_image_tag_getId(ImageName, tag, url, version))

            try:
                delete_repo_result = requests.delete(ReqUrl, timeout=self.timeout, verify=self.verify).json()
            except Exception,e:

                res.update(msg=e)
            else:
                if version == 1:
                    res.update(success=delete_repo_result)
                else:
                    res.update(msg="The operation is unsupported.", code=-1)

        return res


if __name__ == '__main__':
    b = BASE_REGISTRY_API()

    url = 'http://192.168.62.200:5000'
    ImageName = 'saltops'
    ReqUrl = url.strip("/") + "/v2/{}/tags/list".format(ImageName)
    Tags = requests.get(ReqUrl).json()
    print Tags
    print b.list_image_tags(ImageName,url,2)
    print b.from_image_tag_getId(ImageName=ImageName,tag='v2',url=url,version=2)