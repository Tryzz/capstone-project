import pyautogui
import cv2
import numpy as np
import pytesseract

import win32gui, win32ui
from win32api import GetSystemMetrics

import tkinter

pytesseract.pytesseract.tesseract_cmd = (r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\tesseractOCR\tesseract.exe") # needed for Windows as OS

def hide_all_roots():
    for root in tkinter._root_window_list():
        root.withdraw()


def highlightItems():
    dc = win32gui.GetDC(0)
    dcObj = win32ui.CreateDCFromHandle(dc)
    hwnd = win32gui.WindowFromPoint((0,0))
    monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

    while True:
        m = win32gui.GetCursorPos()

        dcObj.MoveTo((m[0], m[1]))
        dcObj.LineTo((m[0] + 30, m[1]))
        dcObj.LineTo((m[0] + 30, m[1] + 30))
        dcObj.LineTo((m[0], m[1] + 30))
        dcObj.LineTo((m[0], m[1]))

        win32gui.InvalidateRect(hwnd, monitor, True) # Refresh the entire monitor

def highlightTk(text, lang='eng'):
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')
    print(text)
    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]
        # Filter rows in DataFrame where text is equal to text
        item_instances = data[data['text'] == text]

        numItems = len(item_instances)

        root = tkinter.Tk()
        root.attributes('-alpha', 0.5)
        root.attributes('-fullscreen', True)

        canvas = tkinter.Canvas(root, bg='black')
        canvas.pack(fill='both', expand=True)

        print(numItems)

        # Loop through each instance of the input text and draw a rectangle with a label
        for idx, (index, row) in enumerate(item_instances.iterrows(), 1):
            x1, y1 = row['left'], row['top']
            width, height = row['width'], row['height']
            x2, y2 = x1 + width, y1 + height

            canvas.create_rectangle(x1, y1, x2, y2, fill='blue')

            # Label the found item with a number above the rectangle
            label_x = (x1 + x2) / 2
            label_y = y1 - 10
            canvas.create_text(label_x, label_y, text=str(idx), fill='white')

        root.after(5000, root.destroy)

        root.mainloop()

    except IndexError:
        print("Text was not found")
        return None
    
    return(x, y)

def clickPic(icon):
    locations = pyautogui.locateAllOnScreen(f'media\{icon}.png', confidence=0.5)
    for location in locations:
        print(location)

def click(text, lang='eng'):
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')
    print(text)
    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        return None

    print(x, y)

    pyautogui.click(x+5, y+5)

    return(x, y)

def doubleClick(text, lang='eng'):
    screenshot = pyautogui.screenshot()

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')

    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        return None

    print(x, y)

    pyautogui.doubleClick(x+5, y+5)

    return(x, y)

def hover(text, lang='eng'):
    screenshot = pyautogui.screenshot()

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')

    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        return None

    print(x, y)

    pyautogui.moveTo(x+5, y+5)

    return(x, y)