from botLib import *
from datetime import time, timedelta

#sendMessage(user_id, message)

def scheduleHandler(SCHEDULE_CHECK):
    result = getAllUsersData()
    for user in result:
        for drug in result[user].keys():
            for timestamp in result[user][drug]:
                if time.strptime(timestamp) <= time.localtime() <= (time.localtime() + timedelta(seconds=SCHEDULE_CHECK)):
                    sendMessage(user, 'Please take the pill ' + drug)