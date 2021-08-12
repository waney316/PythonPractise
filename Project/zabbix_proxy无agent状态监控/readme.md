#### 背景
针对zabix_proxy与server连接状态监控, 由于agent如果挂载在proxy上,依赖proxy与server是否正常通信，如果proxy异常，可能导致告警可能无法正常触发。

#### 思路
- 通过zabbix api获取server下所有代理状态
- 将代理状态数据通过zabbix_sender发送至对应主机的监控模板zabbix采集器监控项
- 自动发现规则使用相关项目和JSONPATH采集zabbix采集器监控项的数据，并配置相关触发器
- 定时5分钟轮询更新代理状态数据


#### 引用功能模块
- subprocess
- zabbix_sender 
- zabbixapi
- crontab
- logging


#### 功能部署
##### zabbix端调整

```
1. 在zabbix创建server主机(不关心是否安装agent,如果agent安装也可适用)
2. 从zabbix server页面导入templates下模板
3. server主机关联对应模板
```

![image-20210811173409718](E:%5CWorkSpace%5CPythonPractise%5CProject%5Czabbix_proxy%E6%97%A0agent%E7%8A%B6%E6%80%81%E7%9B%91%E6%8E%A7%5Creadme.assets%5Cimage-20210811173409718.png)


##### 服务器端部署

```yaml
1. 拷贝脚本目录到指定目录下解压

2. 配置config/config.yml中参数
---
# 日志级别,一般默认不做调整
logging: debug
logfile: proxy_connect_server.log

# zabbix_proxy与server连接超时时间(s),即如果proxy和server如果最近一次通信时间超过timeout,则将状态值置为异常
timeout: 300

zabbix:
  host: "10.12.66.107"
  user: "wangwei"
  password: "aspire@1qaz2wsx"

# 映射zabbix_sender发送的相关信息
map_host: 10.12.66.107
map_proxy: 10.12.7.103
map_port: 10051
# 映射模板键值，一般不需要修改,如修改需要同步修改模板监控项值
key: "proxy_data"



3. 添加如下定时任务, 即每五分钟采集一次数据发至zabbix_server端，需要
*/5 * * * * /bin/python3 /opt/aspire/product/proxy_check/run.py >/dev/null 2>&1
```



#### 数据验证

##### 数据采集

![image-20210811173759212](E:%5CWorkSpace%5CPythonPractise%5CProject%5Czabbix_proxy%E6%97%A0agent%E7%8A%B6%E6%80%81%E7%9B%91%E6%8E%A7%5Creadme.assets%5Cimage-20210811173759212.png)

##### 告警验证

![image-20210811173823202](E:%5CWorkSpace%5CPythonPractise%5CProject%5Czabbix_proxy%E6%97%A0agent%E7%8A%B6%E6%80%81%E7%9B%91%E6%8E%A7%5Creadme.assets%5Cimage-20210811173823202.png)

