
## 消费kafka数据转储告警

### 背景
业务侧方定时向kafak发送指标数据，指标数据类型为JSON,数据中包含key:value形式的数据，需要根据该数据设置产生告警


### 思路
#### zabbix
将数据从kafka取出来的同时，通过zabbix_sender命令将数据发到zabbix对应主机

优点：
- 数据存储可历史查询
- 代码易修改开发

缺点：
- 需要zabbix前端添加对应主机和创建模板
- 数据类型为json,不容易转告警

#### pushgateway
将数据从kafak取出来的同时，通过prometheus_client模块中push_gateway数据发到代理

优点：
- 数据存储标签化
- 需要添加主机和创建监控项，相对动态

缺点：
- 需要自定义告警规则
- 代码可能造成内存溢出

### 说明
#### 数据格式说明
- 每次从kafka消费的数据需要为json字符串
- json字符串需要包含`ip`,`time`,`metrics` 三个key值

### 脚本部署

#### 安装模块

```shell	
# 该方法为在线安装
pip install kafka-python PyYAML prometheus_client 

# 查询是否正常安装
pip list
```

#### 配置文件

```yaml
# 日志级别
logging: debug
logfile: push_metrics.log

# 选择工作模式, 发往数据到zabbix还是pushgateway
model: pushgateway  

# Pprometheus相关配置
pushgateway:
    server: "10.12.70.43:9099"
    job: "gbase_job"   # 分组

# zabbix相关配置
zabbix:
  server: "10.12.70.41"  # zabbix_server或proxyd地址

# kafka集群地址
kafka:
  bootstrap_servers: ["10.12.70.42:9092"]  # kafak地址
  topic: "gbase_data"   # topic地址

```

#### 启动

```
python3 run.py  查看数据正常发送后ctrl+c

后台启动
nohup python3 run.py > /dev/null &

日志查看
tailf logs/push_metrics.log
```

