from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext


def data_interface_window(username='NA'):

    # Set-up UI window
    window = Tk()
    window.title("{}'s Image Processing "  # Sets window title
                 "Application.".format(username))
    window.geometry('500x500')  # Sets window size

    # Create tab control
    tab_control = ttk.Notebook(window)
    tab_control.pack(expand=1, fill="both")
    upload_tab = ttk.Frame(tab_control)
    display_tab = ttk.Frame(tab_control)
    download_tab = ttk.Frame(tab_control)
    metrics_tab = ttk.Frame(tab_control)

    # Label tabs
    tab_control.add(upload_tab, text="Upload")
    tab_control.add(display_tab, text="Display")
    tab_control.add(download_tab, text="Download")
    tab_control.add(metrics_tab, text="User Metrics")

    # Upload tab
    # Function to choose files wanted to open
    def choose_files():  # Function for opening Files
        ftypes = [('Portable Graphics Format .png', '*.png'),
                  ('Joint Photographic Experts Group .jpeg', '*jpeg'),
                  ('Tagged Image File Format .tiff', '*.tiff'),
                  ('Compressed File Format .zip', '*.zip')]
        files = filedialog.askopenfilenames(filetypes=ftypes)
        file_display.insert(INSERT, files)
        return files

    # Choose File Section
    file_display = scrolledtext.ScrolledText(upload_tab,  # Display files
                                             width=50,
                                             height=1)
    file_display.grid(column=1, row=1)  # Location to display files
    file_btn = Button(upload_tab,  # Choose files button
                      text="Choose Files",
                      bg="white",
                      fg="black",
                      command=choose_files)
    file_btn.grid(column=2, row=1)  # Choose file button location

    # Display tab

    # Download tab

    # User Metrics tab

    # Run Window until close
    window.mainloop()
    return


if __name__ == "__main__":
    data_interface_window('sm642')
