from requests import request as sendreq
from json import loads, load, dump
from os import remove as removeFile, walk
from datetime import date, datetime 
from os import path
import sys

##init
token = ""
scr_path = sys.path[0]

token_file_name = path.join(scr_path, "token.txt")
lst_id_file_name = path.join(scr_path, "last_update_id.txt")
msg_log = path.join(scr_path, "logs/bots_messages.txt")
err_log = path.join(scr_path, "logs/error_log.txt")


USER_DATA_PATH = path.join(scr_path, "user_data/")

########################
##### ASSIST FUNCS #####
########################

def getLastID():
    with open(lst_id_file_name, "r") as f:
        id_ = f.readline()
        if id_ == "":
            id_ = 0
        return id_

def setLastID(id_):
    with open(lst_id_file_name, "w") as f:
        f.write(str(id_ + 1))

def logTimeStamp():
    return "[" + str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]"

def consoleLog(msg, critical = False):
    if critical:
        msg = "ERROR " + str(msg).upper()
    print(logTimeStamp(), msg)

def logCheck():
    def check(file_name, creation_stamp = True):
        try:
            with open(file_name, "r") as f:
                pass
        except:
            with open(file_name, "w") as f:
                if creation_stamp:
                    f.write(logTimeStamp() + "File created.\n")
                else:
                    pass
                consoleLog(file_name + " was missing so it has been created.")

    check(msg_log)
    check(err_log)
    check(lst_id_file_name, False)

def writeLog(msg, file_name):
    try:
        with open(file_name, "a") as f:
            f.write(logTimeStamp() + str(msg) + "\n")
        return True
    except:
        return False

def writeMsgLog(msg, from_, to):
    writeLog("Message from: " + str(from_) + " to: " + str(to) + "\n" + msg, msg_log)

def writeErrLog(msg):
    writeLog(msg, err_log)

######################
##### TOKEN INIT #####
######################

try:
    with open(token_file_name, "r") as f:
        token = f.read()
    consoleLog("Token is present.")
except:
    consoleLog("token.txt is missing.", critical=True)
    consoleLog("Please create token.txt file in project's root and paste there you bot's token!")
    quit()

######################
##### MAIN FUNCS #####
######################

def makeRequest(method, data = {}, headers = {}, files = [], token_ = token):
    '''
    Makes a POST request https://api.telegram.org/bot + \<token> + / + \<method> \n
    Returns a dict.\n
    '''

    url = "https://api.telegram.org/bot" + token_.strip("\n") + "/" + method

    #sending a request
    response = sendreq("POST", url, headers=headers, data=data, files=files)
    #getting response
    resp_dict = loads(response.text.encode('utf8'))

    if 'ok' in resp_dict:
        if resp_dict['ok']:
            return resp_dict
        else:
            ret = {
                "request": url,
                "data": data,
                "headers": headers,
                "files": files,
                "response": resp_dict
            }
            writeErrLog(ret)
            return ret

    return resp_dict

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

    d_result = makeRequest("getUpdates", data=data)

    if not "result" in d_result:
        consoleLog("getUpdates() failed.\n" + str(d_result))
        return False

    d_result = d_result["result"]

    if len(d_result) != 0:
        setLastID(d_result[-1]["update_id"])

    out_dict = {}

    for upd in d_result:
        if "message" in upd:
            message = upd["message"]

            user_id = message["from"]["id"]
            text = message["text"]

            writeMsgLog(text, user_id, "BOT")

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
    data = {'chat_id' : user_id,
            'text' : text,
            'parse_mode': 'markdown' }

    result = makeRequest("sendMessage", data=data)

    if 'ok' in result and result['ok']:
        consoleLog("Bot message to " + str(user_id))
        writeMsgLog(text, "BOT", user_id)
        return True
    else:
        return result

def setUserData(user_id, data):
    '''
    Sets 'data' for user with 'user_id'.\n
    'data' is a dict with format:\n
    { 'drug_name' : [array with time strings] }\n
    Example: { 'fennibut' : ['10:30', '15:00', '21:30'], 'noshpa' : ['15:30'] }
    '''

    with open(USER_DATA_PATH + str(user_id) + ".json", "w") as f:
        dump(data, f)

def getUserData(user_id):
    '''
    Gets data by 'user_id'. To see format check 'setUserData()' description
    '''
    try:
        with open(USER_DATA_PATH + str(user_id) + ".json") as f:
            return load(f)

    except IOError:
        setUserData(user_id, {})
        return False
        
def checkDrug(user_id, drug_name):
    user_data = getUserData(user_id)
    if user_data == False:
        return False

    return drug_name in user_data

def addDrug(user_id, drug_name, timetable):
    user_data = getUserData(user_id)
    if user_data == False:
        return False

    user_data[drug_name] = timetable

    setUserData(user_id, user_data)

def editDrug(user_id, drug_name, new_timetable):
    user_data = getUserData(user_id)
    if user_data == False:
        return False

    if drug_name in user_data:
        user_data[drug_name] = new_timetable
        setUserData(user_id, user_data)
        return True
    else:
        return False

def delDrug(user_id, drug_name):
    '''
    Deletes one drug's timetable\n
    Returns 'False' if there is no file for user or\n
    there is no drug with 'drug_name' in file.
    '''
    user_data = getUserData(user_id)
    if not user_data:
        return False

    if drug_name in user_data:
        del user_data[drug_name]
    else:
        return False

    setUserData(user_id, user_data)
    return True

def delUserFile(user_id):
    '''
    Deletes all drugs for user with 'user_id'\n
    (Actually it just deletes the file)\n
    Returns 'False' if there is no file for user
    '''
    try:
        removeFile(USER_DATA_PATH + str(user_id) + ".json")
    except IOError:
        return False

def getAllUsersData():
    '''
    Returns dict with all user data.\n
    Format: { 'user1_id' : { 'drug1_name' : [array_with_time_strings] } }\n
    Example: just use it and see, there is folder with test users. I cant fit example here. Sorry
    '''
    user_data = {}

    files_list = []
    for (dirpath, dirnames, filenames) in walk(USER_DATA_PATH):
        files_list.extend(filenames)
        break
    
    for file_name in files_list:
        user_id = file_name
        if user_id.endswith(".json"):
                user_id = user_id[:-5]

        with open(USER_DATA_PATH + file_name, 'r') as f:
            user_data[user_id] = load(f)

    return user_data
            