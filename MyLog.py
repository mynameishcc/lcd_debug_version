import time
import sys
from logging.handlers import RotatingFileHandler
import logging
import os
import inspect

# class CustomLogger(logging.Logger):
#     def findCaller(self, stack_info=False, stacklevel=1):
#         frame = inspect.currentframe()
#         # 跳过调用栈中的日志记录函数
#         while frame:
#             code = frame.f_code
#             print(frame.f_code)
#             print(logging._srcfile)
#             #if code.co_filename == logging._srcfile:
#             #frame = frame.f_back
#             continue
#             return (code.co_filename, frame.f_lineno, code.co_name, None)
#         return "(unknown file)", 0, "(unknown function)", None

# 设置日志记录器
#logging.setLoggerClass(CustomLogger)
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
file_handler = RotatingFileHandler(os.path.join(log_directory, 'app.log'), maxBytes=1024*1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s %(levelname)s [%(funcName)s]: %(message)s')
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
            #logger.info(f"============The function name is {func.__name__}============")
            return func(*args, **kwargs)
        return wrapper

# 示例函数，使用 MyLog 打印函数名称
@MyLog.print_function_name
def example_function():
    logger.info("This is an example function.")

if __name__ == "__main__":
    example_function()
