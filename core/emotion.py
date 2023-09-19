import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64


app_id="9d39e9ed"
api_key="0c8ac079b6dffec57125c48eb83dcfcf"
url ="http://ltpapi.xfyun.cn/v2/sa"


# send text to emotion analysis api
def analysis_emo(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': app_id,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result.decode('utf-8'))
    return


# get the emotion score
def get_emo(text):
    result = analysis_emo(text)
    # if the request is not success, return -1
    if result['desc'] != 'success':
        return -1
    return float(result['data']['score'])


# get sentiment
def get_sentiment(text):
    result = analysis_emo(text)
    if result['desc'] != 'success':
        return - 1
    return int(result['data']['sentiment']) + 1
