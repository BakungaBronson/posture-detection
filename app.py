# Import opencv for computer vision stuff
import cv2
# Import matplotlib so we can visualize an image
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import requests
from requests.structures import CaseInsensitiveDict
import json
import threading
import datetime
import imutils

root = tk.Tk()
root.title("PhotoBooth App")
root.geometry('600x500')

def authenticate():
    user = username.get("1.0", END)
    passwrd = password.get("1.0", END)

    print(user, passwrd)

    url = "https://muele.mak.ac.ug/login/token.php?service=moodle_mobile_app"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "username={0}&password={1}".format(user.strip(), passwrd.strip())

    resp = requests.post(url, headers=headers, data=data)
    resp_json = resp.json()

    try:
        if resp_json['token']:
            output.insert(END, "Successfully logged in as {}".format(user))

            def take_photo(): 
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite('webcamphoto.jpg', frame)
                cap.release()

            # Connect to webcam
            cap = cv2.VideoCapture(0)
            # Loop through every frame until we close our webcam
            while cap.isOpened(): 
                ret, frame = cap.read()
                
                # Show image 
                cv2.imshow('Webcam', frame)
                
                # Checks whether q has been hit and stops the loop
                if cv2.waitKey(1) & 0xFF == ord('t'):
                    take_photo()

            # Releases the webcam
            cap.release()
            # Closes the frame
            cv2.destroyAllWindows()
    except:
        output.insert(END, "Something went wrong. Try again.")

img = ImageTk.PhotoImage(Image.open("images.png"))
panel = Label(root, image = img)
panel.pack()

username = Text(root, height =  2, width = 52)
username.insert(END, 'Username')
username.pack()

password = Text(root, height =  2, width = 52)
password.insert(END, 'Password')
password.pack()

convert_button = Button(root, height = 2, width = 20, text = "Submit", command = authenticate)
convert_button.pack()

output = Text(root, height = 5, width = 52, bg = "light blue")
output.pack()

root.mainloop()