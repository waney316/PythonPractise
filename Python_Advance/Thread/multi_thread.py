# coding: utf-8

## 单线程和多线程比较
import time
import threading
import spider_thread


def single_thread(urls):
    print("single start")
    for url in urls:
        spider_thread.craw(url)
    print("single end")

def multi_thread(urls):
    print("muti-thread start")
    threads = []
    for url in urls:
        threads.append(
            threading.Thread(target=spider_thread.craw, args=(url, ))
        )

    for th in threads:
        th.start()

    for th in threads:
        th.join()

    print("muti-thread end")

if __name__ == '__main__':
    single_start = time.time()
    urls = spider_thread.urls
    single_thread(urls)
    print("single cost", time.time()- single_start)

    muti_start = time.time()
    multi_thread(urls)
    print("muti cost", time.time()- muti_start)


