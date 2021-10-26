from db import connectDB
from datetime import datetime, date
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne


today = date.today().strftime("%d/%m/%Y")
now = datetime.now()
newline = "\n"


class Session():
    def __init__(self,username):
        self.check = False
        self.user = username
        self.lastModified = ""
        db = connectDB()
        self.database = db['chat']
        
    def switch_DES(self,newDES):
        self.database.bulk_write([
            UpdateOne({'user-list':self.user},{'$pull':{'user-list':self.user}}),
            UpdateOne({'DES':newDES},{'$addToSet':{'user-list':self.user}})
        ])
        
    def send_message(self,message):
        message = f'{self.user} ({now.strftime("%H:%M")}): {message}'
        self.database.find_one_and_update({'DES':self.DES},{'$push':{'chat-list':message}})
        
    def resetchat(self,DES):
        self.database.update_one(
            {'DES':DES},
            {'$set':{'user-list':[],'chat-list':[]}
            },
        )
    
    def getData(self,DES):
        # while True:
        #     if self.check:
        #         break
            self.session = self.database.find_one({'DES':DES})
            if self.session['lastModified'].strftime('%Y-%m-%d %H:%M:%S') != self.lastModified:
                return(newline.join([user for user in self.session['user-list'] if isinstance(user,str)]),newline.join([message for message in self.session['chat-list']]))
    
    def logoutChat(self):
        self.database.update_one(
            {'DES':self.DES},
            {'$pull':{'user-list':self.user}
            },
        )
    
if __name__ == '__main__':
    chat = Session('John')
    chat.send_message('Morning')
    #chat.switch_DES('featureDES')
    chat.update('genderDES')
    # chat.resetchat('locationDES')
    # chat.resetchat('featureDES')
    # chat.resetchat('genderDES')
    
    