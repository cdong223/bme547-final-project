from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import ImageTk, Image
import os
import requests

# ---------------------------Login Screen--------------------------------
def login_window():
    # Initialize global variables
    global login_screen
    global username
    global url
    url = "http://127.0.0.1:5000"

    # Login command
    def validateLogin():
        r = requests.post("http://127.0.0.1:5000/api/login",
                          json=username.get())
        if r.status_code == 200:
            print("{} is logged in".format(username.get()))
            login_screen.withdraw()
            data_interface_window(username.get())
            return
        else:
            username_not_recognized()

    # New user command
    def validateNewUser():
        r = requests.post("http://127.0.0.1:5000/api/new_user",
                          json=username.get())
        if r.status_code == 200:
            print("{} is a new user".format(username.get()))
            login_screen.withdraw()
            data_interface_window(username.get())
            return
        else:
            username_already_exists()

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

    global window
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
    def sort_files(new_files, out_files):
        # Returns sorted list of all elements with no repeated elements
        for filepath in new_files:
            if filepath not in all_files:
                out_files.append(filepath)
        # Returns all files wanting to read as tuple of string paths
        return sorted(out_files)

    # Appends only new files selected to display window
    def display_files(root_box, files):
        # Deletes current box and displays new files in alphabetical order
        root_box.delete('1.0', END)
        for filename in sorted(files):
            head, tail = os.path.split(filename)
            root_box.insert(END, tail+'\n')
        return

    # Function to choose files wanted to open
    def choose_files(out_files):
        # Open file selection box
        ftypes = [('.png (Portable Graphics Format)', '*.png'),
                  ('.jpeg (Joint Photographic Experts Group)', '*jpeg'),
                  ('.tiff (Tagged Image File Format)', '*.tiff'),
                  ('.zip (Compressed File Format)', '*.zip')]
        new_files = filedialog.askopenfilenames(filetypes=ftypes)
        # Sort for non-repeated list of files
        out_files = sort_files(new_files, out_files)  # Sorts files.
        print(out_files)
        # Display all files selected
        display_files(file_display, out_files)  # Displays image names
        # Allow selection of upload button as files are selected
        if out_files:
            upload_btn.config(state='normal',
                              bg='white',
                              fg='black')
        return out_files

    # Reset all files chosen upon upload
    def reset_selection(files):
        removable_files = tuple(files)
        for filepath in removable_files:
            files.remove(filepath)

    # Function if select upload files button
    def upload_files(files, processing):
        # Submit post request to validate files to upload
        # (including processing) and presence in dictionary
        new_url = url + "/api/validate_images"
        validate_dict = {"username": str(username),
                         "filepaths": files,
                         "processing": str(processing)}
        r = requests.post(new_url, json=validate_dict)
        out_dict = r.json()
        if r.status_code != 200:
            return

        # Parse through dictionary to isolate files to upload.
        present_images = out_dict["present"]
        new_images = out_dict["not present"]

        # Call function to display top level tab of files present and those
        # uploading.
        # If Continue button, move forward and delete display/reset file
        # selection/disable upload. If not, simply return.
        if len(present_images.keys()) != 0:
            images_already_present(present_images)

        # For filepath not present - submit post request of files.
        new_url = url + "/api/upload_images"
        store_dict = {"username": str(username),
                      "images": new_images}
        r = requests.post(new_url, json=store_dict)
        status = r.json()
        
        # Reset GUI file download display and file selection
        file_display.delete('1.0', END)
        reset_selection(files)
        upload_btn.config(state='disabled',
                          bg='grey',
                          fg='black')
        return

    # Choose File Section
    all_files = []  # Stores all filepaths of files wanting to upload.
    file_display = scrolledtext.ScrolledText(upload_tab,  # Display files
                                             width=50,
                                             height=5)
    file_display.grid(column=1, row=1)  # Location to display files
    file_btn = Button(upload_tab,  # Choose files button
                      text="Choose Files",
                      bg="white",
                      fg="black",
                      command=lambda: choose_files(all_files))
    file_btn.grid(column=2, row=1)  # Choose file button location

    # Choose Processing Type Section
    processing_type = StringVar()  # Variable for processing type
    processing_type.set('_histogramEqualized')
    hist_process = Radiobutton(upload_tab,
                               text='Histogram Equalization',
                               variable=processing_type,
                               value='_histogramEqualized')
    hist_process.grid(column=1,
                      row=2,
                      sticky=W,
                      pady=5,
                      padx=100)
    cont_stretch = Radiobutton(upload_tab,
                               text='Contrast Stretching',
                               variable=processing_type,
                               value='_contrastStretched')
    cont_stretch.grid(column=1,
                      row=3,
                      sticky=W,
                      pady=5,
                      padx=100)
    log_comp = Radiobutton(upload_tab,
                           text='Log Compression',
                           variable=processing_type,
                           value='_logCompressed')
    log_comp.grid(column=1,
                  row=4,
                  sticky=W,
                  pady=5,
                  padx=100)
    inv_img = Radiobutton(upload_tab,
                          text='Invert Image',
                          variable=processing_type,
                          value='_invertedImage')
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
                        command=lambda: upload_files(all_files,
                                                     processing_type),
                        state="disabled")
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
    # Command for Display Current User Metrics button
    def button_action():
        r = requests.get("http://127.0.0.1:5000/api/user_metrics/"
                         "{}".format(username))
        metrics = r.json()
        total_uploads = metrics["total_uploads"]
        total_hist_equal = metrics["total_hist_equal"]
        total_contrast_stretch = metrics["total_contrast_stretch"]
        total_log_comp = metrics["total_log_comp"]
        total_inv_img = metrics["total_inv_img"]
        upload_num.config(text=total_uploads)
        hist_num.config(text=total_hist_equal)
        contrast_num.config(text=total_contrast_stretch)
        log_num.config(text=total_log_comp)
        invert_num.config(text=total_inv_img)
        return

    def on_tab_selected(event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "User Metrics":
            print("Selected User Metrics tab")

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


def images_already_present(present_images):
    # Screen closed upon clicking "Ok" button
    def exit():
        present_images_screen.destroy()
        return

    # Screen layout
    present_images_screen = Toplevel(window)
    present_images_screen.title("Invalid Image Upload")
    present_images_screen.geometry('600x500')

    present_images_screen.grid_columnconfigure(0, weight=1)
    present_images_screen.grid_columnconfigure(1, weight=1)
    # present_images_screen.grid_rowconfigure(3, weight=1)

    note1 = Label(present_images_screen,
                  text="These processed images already exist in the database.")
    note1.grid(row=0, column=0, columnspan=2)

    note2 = Label(present_images_screen,
                  text="The matching requests will not be sent to the server.")
    note2.grid(row=1, column=0, columnspan=2)

    Label(present_images_screen, text="").grid(row=2, column=0)

    Button(present_images_screen, text="Ok", command=exit).grid(row=3,
                                                                column=0,
                                                                columnspan=2)

    Label(present_images_screen, text="").grid(row=4, column=0, columnspan=2)

    category_L = Label(present_images_screen, text="UPLOADED FILES:")
    category_L.grid(row=5, column=0)

    category_R = Label(present_images_screen,
                       text="LIST OF PROCESSED FILENAMES:")
    category_R.grid(row=5, column=1)

    Label(present_images_screen, text="").grid(row=6, column=0)

    current_row = 7

    for filepath in present_images.keys():
        head, tail = os.path.split(filepath)
        name_list = present_images.get(filepath)
        num_rows = len(name_list)
        Label(present_images_screen,
              text=tail).grid(row=current_row, column=0, rowspan=num_rows)
        for name in name_list:
            Label(present_images_screen,
                  text=name).grid(row=current_row, column=1)
            current_row += 1
        Label(present_images_screen,
              text="").grid(row=current_row, column=0)
        current_row += 1


if __name__ == "__main__":
    login_window()
