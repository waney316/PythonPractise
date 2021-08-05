# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 11:20
# @Author  : waney
# @File    : verify_data.py

import json


# 验证kafak取出数据是否包含指定key值,校验数据合法性
def verify_metrics(metrics):
    # 检查数据是否存在关键key
    data = json.loads(metrics)
    if isinstance(data, dict):
        # 检测数据是否包含关键key值
        if not all([data.get("ip"), data.get("metric"), data.get("time")]):
            return False
        return metrics


