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
    items = host.get("items")
    res = []
    if items:
        for (index, item) in enumerate(items):
            # 如果监控项类型位于excelude_metricd中,去除
            if int(item.get("type")) in exclude_metrics:
                continue

            """
            item["status"]: 0异常，1正常
            """
            # 如果监控项类型为普通
            if item.get("flags") == "0":
                head_key = item.get("key_")
                item["status"] = 1 if int(item.get("lastclock")) > 0 and item.get("state") == "0" else 0
                countMap.update({head_key})
            # 如果为自动发现类型
            elif item.get("flags") == "4":
                head_key = re.match("^(.*)\[", item.get("key_")).group(1)
                if head_key not in countMap:
                    item["status"] = 1 if int(item.get("lastclock")) > 0 and item.get("state") == "0" else 0
                    item["key_"] = head_key
                    countMap.update({head_key})
                else:
                    countMap.update({head_key})
                    continue
            # pop some label
            [ item.pop(remove_key) for remove_key in ("lastclock", "type", "flags" ) ]
            item["count"] = countMap[item["key_"]]
            res.append(item)
    # 更新count
    for item in res:
        item["count"] = countMap[item["key_"]]
    host.update({"items": res})
    return host


if __name__ == '__main__':
    pass