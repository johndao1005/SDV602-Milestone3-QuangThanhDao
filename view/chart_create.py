from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
from tkinter import *
from model.model import Model
import geopandas as gpd
from matplotlib import style
style.use("ggplot")

def draw_graph(window, frame,dataview):
    """Function used to draw the graph on the window depend on the current frame as well
    as controlling the tool bar. the data is provided in the source from dataview.

    Args:
        window (variable): the frame to plot graph
        frame (string): data type to be displayed on the graph      
        dataview (variable): dataview window to control the data source as well as the reloading function
    """
    database = Model(dataview.source)
    # ANCHOR prepare graph
    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)
    # data type plot in graph
    if frame == "feature":
        #Create data store
        labels = []
        mature = []
        immature = []
        size300 = []
        size350 = []
        size400 = []
        sizeUnder440 = []
        sizeAbove440 = []
        #Extract filtered
        data = database.featureData()
        # sort value 
        for key  in sorted (data.keys()):
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
        rects6 = ax.bar(x + width*6, sizeUnder440, width, label='Below 400 cm')
        rects7 = ax.bar(x + width*7, sizeAbove440, width, label='Above 440 cm')
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
        #Create data store
        label = []
        value = []
        #Extract filtered
        data = database.genderData()
        for key  in data:
            label.append(key)
            value.append(data[key])
        #Draw the graph
        ax.pie(value, radius=1, labels=label,autopct='%0.2f%%', shadow=True,)
    
    elif frame == "location":
        #extract filtered data
        data = database.locationData()
        #getting map for NZ
        countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        countries[countries["name"] == "New Zealand"].plot(color="lightgrey", ax=ax)
        # Plot map
        data.plot(x="decimalLongitude", y="decimalLatitude", kind="scatter", colormap="YlOrRd", 
        title=f"New Zealand Location", ax=ax)
        ax.grid(b=True, alpha=0.5)
        ax.set_xlabel('Longtitude')
        ax.set_ylabel('Latitude')
    # ANCHOR draw graph
    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    # ANCHOR Options for adding the tool in tool bar

    NavigationToolbar2Tk.toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] not in (
        'Subplots', 'Back', 'Forward', 'Save')]
    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    canvas.get_tk_widget().grid(column=0, row=1, rowspan=4)  # create canvas
    toolbar.grid(column=0, row=6)  # create tool bar


if __name__ == "__main__":
    root = Tk()
    draw_graph(root, "location")
    root.mainloop()
