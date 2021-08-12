# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 12:14
# @Author  : waney
# @File    : run.py.py
import os
import sys
import pathlib
from common.logger import CustomLogger

# 判断当前python版本是否>3.5
assert sys.version_info > (3,5), "current python version < 3.5, exiting..."
# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

origin_dirs = ["config", "common", "logs", "utils"]
assert len(set(origin_dirs) & set(os.listdir(BASE_DIR))) < len(origin_dirs), f"工作路径不对或缺少工作目录{origin_dirs}"
assert pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")), "please sure config/config.yml is exist"

try:
    import requests
    import yaml
    import pymysql
except ImportError as e:
    raise ImportError(f"module import error{e}")

# 读取config.yml配置信息
with open(os.path.join(BASE_DIR, "config/config.yml"), encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 初始化日志模块
logger = CustomLogger(os.path.join(BASE_DIR, "logs", config.get("logfile")), "get_proxy_status")


class AlertMessage():

    def __init__(self, name, user, host, port, database, table):
        pass


