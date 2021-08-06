# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 11:20
# @Author  : waney
# @File    : run.py

import json
import os
import sys
import pathlib

from common.telnet import scan
from common.logger import CustomLogger
from common.verify_data import verify_metrics

# 判断当前python版本是否>3.5
if not sys.version_info > (3,5):
    print("current python version < 3.5, exiting...")
    sys.exit(1)

# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

# 初始判断当前目录和指定文件是否存在
origin_dirs = ["config", "common", "logs", "tools"]
if len(set(origin_dirs) & set(os.listdir(BASE_DIR))) < len(origin_dirs):
    print(f"工作路径不对或缺少工作目录{origin_dirs}")
    sys.exit(1)

if not pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")):
    print("请确保config目录下存在config.yml文件")
    sys.exit(1)

try:
    import requests
    import yaml
    import subprocess
    from kafka import KafkaConsumer
    from kafka.errors import kafka_errors
    from prometheus_client import CollectorRegistry, Gauge, push_to_gateway # 如果不通过pushgatewaty发送数据,注释
except ImportError as e:
    print(f"模块导入错误，请确保涉及模块已经安装{e}")
    sys.exit(1)

# 读取config.yml配置信息
with open(os.path.join(BASE_DIR, "config/config.yml"), encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 初始化日志模块
logger = CustomLogger(os.path.join(BASE_DIR, "logs", config.get("logfile")), "push_metrics")


class CustomKafkaConsumer():
    def __init__(self, bootstrap_servers, kafkatopic):
        self.kafkatopic = kafkatopic
        self.consumer = KafkaConsumer(self.kafkatopic,
                                      bootstrap_servers=bootstrap_servers,
                                      value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    def consume_data(self):
        try:
            for message in self.consumer:
                # yield生成器返回数据
                yield message
        except KeyboardInterrupt as e:
            print(e)


# send数据到pushgateway:guage
class SendMetricsGateWay():
    def __init__(self, server, job):
        self.server = server
        self.job = job

        # 初始化时判断pushwateway连通性
        host = self.server.split(":")[0]
        port = self.server.split(":")[1]
        is_open,msg = scan(host, port)
        if is_open:
            logger.info(f"{self.server} connnect ok")
        else:
            logger.error(f"{self.server} connnect fail-{msg}, check network and service")
            sys.exit(1)

    def send_metrics(self, data):
        registry = CollectorRegistry()
        # 数据替换
        metric = data.get("metric")
        help = f"Description of gauge metrics-{metric}"
        value = data.get("value")
        data["instance"] = data.pop("ip")

        # 去除data中time/value,否则每次label标签不一致
        data.pop("time")
        data.pop("value")

        # label
        extra_keys = [k for k in data.keys()]

        guage = Gauge(metric, help, extra_keys, registry=registry)
        guage.labels(**data).set(value)

        # push metrics to gateway
        try:
            push_to_gateway(self.server, job=self.job, registry=registry, timeout=5)
        except Exception as e:
            logger.error(f"send metrics {data} to {self.server} failed")


# send数据到zabbix
class SendMetricsZbx():
    def __init__(self, server):
        tools_name = pathlib.Path(os.path.join(BASE_DIR, "tools/zabbix_sender"))
        if not tools_name:
            logger.error("tools dir not contains zabbix_sender")
            sys.exit(1)

        # 检查zabbix_sender命令是否有可执行权限
        if not os.access(tools_name, os.X_OK):
            logger.error("zabbix-sender not have execute privileges, please use chmod +x toosl/zabbix_sender")
            sys.exit(1)

        # 数据发往zabbix的地址
        self.server = server
        # 初始化时判断pushwateway连通性
        is_open, msg = scan(self.server, "10051")
        if is_open:
            logger.info(f"{self.server} connnect ok")
        else:
            logger.error(f"{self.server} connect fail-{msg}, check the zabbix service is running")
            sys.exit(1)

    def send_metrics(self, data):
        # 检查tools目录下是否存在zabbix_sender

        ip = data.get("ip")
        key = data.get("metric")
        # value = data.get("value")

        cmd = f"tools/zabbix_sender -s {ip} -z {self.server} -k '{key}' -o \"{str(data)}\" -vv"
        try:
            res = subprocess.getoutput(cmd)
            logger.info(str(res))
        except Exception as e:
            logger.error(f"send {ip} metrics {key} failed >>> {e}")


if __name__ == '__main__':
    try:
        push_server = config.get("pushfateway")
        kafka_config = config.get("kafka")
        model = config.get("model")

    except Exception as e:
        logger.error("get datasource from config.yml error")
        sys.exit(1)

    # 初始化kafak消费对象
    try:
        kafka_consmer = CustomKafkaConsumer(kafka_config.get("bootstrap_servers"), kafka_config.get("topic"))
    except Exception as e:
        logger.error(f"kafka consumer init faild {e}")
        sys.exit(1)
    else:
        logger.info(f"kafka-{kafka_config.get('bootstrap_servers')} connect success")

    # 根据选择的model确认数据接收端sender
    server = config.get(model).get("server")
    sender = SendMetricsZbx(server) if server == "zabbix" else SendMetricsGateWay(server, config.get(model).get("job"))

    # 获取topic数据
    messages = kafka_consmer.consume_data()
    for msg in messages:
        # 校验数据
        if verify_metrics(msg.value):
            # 发送数据至zabbix
            logger.info(f"get metric {msg}")
            sender.send_metrics(json.loads(msg.value))
            logger.info(f"send metrics {msg} to {model} success")
        else:
            logger.error(f"metrics-{msg} verify failed")