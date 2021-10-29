from config.db import connectDB
import bcrypt
from datetime import datetime
from pymongo import UpdateOne

newline = "\n"

class UserControl():
    def __init__(self):
        db = connectDB()
        self.userDatabase = db['users']
        
    def check(self,field,value):
        return self.userDatabase.count_documents({field : value})
        
    def register(self, username,password,email):
        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        self.userDatabase.insert_one(
                    {"name":username,
                    "password": hashed,
                    "email":email,
                    'chance':3
                    })
        
    def authentication(self,email,password):
        if self.userDatabase.count_documents({"email":email}) != 0:
            user = self.userDatabase.find_one({"email":email})
            if user['chance'] > 0:
                bytePassword = str.encode(password)
                if bcrypt.checkpw(bytePassword, user['password']):
                    self.userDatabase.find_one_and_update({"email":email.strip()},{'$set':{'chance':3}})
                    return user
                else:
                    user = self.userDatabase.find_one_and_update({"email":email},{'$inc':{'chance':-1}})
                    return f"Wrong password. Please contact admin if you forget your password, {user['chance']} tries left"
            else:
                return "This account is locked. Please contact admin"
        else:
            return "The email is not registered"
        
        
class Session():
    def __init__(self, username):
        self.user = username
        self.lastModified = ""
        db = connectDB()
        self.chatDatabase = db['chat']

    def switch_DES(self, newDES):
        self.chatDatabase.bulk_write([
            UpdateOne({'user-list': self.user},
                      {'$pull': {'user-list': self.user}, '$currentDate': {'lastModified': True}}),
            UpdateOne({'DES': newDES}, {'$addToSet': {'user-list': self.user}, '$currentDate': {'lastModified': True}})
        ])

    def send_message(self, message, dataview):
        message = f'{self.user} ({datetime.now().strftime("%H:%M")}): {message}'
        self.chatDatabase.update_one(
            {'DES': dataview.DES}, {'$push': {'chat-list': message}, '$currentDate': {'lastModified': True}})
        dataview.clearEntry()

    def getData(self, DES):
        self.session = self.chatDatabase.find_one(
            {'DES': DES}, {'user-list': 1, 'chat-list': 1})
        return(newline.join([user for user in self.session['user-list'] if isinstance(user, str)]), newline.join([message for message in self.session['chat-list']]))

    def endSession(self,user):
        self.chatDatabase.update_many({'user-list':user},
                                {'$pull': {'user-list': user}, '$currentDate': {'lastModified': True}})
        
    def checkSession(self, DES):
        session = self.chatDatabase.find_one({'DES': DES}, {'lastModified': 1})
        return session['lastModified']

class DataHandler():
    def __init__(self):
        db = connectDB()
        self.database = db['data']
    
    def uploadData(self, data):
        self.database.update_one({'master':True},{'$currentDate': {'lastModified': True}})
        self.database.insert_many(data)
        
    def retrieveData(self):
        return self.database.find({'master':{'$exists':False}})
    
    def checkRecord(self):
        return self.database.find_one({'master':True})['lastModified']
    

if __name__ == '__main__':
    pass
