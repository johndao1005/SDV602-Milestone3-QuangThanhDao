from model.model import Model
import os
from tkinter.messagebox import showerror,showinfo

def mergeFiles(target,source,dataview):
    """working with merging the target file data into the source file data

    Args:
        target (variable): the target file path which give file from the upload window
        source (variable): the source file path which will 
        dataview (variable): the main window which will excute the method to control DES and upload window
    """
    if source =="" or target=="":
        showerror("Error","Please select two files to merge")
    else:
        dataControl = Model()
        dataControl.merge(target,source)
        showinfo("Merge success","The file is merged and will be loaded for viewing")
        dataview.loadDES(source)
        dataview.closeUpload()