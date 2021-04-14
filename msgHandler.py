from botLib import *

#getUpdates(user_id, message)

format_example = {
    13425364 : ["Hello bot"],
    52342431 : ["Hello", "Hey"]
} 

def msgHandler():
    messages = getUpdates()
    for i in messages.keys():
        if message[i] = 'add':
            sendMessage(i, 'Please send me the pill name')
