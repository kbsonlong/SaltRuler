#!/usr/bin/env python
# coding:utf-8
###zabbix自动发现web
import os, sys, json
urllist = ["http://baidu.com",
           "http://www.qq.com",
           "http://www.sina.com.cn/"]

def web_site_discovery():
    web_list = []
    web_dict = {"data": None}
    for url in urllist:
        url_dict = {}
        url_dict["{#SITENAME}"] = url
        web_list.append(url_dict)
    web_dict["data"] = web_list
    jsonStr = json.dumps(web_dict, sort_keys=True, indent=4)
    return jsonStr



def web_site_code():
    cmd = 'curl -o /dev/null -s -w %s %s' % ("%{http_code}", sys.argv[2])
    reply_code = os.popen(cmd).readlines()[0]
    return reply_code


if __name__ == "__main__":
    try:
        if sys.argv[1] == "web_site_discovery":
            web_site_discovery()
        elif sys.argv[1] == "web_site_code":
            web_site_code()
        else:
            print "Pls sys.argv[0] web_site_discovery | web_site_code[URL]"
    except Exception as msg:
        print msg