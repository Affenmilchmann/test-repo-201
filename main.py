import time
from msgHandler import *
from scheduleHandler import *

bot_active = True
MESSAGE_CHECK = 4
SCHEDULE_CHECK = 8
time_passed_since_schedule_check = 0

print("[INFO] Bot is acive. Settings are:")
print("         message check interval -", MESSAGE_CHECK, "sec")
print("         shedule check interval -", SCHEDULE_CHECK, "sec\n")

while bot_active:
    t = time.time()
    #####
    #Schedule processing block
    if time_passed_since_schedule_check >= SCHEDULE_CHECK:
        scheduleHandler()
        time_passed_since_schedule_check = 0
        print("Schedule check")
    #Message processing block
    msgHandler()
    print("Message check")
    #####
    time_passed_since_schedule_check += MESSAGE_CHECK

    t = time.time() - t

    print("Tick took", round(t, 2), "sec")
    time.sleep(max(MESSAGE_CHECK - t, 0))
