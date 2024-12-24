import os

import allure
import pytest
import json

import requests
import json as complexjson
import curlify

# 引入logger
from common.logger import logger

from typing import Optional

# ----------------------------------------------------------------
# env.ini
trello_URL = "https://api.trello.com/1"
trello_Board_name = "My_test_board"

# ----------------------------------------------------------------


# rest_client api交互邏輯
def check_response_json(response):
    try:
        # 嘗試將響應內容解析為 JSON 格式
        response.json()
        # 如果成功，記錄 JSON 響應內容
        logger.info("api response json ==>> {}".format(json.dumps(response.json(), indent=4, ensure_ascii=False)))
    except requests.exceptions.JSONDecodeError:
        # 如果解析失敗，記錄錯誤信息
        logger.error('Json decode error, json text is==>> {}'.format(response.text))


# ----------------------------------------------------------------
# 自定義api方法
class RestClient:
    def __init__(self, api_root_url):
        self.api_root_url = api_root_url
        self.session = requests.session()

    def get(self, url, headers: Optional = {}, **kwargs):
        return self.request(url, "GET", headers, **kwargs)

    def post(self, url, data=None, json=None, headers: Optional = {}, **kwargs):
        return self.request(url, "POST", headers, data, json, **kwargs)

    def put(self, url, data=None, headers: Optional = {}, **kwargs):
        return self.request(url, "PUT", headers, data, **kwargs)

    def delete(self, url, headers: Optional = {}, **kwargs):
        return self.request(url, "DELETE", headers, **kwargs)

    def patch(self, url, data=None, headers: Optional = {}, **kwargs):
        return self.request(url, "PATCH", headers, data, **kwargs)

    def request(self, url, method, headers, data=None, json=None, **kwargs):
        time_out_sec = 35
        url = self.api_root_url + url
        headers = headers
        params = dict(**kwargs).get("params")
        cookies = dict(**kwargs).get("cookies")

        if method == "GET":
            res = self.session.get(url, headers=headers, timeout=time_out_sec, **kwargs)
        elif method == "POST":
            res = self.session.post(url=url, data=data, json=json, headers=headers, timeout=time_out_sec, **kwargs)
        elif method == "PUT":
            if json:
                data = complexjson.dumps(json)
            res = self.session.put(url, data, headers=headers, timeout=time_out_sec, **kwargs)
        elif method == "DELETE":
            res = self.session.delete(url, headers=headers, json=json, timeout=time_out_sec, **kwargs)
        elif method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            res = self.session.patch(url, data, headers=headers, timeout=time_out_sec, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")
        self.extract_curl_res(res)
        self.request_log(url, method, data, json, params, headers, cookies, res)
        check_response_json(res)
        return res

    # 紀錄logger
    @staticmethod
    def request_log(url, method, data=None, json=None, params=None, headers=None, cookies=None, res=None):
        status_code = res.status_code
        logger.info("api url ==>> {}".format(url))
        logger.info("api method==>> {}".format(method))
        logger.info("status code ==>> {}".format(status_code))
        logger.info("api request header ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        allure.attach(
            f'{method} {url} \nStatus Code: {status_code} ',
            'requests method/url/time/header'
        )
        if params:
            logger.info("api request params ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
            allure.attach(f'{complexjson.dumps(params, indent=4, ensure_ascii=False)}', 'requests params')
        if data:
            logger.info("api request data ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
            allure.attach(f'{complexjson.dumps(data, indent=4, ensure_ascii=False)}'.replace('\'', '\"'),
                          'requests data')
        if json:
            logger.info("api request json ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
            allure.attach(f'{complexjson.dumps(json, indent=4, ensure_ascii=False)}'.replace('\'', '\"'),
                          'requests json')
        if cookies:
            logger.info("api request cookies ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))
            allure.attach(f'{complexjson.dumps(cookies, indent=4, ensure_ascii=False)}', 'requests cookies')
        if res.text:
            try:
                allure.attach(
                    complexjson.dumps(res.json(), indent=4, ensure_ascii=False), f'{url} Response body')
            except requests.exceptions.JSONDecodeError:
                allure.attach(res.text, f'{url} Response body')

    # 紀錄錯誤logger
    @staticmethod
    def extract_curl_res(res):
        try:
            allure.attach(f'{curlify.to_curl(res.request)}', 'requests curl')
        except Exception as e:
            allure.attach('None', 'requests curl error')
            logger.error(f"Curlify error: {e}")

# ----------------------------------------------------------------


# 放在api_objects裡面作為打api的方法,以及url
class API(RestClient):
    def __init__(self, api_root_url):
        super().__init__(api_root_url)

    # post方法創建看板並且在api_root_url引入domain
    def create_board_post(self, params):
        res = self.post("/boards/", params=params)
        return res


# ----------------------------------------------------------------
# 放在operation裡面作為api request的內容
class APIOperation:
    def __init__(self, config_url):
        self.api = API(config_url)

    # 創建看板(輸入request)
    def create_trello_board(self):
        params = {
            "name": trello_Board_name,
            "key": trello_KEY,
            "token": trello_Token
        }
        res = self.api.create_board_post(params)
        return res

# ----------------------------------------------------------------


# 放在service層裡,作為整和內容並給予ui使用
class ApiService:
    def __init__(self, domain):
        self.api_operation = APIOperation(domain)

    # 使用post創建看板
    def create_board_use_post(self):
        # 驗證狀態為200
        response = self.api_operation.create_trello_board()
        assert response.status_code == 200
        # 回傳json格式
        response_json = response.json()
        return response_json

# ----------------------------------------------------------------


# case業務邏輯層
class TestTrelloAPI:
    def test_create_custom_field(self):
        # 引入URL
        trello_domain = trello_URL
        # 將URL放入service裡
        api_service = ApiService(trello_domain)
        # 執行case
        api_service.create_board_use_post()


