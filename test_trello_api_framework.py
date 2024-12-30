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
key = ""
token = ""

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
    def create_board(self, params):
        res = self.post("/boards/", params=params)
        return res

    # post方法創建自訂欄位在看板上
    def create_Custom_Field(self, params, payload):
        res = self.post("/customFields", params=params, json=payload)
        return res

    # 檢查看板id
    def get_trello_board(self, params):
        res = self.get("/members/me/boards", params=params)
        return res

    # 刪除看板
    def delete_board(self, params, board_id):
        res = self.delete(f"/boards/{board_id}", params=params)
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
            "key": key,
            "token": token
        }
        res = self.api.create_board(params)
        return res

    # 創建自訂欄位
    def create_trello_Custom_Field_on_board(self, board_id):
        params = {
            "key": key,
            "token": token
        }
        body = {
            "idModel": board_id,
            "modelType": "board",
            "name": "Priority",
            "type": "number",
            "pos": "top",
            "display_cardFront": True
        }
        res = self.api.create_Custom_Field(params, body)
        return res

    # 取得看板
    def get_trello_board(self):
        params = {
            "key": key,
            "token": token,
            "filter": "open"
        }
        res = self.api.get_trello_board(params)
        return res

    # 刪除看板
    def delete_trello_board(self, board_id):
        params = {
            "key": key,
            "token": token
        }
        res = self.api.delete_board(params, board_id)
        return res


# ----------------------------------------------------------------


# 放在service層裡,作為整和內容並給予ui使用
class ApiService:
    def __init__(self, domain):
        self.api_operation = APIOperation(domain)

    # 使用post創建看板
    def create_board(self):
        # 回傳json格式
        Board_ID = self.api_operation.create_trello_board().json().get("id")
        return Board_ID

    # 創建自訂欄位
    def create_trello_Custom_Field(self, Board_ID):
        # 回傳json格式
        Custom_Field_ID = self.api_operation.create_trello_Custom_Field_on_board(Board_ID).json().get("id")
        return Custom_Field_ID

    # 取得看板
    def get_trello_board(self):
        Board_ID = self.api_operation.get_trello_board().json()[0].get("id")
        return Board_ID

    # 刪除看板
    def delete_trello_board(self, Board_ID):
        response = self.api_operation.delete_trello_board(Board_ID)
        assert response.status_code == 200
        return response

    # 創建自訂欄位
    def create_trello_Custom_Field_on_board(self):
        board_id = self.create_board()
        self.create_trello_Custom_Field(board_id)
        return board_id


# ----------------------------------------------------------------
# confest 進行case操作前設定,引入url
@pytest.fixture(autouse=True)
def setUp_and_tearDown():
    trello_domain = trello_URL
    yield trello_domain
    api_service = ApiService(trello_domain)
    board_id = api_service.get_trello_board()
    api_service.delete_trello_board(board_id)


class TestTrelloAPI:
    @pytest.fixture(autouse=True)
    def init_fixtures(self, setUp_and_tearDown):
        self.api_service = ApiService(setUp_and_tearDown)

# 創建自訂欄位
    def test_create_custom_field(self):
        self.api_service.create_trello_Custom_Field_on_board()


