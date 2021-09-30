def logout(dataview):
    """Function destroy the current data view window and display the a new login screen

    Args:
        dataview (variable): data view main window
    """
    from view.login import Login
    dataview.destroy()
    Login().mainloop()