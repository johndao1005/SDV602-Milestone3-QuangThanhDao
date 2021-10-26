from tkinter.messagebox import showinfo, showerror
from db import connectDB
import bcrypt
from dataView import dataView
def authentication(parent, email, pw):
    """Function to check the if username and password is correct then destroy the login window
        and open the main menu to allow users interact with the application

        Args:
            name (string): email from user input
            pw (string): password from user input
        """
    if email.strip() =="" or pw.strip() =="":
        showerror("Empty input","Please type your email and password to login")
    else:
        bytePassword = str.encode(pw)
        db = connectDB()
        currentUser = db["users"].find_one({"email":email.strip()})
        hashed = bcrypt.hashpw(bytePassword, bcrypt.gensalt())
        if bcrypt.checkpw(bytePassword, hashed):
            if currentUser["online"] == True:
                showerror("Occupied account","The user is already logged in. Please contact admin if you think your details is hacked")
            else:
                showinfo(f"Welcome {currentUser['name']} ", "Login successfully, Happy browsing!!")
                parent.destroy()
                # Active this line when everything is done
                #db['users'].update_one({'name':currentUser['name']},{'$set':{'online':True}})
                dataView(currentUser['name'])
        else:
            showerror("Incorrect email/password","Please check your email and password and try again")