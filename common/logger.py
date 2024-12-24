import logging
import os
import time


# 記錄日誌
class Logger:
    def __init__(self, logger_name, log_path):
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.logname = os.path.join(
            log_path, "{}.log".format(logger_name + "_" + time.strftime("%Y%m%d%H%M"))
        )
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        self.formater = logging.Formatter(
            "[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s"
        )

        self.filelogger = logging.FileHandler(self.logname, mode="a", encoding="UTF-8")
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)
        self.filelogger.setLevel(logging.DEBUG)
        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        if logger_name in ("SystemLog"):
            self.logger.addHandler(self.console)


# 指定本地根目錄
BasePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log_directory = os.path.join(BasePath, "Log")
logger = Logger(logger_name="SystemLog", log_path=log_directory).logger
