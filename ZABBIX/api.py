# coding:utf-8
import time
from zabbix_client import ZabbixServerProxy


class Zabbix():
    def __init__(self):
        self.zb = ZabbixServerProxy("http://192.168.10.100/zabbix")
        self.zb.user.login(user="Admin", password="zabbix")

    ############## 查询组所有组获取组id ###############
    def get_hostgroup(self):
        data = {
            "output": ['groupid', 'name']
        }
        ret = self.zb.hostgroup.get(**data)
        return ret

        ########### 通过组id获取相关组内的所有主机 ###############

    def get_hostid(self, groupids=2):
        data = {
            "output": ["hostid", "name"],
            "groupids": groupids
        }
        ret = self.zb.host.get(**data)
        return ret

    ########## 通过获取的hostid查找相关监控想itemid ###################
    def item_get(self, hostids="10115"):
        data = {
            "output": ["itemids", "key_"],
            "hostids": hostids,
        }
        ret = self.zb.item.get(**data)
        return ret

    ######### 通过itemid（传入itemid和i0表示flast类型）获取相关监控项的历史数据 ###########
    def history_get(self, itemid, i, limit=10):
        data = {"output": "extend",
                "history": i,
                "itemids": [itemid],
                "limit": limit
                }
        ret = self.zb.history.get(**data)
        return ret

    ###############添加主机并且指定到组（传入主机名，IP地址和组ID）#####################
    def add_zabbix_host(self, hostname="test_zabbix", ip="192.168.10.100", groupid="2"):
        data = {
            "host": hostname,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": groupid
                }
            ]
        }
        ret = self.zb.host.create(data)
        return ret

    #####################查看现有模板#######################
    def get_template(self):
        datalist = []
        datadict = {}
        data = {
            "output": ["templateid", "name"]
        }
        ret = self.zb.template.get(data)
        for i in ret:
            datadict[i['name']] = i['templateid']
            datalist.append(datadict)
        return datalist

        #################### 关联主机到模板##################################

    def link_template(self, hostid=10156, templateids=10001):
        data = {
            "hostid": hostid,
            "templates": templateids
        }

        ret = self.zb.host.update(data)
        return ret

    ###################  添加维护周期，，######################################

    def create_maintenance(self, name="test", hostids=10156, time=2):
        data = {
            "name": name,
            "active_since": 1458142800,
            "active_till": 1489678800,
            "hostids": [
                hostids
            ],
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": 3600
                }
            ]
        }
        ret = self.zb.maintenance.create(data)
        self.host_status(10130, 1)
        return ret

    ################获取维护周期，，#########################
    def get_maintenance(self):
        data = {
            "output": "extend",
            "selectGroups": "extend",
            "selectTimeperiods": "extend"
        }
        ret = self.zb.maintenance.get(data)
        return ret

    ##############获取维护周期之后，通过传入maintenanceid删除维护周期###########
    def del_maintenance(self, maintenanceids):
        return self.zb.maintenance.delete(maintenanceids)
        #########################添加维护周期时候需要吧zabbix_host设置成非监控状态##################

    def host_status(self, hostid, status):
        data = {
            "hostid": hostid,
            "status": status
        }
        return self.zb.host.update(data)

    ###########通过hostids删除主机id,顺带也删除模板#########

    def host_del(self, hostids=10155):
        return self.zb.host.delete(hostids)


if __name__ == "__main__":
    zabbix_server = Zabbix()
    # print zabbix_server.get_hostgroup()
    # print zabbix_server.get_hostid()
    # print zabbix_server.item_get(10156)
    # data = zabbix_server.history_get("24889",0)
    # print zabbix_server.get_hostgroup()
    # print zabbix_server.add_zabbix_host()
    # data = zabbix_server.get_template()
    # print data[0]['Template OS Linux']
    # print zabbix_server.link_template()
    # print zabbix_server.create_maintenance()
    # print zabbix_server.host_del(10155)
    # print zabbix_server.get_maintenance()
    print zabbix_server.del_maintenance(15)