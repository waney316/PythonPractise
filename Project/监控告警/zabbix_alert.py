# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 16:43
# @Author  : waney
# @File    : 1.py


import smtplib
from email.mime.text import MIMEText

import sys
mail_user = 'xxx@aspirecn.com'   # 公司邮箱
mail_pass = 'xxxx'  # 应用鉴权码

def send_mail(to_list, subject, content):
    me = "深圳zabbix 监控" + "<" + mail_user + ">"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list

    try:
        s = smtplib.SMTP_SSL("smtp.mail.139.com", 465)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False

if __name__ == "__main__":
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])


    list()