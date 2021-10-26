"""
Setup screen for each DES which is a frame to be displayed on main window dataview. DES is the template which handle displaying data as well as holding the buttons
afterward each DES will inherit from DES but responsible for displaying different type of data and graph.
"""
from chart_create import draw_graph
from mttkinter import mtTkinter as tk
from tkinter import ttk
import setup as setup
from logout import logout

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
        self.lastModified = ''
        next = self.nextDES
        prev = self.prevDES
        frame = self.frametype
        label = ttk.Label(window, text=f"White shark {frame} data", font=setup.large).grid(
            column=0, row=0, **setup.pad20, columnspan=3)
        # graph
        draw_graph(window, frame, dataview)
        button = ttk.Button(self,
                            text="Next",
                            command=lambda: dataview.show_frame(next)
                            ).grid(column=2, row=2, **setup.pad20)
        button = ttk.Button(self,
                            text="Previous",
                            command=lambda: dataview.show_frame(prev)
                            ).grid(column=1, row=2, **setup.pad20)

        # ANCHOR chat section

        input = tk.StringVar()
        self.chatList = tk.StringVar()
        self.userList = tk.StringVar()
        # chat box creating and function
        rightSide = ttk.Frame()
        rightSide.grid(column=4, row=0, **setup.pad20,
                       columnspan=2, sticky="N")
        label = ttk.Label(rightSide, text=f"View data as {dataview.user}", font=setup.normal).grid(
            column=0, row=0)
        Location_self = ttk.Button(rightSide,
                                   text="Sign out",
                                   command=lambda: logout(dataview)
                                   ).grid(column=1, row=0)
        # TODO add scrollbar support
        frame1 = ttk.LabelFrame(rightSide, text="Chat box", borderwidth=0)
        frame1.grid(column=0, row=1, **setup.pad20, columnspan=2)
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
        
        entry = ttk.Entry(frame1, textvariable=input, width=40, font=setup.normal).grid(
            column=0, row=2, **setup.pad10, sticky="E")
        button = ttk.Button(frame1,
                            text="Send",
                            command=lambda: dataview.show_frame(next)
                            ).grid(column=1, row=2, **setup.pad10, sticky="E")

        # ANCHOR Data control frame
        frame2 = ttk.LabelFrame(rightSide, text="Data Control", borderwidth=0)
        frame2.grid(column=0, row=2, **setup.pad20, columnspan=2, sticky="NEW")
        button = ttk.Button(frame2,
                            text="Update",
                            command=lambda: dataview.loadDES()
                            ).grid(column=0, row=1, padx=20, sticky="E")
        button = ttk.Button(frame2,
                            text="Upload",
                            command=lambda: dataview.openUpload()
                            ).grid(column=1, row=1, pady=20, sticky="E")
        button = ttk.Button(rightSide,
                            text="Quit",
                            command=lambda: self.quit()  # ANCHOR need change to close chat session
                            ).grid(column=1, row=3, sticky="E", **setup.pad20)

    def update(self,users,chat):
        self.userLog.insert('1.0',users)
        self.chatLog.insert('1.0',chat)
        self.chatLog['state']= 'disable'
        self.userLog['state']= 'disable'
        
    def resetChat(self):
        self.chatLog['state']= 'normal'
        self.userLog['state']= 'normal'
        self.userLog.delete('1.0',tk.END)
        self.chatLog.delete('1.0',tk.END)
        
        
    # def update(self):
    #     print('start update')
    #     self.chatLog.insert('1.0','helllo \n nice to see you')
    #     self.session = self.database['chat'].find_one(
    #         {'DES': f'{self.frametype}DES'})
    #     if self.session['lastModified'].strftime('%Y-%m-%d %H:%M:%S') != self.lastModified:
    #         self.chatLog['state']= 'normal'
    #         self.userLog['state']= 'normal'
    #         self.userLog.insert('1.0', newline.join(
    #             [user for user in self.session['user-list'] if isinstance(user, str)]))
    #         # print(type(newline.join(
    #         #     [user for user in self.session['user-list'] if isinstance(user, str)])))
    #         self.chatLog.insert('1.0', newline.join(
    #             [user for user in self.session['chat-list']]))
    #         self.lastModified = self.session['lastModified']
    #         self.chatLog['state']= 'disable'
    #         self.userLog['state']= 'disable'


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
