#!/usr/bin/python
# -*- coding: utf-8 -*-
# socket 客户端

import socket
import threading
# 创建socket, AF_INET: 网络协议，IPV4; SOCK_STREAM:TCP协议，SOCK_DGRAM：UDP协议
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 客户端连接server端，参数为元祖类型
server_address, server_port = "127.0.0.1", 8000
client.connect((server_address, server_port))



while True:

    # 客户端发送消息
    send_data = input()
    client.send(send_data.encode("utf8"))
    if send_data == "exit":
        break

    # 客户端接受消息
    data = client.recv(1024)
    print("server-{}: {}".format(server_address, data.decode("utf8")))


# 关闭客户端socket
client.close()