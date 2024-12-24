import os
from configparser import ConfigParser


# env.ini檔案取方式
class ConfigPath:
    @staticmethod
    def get_config(basic_key, need_value):
        config = ConfigParser()
        # 取得根目錄
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # 取得根目錄中env檔案
        account_setting_path = os.path.join(base_path, "config", 'trello_env.ini')
        config.read(account_setting_path)
        need_content = config.get(basic_key, need_value)
        return need_content
