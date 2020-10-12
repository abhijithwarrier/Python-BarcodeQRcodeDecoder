# Programmer - python_scripts (Abhijith Warrier)

# PYTHON GUI TO IDENTIFY & DECODE BARCODE AND QRCODE IMAGES USING pyzbar LIBRARY

# ZBar is an open source software suite for reading bar codes from various sources, such as video streams,
# image files and raw intensity sensors. It supports many popular symbologies (types of bar codes)
# including EAN-13/UPC-A, UPC-E, EAN-8, Code 128, Code 39, Interleaved 2 of 5 and QR Code.
#
# The module can be installed using the command - pip install pyzbar

# Importing necessary packages
import os
import cv2
import numpy as np
import tkinter as tk
import pyzbar.pyzbar as pyzbar
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidgets():
    label = Label(text="IMAGE : ", bg="thistle4")
    label.grid(row=0, column=1, padx=5, pady=5)

    root.entry = Entry(width=30, textvariable=imagePath)
    root.entry.grid(row=0, column=2, padx=5, pady=5)

    button = Button(width=10, text="UPLOAD", command=imageBrowse)
    button.grid(row=0, column=3, padx=5, pady=5)

    label = Label(text="INPUT IMAGE : ", bg="thistle4")
    label.grid(row=1, column=1, padx=5, pady=5)

    root.inputImageLabel = Label(root)
    root.inputImageLabel.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    # Opening a random image using the open() of Image class to be displayed when the program starts
    # The following 5 Lines Of Code are optional
    inputRandomImage = Image.open('YOUR RANDOM IMAGE PATH TO BE DISPLAYED WHEN APP STARTS - OPTIONAL')
    # Resizing the image using Image.resize()
    imageResize = inputRandomImage.resize((400, 400), Image.ANTIALIAS)
    # Creating object of PhotoImage() class to display the image
    imageDisplay = ImageTk.PhotoImage(imageResize)
    # Configuring the label to display the frame
    root.inputImageLabel.config(image=imageDisplay)
    # Keeping a reference
    root.inputImageLabel.image = imageDisplay

    button = Button(width=10, text="DECODE", command=imageDecode)
    button.grid(row=3, column=2, padx=5, pady=5)

    label = Label(text="DECODED IMAGE & TEXT", bg="thistle4",  font=('',20))
    label.grid(row=0, column=4, padx=5, pady=5, columnspan=3)

    root.outputImageLabel = Label(root)
    root.outputImageLabel.grid(row=2, column=4, columnspan=3, padx=5, pady=5)

    # Opening a random image using the open() of Image class to be displayed when the program starts
    # The following 5 Lines Of Code are optional
    outputRandomImage = Image.open('YOUR RANDOM IMAGE PATH TO BE DISPLAYED WHEN APP STARTS - OPTIONAL')
    # Resizing the image using Image.resize()
    imageResize = outputRandomImage.resize((400, 400), Image.ANTIALIAS)
    # Creating object of PhotoImage() class to display the image
    imageDisplay = ImageTk.PhotoImage(imageResize)
    # Configuring the label to display the image
    root.outputImageLabel.config(image=imageDisplay)
    # Keeping a reference
    root.outputImageLabel.image = imageDisplay

    root.codeTypeLabel = Label(text="CODE TYPE", bg="snow3", font=('',15))
    root.codeTypeLabel.grid(row=3, column=4, padx=5, pady=5, columnspan=3)

    root.codeDataLabel = Label(text="CODE DATA", bg="snow3", font=('',15))
    root.codeDataLabel.grid(row=4, column=4, padx=5, pady=5, columnspan=3)

# Defining imageBrowse() to select and display the input image to decode
def imageBrowse():
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    i_codeImage = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
    # Displaying the directory in the directory textbox
    imagePath.set(i_codeImage)
    # Opening the image using open() of Image class which takes the input image as argument
    imageView = Image.open(i_codeImage)
    # Resizing the image using Image.resize()
    imageResize = imageView.resize((400,400), Image.ANTIALIAS)
    # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageResize)
    # Configuring the label to display the frame
    root.inputImageLabel.config(image=imageDisplay)
    # Keeping a reference
    root.inputImageLabel.image = imageDisplay

# Defining imageDecode() to deocde the user selected image to decode
def imageDecode():
    # Fetching user-input image path from the tkinter variable and storing it in codeImage
    codeImage = imagePath.get()
    # Reading and storing the code image using the imread() method of cv2 library
    cv2_codeImage = cv2.imread(codeImage)

    # Decoding the image and finding the type of Code whether it is QR Code or Barcodes
    decodeCode = pyzbar.decode(cv2_codeImage)
    # Looping over the decoded objects
    for CodeImg in decodeCode:
        # Printing the code type(QR CODE OR BARCODE) and the code data
        root.codeTypeLabel.config(text="CODE TYPE   :   " + CodeImg.type)
        root.codeDataLabel.config(text="CODE DATA   :   " + str(CodeImg.data))

        # Finding the number of points in the CodeImg
        points = CodeImg.polygon
        # If the points do not form a quad, find the convex hull
        if len(points) > 4:
            conHull = cv2.convexHull(np.array([pts for pts in points],
                                              dtype=np.float32))
            conHull = list(map(tuple, np.squeeze(conHull)))
        else:
            conHull = points
        # Finding the number of points in the code image
        n = len(points)
        # Making the convex hull (Drawing the lines)
        for j in range(0, n):
            cv2.line(cv2_codeImage, conHull[j], conHull[(j + 1) % n],
                     (0, 0, 255), 2)

        # Fetching the name of the input image from the user-input image path
        input_image_name = os.path.splitext(os.path.basename(codeImage))[0]
        # Contatenating keyword decode with image name and storing the new name
        decoded_image_name = input_image_name + "-decoded.jpg"
        # Fetching the path of the user-input image
        input_image_path = os.path.dirname(os.path.abspath(codeImage))
        # Concatenating the input_image_path with decoded_image_name
        final_decoded_image_name = input_image_path + "/" + decoded_image_name

        # Saving decoded image in the same path using imwrite() of cv2 library
        cv2.imwrite(final_decoded_image_name, cv2_codeImage)

        # Opening the decoded image using the open() of Image class
        imageView = Image.open(final_decoded_image_name)
        # Resizing the image using Image.resize()
        imageResize = imageView.resize((400,400), Image.ANTIALIAS)
        # Creating object of PhotoImage() class to display the frame
        imageDisplay = ImageTk.PhotoImage(imageResize)
        # Configuring the label to display the frame
        root.outputImageLabel.config(image=imageDisplay)
        # Keeping a reference
        root.outputImageLabel.image = imageDisplay

# Creating object root of tk
root = tk.Tk()

# Setting the title, window size, disabling the resizing property and setting the
# background color
root.title("PyBarcodeQRCodeDecoder")
root.geometry("980x570")
root.resizable(False, False)
root.config(background = "thistle4")

# Creating tkinter variable
imagePath = StringVar()

# Calling the CreateWidgets() function
CreateWidgets()

# Defining infinite loop to run application
root.mainloop()
