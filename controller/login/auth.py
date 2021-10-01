from tkinter.messagebox import showinfo, showerror
from config.db import connectDB


def authentication(parent, email, pw):
    from view.dataView import dataView
    """Function to check the if username and password is correct then destroy the login window
        and open the main menu to allow users interact with the application

        Args:
            name (string): email from user input
            pw (string): password from user input
        """
    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    db = connectDB()
    currentUser = db["users"].find_one({"email":email})
    print(currentUser)
    if (currentUser.password == pw):
        showinfo("Welcome User", "Login successfully, Happy browsing!!")
        parent.destroy()
        dataView().mainloop()
    else:
        showerror("Incorrect email/password","Please check your email and password and try again")