from config.db import connectDB
from datetime import datetime, date

db = connectDB()
today = date.today()
now = datetime.now()
def updateChat(username,userList,chatList):
    # ANCHOR add user into the user list first
    currentChat = db['chat'][today]
    currentChat['users'].insert(username)
    # ANCHOR creating loop to update chat
    while True:
        if currentChat['time'] != now:
            userList = currentChat['users']
            chatList = currentChat['chat-log']
            pass