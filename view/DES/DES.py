"""
Setup screen for each DES which is a frame to be displayed on main window dataview. DES is the template which handle displaying data as well as holding the buttons
afterward each DES will inherit from DES but responsible for displaying different type of data and graph.
"""
from view.chart_create import draw_graph
import tkinter as tk
from tkinter import ttk
import view.setup as setup
from controller.menu.logout import logout

class DES(tk.Frame):
    def __init__(self, parent, controller):
        self.frametype = None
        self.nextDES = None
        self.prevDES = None
        tk.Frame.__init__(self, parent)

    def DES_setup(self,window, dataview):
        """General setup for DES to be displayed 

        Args:
            window (variable): the frame or container which hold the 3 DES screen
            dataview (object): The main window which responsible for main functionality and data source
        """
        next = self.nextDES
        prev = self.prevDES
        frame = self.frametype
        label = ttk.Label(window, text=f"White shark {frame} data",font=setup.large).grid(
            column=0, row=0, **setup.pad20, columnspan=3)
        # graph
        draw_graph(window, frame,dataview)
        input = tk.StringVar()
        chatLog = tk.StringVar()
        # chat box creating and function
        frame1 = ttk.LabelFrame(window, text="Chat box", borderwidth=0)
        frame1.grid(column=2, row=1, **setup.pad20, sticky="E",columnspan=2)
        chatBox = ttk.Label(frame1,
                            background='light gray',
                            textvariable=chatLog, width=40
                            ).grid(column=1, row=1, **setup.pad20, columnspan=2)
        entry = ttk.Entry(frame1, textvariable=input).grid(
            column=1, row=2, **setup.pad20, sticky="E")
        button = ttk.Button(frame1,
                            text="Send",
                            command=lambda: dataview.show_frame(next)
                            ).grid(column=2, row=2, **setup.pad20, sticky="E")
        # ANCHOR Buttons for self
        frame2 = ttk.LabelFrame(window, text="Control box", borderwidth=0)
        frame2.grid(column=2, row=3, **setup.pad20, sticky="NSEW",columnspan=2)
        button = ttk.Button(frame2,
                            text="Next",
                            command=lambda: dataview.show_frame(next)
                            ).grid(column=0, row=4, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Previous",
                            command=lambda: dataview.show_frame(prev)
                            ).grid(column=1, row=4, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Update",
                            command=lambda: dataview.loadDES()
                            ).grid(column=1, row=5, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Upload",
                            command=lambda: dataview.openUpload()
                            ).grid(column=0, row=5, **setup.pad20)
        Location_self = ttk.Button(window,
                                text="Sign out",
                                command=lambda: logout(dataview)
                                ).grid(column=2, row=4, **setup.pad20)
        button = ttk.Button(window,
                            text="Quit",
                            command=lambda: dataview.destroy()).grid(column=3, row=4, **setup.pad20)
        
# inherit from DES
class genderDES(DES):
    def __init__(self,window, dataview):
        DES.__init__(self, window, dataview)
        self.nextDES = locationDES
        self.prevDES = featureDES
        self.frametype = "gender"
        self.DES_setup(self, dataview)


class locationDES(DES):
    def __init__(self, window, dataview):
        DES.__init__(self, window, dataview)
        self.nextDES = featureDES
        self.prevDES = genderDES
        self.frametype = "location"
        self.DES_setup(self, dataview)


class featureDES(DES):
    def __init__(self,window, dataview):
        DES.__init__(self, window, dataview)
        self.nextDES = genderDES
        self.prevDES = locationDES
        self.frametype = "feature"
        self.DES_setup(self, dataview)
