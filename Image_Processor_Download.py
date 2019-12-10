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

    saved_images = ["bd1", "blue", "yepp"]
    test_image_format = []

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


    def image_format_execution(test_image_format, test_image_type):
        """Image Format Label

        This section adds the format in which the user wishes to download
        the images. Using if statements and for loops, the function add the
        necessary endings to each element in the array. If an option is not
        selected, a pop up notification will appear.

        :param :

        :return :
        """
        if image_type.get() == "JPEG":
            for i in range(0,len(selected_saved_images)):
                selected_saved_images[i] = selected_saved_images[i] + ".JPEG"
                print(selected_saved_images)

        elif image_type.get() == "PNG":
            for i in range(0,len(selected_saved_images)):
                selected_saved_images[i] = selected_saved_images[i] + ".PNG"
                print(selected_saved_images)

        elif image_type.get() == "TIFF":
            for i in range(0,len(selected_saved_images)):
                selected_saved_images[i] = selected_saved_images[i] + ".TIFF"
                print(selected_saved_images)

        else:
            messagebox.showerror("Missing Image Format", "Please select an image format.")
        test_image_format = selected_saved_images
        return test_image_format


    root_download = Tk()

    root_download.title("Image Download")

    top_label = ttk.Label(root_download, text = "Image Download")
    top_label.grid(column = 2, row = 0, columnspan = 3)

    image_type = StringVar()
    jpeg_option = ttk.Radiobutton(root_download, text = "JPEG", variable = image_type, value = "JPEG")
    jpeg_option.grid(column = 2, row = 2)

    png_option = ttk.Radiobutton(root_download, text = "PNG", variable = image_type, value = "PNG")
    png_option.grid(column = 2, row = 3)

    tiff_option = ttk.Radiobutton(root_download, text = "TIFF", variable = image_type, value = "TIFF")
    tiff_option.grid(column = 2, row = 4)

    download_button = ttk.Button(root_download, text = "Download")
    download_button.grid(column = 0, row = 5, columnspan = 3)

    saved_images_button = ttk.Button(root_download, text = "Saved Images")
    saved_images_button.grid(column = 1, row = 1, columnspan = 3)

    root_download.mainloop()
    return


if __name__ == "__main__":
    design_download_window()
