from tkinter import *
from tkinter import ttk


def data_interface_window(username='NA'):

    # Set-up UI window
    window = Tk()
    window.title("{}'s Image Processing "  # Sets window title
                 "Application.".format(username))
    window.geometry('500x500')  # Sets window size

    # Run Window until close
    window.mainloop()
    return


if __name__ == "__main__":
    data_interface_window('sm642')
