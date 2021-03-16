initial_list = [
    {'port': '80', 'protocol': 'TCP', 'service': 'http', 'risk_level': '低危险', 'vuln_name': '可通过HTTP获取远端WWW服务信息'},
    {'port': '443', 'protocol': 'TCP', 'service': 'https', 'risk_level': '低危险', 'vuln_name': '可通过HTTP获取远端WWW服务信息'},
    {'port': '443', 'protocol': 'TCP', 'service': 'https', 'risk_level': '低危险', 'vuln_name': '检测到目标主机加密通信支持的SSL加密算法【原理扫描】'},
    {'port': '4430', 'protocol': 'TCP', 'service': 'https', 'risk_level': '低危险', 'vuln_name': '检测到目标主机加密通信支持的SSL加密算法【原理扫描】'}
]

s = set()
a = set([ i.get("vuln_name") for i in initial_list])
d = {}
d.values()