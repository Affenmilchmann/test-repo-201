from botLib import *

#getUpdates(user_id, message)

format_example = {
    13425364 : ["Hello bot"],
    52342431 : ["Hello", "Hey"]
} 

def msgHandler():
    for i in format_example.keys():
        if i = 'add':
            sendMessage(i, 'Please send me the pill name')