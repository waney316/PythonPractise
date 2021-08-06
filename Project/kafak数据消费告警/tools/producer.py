# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 14:28
# @Author  : waney
# @File    : producer.py

from kafka import KafkaProducer
from kafka.errors import kafka_errors
import traceback
import json

# 生产者测试脚本

with open("example.json", "r", encoding="utf-8") as f:
    data = f.readlines()

producer = KafkaProducer(bootstrap_servers="10.12.70.42:9092")
topic = "gbase_data"

for item in data:
    send_future = producer.send(topic, value=json.dumps(item).encode())
    print((f"send data from kafka {item}"))
    try:
        send_future.get(timeout=10) # 监控是否发送成功
    except kafka_errors:  # 发送失败抛出kafka_errors
        traceback.format_exc()

