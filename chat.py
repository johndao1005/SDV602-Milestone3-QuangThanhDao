from db import connectDB
from datetime import datetime, date
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne


today = date.today().strftime("%d/%m/%Y")
now = datetime.now()
newline = "\n"


class Session():
    def __init__(self, username):
        self.check = False
        self.user = username
        self.lastModified = ""
        db = connectDB()
        self.userDatabase = db['users']
        self.database = db['chat']

    def login(self):
        self.userDatabase.update_one({'name': self.user},
                  {'$set': {'online': True}})

    def switch_DES(self, newDES):
        self.database.bulk_write([
            UpdateOne({'user-list': self.user},
                      {'$pull': {'user-list': self.user}, '$currentDate': {'lastModified': True}}),
            UpdateOne({'DES': newDES}, {'$addToSet': {'user-list': self.user}, '$currentDate': {'lastModified': True}})
        ])

    def send_message(self, message, dataview):
        message = f'{self.user} ({now.strftime("%H:%M")}): {message}'
        self.database.update_one(
            {'DES': dataview.DES}, {'$push': {'chat-list': message}, '$currentDate': {'lastModified': True}})
        dataview.clearEntry()

    def resetchat(self, DES):
        self.database.update_one(
            {'DES': DES},
            {'$set': {'user-list': [], 'chat-list': []}
             })

    def getData(self, DES):
        self.session = self.database.find_one(
            {'DES': DES}, {'user-list': 1, 'chat-list': 1})
        return(newline.join([user for user in self.session['user-list'] if isinstance(user, str)]), newline.join([message for message in self.session['chat-list']]))

    def logoutChat(self):
        self.database.update_one({'DES': self.DES},
                                {'$pull': {'user-list': self.user}, '$currentDate': {'lastModified': True}}),
        self.userDatabase.update_one({'name': self.user},
                  {'$set': {'online': False}})

    def checkSession(self, DES, timestamp):
        session = self.database.find_one({'DES': DES}, {'lastModified': 1})
        return session['lastModified'] == timestamp
