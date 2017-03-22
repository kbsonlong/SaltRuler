#!/bin/bash
# -------------------------------------------------------------------------------
# FileName:    check_Multimysql.sh
# Revision:    1.0
# Date:        2017/03/09
# Author:      kbsonlong
# Email:       kbsonlong@gamil.com
# Website:     www.along.party
# License:     GPL
# -------------------------------------------------------------------------------
 
# 用户名
MYSQL_USER='zabbix'
 
# 密码
MYSQL_PWD='zabbix'
 
# 主机地址/IP
MYSQL_HOST='127.0.0.1'
 
# 端口
MYSQL_PORT=$2
 
# 数据连接
mysqladmin_bin=`which mysqladmin`
MYSQL_CONN="$mysqladmin -u${MYSQL_USER} -p${MYSQL_PWD} -h${MYSQL_HOST} -P${MYSQL_PORT}"


##help函数
help() {
        echo "Usage:$0  [ping|Uptime|Com_update|Slow_queries|Com_select|Com_rollback|Questions|Com_insert|Com_delete|Com_commit|Bytes_sent|Bytes_received|Com_begin]  port"
}

# 参数是否正确
if [ $# -lt "2" ];then 
    echo "参数缺失!"
    help 
    exit 2
fi 
 
# 获取数据
case $1 in 
    ping) 
        ret=`${MYSQL_CONN} ping | grep -c alive` 
        echo $ret 
        ;; 
    Uptime) 
        ret=`${MYSQL_CONN} status |  awk -F\: '{print $2}' | awk '{print $1}' ` 
        echo $ret 
        ;; 
    Questions) 
        ret=`${MYSQL_CONN} status | awk -F\: '{print $4}' | awk '{print $1}' ` 
                echo $ret 
                ;;    
    Slow_queries) 
        ret=`${MYSQL_CONN} status | awk -F\: '{print $5}' | awk '{print $1}'` 
        echo $ret 
        ;; 
    Com_update) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_update" | awk -F\| '{print $3}'` 
        echo $ret 
        ;; 
    Com_select) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_select" | awk -F\| '{print $3}'` 
        echo $ret 
                ;; 
    Com_rollback) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_rollback" | awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
    
    Com_insert) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_insert" | awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
    Com_delete) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_delete"| awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
    Com_commit) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_commit"| awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
    Bytes_sent) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Bytes_sent" | awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
    Bytes_received) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Bytes_received" | awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
    Com_begin) 
        ret=`${MYSQL_CONN} extended-status | grep -w "Com_begin" | awk -F\| '{print $3}'` 
                echo $ret 
                ;; 
                        
        *) 
        help 
        ;; 
esac