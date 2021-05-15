from botLib import *
from datetime import time, timedelta, datetime 
from messages import *

#sendMessage(user_id, message)

def scheduleHandler(SCHEDULE_CHECK):
    result = getAllUsersData()
    for user in result:
        for drug in result[user].keys():
            for timestamp in result[user][drug]:
                pilltime = datetime.strptime(timestamp, '%H:%M')
                localtime = datetime.now().time()
                if (pilltime.time() <= localtime and localtime <= (pilltime + timedelta(seconds=SCHEDULE_CHECK)).time()):
                    sendMessage(user, NOTIFICATION_MSG.format(drug))

result = getUpdates()