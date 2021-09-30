from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *

def selectFile(action,target):
    """Function used to open the csv file to read to file name/ directory
    to used with different action to update the target folder

    Args:
        action (string): the action to perform with file
        target (variable): the target to update with the result of action regarding the file
    """
    filetypes = (
            ('csv', '*.csv'),
        )
    filename = fd.askopenfilename(
            title='Select csv datasource',
            initialdir='./data-sample',
            filetypes=filetypes)
    if action =="merge":
        target.insert(END,filename)
    if action =="open":
        target.loadDES(filename)
