from requests import request as sendreq
from json import loads as loadjson

def makeRequest(method, data = {}, headers = {}, files = [], token = "1664734318:AAH4E4V0uSm4PC1-kDFKtISbJtlLB4t71MM"):
    '''
    Makes a POST request https://api.telegram.org/bot + \<token> + / + \<method> \n
    Returns a dict.\n
    '''

    url = "https://api.telegram.org/bot" + token + "/" + method

    response = sendreq("POST", url, headers=headers, data=data, files=files)
    resp_dict = loadjson(response.text.encode('utf8'))

    return resp_dict
