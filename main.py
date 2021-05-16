import time as tm
import os
from msgHandler import *
from scheduleHandler import *

##Setting timezone
os.environ['TZ'] = 'Europe/Moscow'
tm.tzset()

bot_active = True
MESSAGE_CHECK = 15
SCHEDULE_CHECK = 60
time_passed_since_schedule_check = SCHEDULE_CHECK

print("[INFO] Bot is acive. Settings are:")
print("         message check interval -", MESSAGE_CHECK, "sec")
print("         shedule check interval -", SCHEDULE_CHECK, "sec\n")
print("         local time             -", logTimeStamp())

logCheck()
consoleLog("Logs checked.")

while bot_active:
    t = tm.time()
    #####
    #Schedule processing block
    if time_passed_since_schedule_check >= SCHEDULE_CHECK:
        scheduleHandler(SCHEDULE_CHECK)
        time_passed_since_schedule_check = 0
        #print("Schedule check")
    #Message processing block
    msgHandler()
    #print("Message check")
    #####
    time_passed_since_schedule_check += MESSAGE_CHECK

    t = tm.time() - t

    #print("Tick took", round(t, 2), "sec")
    tm.sleep(max(MESSAGE_CHECK - t, 0)) 
