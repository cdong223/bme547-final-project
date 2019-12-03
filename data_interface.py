from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext


# ------------------------------Main UI Window---------------------------------
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
    data_interface_window('sm642')
