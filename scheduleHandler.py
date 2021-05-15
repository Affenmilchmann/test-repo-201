from botLib import *
from datetime import time, timedelta, datetime 

#sendMessage(user_id, message)

def scheduleHandler(SCHEDULE_CHECK):
    result = getAllUsersData()
    for user in result:
        for drug in result[user].keys():
            for timestamp in result[user][drug]:
                pilltime = datetime.strptime(timestamp, '%H:%M')
                localtime = datetime.now().time()
                if (pilltime.time() <= localtime and localtime <= (pilltime + timedelta(seconds=SCHEDULE_CHECK)).time()):
                    sendMessage(user, 'Please take\n' + "*" + drug + "*")

result = getUpdates()