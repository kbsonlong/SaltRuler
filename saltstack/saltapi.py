#!/usr/bin/env python
#coding=utf-8

import urllib2, urllib, json
import ssl
import json
import re
ssl._create_default_https_context = ssl._create_unverified_context
#Python 2.7.9 之后版本引入了一个新特性
#当你urllib.urlopen一个 https 的时候会验证一次 SSL 证书
#当目标使用的是自签名的证书时就会爆出一个
#urllib.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)> 的错误消息，



class SaltAPI:
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/') #移除URL末尾的/
        self.__username = username
        self.__password = password
        self.__token_id = self.token_id()
    #登陆获取token
    # def SaltLogin(self):
    #     params = {'eauth': 'pam', 'username': self.__username, 'password': self.__password}
    #     encode = urllib.urlencode(params)
    #     obj = urllib.unquote(encode)
    #     headers = {'X-Auth-Token':''}
    #     url = self.__url + '/login'
    #     print url,self.__username,self.__password
    #     req = urllib2.Request(url, obj, headers)
    #     opener = urllib2.urlopen(req)
    #     content = json.loads(opener.read())
    #     try:
    #         token = content['return'][0]['token']
    #         return token
    #     except KeyError:
    #         raise KeyError

    # 登陆获取token
    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__username, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token': ''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        print req
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def command(self, tgt, fun, client='local_async', expr_form='glob', arg=None, **kwargs):
        params = {'client': client, 'tgt': tgt, 'fun': fun, 'expr_form': expr_form, 'arg': arg}
        obj = urllib.urlencode(params)
        req = self.postRequest(obj)
        jid = req['return'][0]['jid']
        return jid

    def salt_job(self, jid=''):
        if jid:
            prefix = '/jobs/' + jid
        else:
            prefix = '/jobs'
        result = self.postRequest(None, prefix)
        return result

    def key_list(self,fun,client='wheel',match=None):
        params = {'client': client, 'fun': fun,'match':match}
        obj = urllib.urlencode(params)
        req = self.postRequest(obj)
        return req

    def minions_key_status(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        req = self.postRequest(obj)
        accept = len(req['return'][0]['data']['return']['minions'])
        unaccept = len(req['return'][0]['data']['return']['minions_pre'])
        rejected = len(req['return'][0]['data']['return']['minions_rejected'])
        totle = accept + unaccept + rejected
        key_status = {'a_n': accept, 'r_n': unaccept, 'u_n': rejected}
        return key_status, totle

    #推送请求
    def PostRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        if obj:
            data, number = re.subn("arg\d*", 'arg', obj) #将arg1 arg2这些关键字都替换成arg，number为替换次数
        else:
            data=None
        req = urllib2.Request(url, data, headers)  # obj为传入data参数字典，data为None 则方法为get，有date为post方法
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content
    #执行命令
    def SaltCmd(self,tgt,fun,client='local',expr_form='glob',arg=None,**kwargs):
        params = {'client':client, 'fun':fun, 'tgt':tgt, 'expr_form':expr_form}
        if arg:
            a=arg.split(',') #参数按逗号分隔
            for i in a:
                b=i.split('=') #每个参数再按=号分隔
                if len(b)>1:
                    params[b[0]]='='.join(b[1:]) #带=号的参数作为字典传入

                else:
                    params['arg%s'%(a.index(i)+100)]=i
        if kwargs:
            params=dict(params.items()+kwargs.items())
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res
        #{u'return': [{u'jid': u'20160331104340284003', u'minions': [u'saltminion01-41.ewp.com']}]}
    #runner=salt-run=master本地执行
    def SaltRun(self,fun,client='runner_async',arg=None,**kwargs):
        params = {'client':client, 'fun':fun}
        if arg:
            a=arg.split(',') #参数按逗号分隔
            for i in a:
                b=i.split('=') #每个参数再按=号分隔
                if len(b)>1:
                    params[b[0]]='='.join(b[1:]) #带=号的参数作为字典传入
                else:
                    params['arg%s'%a.index(i)]=i
        if kwargs:
            params=dict(params.items()+kwargs.items())

        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res
    #获取JOB ID的详细执行结果
    def SaltJob(self,jid=''):
        if jid:
            prefix = '/jobs/'+jid
        else:
            prefix = '/jobs'
        res = self.PostRequest(None,prefix)

        return res
    #获取grains
    def SaltMinions(self,minion=''):
        if minion and minion!='*':
            prefix = '/minions/'+minion
        else:
            prefix = '/minions'
        res = self.PostRequest(None,prefix)
        return res
    #获取events
    def SaltEvents(self):
        prefix = '/events'
        res = self.PostRequest(None,prefix)
        return res

    #列出KEY
    def ListKey(self):
        prefix = '/keys'
        content = self.PostRequest(None,prefix)
        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return accepted,denied,unaccept,rejected
    #接受KEY
    def AcceptKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    #删除KEY
    def DeleteKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret



#测试：python manager.py shell ; from SALT.SaltAPI import * ; main()，代码修改了要ctrl+Z退出重进
def main():
    idc = '2'
    tgt = '*'   #  '*'不能使用list类型
    fun ='test.ping'
    client = 'local'
    arg = ['/srv/salt/test.txt','fadfwef2f']
    # from models import SaltServer
    # salt_server = SaltServer.objects.get(idc=idc)
    # sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
    sapi = SaltAPI(url="https://192.168.62.200:8000",username="salt",password="salt")
    # result = sapi.SaltCmd(tgt=tgt,fun=fun,arg=arg)
    # result = sapi.SaltCmd(tgt="192.168.62.200",fun="cp.get_url",arg='http://192.168.62.1/upload/jd-gui.cfg',arg1='dest=/tmp/jd-gui.cfg')
    print sapi.SaltCmd(tgt='192.168.62.200', fun='cp.get_file', expr_form='list', arg='salt://temp/CentOS-Vault.repo', arg1='/data/PRG/SaltRuler/upload/1231.sss')
    # jid = result['return'][0]['jid']
    # print jid
    # jidinfo=sapi.SaltJob(jid)
    # print jidinfo

if __name__ == '__main__':
    main()