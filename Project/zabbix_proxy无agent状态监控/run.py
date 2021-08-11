# -*- coding: utf-8 -*-
# @Time    : 2021/8/10 11:25
# @Author  : waney
# @File    : run.py

import os
import sys
import json
import pathlib
from urllib.parse import urljoin

from common.common_func import generate_headers, ldd
from common.logger import CustomLogger
from common.telnet import scan

# 判断当前python版本是否>3.5
assert sys.version_info > (3,5), "current python version < 3.5, exiting..."

# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

origin_dirs = ["config", "common", "logs", "utils"]
assert len(set(origin_dirs) & set(os.listdir(BASE_DIR))) < len(origin_dirs), f"工作路径不对或缺少工作目录{origin_dirs}"
assert pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")), "please sure config/config.yml is exist"
tools_name = pathlib.Path(os.path.join(BASE_DIR, "tools/zabbix_sender"))
assert tools_name, "tools/zabbix_sender not exist"
# assert os.access(tools_name, os.X_OK), "zabbix-sender not have execute privileges, please use chmod +x toosl/zabbix_sender"

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
logger = CustomLogger(os.path.join(BASE_DIR, "logs", config.get("logfile")), "get_proxy_status")


# 获取server下代理数据
class ZabbixApi():
    def __init__(self, url, user, password ):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = urljoin(f"http://{url}", "zabbix/api_jsonrpc.php")
        self.token = self._get_token()

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

    def get_proxy(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxy.get",
            "params": {
                "output": ["host", "lastaccess"]

            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception as e:
            logger.error(f"get proxy list error {e}")
        else:
            return res.text

    # 将获取到的代理状态数据send至zabbix_server端
    def send_message(self, server, port, host, key, data):
        # 初始化时判断pushwateway连通性
        is_open, msg = scan(server, port)
        if is_open:
            logger.info(f"{server} connnect ok")
        else:
            logger.error(f"{server} connect fail-{msg}, check the zabbix service is running")
            sys.exit(1)

        """
        zabix_sender
        -s host: hostname
        -p port: server port
        -z server: server host
        -k key: frontend key
        -o data: value
        """

        cmd = f"tools/zabbix_sender -s {host}  -p {port} -z {server} -k '{key}' -o \"{str(data)}\" -vv"
        try:
            res = subprocess.getoutput(cmd)
            logger.info(str(res))
        except Exception as e:
            logger.error(f"send {host} metrics {key} failed >>> {e}")



if __name__ == '__main__':
    try:
        server = config.get("zabbix")
        map_host = config.get("map_host")
        timeout = config.get("timeout")
        key = config.get("key")
    except Exception as e:
        logger.error("get server from config.yml error")
        sys.exit(1)

    if all([server.get("host"), server.get("user"), server.get("password")]):
        zabbix = ZabbixApi(server.get("host"), server.get("user"), server.get("password"))
        # 获取代理数据
        proxy_data = zabbix.get_proxy()
        # 格式化代理数据为ldd格式
        format_data = ldd(proxy_data, timeout, logger)
        print(json.dumps(format_data))
        # 发送数据至zabbix
        zabbix.send_message(server.get("host"), server.get("port"), map_host, key, format_data)
    else:
        logger.error("zabbix config error")
        sys.exit(1)
