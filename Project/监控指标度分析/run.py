# -*- coding: utf-8 -*-
import requests
import json
from common.common_func import generate_headers
import sys

class ZabbixObject():
    def __init__(self, url, user, password):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = url
        self.token = self.get_token()

    # 获取zabbix登录token




    def get_item_value(self):
        print(self.get_all_host())
        data = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": ["lastvalue", "hostid", "lastclock"],
                },
                "auth": self.token,
                "id": 1
            }
        for item in self.get_all_host():
            for host in item.get("items"):

        # for item in items.get("items"):
        #     data["params"]["itemid"] = item["itemid"]
        #     try:
        #         res = requests.post(url=self.url, headers=generate_headers(), data=json.dumps(data))
        #     except Exception:
        #         pass
        #     else:
        #         print(res)




if __name__ == '__main__':
    zabbix = ZabbixObject("http://120.25.168.251:8989//zabbix/api_jsonrpc.php", "Admin", "aspire@1qaz2wsx")
    # zabbix = ZabbixObject("http://10.12.66.107/zabbix/api_jsonrpc.php", "wangwei", "aspire@1qaz2wsx")
    zabbix.get_item_value()