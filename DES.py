"""
Setup screen for each DES which is a frame to be displayed on main window dataview. DES is the template which handle displaying data as well as holding the buttons
afterward each DES will inherit from DES but responsible for displaying different type of data and graph.
"""
from chart_create import draw_graph
from mttkinter import mtTkinter as tk
from tkinter import ttk
import setup as setup
import threading
import time

newline = '\n'

class DES(tk.Frame):
    """
    Create a template for all the DES to follow which contain the buttons graphs and other setting to allow all the DES to be uniformed.
    The DES template is tkinter Frame will be displayed on parent
    """

    def __init__(self, parent, controller):
        """start the DES which have empty details such as next, prev DES as well as the data type
        """
        self.frametype = None
        self.nextDES = None
        self.prevDES = None
        tk.Frame.__init__(self, parent,)

    def DES_setup(self, window, dataview):
        """General setup for DES to be displayed 

        Args:
            window (variable): the frame or container which hold the 3 DES screen
            dataview (object): The main window which responsible for main functionality and data source
        """
        self.lastModified = ""
        next = self.nextDES
        prev = self.prevDES
        self.DES = self.frametype
        label = ttk.Label(window, text=f"White shark {self.DES} data", font=setup.large).grid(
            column=0, row=0, **setup.pad20, columnspan=3)
        # graph
        draw_graph(window, self.DES, dataview)
        button = ttk.Button(self,
                            text="Next",
                            command=lambda: dataview.show_frame(next)
                            ).grid(column=2, row=3, **setup.pad20)
        button = ttk.Button(self,
                            text="Previous",
                            command=lambda: dataview.show_frame(prev)
                            ).grid(column=1, row=3, **setup.pad20)
        
        # ANCHOR chat box right side
        input = tk.StringVar()
        # chat box creating and function
        label = ttk.Label(self, text=f"Current user: {dataview.user}",font=setup.normal).grid(
            column=3, row=0,**setup.pad5)
        
        frame1 = ttk.LabelFrame(self, text="Chat box", borderwidth=0)
        frame1.grid(column=3, row=1, **setup.pad20, columnspan=2)
        self.userLog = tk.Text(frame1,
                               bg='white',
                               font=setup.normal,
                               height=4, width=50, yscrollcommand=set()
                               )
        self.userLog.grid(column=0, row=0, **setup.pad20, columnspan=2)
        self.chatLog = tk.Text(frame1,
                               bg='white',
                               font=setup.normal,
                               height=12,
                               width=50
                               )
        self.chatLog.grid(column=0, row=1, **setup.pad20, columnspan=2)
        
        self.entry = ttk.Entry(frame1, textvariable=input, width=40, font=setup.normal)
        self.entry.grid(
            column=0, row=2, **setup.pad10, sticky="E")
        button = ttk.Button(frame1,
                            text="Send",
                            command=lambda: dataview.chatSession.send_message(self.entry.get(),self)
                            ).grid(column=1, row=2, **setup.pad10, sticky="E")
        
        # ANCHOR Data control frame
        frame2 = ttk.LabelFrame(self, text="Data Control", borderwidth=0)
        frame2.grid(column=3, row=2, **setup.pad10, columnspan=2,sticky="NEW")
        button = ttk.Button(frame2,
                            text="Update",
                            command=lambda: dataview.loadDES()
                            ).grid(column=0, row=1, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Upload",
                            command=lambda: dataview.openUpload()
                            ).grid(column=1, row=1, **setup.pad20)
        button = ttk.Button(self,
                            text="Quit",
                            command=lambda: dataview.quit() ).grid(column=3, row=3,sticky="E",**setup.pad20)
        self.users = ""
        self.chat = ""
        self.thread = threading.Thread(target=self.updateChat, args=[dataview.chatSession],daemon=True)
    
    def updateChat(self,session):
        while True:
            time.sleep(2)
            check = session.checkSession(self.DES)
            if  check != self.lastModified:
                users,chat = session.getData(self.DES)
                self.update(users,chat)
                self.lastModified = check
            
    def clearEntry(self):
        self.entry.delete(0,tk.END)
    
    def update(self,users,chat):
        self.chatLog['state']= 'normal'
        self.userLog['state']= 'normal'
        self.userLog.delete('1.0',tk.END)
        self.chatLog.delete('1.0',tk.END)
        self.userLog.insert('1.0',users)
        self.chatLog.insert('1.0',chat)
        self.chatLog['state']= 'disable'
        self.userLog['state']= 'disable'
        
class genderDES(DES):
    """Generate gender DES which is a child of DES template

    Args:
        DES (object): DES template
    """

    def __init__(self, window, dataview):
        """initial the genderDES which take next DES as location DES and prev DES as feature DES while the data type is gender
        """
        DES.__init__(self, window, dataview)
        self.nextDES = locationDES
        self.prevDES = featureDES
        self.frametype = "gender"
        self.DES_setup(self, dataview)


class locationDES(DES):
    """Generate location DES which is a child of DES template

    Args:
        DES (object): DES template
    """

    def __init__(self, window, dataview):
        """initial the genderDES which take next DES as location DES and prev DES as feature DES while the data type is gender
        """
        DES.__init__(self, window, dataview)
        self.nextDES = featureDES
        self.prevDES = genderDES
        self.frametype = "location"
        self.DES_setup(self, dataview)


class featureDES(DES):
    """Generate feature DES which is a child of DES template
    
    Args:
        DES (object): DES template
    """

    def __init__(self, window, dataview):
        """initial the featureDES which take next DES as gender DES and prev DES as location  DES while the data type is feature
        """
        DES.__init__(self, window, dataview)
        self.nextDES = genderDES
        self.prevDES = locationDES
        self.frametype = "feature"
        self.DES_setup(self, dataview)
