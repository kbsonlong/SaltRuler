#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#

import xmlrpclib
import os

class CobblerAPI(object):
    def __init__(self,url,user,password):
        self.remote = xmlrpclib.Server(url)
        self.token = self.remote.login(user,password)
        self.ret = {
                "result": True,
                "comment": [],
            }
 
    def add_system(self,hostname,ip_add,mac_add,profile,gateway,subnet):
        '''
        Add Cobbler System Infomation
        '''
        system_id = self.remote.new_system(self.token) 
        self.remote.modify_system(system_id,"name",hostname,self.token) 
        self.remote.modify_system(system_id,"hostname",hostname,self.token) 
        self.remote.modify_system(system_id,'modify_interface', { 
 	    "macaddress-eth0"   : mac_add,
            "ipaddress-eth0"    : ip_add,
            "gateway-eth0"      : gateway,
            "subnet-eth0"       : subnet,
            "static-eth0"       : 1,
            "name-servers-eth0"      : "114.114.114.114,8.8.8.8", 
            }, self.token) 
        self.remote.modify_system(system_id,"profile",profile,self.token) 
        self.remote.save_system(system_id, self.token) 
        try:
            self.remote.sync(self.token)
            os.system("cobbler system edit --name=%s --gateway=%s"%(hostname,gateway))
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
        return self.ret


    def get_systems(self):
        try:
            systems = self.remote.get_systems()
            return systems
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
            return self.ret

    def get_profile(self):
        """
	get cobbler profile return
	"""
        try:
            os = self.remote.get_profiles(self.token)
            return os
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
            return self.ret

    def get_distro(self):
        """
	get cobbler distro return
	"""
        try:
            os = self.remote.get_distros(self.token)
            return os
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
            return self.ret

    def create_profile(self,name,distro,ks):
        """
	    create cobbler profile
	"""
        profile_id = self.remote.new_profile(self.token)
        self.remote.modify_profile(profile_id,"name",name,self.token)
        self.remote.modify_profile(profile_id,"distro",distro,self.token)
        self.remote.modify_profile(profile_id,"kickstart",ks,self.token)
        self.remote.save_profile(profile_id, self.token)
        try:
                self.remote.sync(self.token)
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
        return self.ret

    def remove_profile(self,name):
        """
            remove cobbler profile
        """
        try:
            self.remote.remove_profile(name,self.token)
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
        return self.ret

    # def remove_system(self,name):
    #     """
    #         remove cobbler profile
    #     """
    #     try:
    #         self.remote.remove_system(name,self.token)
    #     except Exception as e:
    #         self.ret['result'] = False
    #         self.ret['comment'].append(str(e))
    #     return self.ret
	

if __name__ == '__main__':
    system =  CobblerAPI("http://192.168.62.110/cobbler_api","admin","kbsonlong")
    print system.get_profile()

