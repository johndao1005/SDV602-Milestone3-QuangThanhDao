from config.db import connectDB
from datetime import datetime, date

db = connectDB()
today = date.today().strftime("%d/%m/%Y")
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class ChatSession():
    def __init__(self,username,usersList,chatList):
        self.user = username
        self.usersList = usersList
        self.chatList = chatList
        self.database = db['chat']
        pass    
    
    def updateSession(self):
        while True:
            pass
        
    
    def sendMessage(self):
        
        pass

def addUser(username):
    pass

def getChat(username,userList,chatList):
    # ANCHOR add user into the user list first
    addUser = {'$push':{'user-list': username},'$set':{'last-update':now}}
    currentChat = db['chat']
    currentChat.find_one_and_update({'date':today},addUser,upsert=True)
    
    # ANCHOR creating loop to update chat
    # while True:
    todayChat = currentChat.find_one({'date':today})
    print(todayChat)
    if todayChat['last-update'] == now:
            print(todayChat['user-list'])
            print(todayChat['chat-log'])
            print('update')
            currentChat.update_one({"last-update":now})
            pass