# 通过socket实现http请求
import socket
from urllib.parse import urlparse

def get_url(url):
    url = urlparse(url)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 客户端连接server端，参数为元祖类型
    server_address, server_port = url.netloc, 8000
    client.connect((server_address, server_port))

get_url("www.baidu.com")