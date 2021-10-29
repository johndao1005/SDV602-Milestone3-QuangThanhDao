"""
Setup screen for each DES which is a frame to be displayed on main window dataview. DES is the template which handle displaying data as well as holding the buttons
afterward each DES will inherit from DES but responsible for displaying different type of data and graph.
"""
import view.setup as setup
from model.dataControl import Model
from mttkinter import mtTkinter as tk
from tkinter import ttk
import threading
import time
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import geopandas
from matplotlib import style
style.use("ggplot")


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
        self.draw_graph(self.DES)
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
        label = ttk.Label(self, text=f"Current user: {dataview.user}", font=setup.normal).grid(
            column=3, row=0, **setup.pad5)

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

        self.entry = ttk.Entry(frame1, textvariable=input,
                               width=40, font=setup.normal)
        self.entry.grid(
            column=0, row=2, **setup.pad10, sticky="E")
        button = ttk.Button(frame1,
                            text="Send",
                            command=lambda: dataview.chatSession.send_message(
                                self.entry.get(), self)
                            ).grid(column=1, row=2, **setup.pad10, sticky="E")

        # ANCHOR Data control frame
        frame2 = ttk.LabelFrame(self, text="Control box", borderwidth=0)
        frame2.grid(column=3, row=2, **setup.pad10, columnspan=2, sticky="NEW")
        button = ttk.Button(frame2,
                            text="Update",
                            command=lambda: dataview.refresh()
                            ).grid(column=0, row=1, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Upload",
                            command=lambda: dataview.openUpload()
                            ).grid(column=1, row=1, **setup.pad20)
        button = ttk.Button(frame2,
                            text="Quit",
                            command=lambda: dataview.quit()).grid(column=2, row=1, sticky="E", **setup.pad20)
        self.users = ""
        self.chat = ""
        self.thread = threading.Thread(target=self.updateChat, args=[
                                       dataview.chatSession], daemon=True)

    def updateChat(self, session):
        """function to for thread to update chat while checking the session

        Args:
            session (string): local timestamp of the session
        """
        while True:
            time.sleep(2)
            check = session.checkSession(self.DES)
            if check != self.lastModified:
                users, chat = session.getData(self.DES)
                self.update(users, chat)
                self.lastModified = check

    def clearEntry(self):
        """function to clear the entry after upload
        """
        self.entry.delete(0, tk.END)

    def update(self, users, chat):
        """function to update the text for user log and chat log for the current DES

        Args:
            users (string): user list
            chat (string): chat log
        """
        self.chatLog['state'] = 'normal'
        self.userLog['state'] = 'normal'
        self.userLog.delete('1.0', tk.END)
        self.chatLog.delete('1.0', tk.END)
        self.userLog.insert('1.0', users)
        self.chatLog.insert('1.0', chat)
        self.chatLog['state'] = 'disable'
        self.userLog['state'] = 'disable'

    def draw_graph(self, frame):
        """Function used to draw the graph on the window depend on the current frame as well
        as controlling the tool bar. the data is provided in the source from dataview.

        Args:
            frame (string): data type to be displayed on the graph      
        """
        database = Model()
        # ANCHOR prepare graph
        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)
        # data type plot in graph
        if frame == "feature":
            # Create data store
            labels = []
            mature = []
            immature = []
            size300 = []
            size350 = []
            size400 = []
            sizeUnder440 = []
            sizeAbove440 = []
            # Extract filtered
            data = database.featureData()
            # sort value
            for key in sorted(data.keys()):
                labels.append(key)
                mature.append(data[key][0])
                immature.append(data[key][1])
                size300.append(data[key][2])
                size350.append(data[key][3])
                size400.append(data[key][4])
                sizeUnder440.append(data[key][5])
                sizeAbove440.append(data[key][6])
            # the label locations
            x = np.arange(len(labels))
            # the width of the bars
            width = 0.1
            rects1 = ax.bar(x + width, mature, width, label='Mature')
            rects2 = ax.bar(x + width*2, immature, width, label='Immature')
            rects3 = ax.bar(x + width*3, size300, width, label='300 cm')
            rects4 = ax.bar(x + width*4, size350, width, label='350 cm')
            rects5 = ax.bar(x + width*5, size400, width, label='400 cm')
            rects6 = ax.bar(x + width*6, sizeUnder440,
                            width, label='Below 400 cm')
            rects7 = ax.bar(x + width*7, sizeAbove440,
                            width, label='Above 440 cm')
            ax.set_xlabel('Year')
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()
            ax.bar_label(rects1, padding=2)
            ax.bar_label(rects2, padding=2)
            ax.bar_label(rects3, padding=2)
            ax.bar_label(rects4, padding=2)
            ax.bar_label(rects5, padding=2)
            ax.bar_label(rects6, padding=2)
            ax.bar_label(rects7, padding=2)
            ax.plot()

        elif frame == "gender":
            # Create data store
            label = []
            value = []
            # Extract filtered
            data = database.genderData()
            for key in data:
                label.append(key)
                value.append(data[key])
            # Draw the graph
            ax.pie(value, radius=1, labels=label,
                   autopct='%0.2f%%', shadow=True,)

        elif frame == "location":
            # extract filtered data
            data = database.locationData()
            # getting map for NZ
            countries = geopandas.read_file(
                geopandas.datasets.get_path("naturalearth_lowres"))
            countries[countries["name"] == "New Zealand"].plot(
                color="lightgrey", ax=ax)
            # Plot map
            data.plot(x="decimalLongitude", y="decimalLatitude", kind="scatter", colormap="YlOrRd",
                      title=f"New Zealand Location", ax=ax)
            ax.grid(b=True, alpha=0.5)
            ax.set_xlabel('Longtitude')
            ax.set_ylabel('Latitude')
        # ANCHOR draw graph
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        # ANCHOR Options for adding the tool in tool bar
        NavigationToolbar2Tk.toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] not in (
            'Subplots', 'Back', 'Forward', 'Save')]
        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        toolbar.update()
        canvas.get_tk_widget().grid(column=0, row=1, columnspan=3, rowspan=2)  # create canvas
        toolbar.grid(column=0, row=3)  # create tool bar


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
