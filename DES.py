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
