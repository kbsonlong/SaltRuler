# -*- coding: utf8 -*-

import docker
import os.path, json, requests

class BASE_REGISTRY_API:
    def __init__(self, timeout=2, verify=False):
        self.timeout  = timeout
        self.verify   = verify
    def _checkStatus(self, url, version=1):
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

    def _search_all_repository(self, url, version=1, q=""):
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

    def _list_image_tags(self, ImageName, url, version=1):
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
                    res.update(data={ _:self._from_image_tag_getId(ImageName, _, url, version) for _ in Tags.get('tags', []) })

        return res

    def _delete_image(self, ImageName, url, version=1):
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

    def _from_image_tag_getId(self, ImageName, tag, url, version=1):
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

    def _get_imageId_info(self, ImageId, url, version=1, ImageName=None):
        """ 查询某个镜像的信息(v2时必须定义ImageName), ImageId/Tag(v2) """

        res = {"msg": None, "data": {}}
        if url:
            ReqUrl = url.strip("/") + "/v1/images/{}/json".format(ImageId) if version == 1 else url.strip("/") + "/v2/{}/manifests/{}".format(ImageName, ImageId)

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

    def _delete_imageTag(self, ImageName, tag, url, version=1):
        """ 删除一个镜像标签 """

        res = {"msg": None, "success": False}
        if url:
            ReqUrl = url.strip("/") + "/v1/repositories/{}/tags/{}".format(ImageName, tag) if version == 1 else url.strip("/") + "/v2/{}/manifests/{}".format(ImageName, self._from_image_tag_getId(ImageName, tag, url, version))

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

