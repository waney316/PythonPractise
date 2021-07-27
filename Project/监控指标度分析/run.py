# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import traceback
import pathlib
import logging.handlers

from queue import  Queue
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

from common.common_func import generate_headers, handle_host



# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

# 初始判断当前目录和指定文件是否存在
curren_path = os.getcwd()
origin_dirs = ["config", "common", "logs"]
if len(set(origin_dirs) & set(os.listdir(BASE_DIR))) < len(origin_dirs):
    print(f"工作路径不对或缺少工作目录{origin_dirs}")

if not pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")):
    print("请确保config目录下存在config.yml文件")
    sys.exit(1)

# 确认是否安装requests/queue模块
try:
    import requests
    import queue
    import yaml
    from kafka import KafkaProducer
    from kafka.errors import kafka_errors
except ImportError:
    print("模块导入错误，请确保模块 requests/queue 模块已经安装")
    sys.exit(1)

# 读取config.yml配置信息
with open(os.path.join(BASE_DIR, "config/config.yml"), encoding="utf-8") as f:
    config = yaml.safe_load(f)

#初始化日志配置
logger = logging.getLogger("monitor_metrics_logs")
logger.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 设置为日志轮询handler到指定文件
log_handler = logging.handlers.TimedRotatingFileHandler(
    filename=os.path.join(BASE_DIR, "logs", config.get("logfile")),
    when="D",
    interval=1,
    backupCount=7)
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)

# 输出日志到控制台
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)


class ZabbixObject():
    def __init__(self, url, user, password, queue):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = urljoin(url, "zabbix/api_jsonrpc.php")
        self.token = self._get_token()
        self.queue = queue

    # 获取zabbix登录token
    def _get_token(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.password
            },
            "id": 1,
            "auth": None
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data, timeout=2)
        except Exception as e:
            logger.error(f"zabbix: {self.url}-请求超时或错误{e}, exiting....")
            sys.exit(1)
        else:
            if json.loads(res.text).get("error"):
                logger.error(f"{ json.loads(res.text).get('error')}, exiting....")
                sys.exit(1)
            elif not res.json().get("result"):
                logger.error(f"zabbix: {self.url}-get None token, exiting....")
                sys.exit(1)
            else:
                logger.info(f"zabbix: {self.url}-success: get token-{res.json().get('result')}")
                return res.json().get("result")

    # 获取zabbix所有主机列表主机列表
    def get_all_host(self, *args, **kwargs):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "selectItems": ["itemid", "name", "key_", "lastclock", "state", "flags", "type"],
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception:
            logger.error(f"zabbix: {self.url}-获取主机列表超时或错误")
        else:
            host_list = json.loads(res.text).get("result")
            # host_list列表不为空, 即存在主机接入
            if not host_list:
                logger.error(f"zabix-{self.url}-host_list列表为空")
                return None

            # 遍历所有主机列表
            for host in host_list:
                response = handle_host(host, kwargs.get("exclude_metrics_type"))
                logger.info(f"get response from host: {host}, data: {response}, put to the queue")
                self.queue.put(response)


class Producer():
    def __init__(self, producer, queue):
        # 初始化kafak集群地址
        self.producer = producer
        self.queue = queue

    def send(self):
        # 从队列取出数据
        while not self.queue.empty():
            future = self.producer.send(
                'kafka_demo',  # topic
                key='count_num',  # key
                value=str(self.queue.get()),
                partition=1)  # 向分区1发送消息
            logger.info("send {}".format(str(self.queue.get())))
            try:
                future.get(timeout=10)  # 监控是否发送成功
            except kafka_errors:  # 发送失败抛出kafka_errors
                traceback.format_exc()



if __name__ == '__main__':
    try:
        datasource = config.get("datasource").get("server")
        poolSize = config.get("threadPool")
        excluding_metrics_type = config.get("excluding_metrics_type")

        bootstrap_servers = config.get("bootstrap_servers")
    except Exception as e:
        logger.error("获取zabbix数据源错误,请检查语法")
        sys.exit(1)

    # 根据server数量创建线程池
    tasks = []
    q = Queue(1000)
    executor = ThreadPoolExecutor(max_workers=poolSize)

    # 构建kafka生产者
    print(bootstrap_servers)
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode())
    except Exception:
        logger.error(f"kafka cluster: {bootstrap_servers} connect faild")

    # 开启zabbix数据获取线程
    for server in datasource:
        zabbix = ZabbixObject(server["url"], server["user"], server["password"], q)
        # execute_thread(zabbix)
        # 生产者线程
        zabbix_future = executor.submit(zabbix.get_all_host, **{"exclude_metrics_type": excluding_metrics_type})
        tasks.append(zabbix_future)


    # # 开启kafka数据生产线程
    producer = Producer(producer, q)
    kafka_future = executor.submit(producer.send, )


    # 当zabbix线程结束后, 且队列为空，结束kafak线程
    # if [  task in tasks]
