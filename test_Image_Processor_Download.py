if __name__ == "__main__":
    #init_db()
    #build_db()
    #contents_db()
    import pytest

    saved_images = ["bd1", "blue", "yepp"]


    def test_image_format_execution(test_image_format, test_image_type):
        from Image_Processor_Downlaod import image_format_execution
        test_image_type = "JPEG"
        result1 = image_format_execution(test_image_format, test_image_type)
        assert result1 == ["bd1.JPEG", "blue.JPEG", "yepp.JPEG"]
        test_image_type = "PNG"
        result2 = image_format_execution(test_image_format, test_image_type)
        assert result2 == ["bd1.PNG", "blue.PNG", "yepp.PNG"]
        test_image_type = "TIFF"
        result3 = image_format_execution(test_image_format, test_image_type)
        assert result3 == ["bd1.TIFF", "blue.TIFF", "yepp.TIFF"]
        test_image_type = ""
        result4 = image_format_execution(test_image_format, test_image_type)
        assert result4 == ["bd1", "blue", "yepp"]