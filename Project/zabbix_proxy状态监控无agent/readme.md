#### 背景
针对zabix_proxy与server连接状态监控, 由于agent如果挂载在proxy上,依赖proxy的启动，导致告警可能无法正常触发，

#### 思路
- zabbix上创建zabbix_proxy监控模板，添加自动发现规则
- 通过zabbix api获取server下所有代理状态
- 将代理状态数据通过zabbix_sender发送至对应主机的监控模板
- 定时5分钟轮询更新代理状态数据


#### 引用功能模块
- subprocess
- zabbix_sender
- zabbixapi
- crontab
- logging


#### 功能部署


