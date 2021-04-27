from botLib import *
import time 

#sendMessage(user_id, message)

def scheduleHandler():
    result = getAllUsersData()
    local_time = time.localtime()
    current_time = local_time.tm_hour, local_time.tm_min
    print(result)