from tkinter import *
from tkinter import ttk

def design_download_window():
    """Main GUI User Interface

    This section on consists of the download user interface.
    This consists of a download button, three radio options in which
    choose file format, and a saved images button to select filenames
    that are currently available.

    :param :

    :return :
    """

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
