import socket,json,struct
from threading import Thread

c = socket.socket()
c.connect(("127.0.0.1",8848))
print("连接服务器成功!")
def recver():
    while True:
        lens_bytes = c.recv(8)
        lens = struct.unpack("q", lens_bytes)[0]
        recv_msg = c.recv(lens).decode("utf-8")
        print(recv_msg)

# 开启线程处理接收数据
Thread(target=recver).start()



while True:
    msg = input(">>>>:").strip() # 阻塞
    if "@" in msg:
        info = {"msg":msg.split("@")[0],"to_addr":msg.split("@")[1]}
    else:
        info = {"msg": msg}

    data = json.dumps(info).encode("utf-8")
    c.send(struct.pack("q",len(data)))
    c.send(data)

