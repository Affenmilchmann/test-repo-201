from requests import request as sendreq
from json import loads, load, dump
from os import remove as removeFile, walk, mkdir
from datetime import date, datetime 
from os import path
import sys

##init
token = ""
scr_path = sys.path[0]

USER_DATA_PATH = path.join(scr_path, "user_data/")
LOGS_PATH = path.join(scr_path, "logs/")

token_file_name = path.join(scr_path, "token.txt")
lst_id_file_name = path.join(scr_path, "last_update_id.txt")

msg_log = path.join(scr_path, LOGS_PATH, "bots_messages.txt")
err_log = path.join(scr_path, LOGS_PATH, "error_log.txt")
stats_log = path.join(scr_path, LOGS_PATH, "stats_log.txt")


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
    print(logTimeStamp(), msg, flush=True)

def logCheck():
    def dirCheck(dir_name):
        if path.exists(dir_name):
            consoleLog(dir_name + " is present.")
        else:
            mkdir(dir_name)
            consoleLog(dir_name + " was missing so it was created")
    def fileCheck(file_name, creation_stamp = True, default = False):
        try:
            with open(file_name, "r") as f:
                pass
        except:
            with open(file_name, "w") as f:
                if creation_stamp:
                    f.write(logTimeStamp() + "File created.\n")
                if default != False:
                    f.write(str(default))
                consoleLog(file_name + " was missing so it was created.")

    dirCheck(LOGS_PATH)
    dirCheck(USER_DATA_PATH)
    fileCheck(msg_log)
    fileCheck(err_log)
    fileCheck(stats_log, creation_stamp=False, default={})
    fileCheck(lst_id_file_name, False)

    ########################
    #stats file format check
    stats_file_data = {}
    with open(stats_log, 'r') as f:
        stats_file_data = load(f)
    
    def checkKey(key, default):
        if not key in stats_file_data:
            stats_file_data[key] = default
            consoleLog(str(key) + " stats key was missing so it was added with default " + str(default))
    
    checkKey('uniq_users_amount', 0)
    checkKey('active_users_amount', 0)
    checkKey('max_active_users_amount', 0)
    checkKey('uniq_users_id', [])
    with open(stats_log, 'w') as f:
        dump(stats_file_data, f)
        consoleLog("Stats file was updated.")




def writeLog(msg, file_name):
    try:
        with open(file_name, "a") as f:
            f.write(logTimeStamp() + str(msg) + "\n")
        return True
    except:
        return False

def writeMsgLog(msg, from_, to):
    writeLog("Message from: " + str(from_) + " to: " + str(to) + "\n" + msg, msg_log)

def writeStatsLog(current_ids_list):
    stats_file_data = {}
    with open(stats_log, 'r') as f:
        stats_file_data = load(f)
    
    active_users_amount = len(current_ids_list)
    uniq_users_id = set(stats_file_data['uniq_users_id']).union(set(current_ids_list))    
    uniq_users_id = list(uniq_users_id)
    uniq_users_amount = len(uniq_users_id)

    if stats_file_data['max_active_users_amount'] < active_users_amount:
        stats_file_data['max_active_users_amount'] = active_users_amount
    stats_file_data['active_users_amount'] = active_users_amount
    stats_file_data['uniq_users_id'] = uniq_users_id
    stats_file_data['uniq_users_amount'] = uniq_users_amount

    with open(stats_log, 'w') as f:
        dump(stats_file_data, f)

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
        consoleLog(str(user_id) + "'s file was deleted.")
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
            u_data = load(f)
            if len(u_data) == 0:
                consoleLog(str(user_id) + "'s file is empty")
                delUserFile(user_id)
            else:
                user_data[user_id] = u_data

    writeStatsLog(user_data.keys())
    return user_data
            