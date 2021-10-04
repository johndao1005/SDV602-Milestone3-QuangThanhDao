from tkinter.messagebox import showinfo, showerror
from config.db import connectDB
import re


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def makeUser(window,name,pw,pw2,email):
        """Checking input is valid and not already exist in the current database before creating new user instance

        Args:
            name (string): username taken from user input, need to be more than 2 characters and less than 20 characters
            pw (string):  password taken from user input, need to be more than 8 character and less than 20 characters
            pw2 (string): confirm password, need to be identical with password input
            email (string): email from user, need to have @ and valid email name
        """
        error = ""
        try :
            db = connectDB()
            if len(pw)< 8:
                error += "\nThe password needs to be at least 8 characters"
            if pw2 != pw:
                error += "\nThe confirm password must be the same as pasword"
            if not re.fullmatch(regex, email):
                error += "\nEnter a valid email address"
            # if client["users"].find({"email":email}) != None:
            #     error += "\nThe Email is already in use"
            if error != "":
                showerror("Incorrect input(s)",f"Please correct the following errors:{error}")
            else:
                db["users"].insert_one(
                    {"user":name,
                    "password":pw,
                    "email":email
                    })
                showinfo("Registered success","User is registered successfully")
                window.destroy()
        except:
            showerror("Sign up failed","Encounter error during during sign up")
