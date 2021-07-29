# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import pathlib
import logging.handlers

from queue import Queue
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED, ALL_COMPLETED
from common.common_func import generate_headers, handle_host, handle_thread, send_message


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

# 确认是否安装requests/queue, kafka模块
try:
    import requests
    import queue
    import yaml
    from kafka import KafkaProducer
    from kafka.errors import kafka_errors
except ImportError:
    print("模块导入错误，请确保模块 requests/queue/kafka 模块已经安装")
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
    def __init__(self, url, user, password, queue, excude_metrics):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = urljoin(url, "zabbix/api_jsonrpc.php")
        self.token = self._get_token()
        self.queue = queue
        self.exclude_metrics = excude_metrics

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
                "output": ["hostid", "host"]
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data, stream=True)
        except Exception as e:
            logger.error(f"zabbix: {self.url}-获取主机列表超时或错误{e}")
        else:
            host_list = json.loads(res.text).get("result")
            # host_list列表不为空, 即存在主机接入
            if not host_list:
                logger.error(f"zabix-{self.url}-host_list列表为空")
                return None

            # 返回主机列表
            return host_list

    # 根据host返回主机items
    def get_host_item(self, host, *args, **kwargs):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "hostids": host.get("hostid"),
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "selectItems": ["itemid", "name", "key_", "lastclock", "state", "flags", "type"]
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception as e:
            logger.error(f"zabbix: {self.url}-host: {host}-获取主机监控项数据超时或错误{e}")
        else:
            host_metrics = json.loads(res.text).get("result")[0]
            # host_list列表不为空, 即存在主机接入
            response = handle_host(host_metrics, self.exclude_metrics)
            self.queue.put(response)
            logger.info(f"get response from zabbix {self.url} host: {host.get('host')} and put to the queue")


if __name__ == '__main__':
    try:
        datasource = config.get("datasource").get("server")
        exclude_metrics = config.get("excluding_metrics_type")
        kafka_config = config.get("kafka")
        thread_pool_size = config.get("thread_pool_size")
    except Exception as e:
        logger.error("获取zabbix数据源错误,请检查语法")
        sys.exit(1)

    # 构造队列存储每个主机IP数据
    queue = Queue(10000)
    # 构造线程池
    executor = ThreadPoolExecutor(max_workers=int(thread_pool_size))
    future_tasks = []

    for server in datasource:
        zabbix = ZabbixObject(server["url"], server["user"], server["password"], queue, exclude_metrics)
        hostlist = zabbix.get_all_host()
        zabbix_future = executor.submit(handle_thread, zabbix, hostlist, )
        future_tasks.append(zabbix_future)

    wait(future_tasks, return_when=ALL_COMPLETED)
    # 开启kafka数据同步线程
    kafka_tasks = []
    start_time = time.time()
    try:
        p = KafkaProducer(bootstrap_servers=kafka_config.get("bootstrap_servers"))
        kafka_thread_nums = kafka_config.get("thread_nums")
        topic = kafka_config.get("topic")
    except Exception as e:
        logger.error(f"kafka cluster: {kafka_config.get('bootstrap_servers')} connect faild: {e}")
    else:
        logger.info(f"connect to the kafka cluster {kafka_config.get('bootstrap_servers')}")
        # send_message(p, queue, logger, topic)  # 单线程测试
        print(queue.qsize())
        # 开启kafka_thread_nums个线程用于发送kafak消息
        for i in range(int(kafka_thread_nums)):
            kafka_future = executor.submit(send_message, p, queue, logger, topic)
            kafka_tasks.append(kafka_future)

    for task in as_completed(kafka_tasks):
        data = task.result()
        print(f"main: {data}")
    wait(kafka_tasks, return_when=ALL_COMPLETED)
    executor.shutdown()


