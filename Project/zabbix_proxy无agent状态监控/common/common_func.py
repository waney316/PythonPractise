# -*- coding: utf-8 -*-
# 通用函数

import random
import json
import time


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


intervals = (
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
    )


# 将秒转换为 xd xh xm xs格式
def parse_time(seconds, granularity=3):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ' '.join(result[:granularity])


# 格式化zabbix ldd可识别的数据格式
def ldd(data, timeout, logger):
    current_timestamp = int(time.time())
    if isinstance(data, str):
        dict_data = json.loads(data)
        # 获取result字段
        result = dict_data.get("result")
        if result:
            for item in result:
                lastaccess = int(item.pop("lastaccess"))
                # status: 0异常  1正常
                item["proxy_name"] = item["{#PROXY_NAME}"] = item.pop("host")
                item["proxy_status"] = 0 if abs(current_timestamp-lastaccess) > timeout else 1
                item["proxy_lastaccess"] = parse_time(abs(current_timestamp-lastaccess))
                logger.info(f"proxy data: {item}")
    return {
        "data": dict_data.get("result")
    }
