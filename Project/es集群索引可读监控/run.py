# -*- coding: utf-8 -*-
# @Time    : 2021/8/20 9:55
# @Author  : waney
# @File    : run.py


import os
import sys
import re
import json
import time
import pathlib
from urllib.parse import urljoin

from common.common_func import generate_headers
from common.logger import CustomLogger
from common.telnet import scan

# 判断当前python版本是否>3.5
assert sys.version_info > (3, 5), "current python version < 3.5, exiting..."

# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

origin_dirs = ["config", "common", "logs", "tools"]

assert len(set(origin_dirs) & set(os.listdir(BASE_DIR))) == len(origin_dirs), f"工作路径不对或缺少工作目录{origin_dirs}"
assert pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")), "please sure config/config.yml is exist"
tools_name = pathlib.Path(os.path.join(BASE_DIR, "tools/zabbix_sender"))
assert tools_name, "tools/zabbix_sender not exist"
assert os.access(tools_name,
                 os.X_OK), "zabbix-sender not have execute privileges, please use chmod +x toosl/zabbix_sender"

try:
    import requests
    import yaml
    import subprocess
except ImportError as e:
    raise ImportError(f"module import error{e}")

# 读取config.yml配置信息
with open(os.path.join(BASE_DIR, "config/config.yml"), encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 初始化日志模块
logger = CustomLogger(os.path.join(BASE_DIR, "logs", config.get("logfile")), "get_es_index_status")


# 获取server下代理数据
class ESIndexStatus():
    def __init__(self, es_addr):
        self.es_addr = urljoin(es_addr, "_all/_settings")

    # post请求数据
    def get_index_status(self):
        try:
            res = requests.get(url=self.es_addr, headers=generate_headers(), timeout=5)
        except Exception as e:
            logger.error(f"zabbix: {self.url}-请求超时或错误{e}, exiting....")
            sys.exit(1)
        return res.json() if res.status_code == res.ok else res.text

    @staticmethod
    def formatting(data, exclude_index):
        res = []
        dump_data = json.loads(data)
        if isinstance(dump_data, dict):
            for item in dump_data:
                if not re.match("^.monitoring|^.kibana", item) and item not in exclude_index:
                    res.append({
                        "{#INDEX_NAME}": item,
                        "{#INDEX_STATUS}": dump_data[item].get("settings").get("index").get("blocks", "")
                    })
        return res

    @staticmethod
    def send_message(server, port, host, data, discover_key, item_key):
        is_open, msg = scan(server, port)
        if is_open:
            logger.info(f"{server} connnect ok")
        else:
            logger.error(f"{server} connect fail-{msg}, check the es health status")
            sys.exit(1)
        """
        zabix_sender
        -s host: hostname
        -p port: server port
        -z server: server host
        -k key: frontend key
        -o data: value
        """

        # 向自动发现规则发送数据
        cmd = f"{os.path.join(BASE_DIR, 'tools/zabbix_sender')} -s {host}  -p {port} -z {server} -k '{discover_key}' -o '{json.dumps(data)}' -vv"
        try:
            res = subprocess.getoutput(cmd)
            logger.info(str(res))
        except Exception as e:
            logger.error(f"send {host} metrics of discovery key-{discover_key} failed >>> {e}")

        # 向键值发送数据
        time.sleep(3)
        for item in data:
            cmd = f"""{os.path.join(BASE_DIR, 'tools/zabbix_sender')} -s {host}  -p {port} -z {server} -k "{item_key}[{item['{#INDEX_NAME}']}]" -o "{json.dumps(item['{#INDEX_STATUS}'])}" -vv"""
            try:
                res = subprocess.getoutput(cmd)
                logger.info(f"send {host} metrics of item key - {item_key}")
                logger.info(str(res))
            except Exception as e:
                logger.error(f"send {host} metrics of item key-{item_key} failed >>> {e}")


if __name__ == '__main__':
    try:
        # es地址
        es_addr = config.get("es_addr")

        # 忽略索引
        exclude_index = config.get("exclude_index")

        # zabbix_sender 映射配置
        map_host = config.get("map_host")
        map_proxy = config.get("map_proxy")
        map_port = config.get("map_port")
        # 模板监控项映射
        map_discovery_key = config.get("map_discovery_key")
        map_item_key = config.get("map_item_key")

    except Exception as e:
        logger.error("get server from config.yml error")
        sys.exit(1)

    if all([es_addr, map_host, map_host, map_host]):
        es = ESIndexStatus(es_addr)
        index_data = es.get_index_status()
        format_data = es.formatting(index_data, exclude_index)

        # 发送数据至zabbix
        es.send_message(map_proxy, map_port, map_host, format_data, map_discovery_key, map_item_key)
    else:
        logger.error("zabbix config error")
        sys.exit(1)
