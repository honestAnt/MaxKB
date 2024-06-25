# 备份数据命令

## 创建用户
    CREATE USER maxkb_kunpeng WITH PASSWORD 'maxkb_kunpeng';

## 创建数据库
    CREATE DATABASE maxkb_kunpeng OWNER maxkb_kunpeng;
    CREATE EXTENSION "vector";

## 分配权限
    GRANT ALL PRIVILEGES ON DATABASE maxkb_kunpeng TO maxkb_kunpeng;

## 删除数据库
    DROP DATABASE maxkb_kunpeng


## 导出
    PGPASSWORD='maxkb_dev' pg_dump16 -U maxkb_dev -h 192.168.3.133 -p 15442 -F c -b -v -f /Users/wfb/Documents/20240625/postgres/maxkb_dev.dump maxkb_dev

## 导入
    PGPASSWORD='maxkb_test' pg_restore16 -U maxkb_test -h 192.168.3.133 -p 15442 -d maxkb_test -v /Users/wfb/Documents/20240625/postgres/maxkb_dev.dump
