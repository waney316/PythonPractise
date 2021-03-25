#!/usr/bin/python
# -*- coding: utf-8 -*-
# socket server端

import socket
import datetime
import threading
# 创建socket, AF_INET: 网络协议，IPV4; SOCK_STREAM:TCP协议，SOCK_DGRAM：UDP协议
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口,参数为元祖类型
server.bind(("0.0.0.0", 8000))
# 监听
server.listen()
print("socker server started, receive data...")


# 多线程处理sock连接
def handle_sock(sock, addr):
    print("client: {} is connected".format(addr))
    # 接受客户端socket连接的数据, 1024字节，即1KB
    while True:
        data = sock.recv(1024)
        print("client-{}: {} \n".format(addr, data.decode("utf8")))
        # 回复消息
        re_data = input()
        sock.send(re_data.encode("utf8"))
        if re_data == "exit":
            break

while True:
    # 接收socket连接,返回数据为socket连接客户端和地址
    sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()



# # 关闭socket连接
# sock.close()
