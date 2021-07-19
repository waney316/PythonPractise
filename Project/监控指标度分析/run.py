# -*- coding: utf-8 -*-
import requests
import json
from common.common_func import generate_headers

class ZabbixObject():
    def __init__(self, url, user, password):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = url
        self.token = self.get_token()

    # 获取zabbix登录token
    def get_token(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.password
            },
            "id": 1,
            "auth": None
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception:
            pass
        else:
            if not json.loads(res.text)["result"]:
                return None
            return json.loads(res.text)["result"]


    def get_all_host(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "selectItems": ["itemid", "name", "key_"]
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data)
        except Exception:
            pass
        else:
            # 格式化数据, 取出interfaces接口中第一个ip地址
            def pick_ip(item):
                if item.get("interfaces"):
                    item["ip"] = item.get("interfaces")[0].get("ip")
                    item.pop("interfaces")
                    return item
                return None

            host_list = json.loads(res.text).get("result")

            if host_list:
                format_data = list(map(pick_ip, host_list))
            return format_data



if __name__ == '__main__':
    zabbix = ZabbixObject("http://120.25.168.251:8989//zabbix/api_jsonrpc.php", "Admin", "aspire@1qaz2wsx")
    print(zabbix.get_all_host())