import re
import os
import win32gui
# msg = "哈哈哈S2-18*3"
# pattern = re.compile(r'哈哈哈(.*)')  # 用于匹配order
# level = pattern.match(msg).groups()[0]
# pattern = re.compile(r'S?(.*)-')
# chapter = pattern.match(level).groups()[0]
# pattern = re.compile(r'(.*)\*')
# section = pattern.match(level).groups()[0]
# pattern = re.compile(r'.*\*(.*)')
# times = pattern.match(level).groups()[0]
# order = 'ark.zhuxian(' + "\"" + "chapter" + chapter + "\"" + "," + "\"" + section + "\"" + "," + times + ')'
# print(order)
#
# print(os.listdir("wechatOrders"))
#
# print(os.path.splitext('i.txt')[0])

import os
# os.system(r'"C:\Program Files (x86)\MuMu\emulator\nemu\EmulatorShell\NemuPlayer.exe"')
#from win32gui import *
# titles = set()
# def foo(hwnd,mouse):
#  #去掉下面这句就所有都输出了，但是我不需要那么多
#     if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
#         titles.add(GetWindowText(hwnd))
# EnumWindows(foo, 0)
# lt = [t for t in titles if t]
# lt.sort()
# for t in lt:
#     print (t)
#
# han = FindWindow(None,"MuMu模拟器")
# SetForegroundWindow(han)

#打开关闭
import win32api,win32gui,time,win32con
# win32api.ShellExecute(0, 'open', 'C:\\Program Files (x86)\\MuMu\\emulator\\nemu\\EmulatorShell\\NemuPlayer.exe', '', '', 1)
# time.sleep(3)
# hwnd = win32gui.FindWindow(None,"MuMu模拟器")
# win32api.SendMessage(hwnd,win32con.WM_CLOSE,0,0)


# han = FindWindow(None,"MuMu模拟器")
# SetForegroundWindow(han)

# win32api.ShellExecute(0, 'open', 'C:\\Program Files (x86)\\MuMu\\emulator\\nemu\\EmulatorShell\\NemuPlayer.exe', '', '', 1)

hwnd = win32gui.FindWindow(None, "MuMu模拟器")
if (hwnd == None):
    pass
win32gui.SetForegroundWindow(hwnd)