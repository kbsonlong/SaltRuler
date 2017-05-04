#coding:utf-8

from saltadmin.saltapi import SaltAPI
from SaltRuler.glob_config import glob_config

url = glob_config('salt_api','url')
username = glob_config('salt_api','username')
password = glob_config('salt_api','password')
device0 = glob_config('server','dervice0')

def saltinfo(tgt):
    sapi=SaltAPI(url,username,password)
    grains = sapi.SaltCmd(tgt=tgt,fun='grains.items',client='local')['return'][0]
    disk = sapi.SaltCmd(tgt=tgt,fun='disk.usage',client='local')['return'][0]
    info = sapi.SaltCmd(tgt=tgt,fun='cmd.run',client='local',arg='uptime')['return'][0]
    hostname = grains[tgt]['host']
    ip =  grains[tgt]['ip4_interfaces'][device0][0]
    OS = grains[tgt]['os'] + ' ' + grains[tgt]['osrelease'] + '.' + grains[tgt]['osarch']
    disk_all = float(disk[tgt]['/']['1K-blocks']) / 1000 /1000
    disk_free = float(disk[tgt]['/']['available']) / 1000 /1000
    disk_used = float(disk[tgt]['/']['used']) / 1000 /1000
    disk_used_p = disk[tgt]['/']['capacity']
    Manufacturer = grains[tgt]['manufacturer']
    saltstack_version = grains[tgt]['saltversion']
    mem_total = grains[tgt]['mem_total']
    cpu_logical_cores = grains[tgt]['num_cpus']
    cpu_model = grains[tgt]['cpu_model']
    uptime = info[tgt].split(',')[0]
    loadavg = info[tgt].split(',')[-3:]
    loadavg_1 = loadavg[0].strip('  load average:')
    loadavg_5 = loadavg[1]
    loadavg_15 = loadavg[2]
    login_user_num = sapi.SaltCmd(tgt=tgt,fun='cmd.run',client='local',arg='who |wc -l')['return'][0][tgt]
    processs = sapi.SaltCmd(tgt=tgt,fun='cmd.run',client='local',arg="ps -A -ostat")['return'][0][tgt]
    S = R = Z = 0
    for process in processs:
        if 'S' in process:
            S +=1
        elif 'R' in process:
            R +=1
        elif 'Z' in process:
            Z +=1
    LocalData = {'uptime': uptime,'ip': ip,'hostname': hostname,'os': OS,'disk_all': disk_all,'disk_free': disk_free,'disk_used': disk_used,'disk_used_p': disk_used_p,'loadavg_1': loadavg_1,'loadavg_5': loadavg_5,'loadavg_15': loadavg_15,'salt_version': saltstack_version,'mem_total': mem_total,'cpu_physical_num': cpu_model,'cpu_logical_cores': cpu_logical_cores,'process_num': S+R+Z, 'process_S': S,'process_R': R,'process_Z': Z,'login_user_num': login_user_num,'Manufacturer': Manufacturer,}
    return LocalData




if __name__ == '__main__':
    saltinfo(tgt='192.168.62.200')
