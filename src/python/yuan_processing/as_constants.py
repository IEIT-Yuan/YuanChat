import os
# from colorama import Fore

this_dir = os.path.dirname(__file__)

AS_HOME_DIR = os.path.abspath(os.path.join(this_dir, '../../../'))
AS_LOG_HOME = os.path.join(AS_HOME_DIR, 'logs')   # 日志记录位置
if not os.path.exists(AS_LOG_HOME):
    os.mkdir(AS_LOG_HOME)

DEFAULT_PORT = 5050
AS_CHECK_INFER_CODE = 100

YUAN_2_URL = [["http://127.0.0.1:8000/yuan"]]

if os.environ.get('YUAN_2_URL'):
    YUAN_2_URL = [[os.environ.get('YUAN_2_URL')]]