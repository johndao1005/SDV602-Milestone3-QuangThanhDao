"""
Contain the dataView class which handle the DES window outline as well as upload window view
"""
from mttkinter import mtTkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import view.setup as setup

from merge_csv import mergeFiles
from open_csv import selectFile
from DES import genderDES, locationDES, featureDES
import threading
from chat import Session

class dataView(tk.Tk):
    """Data Explore Screen
    This is the main window which will display all the data regarding the datasource as long as the data is suitable.
    """
    def __init__(self,name='User',*args, **kwargs):
        """
        start the instance of dataView main window when it is called 
        """
        tk.Tk.__init__(self, *args, **kwargs )
        self.user = name
        self.resizable(0,0)
        # self.geometry("940x800+0+0")
        self.title(setup.app_name)
        self.iconbitmap(setup.icon)
        self.firstFrame = True
        self.check = False
        self.protocol("WM_DELETE_WINDOW", self.quit)
        # ANCHOR frame setup left side
        self.container = ttk.Frame()
        self.container.grid(column=0, row=0,sticky="NW")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # ANCHOR menubar setup
        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Choose Data Source",
                            command=lambda: selectFile("open", self))
        filemenu.add_command(label="Merge database",
                            command=lambda: self.openUpload())
        filemenu.add_command(label="Sign out", command=lambda: showinfo("Unavailable","Function is not available, please come back for it later"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        DESmenu = tk.Menu(menubar, tearoff=0)
        DESmenu.add_command(
            label="Gender", command=lambda: self.show_frame(genderDES))
        DESmenu.add_separator()
        DESmenu.add_command(
            label="Feature", command=lambda: self.show_frame(featureDES))
        DESmenu.add_separator()
        DESmenu.add_command(
            label="Location", command=lambda: self.show_frame(locationDES))
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Data view", menu=DESmenu)
        tk.Tk.config(self, menu=menubar)

        # ANCHOR chat box right side
        input = tk.StringVar()
        chatList = tk.StringVar()
        userList = tk.StringVar()
        # chat box creating and function
        rightSide = tk.Frame()
        rightSide.grid(column=1, row=0, **setup.pad20, columnspan=2,sticky="N")
        label = ttk.Label(rightSide, text=f"Current user {self.user}",font=setup.normal).grid(
            column=0, row=0)
        Location_self = ttk.Button(rightSide,
                                text="Sign out",
                                command=lambda: logout(self)
                                ).grid(column=1, row=0)

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
        frame2.grid(column=0, row=2, **setup.pad20, columnspan=2,sticky="NEW")
        button = ttk.Button(frame2,
                            text="Update",
                            command=lambda: self.loadDES()
                            ).grid(column=0, row=1, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Upload",
                            command=lambda: self.openUpload()
                            ).grid(column=1, row=1, **setup.pad20)
        button = ttk.Button(self,
                            text="Quit",
                            command=lambda: self.quit() ).grid(column=2, row=1,sticky="E",**setup.pad20)
        self.startSession()
        self.loadDES()
        
    def startSession(self):
        self.chatSession = Session(self.user)
    
    def update(self,users,chat):
        self.chatLog['state']= 'normal'
        self.userLog['state']= 'normal'
        self.userLog.delete('1.0',tk.END)
        self.chatLog.delete('1.0',tk.END)
        self.userLog.insert('1.0',users)
        self.chatLog.insert('1.0',chat)
        self.chatLog['state']= 'disable'
        self.userLog['state']= 'disable'
        
    # ANCHOR load all DES
    def loadDES(self, source=setup.datasource):
        """
        Load the data explorer screen with the given data source else load the default data source
        """
        self.source = source
        for DES in (genderDES, locationDES, featureDES):
            frame = DES(self.container, self)
            self.frames[DES] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(featureDES)

    def show_frame(self, newFrame):
        """moving between data explorer screen 

        Args:
            newFrame (object): the screen to be presented 
        """
        frame = self.frames[newFrame]
        self.chatSession.switch_DES(f'{frame.frametype}DES')
        users,chat = self.chatSession.getData(f'{frame.frametype}DES')
        print(users,chat)
        self.update(users,chat)
        frame.tkraise()
        


    def uploadWindow(self):
        """
        start a Top level window (pop up window) which attached to the Tk(main window)
        """
        self.check = True
        self.upload = tk.Toplevel()
        self.upload.title(setup.app_name)
        self.upload.iconbitmap(setup.icon)
        options = {'padx': 10, 'pady': 5}
        label = ttk.Label(self.upload, text="Upload").grid(
            column=0, row=0, **options, columnspan=5)
        self.upload.geometry("420x200+1000+200")
        self.upload.protocol("WM_DELETE_WINDOW", self.closeUpload)
        target = tk.StringVar()
        source = tk.StringVar()
        label = ttk.Label(self.upload, text="Target File").grid(
            column=0, row=2, **options)
        text = tk.Entry()
        self.target_entry = tk.Entry(self.upload, textvariable=target)
        self.target_entry.grid(
            column=1, row=2, **options, columnspan=3)
        label = ttk.Label(self.upload, text="Source File").grid(
            column=0, row=3, **options)
        self.source_entry = ttk.Entry(self.upload, textvariable=source)
        self.source_entry.grid(
            column=1, row=3, **options, columnspan=3)
        browse_file = ttk.Button(self.upload,
                                 text="Select",
                                 command=lambda: selectFile("merge", self.target_entry)
                                 ).grid(column=4, row=2, **setup.pad10)
        browse_file = ttk.Button(self.upload,
                                 text="Select",
                                 command=lambda: selectFile("merge", self.source_entry)
                                 ).grid(column=4, row=3, **setup.pad10)
        merge_btn = ttk.Button(self.upload,
                               text="Merge",
                               command=lambda: mergeFiles(self.target_entry.get(), self.source_entry.get(), self)
                               ).grid(column=1, row=4, **setup.pad10)
        quit_btn = ttk.Button(self.upload,
                              text="Quit",
                              command=lambda: self.closeUpload()
                              ).grid(column=2, row=4, **setup.pad10)

    def openUpload(self):
        """check if an instance of upload event is exist, then open the upload window
        """
        if self.check == False:
            self.uploadWindow()

    def closeUpload(self):
        """close the upload window and ensure the check if turn off to open new window
        """
        self.check = False
        self.upload.destroy()
