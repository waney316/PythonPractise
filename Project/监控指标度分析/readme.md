
## 分析过程
#### 采用模块
- requests
- queue
- threading
#### 流程
```
1: 获取当前zabbix下所有主机
返回：hostid, host, interface[0](第一个接口ip)
数据格式：[{"hostid": 1, "host": "1.1.1.1", "ip": "1.1.1.1"}]

2: 遍历主机获取该主机下所有监控项，针对自动发现监控项，仅提取匹配到的第一个
返回： itemid, hostid, count 
数据格式：[{"ip": "1.1.1.1", "data": [{"itemid": 123, "key_": "cpu", count: 1}, {"itemid": 123, "key_": "cpu", count: 1}]}]

3：遍历每个主机下的每个监控项，通过history获取数据，如果能获取到数据，则每个data下key值添加键值status: Boolean

数据格式：[{"ip": "1.1.1.1", "data": [
                                        {"itemid": 123, "key_": "cpu", count: 1, "status": True}, 
                                        {"itemid": 123, "key_": "cpu", count: 1, "status": False}
                                   ]},
          {"ip": "2.3.3.3", "data": [
                                        {"itemid": 123, "key_": "cpu", count: 1, "status": True}, 
                                        {"itemid": 123, "key_": "cpu", count: 1, "status": False}
                                   ]},
        ]

4：采用queue消息队列，每返回一个ip的数据，则向队列push

5: toData函数从queue队列取出数据，吐到kafak
```