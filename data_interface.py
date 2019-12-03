from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext


# ---------------------------Login Screen--------------------------------
def login_window():
    # Initialize global variables
    global login_screen
    global username

    # Login command
    def validateLogin():
        # user = UserMetrics.objects.raw({"_id": username.get()})
        # if(user.count() == 0):
        if(username.get() == "bad"):  # TEMPORARY (future database connection)
            username_not_recognized()
        else:
            print("{} is logged in".format(username.get()))
            login_screen.withdraw()
            data_interface_window(username.get())
            return

    # New user command
    def validateNewUser():
        # user = UserMetrics.objects.raw({"_id": username.get()})
        # if(user.count() != 0):  
        if(username.get() == "bad"):  # TEMPORARY (future database connection)
            username_already_exists()
        else:
            print("{} is a new user".format(username.get()))
            login_screen.withdraw()
            data_interface_window(username.get())
            print("close")
            return

    # Screen layout
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.geometry('300x200')

    login_screen.grid_columnconfigure(0, weight=1)
    login_screen.grid_columnconfigure(1, weight=1)
    login_screen.grid_rowconfigure(0, weight=3)
    login_screen.grid_rowconfigure(3, weight=1)
    login_screen.grid_rowconfigure(5, weight=3)

    usernameLabel = Label(login_screen, text="Enter Username:")
    usernameLabel.grid(row=1, column=0, columnspan=2)
    username = StringVar()
    usernameEntry = Entry(login_screen, textvariable=username)
    usernameEntry.grid(row=2, column=0, columnspan=2)

    loginButton = Button(login_screen, text="Login", command=validateLogin)
    loginButton.grid(row=4, column=0)
    newButton = Button(login_screen, text="New User", command=validateNewUser)
    newButton.grid(row=4, column=1)

    login_screen.mainloop()
    return


# -------------------------Invalid Login Screen-----------------------------
def username_not_recognized():
    # Screen closed upon clicking "Ok" button
    def exit():
        invalid_screen.destroy()
        return

    # Screen layout
    invalid_screen = Toplevel(login_screen)
    invalid_screen.title("Invalid")
    invalid_screen.geometry('200x100')
    Label(invalid_screen, text="Username not recognized.").pack()
    Button(invalid_screen, text="Ok", command=exit).pack()


# -----------------------Invalid Registration Screen---------------------------
def username_already_exists():
    # Screen closed upon clicking "Ok" button
    def exit():
        invalid_screen.destroy()
        return

    # Screen layout
    invalid_screen = Toplevel(login_screen)
    invalid_screen.title("Invalid")
    invalid_screen.geometry('200x100')
    Label(invalid_screen, text="Username already exists.").pack()
    Button(invalid_screen, text="Ok", command=exit).pack()


# ------------------------------Main UI Window---------------------------------
def data_interface_window(username='NA'):
    # Set-up UI window
    window = Toplevel(login_screen)
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

    # ----------------------------Upload tab--------------------------------
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

    # Choose Processing Type Section
    processing_type = StringVar()  # Variable for processing type
    processing_type.set('hist')
    hist_process = Radiobutton(upload_tab,
                               text='Histogram Equalization',
                               variable=processing_type,
                               value='hist')
    hist_process.grid(column=1,
                      row=2,
                      sticky=W,
                      pady=5,
                      padx=100)
    cont_stretch = Radiobutton(upload_tab,
                               text='Contrast Stretching',
                               variable=processing_type,
                               value='cont')
    cont_stretch.grid(column=1,
                      row=3,
                      sticky=W,
                      pady=5,
                      padx=100)
    log_comp = Radiobutton(upload_tab,
                           text='Log Compression',
                           variable=processing_type,
                           value='log')
    log_comp.grid(column=1,
                  row=4,
                  sticky=W,
                  pady=5,
                  padx=100)
    inv_img = Radiobutton(upload_tab,
                          text='Invert Image',
                          variable=processing_type,
                          value='inv')
    inv_img.grid(column=1,
                 row=5,
                 sticky=W,
                 pady=5,
                 padx=100)

    # Function to upload files selected
    def upload_files():
        print("Upload Files")

    # Upload Selection Section
    upload_btn = Button(upload_tab,
                        text="Upload Files",
                        bg="white",
                        fg="black",
                        command=upload_files)
    upload_btn.grid(column=1,  # Choose file button location
                    row=6,
                    sticky=W,
                    pady=5,
                    padx=100)

    # ----------------------------Display tab---------------------------------

    # ----------------------------Download tab--------------------------------

    # ----------------------------User Metrics tab----------------------------

    # Run Window until close
    window.mainloop()
    return


if __name__ == "__main__":
    login_window()
