#coding:utf-8

#pip install python-jenkins -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com

import jenkins
import time

server = jenkins.Jenkins('http://192.168.62.200:9090', username='admin', password='kbsonlong')
user = server.get_whoami()

all_jobs =  server.get_all_jobs()
L=[]
for job in all_jobs:
    L.append(job['fullname'])
jobname = 'empty'
if jobname in  L:
    print "%s is exist!" %jobname
    server.disable_job('empty')

else:
    server.create_job('empty', jenkins.EMPTY_CONFIG_XML)

if "%s_copy" % jobname in L:
    print "%s_copy is exist!" % jobname

    #删除job
    server.delete_job('empty')
    server.delete_job('empty_copy')
else:
    ##复制一个存在的job
    server.copy_job('empty', 'empty_copy')
    ##启用job
    server.enable_job('empty_copy')
    ##调用RECONFIG_XML配置empty_copy
    server.reconfig_job('empty_copy', jenkins.RECONFIG_XML)

jobs = server.get_jobs()
# print jobs




#
# server.enable_job('empty_copy')
# server.reconfig_job('empty_copy', jenkins.RECONFIG_XML)

##触发job构建
server.build_job(name='kbson',token='kbsonlong')

time.sleep(2)

number =  server.get_job_info(name='kbson')['nextBuildNumber'] - 1
print number
#构建输出日志
print server.get_build_console_output(name='kbson',number=number)
