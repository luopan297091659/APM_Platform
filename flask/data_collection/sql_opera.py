#! /bin/python3
# -*- coding:utf-8 -*-
import pymysql,datetime,uuid,string

"""
封装数据库操作
1. sql_exe
2. sql_get
3. insert_devices_info
4. insert_device_mem_info
5. insert_apps_info
6. insert_app_mem_info
7. insert_app_mem_detailed_info
......
"""

class sql_opera(object):

    def __init__(self,host,user_name,passwd,db, char='utf8'):
        self.host = host
        # self.port = port
        self.username=user_name
        self.passwd=passwd
        self.mysqldb=db
        self.char=char

        self.MySQL_db = pymysql.connect(
            host=self.host,
            user=self.username,
            passwd=self.passwd,
            db=self.mysqldb,
            charset=self.char)
        self.cursor=self.MySQL_db.cursor()

    def sql_exe(self,sql):
        cursor = self.MySQL_db.cursor()
        MySQL_sql = sql
        try:
            # 执行SQL语句
            cursor.execute(MySQL_sql)
            self.MySQL_db.commit()
            print(111111)
        except:
            print("Error: unable to fetch data")
            cursor.rollback()
            #self.MySQL_db.close()
        #self.MySQL_db.close()

    def sql_get(self,sql):
        self.cursor.execute(sql)
        datas = self.cursor.fetchall() 
        return datas

    def insert_devices_info(self, *args):
        for device_sn in args:
            #insert_sql = "INSERT IGNORE INTO app_info (device_sn) VALUES ('%s');" % (device_sn)
            #get_table = "select device_sn from devices_info;"
            #query_res = "SELECT IFNULL((SELECT 'Y' from devices_info  where device_sn = '%s' limit 1),'N')" % device_sn
            query_count = "SELECT  count(device_sn) from devices_info where device_sn='%s';" % (device_sn)
            datas = self.sql_get(query_count)
            print(datas,datas[0][0],type(datas[0][0]))
            if datas[0][0] == 0:
                insert_sql = "INSERT INTO devices_info (device_sn) VALUES ('%s');" % (device_sn)
                print(device_sn,insert_sql)
                self.sql_exe(insert_sql)

    def insert_device_mem_info(self, m_uuid, device_id, os_version, time=None):
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        if not time:
            insert_sql = "INSERT device_mem_info (m_uuid, device_id, os_version, start_time) VALUES ('%s','%s','%s','%s')" % (m_uuid, device_id, os_version, current_time)
        else:
            insert_sql = "UPDATE device_mem_info SET end_time='%s' WHERE uuid=%s;" %(current_time, m_uuid)
        self.sql_exe(insert_sql)
        
    def insert_device_mem_detail_info(self, phy_mem, used_mem, free_mem):
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        insert_sql = "INSERT INTO device_mem_info (phy_mem, used_mem, free_mem, cur_time) VALUES ('%s','%s','%s','%s');" % (phy_mem, used_mem, free_mem, current_time)
        self.sql_exe(insert_sql)

    def insert_apps_info(self, *args):
        for app_name in args:
            query_count = "SELECT  count(app_id) from apps_info where app_name='%s';" % (app_name)
            datas = self.sql_get(query_count)
            if datas[0][0] == 0:
                insert_sql = "INSERT INTO apps_info (app_name) VALUES ('%s');" % (app_name)
                self.sql_exe(insert_sql)

    def insert_app_mem_info(self, uuid, app_id, app_version, device_id, time=None):   
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')            
        #a_uuid = str(uuid.uuid1()).replace("-", '')
        if not time:
            insert_sql = "INSERT INTO app_mem_info (uuid, app_id, app_version, device_id, start_time) VALUES ('%s', '%s', '%s', '%s', '%s');" % (uuid, app_id, app_version, device_id, current_time)
        else:
            insert_sql = "UPDATE app_mem_info SET end_time='%s' WHERE uuid=%s;" %(current_time, uuid)
        print(insert_sql)
        self.sql_exe(insert_sql)

    def insert_app_mem_detailed_info(self, a_uuid, app_id, device_id, java_mem, naive_mem, graph_mem, stack_mem, code_mem, others_mem, system_mem, total_mem):
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        insert_sql = "INSERT INTO app_mem_detailed_info (uuid, app_id, device_id, java_mem, native_mem, graph_mem, stack_mem, code_mem, others_mem, system_mem, total_mem, cur_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (a_uuid, app_id, device_id, java_mem, naive_mem, graph_mem, stack_mem, code_mem, others_mem, system_mem, total_mem, current_time)
        print(insert_sql)
        self.sql_exe(insert_sql)



if __name__ == '__main__':
    conn=sql_opera("127.0.0.1","root","rokid@123","apm_test")
    conn.insert_devices_info("031E002109000029","031E002109000021","031E002109000019")
    conn.insert_apps_info("com.rokid.glass.launcher")
    res=conn.sql_get("select app_id from apps_info where app_name='com.rokid.glass.launcher';")
    app_id=res[0][0]
    res=conn.sql_get("select device_id from devices_info where device_sn='031E002109000029';")
    device_id=res[0][0]
    a_uuid = str(uuid.uuid1()).replace("-", '')
    app_version='1.2.0'
    conn.insert_app_mem_info(a_uuid, app_id, app_version, device_id)
    conn.insert_app_mem_detailed_info(a_uuid, app_id,  device_id, "1212121", "67899", "212121", "112121", "12123565", "98669", "90", "908080")


    
