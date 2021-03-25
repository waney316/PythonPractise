'''
多线程的两种实现方式：
1：实例化threading.Thread
2:继承threading.Thread类
'''
import time
import threading

# 通过实例化threading.Tread
def download_file(url):
    print("get download file started...\n")
    time.sleep(2)
    print("get download file end...\n")


def parse_data(file):
    print("parse data started...\n")
    time.sleep(2)
    print("parse data end...\n")


# 通过继承threading.Thread
class DownloadFile(threading.Thread):
    # 初始化线程属性
    def __init__(self, name):
        super().__init__(name=name)

    # 重写父类run方法
    def run(self):
        print("get download file started...\n")
        time.sleep(2)
        print("get download file end...\n")


# 通过继承threading.Thread
class ParseData(threading.Thread):
    # 初始化线程属性
    def __init__(self, name):
        super().__init__(name=name)

    # 重写父类run方法
    def run(self):
        print("get download file started...\n")
        time.sleep(2)
        print("get download file end...\n")

if __name__ == '__main__':
    url = "www.baidu.com"

    # 实例化Thread
    # thread1 = threading.Thread(target=download_file, args=(url,))
    # thread2  =threading.Thread(target=parse_data, args=(url,))
    # start_time = time.time()
    #
    # # 设置thread1 thread2 为守护线程，即主线程退出后，子线程立刻结束
    # # thread1.setDaemon(True)
    # # thread2.setDaemon(True)
    #
    # thread1.start()
    # thread2.start()
    #
    # # 设置thread1 thread 为堵塞状态，待子线程执行完，在执行主线程
    # thread1.join()
    # thread2.join()
    #
    # print("\nlast time: {}".format(time.time() - start_time))


    # 继承Thread类
    thread1 = DownloadFile(name="downfile")
    thread2 = ParseData(name="parse_data")
    start_time = time.time()
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("cost time: {}".format(time.time() - start_time))