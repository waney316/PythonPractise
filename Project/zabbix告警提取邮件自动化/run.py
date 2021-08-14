# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 12:14
# @Author  : waney
# @File    : run.py.py
import os
import sys
import pathlib
import datetime

from common.logger import CustomLogger
from common.check import check_config
from common.mail import data2html
from decimal import Decimal

# 判断当前python版本是否>3.5
assert sys.version_info > (3, 5), "current python version < 3.5, exiting..."
# 脚本工作目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

origin_dirs = ["config", "common", "logs", "utils"]
assert len(set(origin_dirs) & set(os.listdir(BASE_DIR))) < len(origin_dirs), f"工作路径不对或缺少工作目录{origin_dirs}"
assert pathlib.Path(os.path.join(BASE_DIR, "config/config.yml")), "please sure config/config.yml is exist"

try:
    import requests
    import yaml
    import pymysql
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
except ImportError as e:
    raise ImportError(f"module import error{e}")

# 读取config.yml配置信息
with open(os.path.join(BASE_DIR, "config/config.yml"), encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 初始化日志模块
logger = CustomLogger(os.path.join(BASE_DIR, "logs", config.get("logfile")), "alert_report_mail")


class AlertMessage():

    def __init__(self, name, user, host, password, port, database):
        self.name = name  # db名称
        self.user = user  # db user
        self.host = host  # db host
        self.password = password
        self.port = port
        self.database = database
        self.sql = """SELECT 
            DATE_FORMAT(FROM_UNIXTIME(clock),'%Y-%m-%d') AS 日期 ,
            SUM(severity) AS 总数,
              SUM(CASE severity WHEN 5 THEN severity ELSE 0 END) AS '重大', 
              SUM(CASE severity WHEN 4 THEN severity ELSE 0 END) AS '高', 
              SUM(CASE severity WHEN 3 THEN severity ELSE 0 END) AS '中', 
              SUM(CASE severity WHEN 2 THEN severity ELSE 0 END) AS '低'
            FROM `events`  WHERE  DATE_SUB(CURDATE(), INTERVAL 7 DAY) < DATE_FORMAT(FROM_UNIXTIME(clock),'%Y-%m-%d') 
        GROUP BY DATE_FORMAT(FROM_UNIXTIME(clock),'%Y-%m-%d');
        """

    def exceute_sql(self):
        try:
            # 建立连接
            con = pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, passwd=self.password,
                                  db=self.database, charset="utf8")
            con.ping()
        except Exception as e:
            logger.error(f"mysql conection error {e}")
        else:
            cursor = con.cursor()
            try:
                cursor.execute(self.sql)
            except Exception as e:
                logger.error(f"{self.name} execute sql error {e}")
            res = cursor.fetchall()
            cursor.close()
            return res

    @classmethod
    def send_mail(cls, data, from_user, receiver, smtp_server):
        mail_template = data2html(data)

        # 邮件类型
        msg = MIMEText(mail_template, _subtype='html', _charset='utf-8')
        # 邮件标题
        start_date = datetime.datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        msg['Subject'] = f"告警统计{str(start_date)} - {str(end_date)}"

        # 发件人
        msg["From"] = from_user
        # 收件人
        msg["To"] = ",".join(receiver)

        try:
            server = smtplib.SMTP()
            server.connect(smtp_server)
            server.sendmail(from_user, receiver, msg.as_string())
            logger.info(f"send mail from {from_user} to {receiver} success ")
        except Exception as e:
            logger.error(f"send mail from {from_user} to {receiver} failed: {e}")
        finally:
            server.close()


if __name__ == '__main__':
    try:
        dbs = config.get("db")
        check_gen = map(check_config, dbs)

        # smtp
        smtp_server = config.get("smtp_server")
        smtp_from = config.get("smtp_from")
        receiver = config.get("receiver")

        # db配置校验
        if not all(check_gen):
            logger.error("db configation must have [name, database, user, host, password, port], check config.yml ")
            sys.exit(1)

    except Exception as e:
        logger.error("read configuration error")
        sys.exit(1)

    # 查询数据
    messages = []
    for db in dbs:
        alert_message = AlertMessage(db.get("name"), db.get("user"), db.get("host"),
                                     db.get("password"), db.get("port"), db.get("database"))
        # 执行sql
        data = alert_message.exceute_sql()
        # 校验数据格式化数据
        messages.append({
            "name": db.get("name"),
            "zabbix_server": db.get("host"),
            "data": data
        })

    # 邮件发送
    # messages = [{'name': 'idc_zabbix', 'zabbix_server': '10.12.66.106', 'data': (('2021-08-07', Decimal('19295'), Decimal('0'), Decimal('160'), Decimal('45'), Decimal('19086')), ('2021-08-08', Decimal('17178'), Decimal('0'), Decimal('104'), Decimal('24'), Decimal('17048')), ('2021-08-09', Decimal('17953'), Decimal('5'), Decimal('476'), Decimal('48'), Decimal('17420')), ('2021-08-10', Decimal('17756'), Decimal('10'), Decimal('304'), Decimal('66'), Decimal('17368')), ('2021-08-11', Decimal('17967'), Decimal('0'), Decimal('428'), Decimal('99'), Decimal('17436')), ('2021-08-12', Decimal('17751'), Decimal('0'), Decimal('1088'), Decimal('132'), Decimal('16522')), ('2021-08-13', Decimal('14358'), Decimal('5'), Decimal('648'), Decimal('63'), Decimal('13640')))}]
    # print(smtp_from, receiver, smtp_server)
    AlertMessage.send_mail(messages, smtp_from, receiver, smtp_server)
