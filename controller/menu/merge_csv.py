from model.dataControl import Model
from tkinter.messagebox import showerror, showinfo


def mergeFiles(target, dataview):
    """working with merging the target file data into the source file data

    Args:
        target (variable): the target file path which give file from the upload window
        dataview (variable): the main window which will excute the method to control DES and upload window
    """
    if target == "":
        showerror("Error", "Please select to merge")
    elif dataview.dataHandler.checkRecord() != dataview.lastModified:
        showerror(
            "Error", "There are change to database please update before upload the new data")
    else:
        dataControl = Model()
        dataControl.upload(target)
        showinfo("Upload success",
                 "The data is uploaded and will be loaded for viewing")
        dataview.refresh()
        dataview.closeUpload()
