"""Data Explore Application
The program helps presenting as well as reading data regard the tagging of white shark
With the application user can view data in graph with matplotlib while enjoy the GUI navigation of Tkinter

"""

from view.login import Login 

def start():
    app = Login()
    app.mainloop()
if __name__ == '__main__':
    """
    Initiate the app
    """
    from view.dataView import dataView
    start()
