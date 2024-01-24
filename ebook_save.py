import os
import pyautogui as pag
import datetime
import time
import shutil
import img2pdf
import tkinter as tk
from PIL import Image

dt_now = datetime.datetime.now()

def screenshot():
    if LEFT_SCROLL.get():
        SCROLL_DIRECTION = 'left'
    else:
        SCROLL_DIRECTION = 'right'
    if not os.path.exists(fr'outputs/{FILE_NAME.get()}'):
        os.makedirs(fr'outputs/{FILE_NAME.get()}')
    for page in range(int(PAGE_NUM.get())):
        x1, y1, x2, y2 = map(int, REGION_ARG.get().split(','))
        sc = pag.screenshot(region=(x1, y1, x2-x1, y2-y1))
        sc.save(fr'outputs/{FILE_NAME.get()}/{page}.png')
        pag.press(SCROLL_DIRECTION)
        time.sleep(float(INTERVAL_TIME.get()))

def img_to_pdf():
    with open(fr'outputs/{FILE_NAME.get()}.pdf', 'wb') as f:
        f.write(img2pdf.convert(
            [Image.open(fr'outputs/{FILE_NAME.get()}/{page}.png').filename for page in range(int(PAGE_NUM.get()))]))

def delete_img():
    shutil.rmtree(fr'outputs/{FILE_NAME.get()}/')

def start():
    time.sleep(15)
    screenshot()
    if PDF.get():
        img_to_pdf()
        if DELETE_IMG.get():
            delete_img()

def temp_text(e):
    REGION_ARG.delete(0,"end")

root = tk.Tk()
root.title('Ebook Save')

root.option_add("*font", "Arial 15")
root.resizable(False, False)

textinput = tk.Frame(root)
textinput.grid(row=0, column=0, pady=5)
checkbox = tk.Frame(root)
checkbox.grid(row=1, column=0)
button = tk.Frame(root)
button.grid(row=2, column=0)

tk.Label(textinput, text='Number of pages').grid(row=0)
PAGE_NUM = tk.Entry(textinput)
PAGE_NUM.grid(row=0, column=1)
tk.Label(textinput, text='Region').grid(row=1)
REGION_ARG = tk.Entry(textinput)
REGION_ARG.insert(0, "x1,y1,x2,y2")
REGION_ARG.grid(row=1, column=1)
REGION_ARG.bind("<FocusIn>", temp_text)
tk.Label(textinput, text='File Name').grid(row=2)
FILE_NAME = tk.Entry(textinput)
FILE_NAME.insert(0, dt_now.strftime('%Y_%m%d_%H%M%S'))
FILE_NAME.grid(row=2, column=1)
tk.Label(textinput, text='Interval Time').grid(row=3)
INTERVAL_TIME = tk.Entry(textinput)
INTERVAL_TIME.insert(0, '3')
INTERVAL_TIME.grid(row=3, column=1)

DELETE_IMG = tk.IntVar(value = 0)
tk.Checkbutton(checkbox, text='Delete Images', variable=DELETE_IMG).grid(row=0, sticky="W")
LEFT_SCROLL = tk.IntVar(value = 0)
tk.Checkbutton(checkbox, text='Scroll to the left', variable=LEFT_SCROLL).grid(row=1, sticky="W")
PDF = tk.IntVar(value=1)
tk.Checkbutton(checkbox, text='Create PDF', variable=PDF).grid(row=2, sticky="W")

START_BUTTON = tk.Button(button, text='Start', width=30, command=start)
START_BUTTON.grid(pady=5, padx=20)

root.mainloop() 