# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 16:00
# @Author  : waney
# @File    : check_config.py


# 检查配置文件db是否正确
def check_config(configation):
    config_must = ["name", "database", "user", "password", "host"]
    for item in config_must:
        if item not in configation:
            return False
    return True