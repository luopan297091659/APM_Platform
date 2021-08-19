#! /bin/python3
# -*- coding:utf-8 -*-
from .android_adb import ADB as a
import os,re

a = a()
class device_meminfo(object):
    def __init__(self, *args):
        pass


    def get_device_meminfo(self, device_info):
        """
        获取设备内存信息
        """
        result = a.adb_dev_output(device_info, "free -k |grep -i mem")
        res = list(filter(None,result.split(" ")))
        total_mem, used_mem, free_mem = res[1], res[2], res[3]
        return total_mem, used_mem, free_mem


    def get_app_meminfo(self, device_info, app_name):
        result = a.adb_dev_output(device_info, "dumpsys meminfo", app_name,  '|grep -A 12 Summary |grep : |cut -d : -f 2')
        res = list(filter(None,result.split(" ")))
        java_mem, native_mem, code_mem, stack_mem, graph_mem, others_mem, system_mem, total_mem = res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]
        return java_mem, native_mem, code_mem, stack_mem, graph_mem, others_mem, system_mem, total_mem


    def get_device_info(self, device_info):
        device_sn = a.adb_dev_output(device_info,"getprop ro.boot.serialno")
        os_version = a.adb_dev_output(device_info,"getprop ro.build.version.incremental")
        return  device_sn, os_version
        

    def get_app_info(self, device_info, app_name):
        result = a.adb_dev_output(device_info, "dumpsys package", app_name,  '|grep -A 12 Summary |grep : |cut -d : -f 2')
        app_version = result
        return app_version

if __name__ == '__main__':
    #info=meminfo().get_device_meminfo('031E002109000013')
    #print(info)
    print(meminfo().get_device_info("031E002109000013"))
    print(meminfo().get_device_meminfo("031E002109000013"))
    print(meminfo().get_app_meminfo("031E002109000013", "com.rokid.launcher3"))