# -*- coding: utf-8 -*-
# @Time    : 2021/8/5 16:24
# @Author  : waney
# @File    : telnet.py

import telnetlib
import socket


def scan(ip, port):
    server = telnetlib.Telnet()
    try:
        server.open(ip, port, timeout=3)
        return True, "open"
    except ConnectionRefusedError:
        return False, "Connection Refused"
    except socket.timeout:
        return False, "Connection Timeout"
    except OSError:
        return False, "No route to host"
    finally:
        server.close()


if __name__ == "__main__":
    pass
