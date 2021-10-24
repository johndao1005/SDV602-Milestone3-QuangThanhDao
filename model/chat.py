#from config.db import connectDB
from datetime import datetime, date
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

from pymongo import MongoClient
from dotenv import load_dotenv

from pathlib import Path
import os
import certifi
ca = certifi.where()
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
def connectDB():
    try:
        client = MongoClient(f"{MONGO_URI}",tlsCAFile=ca)
        print("Connect to Database")
        return client["white-shark"]
    except:
        print("Connection failed")

today = date.today().strftime("%d/%m/%Y")
now = datetime.now()
newline = "\n"


# TODO show user is online depend on the current screen
class ChatSession():
    def __init__(self,username,usersList,chatList):
        self.check = True
        self.DES = 'featureDES'
        self.user = username
        self.usersList = usersList
        self.chatList = chatList
        db = connectDB()
        self.database = db['chat']
        self.start_session()
        
    def switch_DES(self,DES):
        self.database.bulk_write([
            UpdateOne({'DES':DES},{'$addToSet':{'user-list':self.user}}),
            UpdateOne({'DES':self.DES},{'$pull':{'user-list':self.user}})
        ])
        self.DES = DES
        
    def send_message(self,message):
        message = f'{self.user} ({now.strftime("%H:%M")}): {message}'
        self.database.find_one_and_update({'DES':self.DES},{'date':today},{'$push':{'chat-list':message}})
    
    def start_session (self):
        self.database.update_one(
            {'DES':self.DES},
            {'$push':{'user-list':self.user}
            },
            upsert=True)
    
    # def update_session(self):
    #     while self.check is True:
    #         self.session = self.database.find_one({'date':today})
    #         self.usersList.set(newline.join([user for user in self.session['user-list'] if isinstance(user,str)]))
    #         self.chatList.set(newline.join([user for user in self.session['chat-list']]))
    
    
if __name__ == '__main__':
    chat = ChatSession('Kim1',['he','he'],["hoho",'haha'])
    chat.send_message('Nice')
    # chat.switch_DES('locationDES')
    