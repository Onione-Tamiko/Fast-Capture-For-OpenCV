import numpy as np
import numpy

import cv2

import win32gui
import win32con
import win32ui
import win32process

import os

import time
from time import strftime
from time import gmtime

def Get_Image(hwnd):
    a,b,c,d = win32gui.GetWindowRect(hwnd)
    width, height = c-a,d-b
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    np_image_app = np.frombuffer(dataBitMap.GetBitmapBits(True),'u1')
    np_image_app.shape = (height,width,4)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return np_image_app


def Get_HWND(pid):
    hwnd_app = []
    def enum_window_callback(hwnd, pid):
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if int(pid) == int(current_pid) and win32gui.IsWindowVisible(hwnd):
            hwnd_app.append(hwnd)
            
    win32gui.EnumWindows(enum_window_callback, pid)
    return hwnd_app

def Get_PID(name_proces):
    return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if name_proces in item.split()][0]

def Capture_APP(hwnd_app):
    fps = 1
    while True:
##        time.sleep(0.02) Lock 30 fps | time.sleep(0.01) Lock 60 fps
        np_image_app = Get_Image(int(hwnd_app[0]))
        opencv_frame_image = cv2.cvtColor(np_image_app, cv2.COLOR_RGBA2RGB)
        cv2.imshow(f'Streaming {name_proces}',opencv_frame_image)
        if cv2.waitKey(1) & 0xFF == ord('q') :
            cv2.destroyAllWindows()
            break
        fps +=1
    return fps
      
name_proces = 'mspaint.exe'
pid = Get_PID(name_proces)
hwnd_app = Get_HWND(pid)
print("NAME:",name_proces,"| PID:",pid,"| HWND:",hwnd_app[0])


start_time = time.time()
fps = Capture_APP(hwnd_app)
end_time = time.time()
seconds_work = end_time-start_time


print('ALL TIME WORK:',strftime("%H:%M:%S", gmtime(seconds_work)))
print('ALL SECONDS:',seconds_work)
print('ALL FPS:',fps,'|  ',int(fps/seconds_work),'FPS/s')


