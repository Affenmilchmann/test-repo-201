from requests import request as sendreq
from json import loads as loadjson

token = ""
with open("token.txt", "r") as f:
    token = f.read()

def makeRequest(method, data = {}, headers = {}, files = [], token_ = token):
    '''
    Makes a POST request https://api.telegram.org/bot + \<token> + / + \<method> \n
    Returns a dict.\n
    '''

    url = "https://api.telegram.org/bot" + token_ + "/" + method

    #sending a request
    response = sendreq("POST", url, headers=headers, data=data, files=files)
    #getting response
    resp_dict = loadjson(response.text.encode('utf8'))

    return resp_dict
