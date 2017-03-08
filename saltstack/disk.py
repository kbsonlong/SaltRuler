#!/usr/bin/env python
#coding:utf-8

from saltapi import SaltAPI

sapi = SaltAPI('https://192.168.234.158:8000','salt','pcgames2016')

def disk(hosts):
    for host in hosts:
        disk = sapi.SaltCmd(host,fun='disk.usage',client='local')['return'][0][host]
        L = []
        for k,v  in disk.items():
            # print int(i['capacity'].strip('%'))
            if  int(v['capacity'].strip('%')) > 70:
                L.append("%s free: %s GB " %(k, int(v['available'])/1000/1000))
        if L:
            print host,L

if __name__ == '__main__':
    # minions=['192.168.234.158']
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    disk(minions)