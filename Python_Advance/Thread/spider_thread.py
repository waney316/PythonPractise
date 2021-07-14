# coding: utf-8
import requests


url_index = "https://www.cnblogs.com/#p{}"
urls = [ url_index.format(page) for page in range(1,50)]
# print(urls)
def craw(url):
    r = requests.get(url)
    print(url, len(r.text))

# craw(urls[0])
