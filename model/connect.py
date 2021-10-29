from config.db import connectDB
import bcrypt
from datetime import datetime
from pymongo import UpdateOne

newline = "\n"
db = connectDB()


class UserControl():
    """Create a class to handle user collection of the database
    """

    def __init__(self):
        """Connect to the user collection
        """
        self.userDatabase = db['users']

    def check(self, field, value):
        """check the number of collection using the criteria provided in the argument

        Args:
            field (string): field to check the number of collection
            value (string): the value to find in the collection

        Returns:
            int: number of documents in the collection match the search value
        """
        return self.userDatabase.count_documents({field: value})

    def register(self, username, password, email):
        """start the register request after validate the input from user throw the GUI interface

        Args:
            username (string): username input from user 
            password (string): user password
            email (string): email
        """
        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        self.userDatabase.insert_one(
            {"name": username,
             "password": hashed,
             "email": email,
             'chance': 3
             })

    def authentication(self, email, password):
        """Check the password and email address pair to enable user to login.

        Args:
            email (string): user email address
            password (string): password

        Returns:
            string or dictionary: return the error message depend on the result of the request for any failed requirements or return user detail and allow user to lock in
        """
        if self.check("email", email) != 0:
            user = self.userDatabase.find_one({"email": email})
            if user['chance'] > 0:
                bytePassword = str.encode(password)
                if bcrypt.checkpw(bytePassword, user['password']):
                    self.userDatabase.find_one_and_update(
                        {"email": email.strip()}, {'$set': {'chance': 3}})
                    return user
                else:
                    user = self.userDatabase.find_one_and_update(
                        {"email": email}, {'$inc': {'chance': -1}})
                    return f"Wrong password. Please contact admin if you forget your password, {user['chance']} tries left"
            else:
                return "This account is locked. Please contact admin"
        else:
            return "The email is not registered"


class Session():
    """Create a class to handle chat collection of the database
    """

    def __init__(self, username):
        """Connect to the user collection and save username as well as the chat timestamp
        """
        self.user = username
        self.lastModified = ""
        self.chatDatabase = db['chat']

    def switch_DES(self, newDES):
        """function enable user to show which DES they are viewing and remove the previous DES

        Args:
            newDES (string): name of the dataview user switching to
        """
        self.chatDatabase.bulk_write([
            UpdateOne({'user-list': self.user},
                      {'$pull': {'user-list': self.user}, '$currentDate': {'lastModified': True}}),
            UpdateOne({'DES': newDES}, {'$addToSet': {
                      'user-list': self.user}, '$currentDate': {'lastModified': True}})
        ])

    def send_message(self, message, dataview):
        """create a request to add message to the chat database and clear the entry of the window

        Args:
            message (string): message to be sent
            dataview (class): instance of current dataview
        """
        message = f'{self.user} ({datetime.now().strftime("%H:%M")}): {message}'
        self.chatDatabase.update_one(
            {'DES': dataview.DES}, {'$push': {'chat-list': message}, '$currentDate': {'lastModified': True}})
        dataview.clearEntry()

    def getData(self, DES):
        """create a request to get the new chat data from the database and return that data when called

        Args:
            DES (string): the DES need to get data from
        """
        self.session = self.chatDatabase.find_one(
            {'DES': DES}, {'user-list': 1, 'chat-list': 1})
        return(newline.join([user for user in self.session['user-list'] if isinstance(user, str)]), newline.join([message for message in self.session['chat-list']]))

    def endSession(self, user):
        """end the chat Session and remove the user name from current DES

        Args:
            user (string): user name to be remove from the chat
        """
        self.chatDatabase.update_many({'user-list': user},
                                      {'$pull': {'user-list': user}, '$currentDate': {'lastModified': True}})

    def checkSession(self, DES):
        """check the database timestamp for the particular DES and return the new time stamp

        Args:
            DES (string): current DES to check

        Returns:
            string: new timestamp
        """
        session = self.chatDatabase.find_one({'DES': DES}, {'lastModified': 1})
        return session['lastModified']


class DataHandler():
    """Create a class to handle data collection of the database
    """

    def __init__(self):
        """Connect to the data collection
        """
        self.database = db['data']

    def uploadData(self, data):
        """upload the data recieved from the file and upload to the data collection while update the master record timestamp

        Args:
            data (array): array of data to be uploaded
        """
        self.database.update_one(
            {'master': True}, {'$currentDate': {'lastModified': True}})
        self.database.insert_many(data)

    def retrieveData(self):
        """get the latest data from the database

        Returns:
            array: data
        """
        return self.database.find({'master': {'$exists': False}})

    def checkRecord(self):
        """check the master record against the timestamp on the system to prevent multiple upload attempt

        Returns:
            string: current timestamp on the master record
        """
        return self.database.find_one({'master': True})['lastModified']


if __name__ == '__main__':
    pass
