"""
Contain the dataView class which handle the DES window outline as well as upload window view
"""
from mttkinter import mtTkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import view.setup as setup
from controller.menu.merge_csv import mergeFiles
from controller.menu.upload import selectFile
from view.DES import genderDES, locationDES, featureDES
from model.connect import Session, UserControl, DataHandler


class DataView(tk.Tk):
    """Data Explore Screen
    This is the main window which will display all the data regarding the datasource as long as the data is suitable.
    """

    def __init__(self, name='User', *args, **kwargs):
        """
        start the instance of dataView main window when it is called 
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.user = name
        self.resizable(0, 0)
        self.title(setup.app_name)
        self.iconbitmap(setup.icon)
        # self.geometry("1080x750+0+0")
        self.check = False
        self.protocol("WM_DELETE_WINDOW", self.quit)
        # ANCHOR frame setup left side
        self.container = ttk.Frame()
        self.container.grid(column=0, row=0, sticky="NW")
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
        filemenu.add_command(label="Sign out", command=lambda: showinfo(
            "Unavailable", "Function is not available, please come back for it later"))
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
        # START CHAT AND LOAD DES
        self.chatSession = Session(self.user)
        self.loadDES()
        self.userControl = UserControl()
        self.dataHandler = DataHandler()
        self.lastModified = self.dataHandler.checkRecord()

    # ANCHOR load all DES
    def loadDES(self):  # , source=setup.datasource):
        """
        Load the data explorer screen with the given data source else load the default data source
        """
        #self.source = source
        for DES in (genderDES, locationDES, featureDES):
            frame = DES(self.container, self)
            frame.thread.start()
            self.frames[DES] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.updateDES = False
        self.show_frame(featureDES)

    def refresh(self):
        """redraw the graph to retrieve the latest data or render the upload data
        """
        for DES in (genderDES, locationDES, featureDES):
            frame = self.frames[DES]
            frame.draw_graph(frame.DES)

    def show_frame(self, newFrame):
        """moving between data explorer screen 
        Args:
            newFrame (object): the screen to be presented 
        """
        frame = self.frames[newFrame]
        self.DES = frame.frametype
        self.chatSession.switch_DES(self.DES)
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
        label = ttk.Label(self.upload, text="Upload File").grid(
            column=0, row=2, **options)
        text = tk.Entry()
        self.target_entry = tk.Entry(self.upload, textvariable=target)
        self.target_entry.grid(
            column=1, row=2, **options, columnspan=3)
        browse_file = ttk.Button(self.upload,
                                 text="Select",
                                 command=lambda: selectFile(
                                     "upload", self.target_entry)
                                 ).grid(column=4, row=2, **setup.pad10)
        merge_btn = ttk.Button(self.upload,
                               text="Upload",
                               command=lambda: mergeFiles(
                                   self.target_entry.get(), self)
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
