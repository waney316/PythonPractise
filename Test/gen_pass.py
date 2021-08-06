# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 10:01
# @Author  : waney
# @File    : gen_pass.py

import getpass
import bcrypt

password = getpass.getpass("password: ")
hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
print(hashed_password.decode())