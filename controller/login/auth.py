from tkinter.messagebox import showinfo, showerror

def authentication(parent, name, pw=""):
    from view.dataView import dataView
    """Function to check the if username and password is correct then destroy the login window
        and open the main menu to allow users interact with the application

        Args:
            name (string): username from user input
            pw (string): password from user input
        """
    showinfo("Welcome User", "Login successfully, Happy browsing!!")
    parent.destroy()
    dataView().mainloop()
