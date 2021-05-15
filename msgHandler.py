from botLib import *
from messages import *
from re import match

#getUpdates(user_id, message)

user_cache = {}

def msgHandler():
    messages = getUpdates()
    for uid in messages.keys():
              #greeting if its the first user's time
        if getUserData(uid) == False:
            setUserData(uid, {})
        for msg in messages[uid]:
            msg_l = msg.lower()
      
            #creating cache for the user
            if not uid in user_cache:
                user_cache[uid] = {}
            #######################
            #message handle section
            #######################
            if msg_l == 'stop' or msg_l == 's' or msg_l == 'q' or msg_l == '/stop' or msg_l == '/s' or msg_l == '/q':
                if uid in user_cache:
                    del user_cache[uid]
                    sendMessage(uid, ABORTED)
            elif msg_l == 'help' or msg_l == '/help':
                sendMessage(uid, HELP_MSG)
            elif msg_l == 'show' or msg_l == '/show':
                formShowMessage(uid)
                # if no other command is running           or   current command is running
            elif ((msg_l == 'add' or msg_l == '/add') and len(user_cache[uid]) == 0) or ("add" in user_cache[uid]):
                addHandler(msg, uid)
            elif ((msg_l == 'del' or msg_l == '/del') and len(user_cache[uid]) == 0) or ("del" in user_cache[uid]):
                delHandler(msg, uid)
            elif ((msg_l == 'edit' or msg_l == '/edit') and len(user_cache[uid]) == 0) or ("edit" in user_cache[uid]):
                editHandler(msg, uid)
            elif msg_l == '/start':
                sendMessage(uid, GREETING_MSG)
            else:
                sendMessage(uid, UNKNOWN_COMMAND)

def nextStage(uid, command):
    user_cache[uid][command]["stage"] += 1

def checkTimeFormat(time):
    if type(time) is str and len(time) == 5 and time[2] == ":":
        try:
            arr = time.split(":")
            if len(arr) != 2:
                return False
            
            hours = int(arr[0])
            mins = int(arr[1])

            if hours > 23 or mins > 59:
                return False
            
            return True
        except:
            return False
    else:
        return False

def formShowMessage(uid):
    data = getUserData(uid)
    message = "Here is your schedule:\n"
    for drug in data.keys():
        message += "*" + drug + "*\n"
        for t in data[drug]:
            message += t + "\n"

    sendMessage(uid, message)

def trySetDrugArray(uid, command, msg):
    try:
        temp_array = msg.split("\n")
        is_arr_ok = True
        for t in temp_array:
            if not checkTimeFormat(t):
                is_arr_ok = False
                break

        drug_name = user_cache[uid][command]["name"]

        if is_arr_ok:
            addDrug(uid, drug_name, temp_array)
            sendMessage(uid, DRUG_ADDED_MSG.format(drug_name))
            del user_cache[uid]
        else:
            sendMessage(uid, ARR_FORMAT_ERR)

    except:
        sendMessage(uid, ARR_FORMAT_ERR)

def addHandler(msg, uid):
    if not uid in user_cache:
        user_cache[uid] = {}
    if not "add" in user_cache[uid]:
        user_cache[uid]["add"] = {
            "stage": 0,
            "name": False
        }
    
    stage = user_cache[uid]["add"]["stage"]

    if stage == 0:
        sendMessage(uid, ADD_ST_ZERO)
        nextStage(uid, "add")
    elif stage == 1:
        user_cache[uid]["add"]["name"] = msg
        nextStage(uid, "add")
        sendMessage(uid, ADD_ST_ONE)
    elif stage == 2:
        trySetDrugArray(uid, "add", msg)

def delHandler(msg, uid):
    if not uid in user_cache:
        user_cache[uid] = {}
    if not "del" in user_cache[uid]:
        user_cache[uid]["del"] = {
            "stage": 0
        }

    stage = user_cache[uid]["del"]["stage"]

    if stage == 0:
        sendMessage(uid, DELL_ST_ZERO)
        nextStage(uid, "del")
    elif stage == 1:
        if delDrug(uid, msg):
            sendMessage(uid, DRUG_DELETED_MSG.format(msg))
            del user_cache[uid]
        else:
            sendMessage(uid, DRUG_DEL_FAILED.format(msg))

def editHandler(msg, uid):
    if not uid in user_cache:
        user_cache[uid] = {}
    if not "edit" in user_cache[uid]:
        user_cache[uid]["edit"] = {
            "stage": 0,
            "name": False
        }

    stage = user_cache[uid]["edit"]["stage"]

    if stage == 0:
        sendMessage(uid, EDIT_ST_ZERO)
        nextStage(uid, "edit")
    elif stage == 1:
        if checkDrug(uid, msg):
            sendMessage(uid, EDIT_ST_ONE.format(msg))
            user_cache[uid]["edit"]["name"] = msg
            nextStage(uid, "edit")
        else:
            sendMessage(uid, DRUG_NOT_FOUND.format(msg))
    elif stage == 2:
        trySetDrugArray(uid, "edit", msg)