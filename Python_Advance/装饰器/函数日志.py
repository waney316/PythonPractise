# -*- coding: utf-8 -*-

# 记录函数执行日志
import logging
import time
def record_log(func):
    def wrapper(*args, **kwargs):
        logging.info(f"enter func {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"execute done func {func.__name__}")
        return result
    return wrapper


# 记录函数慢调用
def log_slow_call(func=None, second=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            if (end_time - start_time) > second:
                logging.warning(f"slow func execute {func.__name__}")
            return result
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)


from functools import wraps, partial


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper



@log_slow_call(second=2)
def test():
    time.sleep(3)
    print("test func")
