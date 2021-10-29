from tkinter.messagebox import showinfo, showerror
from view.dataView import DataView


def authentication(login, email, pw):
    """Function to check the if username and password is correct then destroy the login window
        and open the main menu to allow users interact with the application

        Args:
            login (class): instance of login window
            name (string): email from user input
            pw (string): password from user input
        """
    if email.strip() == "" or pw.strip() == "":
        showerror("Empty input", "Please type your email and password to login")
    else:
        checkUser = login.userControl.authentication(email, pw)
        if isinstance(checkUser, str):
            showerror("Authentication failed", checkUser)
        else:
            showinfo("Login success", "You seem legal, happy browsing")
            login.destroy()
            DataView(checkUser['name']).mainloop()
