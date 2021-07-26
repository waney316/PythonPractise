# -*- coding: utf-8 -*-
# 通用函数

import time
import random
from collections import Counter
import re

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

    # 计数自动发现数量
    countMap = Counter()

    if host.get("items"):
        for item in host.get("items"):
            # 如果监控项类型位于excelude_metricd中,去除
            if item.get("type") in exclude_metrics:
                host.pop(item)

            # 如果监控项类型为普通
            if item.get("flags") == "0":
                head_key = item.get("key")
                item["status"] = 0 if int(item.get("lastclock")) > 0 and item.get("state") == "0" else 1
                item.pop("lastvalue")

            # 如果为自动发现类型
            elif item.get("flags") == "4":
                head_key = re.match("^(.*)\[", item.get("key")).group(1)
                if head_key not in countMap:
                    item["status"] = 0 if int(item.get("lastclock")) > 0 and item.get("state") == "0" else 1

            countMap.update(head_key)
            item["count"] = countMap[head_key]

            # pop some items
    else:
        host["items"] = None

    return host





if __name__ == '__main__':
    pass