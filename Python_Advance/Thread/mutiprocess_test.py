# coding: utf-8
# 多进程编程
from multiprocessing import Process, Queue, Manager, Pool, Pipe
import time

def producer(queue):
    # queue
    # queue.put("a")

    #pipe
    queue.send("hello")
    time.sleep(2)

def consumer(queue):
    time.sleep(2)
    # queue
    # data = queue.get()

    #pipe
    print(queue.recv())


if __name__ == '__main__':

    # 实例化进程，Queue用于实例化进程，不能用于进程池
    # queue = Queue(10)
    # producer_process = Process(target=producer, args=(queue, ))
    # consumer_process = Process(target=consumer, args=(queue, ))
    #
    # producer_process.start()
    # consumer_process.start()
    #
    # producer_process.join()
    # consumer_process.join()

    ## 进程池
    # pool = Pool(2)
    # queue = Manager().Queue(10)
    # pool.apply_async(producer, args=(queue, ))
    # pool.apply_async(consumer, args=(queue, ))
    #
    # # 关闭进程池
    # pool.close()
    # pool.join()

    ## 利用pipe实现进程间通信, pipe只适用于两个进程的场景
    send_pipe, recive_pipe = Pipe()
    my_producer = Process(target=producer, args=(send_pipe, ))
    my_consumer = Process(target=consumer, args=(recive_pipe, ))

    my_producer.start()
    my_consumer.start()

    my_producer.join()
    my_consumer.join()


