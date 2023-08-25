import requests
from typing import Dict
import time


# some gpt api that can be used
url1 = "https://fastgpt.run/api/openapi/v1/chat/completions"
url2 = "https://chat.wantongyun.cn/api/openapi/v1/chat/completions"


# check/use proxy
def check_proxy(proxy_address: str = None, is_use: bool = False,
                session: requests.Session = None):
    if is_use:
        if proxy_address is None:
            raise ValueError("Proxy address is not provided!")
        else:
            session.proxies = {
                "http": "https://" + proxy_address,
                "https": "http://" + proxy_address
            }


# send the text to fastgpt api
def give_to_gpt(url: str, apikey: str, app_id: str, chat_id: str, 
                is_stream: bool = False, is_detail: bool = False,
                prompt: str = "", content: str = "",
                model: str = "gpt-3.5-turbo", 
                proxy_address: str = None, is_use: bool = False):
    # make up user messages
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": content}
    ]
    # create headers for api access
    headers = {
        "Authorization": f"Bearer {apikey}-{app_id}",
        'content-type': 'application/json'
    }
    # make up data
    data = {
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2000,
        "user": "live-virtual-digital-person",
        "model": model,
        "stream": is_stream,
        "detail": is_detail,
        "chatID": chat_id
    }

    # open session
    session = requests.Session()
    session.verify = False

    # check proxy
    check_proxy(proxy_address, is_use, session)

    # set up time counter
    start_time = time.time()
    resutl = ""

    try:
        response = requests.post(url=url, headers=headers, json=data, verify=False)
        # check if the response is valid
        response.raise_for_status()
        # evaluate the response to a dictionary
        result = eval(response.text)
        # get the response content
        result_content = result["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as err:
        print(f"GPT API Error: {err}")
        result = "GPT出现错误，请稍后再试。"

    print(f"Time used: {time.time() - start_time}")
    return result


# test
def test(url, data):
    result = give_to_gpt(url, data["apikey"], data["appID"], data["chatID"], 
                         content=data["content"])
    print(result)


# @DeprecationWarning
# def send_to_gpt(text: str, apikey: str, appID: str, 
#                     chatID: str, is_stream: bool = False, is_detail: bool = False,
#                     messages: Dict[str, str] = None):
#     url = "https://fastgpt.run/api/openapi/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {apikey}-{appID}",
#         'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "chatID": chatID,
#         "is_stream": is_stream,
#         "is_detail": is_detail,
#         "messages": [messages],
#     }
#     response = requests.post(url=url, headers=headers, json=data)
#     return response


if __name__ == '__main__':
    data1 = {
        "apikey": "fastgpt-zdtpvsanm1qa5d0mkfwisuvd",
        "appID": "64dc85c6afb25886d191fd43",
        "chatID": "1",
        "content": "尼日利亚2017到2018年的GDP增长率是多少"
    }
    data2 = {
        "apikey": "fastgpt-70aq3o62rpe92tk7glkbw0r6",
        "appID": "64de266f44b9f7a967f84be9",
        "chatID": "1",
        "content": "你是谁？"
    }

    test(url2, data2)
