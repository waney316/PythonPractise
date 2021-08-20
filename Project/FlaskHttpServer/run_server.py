# -*- coding: utf-8 -*-
# @Time    : 2021/8/18 14:16
# @Author  : waney
# @File    : run_server.py.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.debug = True


@app.route('/alert/getservicesbyhost', methods=['get'])
def get_http():
    info_file = "cluster_info.json"
    with open(info_file, "r", encoding="utf-8") as f:
        load_dict = json.load(f)

    # 返回JSON数据
    return load_dict



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234)