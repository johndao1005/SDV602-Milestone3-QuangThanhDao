from tkinter.messagebox import showinfo, showerror
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def register(login, name, pw, pw2, email):
    """Checking input is valid and not already exist in the current database before creating new user instance

    Args:
        login (class): an instance of login window
        name (string): username taken from user input, need to be more than 2 characters and less than 20 characters
        pw (string):  password taken from user input, need to be more than 8 character and less than 20 characters
        pw2 (string): confirm password, need to be identical with password input
        email (string): email from user, need to have @ and valid email name
    """
    error = ""
    pw = pw.strip()
    pw2 = pw2.strip()
    name = name.strip()
    email = email.strip()

    # validate the information
    if len(pw) < 8:
        error += "\nThe password needs to be at least 8 characters"
    if pw2 != pw:
        error += "\nThe confirm password must be the same as pasword"
    if not re.fullmatch(regex, email):
        error += "\nEnter a valid email address"
    elif login.userControl.check('email', email) != 0:
        error += "\nThe email is already in use"
    if login.userControl.check('name', name) != 0:
        error += "\nThe username is already in use"
    # check if there is no error then create users
    if error != "":
        showerror("Incorrect input(s)",
                  f"Please correct the following errors:{error}")
    else:
        login.userControl.register(name, pw, email)
        showinfo("Registered success", "User is registered successfully")
        login.closeSignup()
