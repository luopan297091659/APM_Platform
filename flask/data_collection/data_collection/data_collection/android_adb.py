# /bin/python3
# -*- coding:utf-8 -*-


"""
封装常用的adb操作
1. adb options
2. adb devices
3. adb get-state
4. adb reboot
5. adb push
6. adb pull
7. adb shell am start
8. adb shell ps | grep
......
"""


import os,logging
import adbutils,subprocess

class ADB(object):
    def __init__(self):
        pass


    def adb_dev_output(self, dock_info, *args, port="5555"):
        """
        网络接连指定设备运行命令
        """
        cmds = [adbutils.adb_path(), '-s', dock_info, 'shell']
        cmds.extend(args)
        cmdline = subprocess.list2cmdline(map(str, cmds))
        print(cmdline)
        try:
            return subprocess.check_output(cmdline, stderr=subprocess.STDOUT, shell=True).decode('utf-8').replace('\n', '')
        except EOFError:
            logging.error("%s 命令执行失败" % cmdline)

    
    def get_state(self, device: str) -> str:
        """
        获取设备的连接状态
        :param device: 设备sn号
        :return: 设备连接状态
        """
        result = self.adb_dev_output("-s %s get-state" % device)
        result = result.strip(' \t\n\r')
        return result or None