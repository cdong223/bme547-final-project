from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import ImageTk, Image
import os


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
    def sort_files(new_files, all_files):
        # Returns sorted list of all elements with no repeated elements
        for filepath in new_files:
            if filepath not in all_files:
                all_files.append(filepath)
        # Returns all files wanting to read as tuple of string paths
        return sorted(all_files)

    # Appends only new files selected to display window
    def display_files(root_box, files):
        # Deletes current box and displays new files in alphabetical order
        root_box.delete('1.0', END)
        for filename in sorted(files):
            head, tail = os.path.split(filename)
            root_box.insert(END, tail+'\n')
        return

    # Function to choose files wanted to open
    def choose_files(out_files):  # Function for opening Files
        ftypes = [('.png (Portable Graphics Format)', '*.png'),
                  ('.jpeg (Joint Photographic Experts Group)', '*jpeg'),
                  ('.tiff (Tagged Image File Format)', '*.tiff'),
                  ('.zip (Compressed File Format)', '*.zip')]
        new_files = filedialog.askopenfilenames(filetypes=ftypes)
        out_files = sort_files(new_files, out_files)  # Sorts files.
        print(out_files)
        display_files(file_display, out_files)  # Displays image names in file_display box.
        return

    # Function if select upload files button
    def upload_files():
        file_display.delete('1.0', END)
        print("Upload Files")

    # Choose File Section
    all_files = []  # Stores all filepaths of files wanting to upload. 
    file_display = scrolledtext.ScrolledText(upload_tab,  # Display files
                                             width=50,
                                             height=1)
    file_display.grid(column=1, row=1)  # Location to display files
    file_btn = Button(upload_tab,  # Choose files button
                      text="Choose Files",
                      bg="white",
                      fg="black",
                      command=lambda: choose_files(all_files))
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

    # Upload Selection Section
    upload_btn = Button(upload_tab,
                        text="Upload Files",
                        bg="grey",  # Set to grey when disabled
                        fg="black",
                        command=upload_files)#,
                        #state="disabled")
    upload_btn.grid(column=1,  # Choose file button location
                    row=6,
                    sticky=W,
                    pady=5,
                    padx=100)


    # ----------------------------Display tab---------------------------------
    def left_display():  # find the picture according to the name
        # Only dummy variables are used now, but should be easy to
        # find image metrics if given image name
        if image_name_1.get() == 'A':
            path = "Apple.png"
            timestamp = ttk.Label(display_tab,
                                  text="Timestamp: {}".format(A[0]))
            cpu = ttk.Label(display_tab, text="CPU Time: {}".format(A[1]))
            size = ttk.Label(display_tab, text="Size: {}".format(A[2]))
        if image_name_1.get() == 'B':
            path = "BD.jpg"
            timestamp = ttk.Label(display_tab,
                                  text="Timestamp: {}".format(B[0]))
            cpu = ttk.Label(display_tab, text="CPU Time: {}".format(B[1]))
            size = ttk.Label(display_tab, text="Size: {}".format(B[2]))
        if image_name_1.get() == 'C':
            path = "Cat.jpg"
            timestamp = ttk.Label(display_tab,
                                  text="Timestamp: {}".format(C[0]))
            cpu = ttk.Label(display_tab, text="CPU Time: {}".format(C[1]))
            size = ttk.Label(display_tab, text="Size: {}".format(C[2]))
        print(path)
        timestamp.grid(column=0, row=5, pady=5)
        cpu.grid(column=0, row=6, pady=5)
        size.grid(column=0, row=7, pady=5)
        load = Image.open(path)
        load = load.resize((150, 150), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(display_tab, image=render)
        img.image = render
        img.grid(column=0, row=4, pady=5)
        return

    def right_display():  # find the picture according to the name
        if image_name_2.get() == 'A':
            path = "Apple.png"
            timestamp = ttk.Label(display_tab,
                                  text="Timestamp: {}".format(A[0]))
            cpu = ttk.Label(display_tab, text="CPU Time: {}".format(A[1]))
            size = ttk.Label(display_tab, text="Size: {}".format(A[2]))
        if image_name_2.get() == 'B':
            path = "BD.jpg"
            timestamp = ttk.Label(display_tab,
                                  text="Timestamp: {}".format(B[0]))
            cpu = ttk.Label(display_tab, text="CPU Time: {}".format(B[1]))
            size = ttk.Label(display_tab, text="Size: {}".format(B[2]))
            print(path)
        if image_name_2.get() == 'C':
            path = "Cat.jpg"
            timestamp = ttk.Label(display_tab,
                                  text="Timestamp: {}".format(C[0]))
            cpu = ttk.Label(display_tab, text="CPU Time: {}".format(C[1]))
            size = ttk.Label(display_tab, text="Size: {}".format(C[2]))
        print(path)
        timestamp.grid(column=2, row=5, pady=5)
        cpu.grid(column=2, row=6, pady=5)
        size.grid(column=2, row=7, pady=5)
        load = Image.open(path)
        load = load.resize((150, 150), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(display_tab, image=render)
        img.image = render
        img.grid(column=2, row=4, pady=5)
        return

    A = ["2019/12/3", "1.5s", "600x600"]  # Dummy variables of image metrics
    B = ["2019/12/4", "1.2s", "400x400"]
    C = ["2019/12/5", "1.4s", "200x200"]

    ttk.Separator(display_tab, orient=VERTICAL).grid(column=1, row=0,
                                                     rowspan=10, sticky='ns')

    choice_1 = ttk.Label(display_tab, text="Choose picture 1 from below")
    choice_1.grid(column=0, row=1, padx=50, pady=5)
    choice_2 = ttk.Label(display_tab, text="Choose picture 2 from below")
    choice_2.grid(column=2, row=1, padx=50, pady=5)

    image_list = ["A", "B", "C"]  # Need to read the actual list of image
    image_name_1 = StringVar()
    display_sel_1 = ttk.Combobox(display_tab, textvariable=image_name_1)
    display_sel_1.grid(column=0, row=2, pady=5)
    display_sel_1['values'] = image_list
    display_sel_1.state(['readonly'])
    image_name_2 = StringVar()
    display_sel_2 = ttk.Combobox(display_tab, textvariable=image_name_2)
    display_sel_2.grid(column=2, row=2, pady=5)
    display_sel_2['values'] = image_list
    display_sel_2.state(['readonly'])

    ok_btn_left = ttk.Button(display_tab, text='ok', command=left_display)
    ok_btn_left.grid(column=0, row=3, pady=5)
    ok_btn_right = ttk.Button(display_tab, text='ok', command=right_display)
    ok_btn_right.grid(column=2, row=3, pady=5)
    # ----------------------------Download tab--------------------------------

    # ----------------------------User Metrics tab----------------------------
    # Retrieve metrics for given user from database
    def get_metrics():
        # user_entry = UserMetrics.objects.raw({"_id": username})
        # user = user_entry[0]
        # total_uploads = user.total_uploads
        # total_hist_equal = user.total_hist_equal
        # total_contrast_stretch = user.total_contrast_stretch
        # total_log_comp = user.total_log_comp
        # total_inv_img = user.total_inv_img
        total_uploads = 6
        total_hist_equal = 2
        total_contrast_stretch = 1
        total_log_comp = 0
        total_inv_img = 3
        return [total_uploads, total_hist_equal, total_contrast_stretch,
                total_log_comp, total_inv_img]

    # Command for Display Current User Metrics button
    def button_action():
        metrics = get_metrics()
        upload_num.config(text=metrics[0])
        hist_num.config(text=metrics[1])
        contrast_num.config(text=metrics[2])
        log_num.config(text=metrics[3])
        invert_num.config(text=metrics[4])
        return

    # def on_tab_selected(event):
    #     selected_tab = event.widget.select()
    #     tab_text = event.widget.tab(selected_tab, "text")
    #     if tab_text == "User Metrics":
    #         print("Selected User Metrics tab")

    metrics_tab.grid_columnconfigure(0, weight=1)
    metrics_tab.grid_columnconfigure(1, weight=2)
    metrics_tab.grid_rowconfigure(0, weight=3)
    metrics_tab.grid_rowconfigure(2, weight=1)
    metrics_tab.grid_rowconfigure(8, weight=3)

    # Screen layout
    button = ttk.Button(metrics_tab, text="Display Current User Metrics",
                        command=button_action)
    button.grid(row=1, column=0, columnspan=2)

    upload_label = ttk.Label(metrics_tab,
                             text="Total number of uploads by user: ")
    upload_label.grid(row=3, column=0, sticky=E)
    upload_num = ttk.Label(metrics_tab, text="")
    upload_num.grid(row=3, column=1, sticky=W)

    hist_label = ttk.Label(metrics_tab,
                           text="# of times Histogram Equalization "
                                "performed: ")
    hist_label.grid(row=4, column=0, sticky=E)
    hist_num = ttk.Label(metrics_tab, text="")
    hist_num.grid(row=4, column=1, sticky=W)

    contrast_label = ttk.Label(metrics_tab,
                               text="# of times Contrast Stretching "
                                    "performed: ")
    contrast_label.grid(row=5, column=0, sticky=E)
    contrast_num = ttk.Label(metrics_tab, text="")
    contrast_num.grid(row=5, column=1, sticky=W)

    log_label = ttk.Label(metrics_tab,
                          text="# of times Log Compression performed: ")
    log_label.grid(row=6, column=0, sticky=E)
    log_num = ttk.Label(metrics_tab, text="")
    log_num.grid(row=6, column=1, sticky=W)

    invert_label = ttk.Label(metrics_tab,
                             text="# of times Image Inversion performed: ")
    invert_label.grid(row=7, column=0, sticky=E)
    invert_num = ttk.Label(metrics_tab, text="")
    invert_num.grid(row=7, column=1, sticky=W)
    

    # Run Window until close
    window.mainloop()
    return


if __name__ == "__main__":
    login_window()
