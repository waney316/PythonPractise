
## 监控指标覆盖度分析

### 背景
监控指标覆盖度主要统计每个IP下所有指标，并判断该指标是否正常监控采集，从而用来分析主机的监控覆盖度。

### 开发过程

 #### 分析过程
- 取出zabbix上所有主机及每个主机下的监控项
- 针对监控项过滤去重处理
    - 判断当前主机当前监控项是否采集到值
    - 判断当前主机当前监控项是否为自动发现, 如果是,取出第一个
    - 统计监控项数量(普通监控项和自动发现监控项)
- 数据处理后返回发到kafak指定topic

#### 采用模块
- requests (zabbix api请求)
- queue (队列, 存储IP数据)
- KafkaProducer (生产数据)
- ThreadPoolExecutor(线程池,处理多个zabbix和多线程kafka生产message)
- logging (日志记录)
- yaml(配置文件解析)

#### BUG问题

- 使用host.get方法可返回zabbix上所有主机和主机下监控项，当主机数量超过1000或更多时，会触发500错误，无法从zabbix取出数据

- 当使用多线程遍历主机列表取出监控项数据时，zabbixapi限制导致部分主机查询报错remote no response

  

### 脚本部署

#### 安装模块

```shell	
# 该方法为在线安装
pip install kafka-python PyYAML requests 

# 查询是否正常安装
pip list
```

#### 配置文件

```yaml
---
# 日志级别
logging: debug
logfile: monitor_metrics.log    #日志名称


# 线程池数量：
thread_pool_size: 20

# zabbix数据源配置
datasource:
  server:
    - name: "idc_zabbix"
      url: "http://10.12.66.107"
      user: "wangwei"
      password: "aspire@1qaz2wsx"

# kafka集群地址
kafka:
  bootstrap_servers: ["10.12.70.42:9092"]
  topic: "zabbix"
  thread_nums: 10    # kafka消息发送线程数量, 需要小于thread_pool_size

# 忽略的监控项类型
excluding_metrics_type:
  - 17  # snmptrap监控项
  - 9  	# web监控项
  - 5  	# zabbix内部监控项
```

#### 创建定时任务

```
* */12 * * * /bin/python /xxx/xxxx/run.py
```


#### 指标范例
- hostid: 主机ID
- host: 主机名
- ip: 主机IP
- data：当前主机的监控项集合
  - itemid: 监控项id
  - name： 监控项名称
  - key_: 监控项键值
  - state: 监控项状态(1: 禁用/0:启用)
  - value: 监控项是否正常采集 (1:正常/0:异常)
  - count: 关联指标项计数 (区分自动发现监控项和普通监控项)

```json
{
    "hostid":"10084",
    "host":"Zabbix server",
    "ip":"127.0.0.1",
    "data":[
        {
            "itemid":"23327",
            "name":"Host name of Zabbix agent running",
            "key_":"agent.hostname",
            "state":"0",
            "value":1,
            "count":1
        }
    ]
}
```
