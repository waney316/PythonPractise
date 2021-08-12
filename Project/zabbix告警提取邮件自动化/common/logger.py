# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 11:22
# @Author  : waney
# @File    : logger.py

import logging.handlers
import sys

#初始化日志配置
class CustomLogger():
    def __init__(self, filepath, name):
        self.filepath = filepath
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 设置为日志轮询handler到指定文件
        log_handler = logging.handlers.TimedRotatingFileHandler(
            filename=filepath,
            when="D",
            interval=1,
            backupCount=7)

        log_handler.setFormatter(log_format)
        self.logger.addHandler(log_handler)

        # 输出日志到控制台
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_format)
        self.logger.addHandler(stream_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
