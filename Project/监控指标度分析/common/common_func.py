# -*- coding: utf-8 -*-
# 通用函数

import time
import random
from collections import Counter
import json
import requests

#时间装饰器
def time_deactor(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        last_time = time.time() - start_time
        print(f"cost time {last_time}")
    return wrapper


def generate_headers():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]
    return {
        "Content-Type": "application/json",
        'User-Agent': random.choice(user_agent_list)
    }


def handle_host(host):
    """
    1：将host中获取到的interfaces第一个值置换为ip，剔除interfaces接口
    2：将监控项key_去重，去除自动发现里较多的监控项
    :param item:
    :return:
    """
    # 剔除interfaces，置换ip
    if host.get("interfaces"):
        host["ip"] = host.get("interfaces")[0].get("ip")
        host.pop("interfaces")
    else:
        host["ip"] = None

    # 去重监控项, 自动发现的监控项规则为 xx.xx.xx[]，通过正则匹配[
    hashMap = {}
    exclude_str = ["snmptrap", "zabbix"]  # 不包含snmptrap类型的监控项

    if host.get("items"):
        for item in host.get("items"):
            key = item.get("key_")
            # 如果键值未在hashMap
            if key not in hashMap or key.startwith():
                hashMap.add(key)
    else:
        host["items"] = None
    return host


# 获取zabbix登录token
def get_token(url, user, password):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": user,
            "password": password
        },
        "id": 1,
        "auth": None
    })
    try:
        res = requests.post(url=url, headers=generate_headers(), data=data)
    except Exception:
        pass
    else:
        if not json.loads(res.text)["result"]:
            return None
        return json.loads(res.text)["result"]

# 获取主机列表
def get_all_host(self, url, token):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "selectItems": ["itemid", "name", "key_", "selectItemDiscovery"]
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception:
            pass
        else:
            # 格式化数据, 取出interfaces接口中第一个ip地址
            def pick_ip(item):
                if item.get("interfaces"):
                    item["ip"] = item.get("interfaces")[0].get("ip")
                    item.pop("interfaces")
                    return item
                return None

            host_list = json.loads(res.text).get("result")

            if host_list:
                format_data = list(map(pick_ip, host_list))
            # print(type(format_data))
            # print(sys.getsizeof(format_data))
        return (host for host in format_data)


