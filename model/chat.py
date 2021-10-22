from config.db import connectDB
from datetime import datetime, date

db = connectDB()
today = date.today().strftime("%d/%m/%Y")
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
newline = "\n"
class ChatSession():
    def __init__(self,username,usersList,chatList):
        self.user = username
        self.usersList = usersList
        self.chatList = chatList
        self.database = db['chat']
        self.get_current_session()
        self.session = self.database.find_one({'date':today},)
    
    def get_current_session (self):
        if self.database.count_documents({'date':today}) == 0:
            self.database.insert_one({
                'date':today,
                'user-list':[self.user],
                'chat-list':[],
                'last-modified':now
            })
        else:
            self.database.update_one(
                {'date':today},
                {'$push':{'user-list': self.user}
                ,'$set':{'last-modified':now}},
                upsert=True)
    
    def update_session(self):
        #while True:
            self.usersList.set(newline.join([user for user in self.session['user-list'] if isinstance(user,str)]))
            self.chatList.set(newline.join([user for user in self.session['chat-list']]))
    
    def send_message(self):
        
        pass

# def addUser(username):
#     pass

# def getChat(username,userList,chatList):
#     # ANCHOR add user into the user list first
#     addUser = {'$push':{'user-list': username},'$set':{'last-update':now}}
#     currentChat = db['chat']
#     currentChat.find_one_and_update({'date':today},addUser,upsert=True)
    
#     # ANCHOR creating loop to update chat
#     # while True:
#     todayChat = currentChat.find_one({'date':today})
#     print(todayChat == None)
#     if todayChat['last-update'] == now:
#             print(todayChat['user-list'])
#             print(todayChat['chat-log'])
#             print('update')
#             currentChat.update_one({"last-update":now})
#             pass
        