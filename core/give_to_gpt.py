import requests
from typing import Dict
import time


# some gpt api that can be used
# https://fastgpt.run/api/openapi/v1/chat/completions
# https://chat.wantongyun.cn/api/openapi/v1/chat/completions


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
                prompt: str = None, content: str = None,
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
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json'
    }
    # make up data
    data = {
        "chatID": chat_id,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2000,
        "user": "live-virtual-digital-person",
        "model": model,
    }

    # open session
    session = requests.Session()
    session.verify = False

    # check proxy
    check_proxy(proxy_address, is_use, session)

    # set up time counter
    start_time = time.time()

    try:
        response = requests.post(url=url, headers=headers, json=data)
        # check if the response is valid
        response.raise_for_status()
        return eval(response.text)["replies"][0]["content"]
    except requests.exceptions.HTTPError as err:
        print(f"GPT API Error: {err}")
        return "GPT出现错误，请稍后再试。"


# send the text to fastgpt api
@DeprecationWarning
def send_to_gpt(text: str, apikey: str, appID: str, 
                    chatID: str, is_stream: bool = False, is_detail: bool = False,
                    messages: Dict[str, str] = None):
    url = "https://fastgpt.run/api/openapi/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apikey}-{appID}",
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json'
    }
    data = {
        "chatID": chatID,
        "is_stream": is_stream,
        "is_detail": is_detail,
        "messages": [messages],
    }
    response = requests.post(url=url, headers=headers, json=data)
    return response


if __name__ == '__main__':
    apikey = "fastgpt-zdtpvsanm1qa5d0mkfwisuvd"
    appID = "64dc85c6afb25886d191fd43"
    chatID = "1"
    messages = {
        "content": "尼日利亚2017到2018年的GDP增长率是多少",
        "role": "user"
    }
    print(give_to_gpt("尼日利亚2017到2018年的GDP增长率是多少", apikey, appID, chatID, False, False, messages))

