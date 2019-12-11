def image_format_modifier(current_image_type, selected_saved_images):
    if current_image_type == "JPEG":
        for i in range(0,len(selected_saved_images)):
            selected_saved_images[i] = selected_saved_images[i] + ".JPEG"
            print(selected_saved_images)
            return selected_saved_images

    elif current_image_type == "PNG":
        for i in range(0,len(selected_saved_images)):
            selected_saved_images[i] = selected_saved_images[i] + ".PNG"
            print(selected_saved_images)
            return selected_saved_images

    elif current_image_type == "TIFF":
        for i in range(0,len(selected_saved_images)):
            selected_saved_images[i] = selected_saved_images[i] + ".TIFF"
            print(selected_saved_images)
            return selected_saved_images

    else:
        return False
