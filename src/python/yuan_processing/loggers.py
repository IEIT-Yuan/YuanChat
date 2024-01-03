# -*- coding: UTF-8 -*-

import logging
import os
import time
import colorlog
from as_constants import AS_LOG_HOME
# 设置logging模块的默认编码为UTF-8
# logging.basicConfig(encoding='utf-8')


def __logfun(isfile=True):
    # black, red, green, yellow, blue, purple, cyan(青) and white, bold(亮白色)
    log_colors_config = {
        'DEBUG': 'bold_white',
        'INFO': 'bold',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red', # 加bold后色彩变亮
    }
    logger = logging.getLogger()
    # 输出到console
    logger.setLevel(level=logging.INFO) # 某些python库文件中有一些DEBUG级的输出信息，如果这里设置为DEBUG，会导致console和log文件中写入海量信息
    console_formatter = colorlog.ColoredFormatter(
        # fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        fmt='%(log_color)s %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        # datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )
    console = logging.StreamHandler()  # 输出到console的handler
    console.setFormatter(console_formatter)
    logger.addHandler(console)

    # 输出到文件
    if isfile:
        # 设置文件名
        log_name = 'yuan_processing_' + time.strftime("%Y-%m-%d", time.localtime(time.time())) + ".log"
        logfile = os.path.join(AS_LOG_HOME, log_name)
        # 设置文件日志格式
        filer = logging.FileHandler(logfile, mode='a') # 输出到log文件的handler
        # filer.setLevel(level=logging.DEBUG)
        file_formatter = logging.Formatter(
            fmt='%(asctime)s - %(filename)s - %(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
        filer.setFormatter(file_formatter)
        logger.addHandler(filer)

    return logger


logger =__logfun()


if __name__=='__main__':
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')
