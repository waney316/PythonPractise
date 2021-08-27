# -*- coding: utf-8 -*-
# @Time    : 2021/8/27 10:22
# @Author  : waney
# @File    : common_func.py

import random
from itertools import starmap

# 随机生成头部
def generate_headers():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    ]
    return {
        "Content-Type": "application/jsonrequest",
        "Connection": "Keep-alive",
        'User-Agent': random.choice(user_agent_list)
    }

# 处理host数据格式化等
def handle_host(proxies_data):
    def inner(host):
        # 剔除interfaces，置换ip
        if host.get("interfaces"):
            host["ip"] = host.get("interfaces")[0].get("ip")
            host["type"] = host.get("interfaces")[0].get("type")
            host.pop("interfaces")

        # 取出分组
        if host.get("groups"):
            groups = host.pop("groups")
            host["groups"] =[ item.get("name") for item in groups ]

        # 取出代理进行关联
        if proxies_data:
            proxy_map = {item.get("proxyid"): item.get("host") for item in proxies_data }
            # 从proxy_map取出proxy_host
            host["proxy"] = proxy_map.get(host.pop("proxy_hostid"))
        else:
            host["proxy"] = None if host.pop("proxy_hostid") == 0 else None
        return host

    return inner


def handle_metrics(host):
    # 处理监控项数据
    if all([host.get("itemid"), host.get("lastclock"), host.get("lastvalue")]):
        host.pop("itemid")
        host["status"] = "正常采集"  if int(host.pop("lastclock")) > 0 else "异常采集"

    return host


def handle_groups(data):
    pass

def handle_proxies(data):
    dataMap = {}
    dataList = []
    for item in data:
        print(item)
        if not item.get("proxy"):
            continue

        lower_proxy = item.get("proxy").lower()
        if lower_proxy not in dataMap:
            dataMap[lower_proxy] = [item]
        else:
            dataMap[lower_proxy].append(item)
        dataList.append(dataMap)




if __name__ == '__main__':
    pass



