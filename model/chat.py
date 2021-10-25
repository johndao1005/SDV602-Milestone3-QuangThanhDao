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


class Session():
    def __init__(self,username):
        self.check = True
        self.DES = 'genderDES'
        self.user = username
        self.lastModified = ""
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
        self.database.find_one_and_update({'DES':self.DES},{'$push':{'chat-list':message}})
    
    def start_session (self):
        self.database.update_one(
            {'DES':self.DES},
            {'$addToSet':{'user-list':self.user},
            '$currentDate': {
            'lastModified': True
            }
            },
            upsert=True)
        
    def resetchat(self,DES):
        self.database.update_one(
            {'DES':DES},
            {'$set':{'user-list':[],'chat-list':[]}
            },
        )
    
    def logoutChat(self):
        self.database.update_one(
            {'DES':self.DES},
            {'$pull':{'user-list':self.user}
            },
        )
    
if __name__ == '__main__':
    chat = Session('Kim',['he','he'],["hoho",'haha'])
    chat.send_message('Hello')
    chat.switch_DES('featureDES')
    chat.logoutChat()
    # chat.resetchat('locationDES')
    # chat.resetchat('featureDES')
    # chat.resetchat('genderDES')
    
    