class MultiRegistryManager(BASE_REGISTRY_API):


    def __init__(self, timeout=2, verify=False):
        self.timeout = timeout
        self.verify  = verify
        self._BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._dir0   = os.path.join(self._BASE, 'logs', ".Registries.db")
        self._dir1   = os.path.join(self._BASE, 'logs', ".ActiveRegistry.db")
        self._registries  = self._unpickle
        self._active      = self._unpickleActive

    def _pickle(self, data):
        """ 序列化所有数据写入存储 """
        try:
            with open(self._dir0, "w") as f:
                json.dump(data, f)
        except Exception,e:

            res = False
        else:
            res = True


        return res

    @property
    def _unpickle(self):
        """ 反序列化信息取出所有数据 """
        try:
            with open(self._dir0, "r") as f:
                    data = json.load(f)
        except Exception,e:

            res = []
        else:
            res = data or []


        return res

    def _pickleActive(self, data):
        """ 序列化活跃仓库数据写入存储 """
        try:
            with open(self._dir1, "w") as f:
                json.dump(data, f)
        except Exception,e:

            res = False
        else:
            res = True


        return res

    @property
    def _unpickleActive(self):
        """ 反序列化信息取出活跃仓库 """
        try:
            with open(self._dir1, "r") as f:
                data = json.load(f)
        except Exception,e:

            res = {}
        else:
            res = data or {}


        return res

    @property
    def getMember(self):
        """ 查询所有仓库名称 """
        return [ _.get("name") for _ in self._registries ]

    def isMember(self, name):
        """ 查询某name的仓库是否在存储中 """
        return name in self.getMember

    def getOne(self, name):
        """ 查询某name的仓库信息 """

        if self.isMember(name):
            return ( _ for _ in self._registries if _.get("name") == name ).next()
        else:

            return {}

    @property
    def getActive(self):
        """ 查询活跃仓库 """
        return self._active

    def isActive(self, name):
        """ 判断某name的仓库是否为活跃仓库 """
        return name == self.getActive.get("name")

    def setActive(self, name):
        """ 设置活跃仓库 """


        if self.isActive(name):
            print "The name of the request is already active, think it successfully"
        else:

            self._active = self.getOne(name)
            self._pickleActive(self._active)
            if self.isActive(name):
                print "setActive, the request name sets it for active, successfully"
            else:
                print "setActive, the request name sets it for active, but fail"
                return False
        return True

    def getRegistries(self):
        """ 查询所有仓库信息 """
        return self._registries

    def GET(self, query, state=False):
        """ 查询 """

        res = {"msg": None, "code": 0}


        if not isinstance(query, (str, unicode)) or not query:
            res.update(msg="GET: query params type error or none", code=10000)
        else:
            query = query.lower()
            if query == "all":
                res.update(data=self.getRegistries())
            elif query == "active":
                res.update(data=self.getActive)
            elif query == "member":
                res.update(data=self.getMember)
            else:
                if self.isMember(query):
                    res.update(data=self.getOne(query))
                else:
                    res.update(msg="No such registry", code=10001)

        return res

    def POST(self, name, addr, version=1, auth=None):
        """ 创建 """

        res  = {"msg": None, "code": 0}
        try:
            version = int(version)
        except Exception,e:

            res.update(msg="params error", code=-10002)

            return res
        else:
            print "post a registry, name is %s, addr is %s, version is %s" %(name, addr, version)

        if not name or not addr:
            res.update(msg="params error", code=10002)
        elif not "http://" in addr and not "https://" in addr:
            res.update(msg="addr params error, must be a qualified URL(include protocol)", code=10003)
        elif self.isMember(name):
            res.update(msg="registry already exists", code=10004)
        else:
            self._registries.append(dict(name=name.strip(), addr=addr.strip(), version=version, auth=auth))
            self._pickle(self._registries)
            res.update(success=True, code=0)



        return res

    def DELETE(self, name):
        """ 删除当前存储中的私有仓 """

        res = {"msg": None, "code": 0, "success": False}


        if name in ("member", "active", "all"):
            res.update(msg="name reserved for the system key words", code=10005)

        elif self.isActive(name):
            res.update(msg="not allowed to delete the active cluster", code=10006)

        elif self.isMember(name):
            registry = self.getOne(name)

            self._registries.remove(registry)
            if self.isMember(name):

                res.update(success=False)
            else:

                self._pickle(self._registries)
                res.update(success=True)

        else:
            res.update(msg="This registry does not exist", code=10007)

        return res

    def PUT(self, name, setActive=False):
        """ 设置活跃仓库 """

        res = {"msg": None, "code": 0}


        if setActive:
            if name and self.isMember(name):
                res.update(success=self.setActive(name))
            else:
                res.update(msg="setActive, but no name param or name non-existent", code=10008)
        else:
            pass


        return res

class ApiRegistryManager(BASE_REGISTRY_API):


    def __init__(self, timeout=2, verify=False, ActiveRegistry={}):
        self.timeout = timeout
        self.verify  = verify
        self._addr   = ActiveRegistry.get("addr")
        self._ver    = ActiveRegistry.get("version")
        self._auth   = ActiveRegistry.get("auth")


    @property
    def url(self):
        """ 返回私有仓地址 """
        return self._addr

    @property
    def version(self):
        """ 返回私有仓版本 """
        return self._ver

    @property
    def isHealth(self):
        """ 返回私有仓健康状态 """
        return self._checkStatus(self.url, self.version)

    def list_repository(self, q=""):
        """ 查询私有仓镜像名称(默认列出所有镜像) """
        return self._search_all_repository(url=self.url, version=self.version, q=q)

    def list_imageTags(self, ImageName):
        """ 查询某镜像的tag列表 """
        return self._list_image_tags(url=self.url, version=self.version, ImageName=ImageName)

    def get_tag_info(self, ImageId, ImageName=None):
        """ 查询某tag(ImageId)的镜像信息 """
        return self._get_imageId_info(url=self.url, version=self.version, ImageId=ImageId, ImageName=ImageName)

    def delete_an_image(self, ImageName):
        """ 删除一个镜像 """
        return self._delete_image(url=self.url, version=self.version, ImageName=ImageName)

    def delete_an_image_tag(self, ImageName, tag):
        """ 删除一个镜像标签 """
        return self._delete_imageTag(url=self.url, version=self.version, ImageName=ImageName, tag=tag)