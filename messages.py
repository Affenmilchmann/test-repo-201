GREETING_MSG = "Hello! Im a PillBot! I can remind you to take you drugs. Type help to see my commands!"
ABORTED = "All current commands were aborted."

ADD_ST_ZERO = "Send me pill name please"
ADD_ST_ONE = "Please send me time stamps in one message. Each time stamp on the new line"
DRUG_ADDED_MSG = "*{}* was set!"

DELL_ST_ZERO = "Send me drug name please"
DRUG_DELETED_MSG = "*{}* was deleted!"
DRUG_DEL_FAILED = "Looks like there is no drug named *{}*"

EDIT_ST_ZERO = "Send me drug name please"
EDIT_ST_ONE = "Send me new schedule for *{}* please. Each time stamp on the new line"

NOT_A_NUMBER_ERR = "Looks like you have sent me not a number..."
ARR_FORMAT_ERR = "Something went wrong. Check your message format.\n Format example:\n10:30\n15:40\n20:00"
UNKNOWN_COMMAND = "Whoopsie... Looks like its unknown commant for me. Try 'help' command."
DRUG_NOT_FOUND = "It looks like you dont have *{}* in you schedule"

HELP_MSG = '''
Here are my commands:
 - *add* - to add a new drug to your schedule
 - *del* - to delete a drug from your schedule
 - *edit* - to edit the drug's schedule
 - *stop or s* - to stop current operation
 - *show* - shows you schedule
 - *help* - shows this message)

Pill a day keeps a doctor away!
'''