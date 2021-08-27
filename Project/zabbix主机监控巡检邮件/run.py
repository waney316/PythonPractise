# -*- coding: utf-8 -*-
# @Time    : 2021/8/27 9:57
# @Author  : waney
# @File    : run.py.py

# -*- coding: utf-8 -*-
import json
import os
import time
import sys
import pathlib
import logging.handlers

from urllib.parse import urljoin
from common.common_func import generate_headers, handle_host, handle_metrics, handle_proxies, handle_groups
from common.send_mail import Mail


assert sys.version_info > (3,5), "current python version < 3.5, need python version > 3.5"

# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

# 初始判断当前目录和指定文件是否存在
curren_path = os.getcwd()
origin_dirs = ["config", "common", "logs"]
assert len(set(origin_dirs) & set(os.listdir(BASE_DIR))) == len(origin_dirs), f"工作路径不对或缺少工作目录{origin_dirs}"
assert pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")), "please sure config/config.yml is exist"

# 确认是否安装requests/queue, kafka模块
try:
    import requests
    import pandas
    import yaml
except ImportError:
    print("模块导入错误，请确保模块 requests/pandas/yaml 模块已经安装")
    sys.exit(1)

# 读取config.yml配置信息
with open(os.path.join(BASE_DIR, "config/config.yml"), encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 初始化日志配置
logger = logging.getLogger("monitor_hosts_inspect")
logger.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 设置为日志轮询handler到指定文件
log_handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(BASE_DIR, "logs", config.get("logfile")),
    maxBytes=100 * 1024 * 1024,
    backupCount=7)
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)

# 输出日志到控制台
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)


class ZabbixObject():
    def __init__(self, url, user, password):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = urljoin(url, "zabbix/api_jsonrpc.php")
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
                logger.error(f"{json.loads(res.text).get('error')}, exiting....")
                sys.exit(1)
            elif not res.json().get("result"):
                logger.error(f"zabbix: {self.url}-get None token, exiting....")
                sys.exit(1)
            else:
                logger.info(f"zabbix: {self.url}-success: get token-{res.json().get('result')}")
                return res.json().get("result")

    # 获取代理id和代理名信息
    def _get_proxy_data(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "proxy.get",
                "params": {
                    "output": ["host"],
                },
                "auth": self.token,
                "id": 1
            }
        )
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data, stream=True)
        except Exception as e:
            logger.error(f"zabbix: {self.url}-获取代理数据超时或错误{e}")
        else:
            return json.loads(res.text).get("result")

    def get_proxies(self):
        return self._get_proxy_data()

    # 获取zabbix所有主机列表主机列表
    def get_all_host(self, *args, **kwargs):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host", "proxy_hostid"],
                "selectGroups": ["groupid", "name"],
                "selectInterfaces": ["ip", "type"],
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
            # yield host_list
            return host_list

    # 根据host返回主机items
    def get_host_item(self, host, key_map):
        # 提取数据
        hostid = host.get("hostid")
        key = key_map.get(int(host.get("type")))

        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "hostids": hostid,
                "output": ["lastclock", "lastvalue"],
                "filter": {
                    "key_": key
                },
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception as e:
            logger.error(f"zabbix: {self.url}-host: {host}-获取主机监控项数据超时或错误{e}")
        else:
            results = json.loads(res.text).get("result")
            if results:
                host_metrics = json.loads(res.text).get("result")[0]
                host.update(**host_metrics)
                res = handle_metrics(host)
                logger.info(f"{sys._getframe().f_code.co_name} {res}")
                return res
            else:
                logger.error(f"{host.get('ip')} 未关联包含{key} 监控项模板")



if __name__ == '__main__':
    try:
        datasource = config.get("datasource").get("server")
        key_map = {k["type"]: k["key"] for k in config.get("inspect_map")}
        related_key = config.get("related_key")
    except Exception as e:
        logger.error("获取zabbix数据源错误,请检查语法")
        sys.exit(1)

    # 初始化mail
    mail = Mail()

    assert related_key in ["server", "proxy", "group"], f"{related_key} not in ['server', 'proxy', 'group']"
    if related_key in ["proxy", "group"]:
        assert len(datasource) == 1, f"{related_key} 仅支持一个数据源配置"

    # storage = []
    # for ds in datasource:
    #     zabbix = ZabbixObject(ds["url"], ds["user"], ds["password"])
    #     origin_hosts_data = zabbix.get_all_host()
    #     proxies_data = zabbix.get_proxies()
    #     # map函数处理每个host, 返回迭代器
    #     data = map(handle_host(proxies_data), origin_hosts_data)
    #     # 存放当前zabbix_server主机数据的容器
    #     ds_hosts = []
    #     for host in data:
    #         # 根据host接入类型判断是否有最新数据
    #         host_res = zabbix.get_host_item(host, key_map)
    #         ds_hosts.append(host_res)
    #
    #     storage.append({
    #         "datasource": ds["name"],
    #         "data": ds_hosts
    #     })

    if related_key == "server":
        mail.send_message()

    elif related_key == "proxy":
        with open("data/1.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        handle_proxies(data)





