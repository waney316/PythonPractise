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


# 随机生成头部
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


# 处理zabbix返回hosts信息
def handle_host(host, exclude_metrics):
    """
    1：将host中获取到的interfaces第一个值置换为ip，剔除interfaces接口
    2：自动发现的key值取出[]前字符，置换原本key值
    3：计算key值是否有最新数据
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

    if host.get("items"):
        for item in host.get("items"):
            # 如果监控项类型位于excelude_metricd中,去除
            if item.get("type") in exclude_metrics:
                host.pop(item)

            # 如果监控项类型为普通
            if item.get("flags") == "0":
                # 如果有最新值且监控项状态为0
                if int(item.get("lastclock")) > 0 and item.get("state") == "0":
                    # 去除判断数据
                    item.pop("lastvalue")

                    # 更新状态
                    item.update({"status": "1"})

            key = item.get("key_")
            # 如果键值未在hashMap
            if key not in hashMap or key.startwith():
                hashMap.add(key)
    else:
        host["items"] = None
    return host





if __name__ == '__main__':
    pass