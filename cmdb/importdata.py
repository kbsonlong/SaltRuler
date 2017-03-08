#!/usr/bin/env python
#coding:utf-8
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SaltRuler.settings")

from cmdb.models import Blog,Assetmanage
def importdata(file):
    f = open(file)

    List = []
    for line in f:
        values = line.split(',')
        List.append(Assetmanage(asset_num=values[0].strip(' '), type=values[1].strip(' ') , server_ip=values[2].strip(' ') , remote_ip=values[3].strip(' ') , data_center=values[4].strip(' ') , room_num=values[5].strip(' ') , rack_num=values[6].strip(' ') , system_type=values[7].strip(' ') , cputype_num=values[8].strip(' ') , disksize_num=values[9].strip(' ') , memsize_num= values[10].strip(' '), disk_raid=values[11].strip(' ') , card_type_num=values[12].strip(' ') , power_num=values[13].strip(' ') , service_num=values[14].strip(' ') , buy_time=values[15].strip(' ') , expiration_time=values[16].strip(' ') , note=values[17]))
    f.close()

    # 以上四行 也可以用 列表解析 写成下面这样
    # BlogList = [Blog(title=line.split('****')[0], content=line.split('****')[1]) for line in f]

    Assetmanage.objects.bulk_create(List)


if __name__ == "__main__":
    importdata(u'importserver.txt')
    print('Done!')