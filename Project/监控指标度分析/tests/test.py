from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, ProcessPoolExecutor
import requests
import json
from common.common_func import generate_headers, handle_host
import time

    # 根据host返回主机items
def get_host_item(url, hostid, *args, **kwargs):
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "hostids": str(hostid.strip()),
            "output": ["hostid", "host"],
            "selectInterfaces": ["ip"],
            "selectItems": ["itemid", "name", "key_", "lastclock", "state", "flags", "type"]
        },
        "auth": "4cae14acbb54fa5d168b4128cf2741ec",
        "id": 1
    })
    try:
        res = requests.post(url=url, headers=generate_headers(), data=data)
    except Exception as e:
        print(f">>>>> host: {hostid.strip()}-获取主机监控项数据超时或错误{e}")
    else:
        host_metrics = json.loads(res.text).get("result")[0]
        # host_list列表不为空, 即存在主机接入
        print(f">>>>> host: {hostid.strip()}-获取主机监控项数据超成功")

if __name__ == '__main__':
    url = "http://10.12.66.107/zabbix/api_jsonrpc.php"
    with open("hostid.txt", encoding="utf-8") as f:
        hostlist = f.readlines()

    tasks = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=50) as p:
        for hostid in hostlist:
            future = p.submit(get_host_item, url, hostid)
            tasks.append(future)

    wait(tasks, return_when=ALL_COMPLETED)
    print(f"cost time: {time.time()- start_time} s")