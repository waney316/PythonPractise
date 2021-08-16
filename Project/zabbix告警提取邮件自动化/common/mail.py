# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 17:26
# @Author  : waney
# @File    : mail_format.py


from decimal import Decimal

# 格式化邮件内容为html格式

mail_template = """
<table border width="600px" height="200px" > 
    <tr>
        <th>告警日期</th>
        <th>告警总数</th>
        <th>重大</th> 
        <th>高</th> 
        <th>中</th> 
        <th>低</th> 
    </tr>

"""

def data2html(data):
    global mail_template
    if isinstance(data, list):
        for alert_data in data:
            single_data = alert_data.get("data")
            for item in single_data:
                print(item)
                line = f"""<tr><td > {item[0]} </td>
                            <td> {str(item[1])} </td>
                            <td> {str(item[2])} </td>
                            <td> {str(item[3])} </td>
                            <td> {str(item[4])} </td>
                            <td> {str(item[5])} </td></tr>"""
                mail_template = mail_template + line

            # 拼接table底部
            mail_template += "</table>"

    return mail_template

