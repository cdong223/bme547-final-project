# Image Processor Server

[![Build Status](https://travis-ci.com/bme547-fall2019/final-project-dervil_dong_moavenzadeh_qi.svg?token=S1GryLqVRUGxLdXx1yV4&branch=master)](https://travis-ci.com/bme547-fall2019/final-project-dervil_dong_moavenzadeh_qi)


---
## Description
The purpose of this program is to allow users to create an account and log into the image processing server and their personal database. In the server, the user can upload an image and choose an image processing method. The server will process the image accordingly and save the original as well as the processed image into an online database (MongoDB). Upon successfully uploading image, the user can choose to display one or two images (together with image metrics associated with each image, such as CPU processing time, timestamp of upload, image size, and histogram), download the original images and/or processed images that they uploaded or processed, and view their user metrics, which includes how many images uploads the user has made and the total number of times the user has called each of the four image processing steps.

## Instructions for Use
### Deployment of Server
- The hostname of the virtual machine the server is deployed on is vcm-11657.vm.duke.edu
### Running the GUI
- Locate data_interface.py document, and run it with python data_interface.py
### Log-In Interface
- If you are a returning user, enter the username that you used with the database last time and click "Log In". If you accidentally clicked the "New User" button, a pop-up window will appear and lets you know that you are already registered in the system.
- If you are a new user, enter in your desired username and click "New User". If you accidentally clicked the "Log In" button, a pop-up window will appear and lets you know that you are not registered in the system and needs to be created.
- After you log in or create a new user, the Log-In interface will close and the main interface will open. You can also close the Log-In interface any time by clicking the "x" on the upper right corner.
### Main Interface
The main interface consists of the following tabs:
* Upload Tab
    - In the upload tab, you can choose the image you want to upload by clicking the button and browsing the files on your laptop. Select the image you want to upload and process. The upload button will be grayed out until an image is selected.
    - Choose a processing method you desire. Currently, histogram equalization, contrast stretching, log compression, and inverting are available. The default is histogram equalization.
    - Hit the upload button once you have chosen the desired image and processing method. You can re-select the image if the image is selected accidentally the first time.
    - If one or more of the original image or processed image already exists in the database, the GUI will indicates so and continue to upload and process the leftover images.
* Display Image Tab
    - In the display image tab, you can use the drop-down menu to select an image you want to display. The drop-down menu uploads automatically as more images are uploaded or processed.
    - After choosing the image, click the "ok" button, and the following will be displayed: the selected picture, CPU processing time, timestamp of upload, image size, RGB histogram (the top one is for red, middle one for green, and bottom one for blue)
    - If no image is selected and the "ok" button is clicked, an error box will pop up
    - The left and right side works independently. One or two images can be displayed at the same time.
* User Metrics Tab
    - Clicks "Get User Metrics" to refresh the page
    - Displays how many images uploads the user has made and the total number of images performed on by each different processing steps
* Download Tab
    - Displays a list of images available for download. The user can select an image or multiple images as well as the download format
    - Download the image or list of image (in zip) in the chosen format
    
## Disclaimer
As of today, the program does not have the download tab and its associated functionalities. 



MIT License

Copyright (c) [2019] [Spencer Moavenzadeh, Claire Dong, Wei Qi, Therlking Dervil]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
