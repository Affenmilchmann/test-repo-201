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

def getLastID():
    with open("last_update_id.txt", "r") as f:
        id_ = f.readline()
        if id_ == "":
            id_ = 0
        return id_

def setLastID(id_):
    with open("last_update_id.txt", "w") as f:
        f.write(str(id_ + 1))

def getUpdates(relevant_ones = True):
    '''
    Returns dict with user messages.\n
    Format:\n
     { user1_id : [array_of_messages],\n
    user2_id : ['Hello', 'Bye'] }
    '''
    #####################
    if relevant_ones:
        data = { "offset" : getLastID()}
    else:
        data= {}
    #####################
    
    d_result = makeRequest("getUpdates", data=data)["result"]
    if len(d_result) != 0:
        setLastID(d_result[-1]["update_id"])

    out_dict = {}

    for upd in d_result:
        if "message" in upd:
            message = upd["message"]

            user_id = message["from"]["id"]
            text = message["text"]

            if user_id in out_dict:
                out_dict[user_id].append(text)
            else:
                out_dict[user_id] = [text]

    return out_dict

def sendMessage(user_id, text):
    '''
    Sends message with 'text' to user with 'user_id'\n \n
    -Returns True on success\n
    -Returns dict with provided by telegram error code end description on fail
    '''
    data = {'chat_id' : user_id * 1000,
            'text' : text }

    result = makeRequest("sendMessage", data=data)

    if 'ok' in result and result['ok']:
        return True
    else:
        return result

print(sendMessage(421823263, "Wasup"))