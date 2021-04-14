from botLib import *

#getUpdates(user_id, message)

format_example = {
    13425364 : ["Hello bot"],
    52342431 : ["Hello", "Hey"]
} 

def msgHandler():
    messages = getUpdates()
    for id in messages.keys():
        for msg in messages[id]:
            if msg == 'add':
                sendMessage(id, 'Please send me the pill name')
