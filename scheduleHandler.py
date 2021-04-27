from botLib import *
import time 

#sendMessage(user_id, message)

def scheduleHandler():
    result = getAllUsersData()
    local_time = time.localtime()
    current_time = str(local_time.tm_hour) + ':' + str(local_time.tm_min)
    