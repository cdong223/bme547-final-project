from tkinter import *
from tkinter import ttk

def design_download_window():
    """Main GUI User Interface

    This section consists of the download user interface.
    This consists of a download button, three radio options in which
    choose file format, and a saved images button to select filenames
    that are currently available.

    :param :

    :return :
    """

    selected_saved_images = []


    saved_images = ["bd1", "blue", "yepp"]

    def download_button_execution():
        """ Download Button Execution
        This function uses an if statement to decide if an image name
        has been selected. If so, it then activates the image_format_execution
        function. If not, a pop up notification appears.

        :param :

        :return :
        """
        if not selected_saved_images:
            messagebox.showerror("Missing Image", "No image(s) selected")
        else:
            image_format_execution()
        return


    def image_format_execution():
        """Image Format Label

        This section adds the format in which the user wishes to download
        the images. Using if statements and for loops, the function add the
        necessary endings to each element in the array. If an option is not
        selected, a pop up notification will appear.

        :param :

        :return :
        """
        current_image_type = image_type.get()
        from download_GUI_functions import image_format_modifier
        response = image_format_modifier(current_image_type, selected_saved_images)
        if response is False:
            messagebox.showerror("Missing Image Format", "Please select an image format.")
        else:
            selected_saved_images = response
        return

    def saved_images_listbox_execution():
        """Saved Images Listbox Execution
        This function determines if the saved_images list is empty.
        If it is empty, a pop up notification appears. If it is
        occupied, the okay_button_execution fuction is enabled.

        :param :

        :return :
        """
        if not saved_images:
            messagebox.showinfo("No Images Available", "No available image(s) to select.")
        else:
            def ok_button_execution():
                """OK Button Execution
                This function responds once the okay button has been clicked on
                the saved_images_listbox interface. This will use if statements
                and for loops to save the selected images into selected_saved_images
                array. The window will then close.

                :param :

                :return :
                """
                for i in saved_images_listbox.curselection():
                    if saved_images[i] not in selected_saved_images:
                        selected_saved_images.extend([saved_images[i]])
                    print(selected_saved_images)
                saved_images_windows.destroy()
                return

            def cancel_saved_images_button_execution():
                """Cancel Saved Images Button Execution
                This function closes the window in which one could select saved images.

                :param :

                :return :
                """
                saved_images_windows.destroy()
                return

            saved_images_windows = Toplevel()
            ok_button = ttk.Button(saved_images_windows, text="OK", command=ok_button_execution)
            ok_button.grid(column=0, row=5, columnspan=3)

            cancel_saved_images_button = ttk.Button(saved_images_windows, text="Cancel", command=cancel_saved_images_button_execution)
            cancel_saved_images_button.grid(column=4, row=5, columnspan=3)

            saved_images_var = StringVar(value = saved_images)
            saved_images_listbox = Listbox(saved_images_windows, selectmode = 'multiple', height = len(saved_images), listvariable = saved_images_var)
            saved_images_listbox.grid(column = 2, row = 1, columnspan = 3)

    root_download = Tk()

    root_download.title("Image Download")

    top_label = ttk.Label(root_download, text="Image Download")
    top_label.grid(column=2, row=0, columnspan=3)

    image_type = StringVar()
    jpeg_option = ttk.Radiobutton(root_download, text="JPEG", variable=image_type, value="JPEG")
    jpeg_option.grid(column=2, row=2)

    png_option = ttk.Radiobutton(root_download, text="PNG", variable=image_type, value="PNG")
    png_option.grid(column=2, row=3)

    tiff_option = ttk.Radiobutton(root_download, text="TIFF", variable=image_type, value="TIFF")
    tiff_option.grid(column=2, row=4)

    download_button = ttk.Button(root_download, text="Download", command=download_button_execution)
    download_button.grid(column=0, row=5, columnspan=3)

    saved_images_button = ttk.Button(root_download, text="Saved Images", command=saved_images_listbox_execution)
    saved_images_button.grid(column=1, row=1, columnspan=3)

    root_download.mainloop()
    return

if __name__ == "__main__":
    design_download_window()
