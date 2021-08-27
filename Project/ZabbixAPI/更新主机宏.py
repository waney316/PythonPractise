import sys
import random
from urllib.parse import urljoin
import json


assert sys.version_info > (3, 5), "current python version < 3.5, exiting..."

try:
    import requests
except ImportError:
    print("模块导入错误，请确保模块 requests 模块已经安装")
    sys.exit(1)

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


class ZabbixObject():
    def __init__(self, url, user, password,):
        # 初始化zabbix登录信息
        self.user = user
        self.password = password
        self.url = urljoin(url, "zabbix/api_jsonrpc.php")
        self.token = self._get_token()


    # 获取zabbix登录token
    def _get_token(self):
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
            res = requests.post(url=self.url, headers=generate_headers(), data=data, timeout=2)
        except Exception as e:
            print(f"zabbix: {self.url}-请求超时或错误{e}, exiting....")
            sys.exit(1)
        else:
            if json.loads(res.text).get("error"):
                print(f"{ json.loads(res.text).get('error')}, exiting....")
                sys.exit(1)
            elif not res.json().get("result"):
                print(f"zabbix: {self.url}-get None token, exiting....")
                sys.exit(1)
            else:
                print(f"zabbix: {self.url}-success: get token-{res.json().get('result')}")
                return res.json().get("result")

    # 获取zabbix所有主机列表主机列表
    def get_host_id(self, host, *args, **kwargs):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",

            "params": {
                "filter": {"host": host},
                "output": ["hostid", "host"]
            },
            "auth": self.token,
            "id": 1
        })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data, stream=True)
        except Exception as e:
            print(f"zabbix: {self.url}-获取主机列表超时或错误{e}")
        else:
            hostid = json.loads(res.text).get("result")[0].get("hostid")
            return hostid

    def update_host_macros(self, hostid, key, v):
        data = json.dumps({
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": {
                    "hostid": hostid,
                    "macros": [
                        {
                            "macro": key,
                            "value": v
                        }
                    ]
                },
                "auth": self.token,
                "id": 1
            })
        try:
            res = requests.post(url=self.url, headers=generate_headers(), data=data, stream=True)
        except Exception as e:
            print(f"zabbix: {self.url}-获取主机列表超时或错误{e}")
        else:
            response_data = json.loads(res.text).get("result")
            # 返回主机列表
            return response_data


if __name__ == '__main__':
    # zabbix api 数据
    url = "http://10.12.70.41"
    user = "Admin"
    password = "aspire@1qaz2wsx"
    zbx = ZabbixObject(url, user, password)

    # 宏的k:v
    macros_key = "{$DISC}"
    macros_value = "test"

    # host列表
    hostlist = "ip.txt"

    with open(hostlist, "r", encoding="utf-8") as f:
        hosts = f.readlines()

    for host in hosts:
        hostid = zbx.get_host_id(host)
        res = zbx.update_host_macros(hostid, macros_key, host.strip())
        if res:
            print(f"{host} update macros {macros_key} to {host.strip()} success")
        else:
            print(f"{host} update macros {macros_key} to {host.strip()} failed")
