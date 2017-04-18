#!/bin/env python
# encoding: utf-8
import ConfigParser, time, sys
from jenkinsapi.jenkins import Jenkins

# 配置文件
path = 'config.ini'

# 创建一个连接
def get_server_instance(jenkins_url,username,password):
    server = Jenkins(jenkins_url, username=username, password=password)
    return server

# 判断job是否正在运行10s检测一次
def is_run_or_queue(jenkins_server,jobname):
    job_status = jenkins_server[jobname]
    while True:
        if job_status.is_queued_or_running():
           time.sleep(10)
        else:
            break

# 判断执行结果是否正确
def run_server_job(jenkins_server,jobname):
    job_status = jenkins_server[jobname]
    if job_status.is_queued_or_running():
        '''防止job重复执行'''
    else:
        jenkins_server.build_job(jobname)
    is_run_or_queue(jenkins_server,jobname)
    if job_status.get_last_build_or_none().get_status() == "SUCCESS":
        print '''job执行成功,执行编号: %s''' % job_status.get_last_build()
    else:
        print '''job执行失败,,执行编号: %s''' % job_status.get_last_build()



if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()

    # 读取配置文件
    cf.read(path)

    # 读取文件配置,设置变量
    jenkins_url = cf.get("config","jenkins_url")
    username = cf.get("config","username")
    password = cf.get("config","password")

    # 创建一个连接
    jenkins_server = get_server_instance(jenkins_url,username,password)
    # 运行jenkins job: test
    run_server_job(jenkins_server,"zsl")



#coding:utf-8
from jenkinsapi.jenkins import Jenkins


def get_server_instance():
    jenkins_url = 'http://192.168.62.200:9090'
    server = Jenkins(jenkins_url,username='admin',password='kbsonlong')
    server.keys()

    return server


def get_job_details():
    server = get_server_instance()
    for job_name,job_instance in server.get_jobs():
        print 'Job Nmae: %s' % (job_instance.name)
        print 'Job Description: %s' % (job_instance.get_description())
        print 'Is Job running: %s' % (job_instance.is_running())
        print 'Is Job enabled: %s' % (job_instance.is_enabled())

def disable_job():
    server = get_server_instance()
    for job_name, job_instance in server.get_jobs():
        if (server.has_job(job_name)):
            job_instance = server.get_job(job_name)
            job_instance.disable()
            print 'Name: %s , Is Job Enabled ? : %s' % (job_name,job_instance.is_enabled())

def create_jobtest():
    server = get_server_instance()
    job_name="myjob"
    job_xml="config.xml"
    create = server.create_job(job_name,job_xml)
    print create

def copy_jobtest():
    server = get_server_instance()
    job_name = "myjob"
    job_xml = "config.xml"
    copy = server.copy_job(job_name,job_xml)
    return copy


if __name__ == '__main__':
    server = get_server_instance()
    print server.version
    get_job_details()
    disable_job()  ##禁用job
    for job_url,job_name in  server.get_jobs_info():
        print job_url,job_name


    # print copy_jobtest()
