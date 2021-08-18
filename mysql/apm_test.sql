exec sp_addlinkedserver '','ms','SQLOLEDB','127.0.0.1,3306';
CREATE DATABASE if not EXISTS apm_test;

#device_info
CREATE TABLE if not EXISTS `devices_info`(
    `device_id`int(11) NOT NULL AUTO_INCREMENT COMMENT '设备id',
    `device_sn` varchar(25) NOT NULL COMMENT '设备sn',
    PRIMARY KEY(device_id)
)ENGINE=INNODB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `device_mem_info`(
    `m_uuid` varchar(40) NOT NULL COMMENT 'uuid',
    `device_id` int(11) NOT NULL COMMENT '设备id',
    `os_version` VARCHAR(40) NOT NULL COMMENT '系统版本',
    `start_time`  DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01' COMMENT '开始时间',
    `end_time` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01' COMMENT '结束时间',
    PRIMARY key(m_uuid),
    foreign key (device_id) references devices_info (device_id)  
)ENGINE=INNODB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `device_mem_detailed_info`(
    `m_uuid` varchar(40) NOT NULL COMMENT 'uuid',
    `device_id` int(11) NOT NULL COMMENT '设备id',
    `phy_mem` DOUBLE(30,3) NOT NULL COMMENT '物理内存',
    `used_mem` DOUBLE(30,3) NOT NULL COMMENT '使用内存',
    `free_mem` DOUBLE(30,3) NOT NULL COMMENT '空闲内存',
    `cur_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:01' COMMENT '时间',
    FOREIGN KEY (`m_uuid`) REFERENCES `device_mem_info` (`m_uuid`),
    foreign key (device_id) references devices_info (device_id) 
)ENGINE=INNODB DEFAULT CHARSET=utf8mb4;

CREATE TABLE if NOT EXISTS `apps_info`(
    `app_id` int(8) NOT NULL AUTO_INCREMENT COMMENT '应用ID',
    `app_name` VARCHAR(100) COMMENT '应用名称',
    PRIMARY KEY(app_id)
)ENGINE=INNODB DEFAULT CHARSET=utf8mb4;

CREATE TABLE if NOT EXISTS `apps_version`(
    `app_id` int(8) NOT NULL COMMENT '应用ID',
    `app_version` VARCHAR(100) COMMENT '应用名称',
    PRIMARY KEY(app_id)
)ENGINE=INNODB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `app_mem_info` (
  `uuid` varchar(40) NOT NULL COMMENT 'uuid',
  `app_id` int(8) NOT NULL COMMENT '应用id',
  `app_version` VARCHAR(8) NOT NULL COMMENT '应用版本',
  `device_id` int(11) NOT NULL COMMENT '设备id',
  `start_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:01' COMMENT '开始时间',
  `end_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:01' COMMENT '结束时间',
  PRIMARY KEY (`uuid`),
  FOREIGN KEY (`app_id`) REFERENCES `apps_info` (`app_id`),
  foreign key (`device_id`) references devices_info (`device_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `app_mem_detailed_info` (
  `uuid` varchar(40) NOT NULL COMMENT 'uuid',
  `app_id` int(8) NOT NULL COMMENT '应用id',
  `device_id` int(11) NOT NULL COMMENT '设备id',
  `java_mem` decimal(30,3) NOT NULL,
  `native_mem` decimal(30,3) NOT NULL,
  `graph_mem` decimal(30,3) NOT NULL,
  `stack_mem` decimal(30,3) NOT NULL,
  `code_mem` decimal(30,3) NOT NULL,
  `others_mem` decimal(30,3) NOT NULL,
  `system_mem` decimal(30,3) NOT NULL,
  `total_mem` decimal(30,3) NOT NULL,
  `cur_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:01',
  KEY `uuid` (`uuid`),
  FOREIGN KEY (`uuid`) REFERENCES `app_mem_info` (`uuid`),
  FOREIGN KEY (`app_id`) REFERENCES `apps_info` (`app_id`),
  foreign key (`device_id`) references devices_info (`device_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#INSERT INTO app_mem_detailed_info (uuid, app_id, java_mem, native_mem, graph_mem, stack_mem, code_mem, others_mem, system_mem, total_mem, cur_time) VALUES ('f8911726f82011eba487acde48001122', '12', '1212121', '67899', '212121', '112121', '12123565', '98669', '90', '908080', '2021-08-08 16:16:45');