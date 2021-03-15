from time import sleep, time
from msgHandler import *
from scheduleHandler import *

bot_active = True
MESSAGE_CHECK = 2
SCHEDULE_CHECK = 10
time_passed_since_schedule_check = 0

while bot_active:
    t = time()
    #####
    #Schedule processing block
    if time_passed_since_schedule_check >= SCHEDULE_CHECK:
        scheduleHandler()
        time_passed_since_schedule_check = 0
        print("Schedule")
    #Message processing block
    msgHandler()
    #####
    t = time() - t

    print("Msg")
    time_passed_since_schedule_check += MESSAGE_CHECK
    sleep(MESSAGE_CHECK - t)
