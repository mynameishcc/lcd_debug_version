import time
import sys
from logging.handlers import RotatingFileHandler
import logging
import os

# 设置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# 确保日志目录存在
log_directory = './log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# 创建文件处理器
file_handler = RotatingFileHandler('./log/app.log', maxBytes=1024*1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class MyLog:
    @staticmethod
    def cout(debug_window, out):
        now = time.localtime()
        debug_window.append(time.strftime("[%Y-%m-%d %H:%M:%S] ", now) + str(out))
        logger.info(out)

    @staticmethod
    def print_function_name(func):
        def wrapper(*args, **kwargs):
            logger.info(f"============The function name is {func.__name__}============")
            #print(*args)
            #print(**kwargs)
            return func(*args, **kwargs)
        return wrapper