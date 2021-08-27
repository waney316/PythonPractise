#### 说明
通过巡检zabbix上监控的主机指定监控项，来判断主机监控数据采集是否正常，并可通过配置按照zabbix数据源/proxy代理/主机群组来邮件告知指定人员

##### 三种模式related_key
- server  按照server进行通知,可配置多个数据源
- proxy: 按照proxy进行通知,仅支持配置一个数据源
- group: 按照主机群组进行通知,仅支持配置一个数据源


#### 适用环境
- 适用于agent/snmp接口类型的数据巡检，不支持web监控等其他方式
- 不支持windwos类型的agent


#### 配置参数
```yaml
---
# 只适用于agent/snmp接口类型的数据巡检，不支持web监控等其他方式

# 日志级别
logging: debug
logfile: monitor_hosts_inspect.log


# 巡检指标映射值
inspect_map:
  - type: 1  # 1: agent类型
    key: "system.cpu.util[,idle,avg5]"
  - type: 2  # 2： snmp类型
    key: "sysDescr"

related_key: server

# zabbix数据源配置,name需要保证唯一性,避免奇怪问题产生
datasource:
  server:
    - name: "idc_zabbix"
      url: "http://10.12.66.107"
      user: "wangwei"
      password: "aspire@1qaz2wsx"

#    - name: "cloud_zabbix"
#      url: "http://120.25.168.251:8989"
#      user: "Admin"
#      password: "aspire@1qaz2wsx"
#
#    - name: "cloud_zabbix2"
#      url: "http://120.25.168.251:8989"
#      user: "Admin"
#      password: "aspire@1qaz2wsx"

# smtp发件服务器配置
smtp_from: "zabbix@sz.mail"
smtp_server: 10.1.9.82

# 收件人配置
receivers:
  - name: "北京xxxx"       # 邮件标题关键字
    related_value: []     # 收件人关联信息, 如果related_key为proxy, 需要填代理数据(无需区分大小写)；如果为group需要为主机群组数据
    emails: []            # 收件邮箱

```