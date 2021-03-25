import socket
import json,struct
from concurrent.futures import ThreadPoolExecutor
debug = True

s = socket.socket()
s.bind(("127.0.0.1",8848))
s.listen()
clients = {}

pool = ThreadPoolExecutor(100)

def send_msg(soc, msg):
    l = len(msg.encode("utf-8"))
    soc.send(struct.pack("q",l))

    # 发数据
    soc.send(msg.encode("utf-8"))

'''用于监听已经建立连接的客户端发来的消息'''
def task(ip,c):
    while True:
        l = c.recv(8)
        ls = struct.unpack("q",l)[0]
        data = json.loads(c.recv(ls).decode("utf-8"))   #接收到来自客户端的消息。 eg:    data = {'to_addr':'msg':''}
        print('来自%s的消息：%s'%(ip,data['msg']))
        # 客户端发过来的数据
        # 数据有两种情况 一种是发给所有人的 另一种单独发给某一个人的
        if data.get('to_addr'): #传过来一个json格式的字典，如果这个to_addr不是空的话，就私发给目标客户
            target_ip = data["to_addr"]        #从data字典里中获取目标ip
            target_conn = clients.get(target_ip)   #获取目标客户的conn链接
            send_msg(target_conn,data['msg'])    #发送讯息
        else:
            for ip,conn in clients.items():
                # if c != target_conn:
                send_msg(conn,data['msg'])#data['msg']


        #     # 从所有客户端列表中找到这一个  发给它
        #     to_addr = data["to_addr"]
        #     # print(data["to_addr"],"_______________")
        #     soc = clients.get(to_addr)
        #     send_msg(soc,data["msg"])
        # else:
        #     # 遍历所有客户端 发给每一个人
        #     for k,soc in clients.items():
        #         # if soc != c:
        #             send_msg(soc,data["msg"])

while True:
    '''以下代码用于检测是否有客户端连接'''
    c,add = s.accept()
    print("%s" % add[0],"连接到服务器!")
    clients[add[0]] = c  # 把ip地址作为key，conn作为value存入clients字典中 ,clients = {'192.188.3.4':conn链接}
    if debug:
        print('clients=%s'%clients)

    '''以下代码用于监听已经建立连接的客户端发来的消息'''
    pool.submit(task,add,c)

