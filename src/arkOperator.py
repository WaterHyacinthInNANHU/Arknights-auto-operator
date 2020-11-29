# import psutil as psutil
import pyautogui as auto
import time
from getWords import baiduOCR
import win32gui, win32api, win32com.client, win32con
import os
import traceback


class ArknightsErr(Exception):
    pass


class Arknights(object):
    def __init__(self, password='', email='', APP_ID='', API_KEY='', SECRECT_KEY='', path=''):
        self.imgdirs = ['imgs\\common\\', 'imgs\\supplies\\', 'imgs\\chapters\\', 'imgs\\activities\\', 'imgs\\']
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.logfilepath = "output\\log.txt"
        self.log("Welcome back, doctor!")
        self.email = email
        self.password = password
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRECT_KEY = SECRECT_KEY
        self.path = path
        # 检查图片资源路径
        for dir in self.imgdirs:
            if (os.path.exists(dir) == False):
                raise ArknightsErr('imgs resources load error: can not find dir: ' + dir)
        # 创建输出目录
        self.mkdir('.\\output')
        self.mkdir('.\\output\\screenshot')
        self.mkdir('.\\output\\wordsImgs')
        # 初始化log文件
        with open(self.logfilepath, "w+") as file:
            file.write('')
            pass

    def mkdir(self, path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print('mkdir: ' + path)

    def log(self, str, end="\n"):
        with open(self.logfilepath, "r") as file:
            original = file.read()
        with open(self.logfilepath, "w+") as file:
            file.write(original + str + end)
            print(str + end)

    def delay(self, t):
        time.sleep(t)

    def getTag(self, name, confidence=0.9):
        path = None
        for dir in self.imgdirs:
            if (os.path.exists(dir + name + '.jpg')):
                path = dir + name + '.jpg'
                break
        if (path == None):
            raise ArknightsErr('can not find image: ' + name)
        else:
            return auto.locateCenterOnScreen(path, grayscale=False, confidence=confidence)

    def click(self, pos):
        auto.click(pos.x, pos.y)
        self.delay(1.5)

    def typeStr(self, str):
        for char in str:
            auto.keyDown(char)
            auto.keyUp(char)

    def drag(self, xstart=1020, ystart=160, xdistance=0, ydistance=0, speed=250):
        auto.moveTo(xstart, ystart)  # move mouse to the start position
        auto.dragTo(xstart + xdistance, ystart + ydistance, button='left',
                    duration=pow(pow(xdistance, 2) + pow(ydistance, 2), 0.5) / speed)  # drag
        auto.click(xstart + xdistance, ystart + ydistance)
        self.delay(0.5)

    def to(self, name, targetname=None, timeoutforname=10, timeoutfortarget=10, israiseErr=True):
        self.log("name:" + str(name) + " targetname:" + str(targetname) + '\n')
        cnt = 0
        while True:
            cnt += 1
            self.foucusOnTheWindow()
            pos = self.getTag(name)
            if (pos != None): break
            self.delay(1)
            if (cnt >= timeoutforname):
                self.log("can't find : " + name)
                if (israiseErr):
                    raise ArknightsErr("can't find tag:" + name)
                return
        cnt = 0
        while True:
            cnt += 1
            self.foucusOnTheWindow()
            self.click(pos)
            self.delay(1)
            if (targetname == None):
                break
            elif (targetname == name):
                if (self.getTag(name) == None): break
            else:
                if (self.getTag(targetname) != None): break
            if (cnt >= timeoutfortarget):
                self.log("no reaction by pressing : " + name)
                if (israiseErr):
                    raise ArknightsErr("can't find tag:" + targetname)
                return
        return

    def backToMenu(self):
        self.foucusOnTheWindow()
        if (self.getTag("maximizemumu") != None):
            self.to("maximizemumu", "maximizemumu", timeoutfortarget=120)
        if (self.getTag("zuozhan") == None):
            self.to("navigator", "navigator_shouye")
            self.to("navigator_shouye", "navigator_shouye")

    def findTag(self, level, max_drag=20):
        cnt = 0
        while True:
            if cnt >= max_drag:
                break
            cnt += 1
            if self.getTag(level) is None:
                self.drag(xdistance=-500, speed=500)
            else:
                break
        if cnt >= max_drag:
            cnt = 0
            while True:
                if cnt >= max_drag:
                    return
                cnt += 1
                if self.getTag(level) is None:
                    self.drag(xdistance=500, speed=500)
                else:
                    break

    def onMission(self, scantime):  # 等待任务结束，scantime扫描间隔
        self.log("running", end='')
        while True:
            self.log(".", end=' ')
            self.delay(scantime)
            self.foucusOnTheWindow(throwExp=True)
            if (self.getTag("xingdongjieshu") != None):
                self.to("xingdongjieshu", "xingdongjieshu")
                return True
            if (self.getTag("dengjitisheng") != None):
                self.to("dengjitisheng", "dengjitisheng")
                self.to("xingdongjieshu", "xingdongjieshu")
                return True
            if (self.getTag("zuozhanjianbao") != None):
                self.to("zuozhanjianbao", "zuozhanjianbao")
                self.to("meizhoubaochoujindu", "meizhoubaochoujindu")
                return True
            if (self.getTag("fangqixingdong") != None):
                self.to("fangqixingdong", "fangqixingdong")
                self.to("renwushibai", "renwushibai")
                return False
            if (self.getTag("reconnect") != None):
                self.to("reconnect")
                return False

    def forTest(self):
        self.log("Arknight test")

    def setForegroundWindow(self, hwnd):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

    def foucusOnTheWindow(self, throwExp=False):
        hwnd = win32gui.FindWindow(None, "明日方舟 - MuMu模拟器")
        if (hwnd == 0):
            hwnd = win32gui.FindWindow(None, "MuMu模拟器")
        if (hwnd == 0):
            if (throwExp):
                raise ArknightsErr("Mumu has crashed")
            # self.log("can't find Mumu window")
            return False
        self.setForegroundWindow(hwnd)
        return True

    def exitMumu(self):
        try:
            #####daily tasks
            self.foucusOnTheWindow()
            cnt = 0
            self.backToMenu()
            self.to("renwu", "renwu")
            while cnt < 20:
                self.delay(0.5)
                if self.getTag('baochouyilingqu') != None:
                    break
                if self.getTag('dianjilingqu') != None:
                    self.to('dianjilingqu', 'dianjilingqu')
                    self.to('confirm', 'confirm', timeoutforname=10, israiseErr=False)
                    cnt = 0
                else:
                    cnt += 1
            ######
        except:
            self.log(traceback.format_exc())
        hwnd = win32gui.FindWindow(None, "明日方舟 - MuMu模拟器")
        if (hwnd == 0):
            hwnd = win32gui.FindWindow(None, "MuMu模拟器")
        if (hwnd == 0):
            self.log("can't find Mumu window")
            return
        else:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            self.to("exitmumu_confirm", "exitmumu_confirm")
        # self.to("exitmumu","exitmumu_confirm")
        # self.to("exitmumu_confirm","exitmumu_confirm")

    def exitArknights(self):
        self.foucusOnTheWindow()
        self.to("exitarknights", "exitarknights")

    # def mumuInit(self):
    #     errormsg = "error happened while starting Mumu"
    #     if(win32gui.FindWindow(None, "MuMu模拟器") == 0):
    #         win32api.ShellExecute(0, 'open', self.path,'', '', 1)
    #         while(self.foucusOnTheWindow()==False):self.delay(1)
    #         self.log("waiting for mumu being ready",end="")
    #     cnt=0
    #     while True:
    #         if(cnt>=120):
    #             self.log(errormsg)
    #             raise ArknightsErr(errormsg)
    #         cnt+=1
    #         self.log(".",end="")
    #         if(self.getTag("maximizemumu")!=None):
    #             self.to("maximizemumu","maximizemumu",timeoutfortarget=120)
    #             break
    #         if(self.getTag("minimizemumu")!=None):
    #             break
    #     self.log("start operating")
    #     cnt = 0
    #     while True:
    #         if(cnt>=120):
    #             self.log(errormsg)
    #             raise ArknightsErr(errormsg)
    #         cnt+=1
    #         if(self.getTag("close_advertisement")):
    #             self.to("close_advertisement","close_advertisement")
    #         if(self.getTag("arknight_launcher")):
    #             self.to("arknight_launcher","arknight_launcher")
    #             break
    #     self.to("login_start","login_start",timeoutforname=120)
    #     cnt=0
    #     while True:
    #         if(cnt>=120):
    #             self.log(errormsg)
    #             raise ArknightsErr(errormsg)
    #         cnt+=1
    #         if(self.getTag("login_kaishihuanxing")!=None):
    #             self.to("login_kaishihuanxing","login_kaishihuanxing",timeoutfortarget=60)
    #             cnt_sub1 = 0
    #             while True:
    #                 if (cnt_sub1 >= 60):
    #                     self.log(errormsg)
    #                     raise ArknightsErr(errormsg)
    #                 cnt_sub1 += 1
    #                 if(self.getTag("login_arknights")==None):break
    #             if (self.getTag("login_relogconfirm") != None):
    #                 self.to("login_relogconfirm", "login_relogconfirm")
    #                 self.to("login_zhanghaodenglu", "login_zhanghaodenglu")
    #                 self.to("login_focuspassword")
    #                 win32api.LoadKeyboardLayout('00000401', 1)#change keyboard layout
    #                 self.delay(3)
    #                 self.typeStr(self.password)
    #                 self.to("login_denglu", "login_denglu", timeoutfortarget=60)
    #             break
    #         if(self.getTag("login_zhanghaodenglu")!=None):
    #             self.to("login_zhanghaodenglu","login_zhanghaodenglu")
    #             self.to("login_focuspassword")
    #             self.delay(3)
    #             self.typeStr(self.password)
    #             self.to("login_denglu","login_denglu",timeoutfortarget=60)
    #             break
    #     cnt=0
    #     while True:
    #         if(cnt>=180):
    #             self.log(errormsg)
    #             raise ArknightsErr(errormsg)
    #         cnt+=1
    #         if(self.getTag("zuozhan")!=None):
    #             self.delay(3)
    #             if(self.getTag("zuozhan")!=None):
    #                 break
    #         if(self.getTag("close_message")!=None):
    #             self.to("close_message",israiseErr=False)
    #         if (self.getTag("confirm") != None):
    #             self.to("confirm",israiseErr=False)
    #     self.log("login successfully")

    def mumuInit(self):
        errormsg = "error happened while starting Mumu"
        if (win32gui.FindWindow(None, "MuMu模拟器") == 0):
            win32api.ShellExecute(0, 'open', self.path, '', '', 1)
            while (self.foucusOnTheWindow() == False): self.delay(1)
            self.log("waiting for mumu being ready", end="")
        cnt = 0
        while True:
            if (cnt >= 120):
                self.log(errormsg)
                raise ArknightsErr(errormsg)
            cnt += 1
            self.log(".", end="")
            if (self.getTag("maximizemumu") != None):
                self.to("maximizemumu", "maximizemumu", timeoutfortarget=120)
                break
            if (self.getTag("minimizemumu") != None):
                break
        self.log("start operating")
        cnt = 0
        while True:
            if (cnt >= 120):
                self.log(errormsg)
                raise ArknightsErr(errormsg)
            cnt += 1
            if (self.getTag("close_advertisement")):
                self.to("close_advertisement", "close_advertisement")
            if (self.getTag("arknight_launcher")):
                self.to("arknight_launcher", "arknight_launcher")
                break
        self.to("login_start", "login_start", timeoutforname=120)
        cnt = 0
        while True:
            if (cnt >= 120):
                self.log(errormsg)
                raise ArknightsErr(errormsg)
            cnt += 1
            if (self.getTag("zhanghaoguanli") != None):
                self.to('zhanghaoguanli','zhanghaoguanli')
            if (self.getTag("login_zhanghaodenglu") != None):
                self.to("login_zhanghaodenglu", "login_zhanghaodenglu")
                auto.click(1043, 602)  # click account bar
                self.delay(2)
                self.typeStr('backspace')   # clear account
                self.typeStr(self.email)
                self.typeStr('enter')  # confirm
                self.to("login_focuspassword")
                self.delay(2)
                self.typeStr(self.password)
                self.typeStr('enter')  # confirm
                self.to("login_denglu", "login_denglu", timeoutfortarget=60)
                break
        cnt = 0
        while True:
            if (cnt >= 180):
                self.log(errormsg)
                raise ArknightsErr(errormsg)
            cnt += 1
            if (self.getTag("zuozhan") != None):
                self.delay(3)
                if (self.getTag("zuozhan") != None):
                    break
            if (self.getTag("close_message") != None):
                self.to("close_message", israiseErr=False)
            if (self.getTag("confirm") != None):
                self.to("confirm", israiseErr=False)
        self.log("login successfully")

    def zhuxian(self, part, level, times):
        self.foucusOnTheWindow()
        self.backToMenu()
        self.to("zuozhan", "zhuxian")
        self.to("zhuxian")
        self.findTag(part)
        self.to(part)
        self.findTag(level)
        cnt = 0
        while True:
            cnt += 1
            self.to(level, "kaishixingdong")
            if (self.getTag("dailizhihui_ON") == None):
                self.to("dailizhihui_OFF", "dailizhihui_ON")
            self.to("kaishixingdong")
            if (self.getTag("lizhihaojin") != None):
                self.to("lizhihaojin", "lizhihaojin")
                self.log("run out of itellect")
                return
            self.to("kaishixingdong_1", "kaishixingdong_1")
            self.log("round " + str(cnt) + " begins")
            if (self.onMission(5) == True):
                self.log("round " + str(cnt) + " finished")
            else:
                self.log("mission failed, try again")
                cnt -= 1
            if (cnt >= times):
                self.log("mission complete")
                return
            else:
                self.to("back")

    def wuzichoubei(self, part, level, times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan", "wuzichoubei")
        self.to("wuzichoubei")
        self.delay(2)
        while (self.getTag(part) == None):
            if (cnt > 5):
                self.log("the part is not open today")
                return
            self.drag(xdistance=-500, speed=500)
            cnt += 1
        cnt = 0
        self.to(part, level)
        while True:
            cnt += 1
            self.to(level, "kaishixingdong")
            if (self.getTag("dailizhihui_ON") == None):
                self.to("dailizhihui_OFF", "dailizhihui_ON")
            self.to("kaishixingdong")
            if (self.getTag("lizhihaojin") != None):
                self.to("lizhihaojin", "lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1", "kaishixingdong_1")
            self.log("round " + str(cnt) + " begins")
            if (self.onMission(5) == True):
                self.log("round " + str(cnt) + " finished")
            else:
                self.log("mission failed, try again")
                cnt -= 1
            if (cnt >= times):
                self.log("mission complete")
                return
            else:
                self.to("back")

    def xinpiansousuo(self, part, level, times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan", "xinpiansousuo")
        self.to("xinpiansousuo", part)
        self.to(part, level)
        while True:
            cnt += 1
            self.to(level, "kaishixingdong")
            if (self.getTag("dailizhihui_ON") == None):
                self.to("dailizhihui_OFF", "dailizhihui_ON")
            self.to("kaishixingdong")
            if (self.getTag("lizhihaojin") != None):
                self.to("lizhihaojin", "lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1", "kaishixingdong_1")
            self.log("round " + str(cnt) + " begins")
            if (self.onMission(5) == True):
                self.log("round " + str(cnt) + " finished")
            else:
                self.log("mission failed, try again")
                cnt -= 1
            if (cnt >= times):
                self.log("mission complete")
                return
            else:
                self.to("back")

    def jiaomiemoshi(self, part, times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan", "jiaomiezuozhan")
        self.to("jiaomiezuozhan")
        self.findTag('yanguolongmen')
        self.to('yanguolongmen')
        cnt = 0
        while True:
            cnt += 1
            self.to(part, "kaishixingdong")
            if (self.getTag("dailizhihui_ON") == None):
                self.to("dailizhihui_OFF", "dailizhihui_ON")
            self.to("kaishixingdong")
            if (self.getTag("lizhihaojin") != None):
                self.to("lizhihaojin", "lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1", "kaishixingdong_1")
            self.log("round " + str(cnt) + " begins")
            if (self.onMission(5) == True):
                self.log("round " + str(cnt) + " finished")
            else:
                self.log("mission failed, try again")
                cnt -= 1
            if (cnt >= times):
                self.log("mission complete")
                return
            else:
                self.to("back")

    def activityCheckpoint(self, activityname, part, level, times):  # 活动关卡
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan", activityname)
        self.to(activityname, activityname)
        self.delay(2)
        while (self.getTag(part) == None):
            if (cnt > 5):
                self.log("the part is not open today")
                return
            self.drag(xdistance=-500, speed=500)
            cnt += 1
        cnt = 0
        self.to(part, part)
        self.getTag(level)
        cnt = 0
        while True:
            cnt += 1
            self.to(level)
            if (self.getTag("dailizhihui_ON") == None):
                self.to("dailizhihui_OFF", "dailizhihui_ON")
            try:
                self.to("kaishixingdong")
            except:
                self.to("kaishixingdong_activity")
            if (self.getTag("lizhihaojin") != None):
                self.to("lizhihaojin", "lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1", "kaishixingdong_1")
            self.log("round " + str(cnt) + " begins")
            if (self.onMission(5) == True):
                self.log("round " + str(cnt) + " finished")
            else:
                self.log("mission failed, try again")
                cnt -= 1
            if (cnt >= times):
                self.log("mission complete")
                return
            else:
                self.to("back")

    def generateMaterialList(self):
        self.foucusOnTheWindow()
        loc1 = r"output\\wordsImgs\\MaterialName.jpg"
        loc2 = r"output\\wordsImgs\\MatrerialNumber.jpg"
        outputloc = r"output\\MaterialList.txt"
        file = open(outputloc, "w+", encoding="utf-8")
        list = []

        def back():
            auto.click(1498, 164)

        def drag():
            self.drag(xstart=1706, ystart=403, speed=250, xdistance=-240, ydistance=0)

        def getInfo(x, y):
            auto.click(x, y)
            self.delay(1)
            auto.screenshot(region=(424, 262, 672 - 424, 307 - 262)).save(loc1)
            auto.screenshot(region=(1352, 262, 1499 - 1352, 307 - 262)).save(loc2)
            try:
                name = baiduOCR(loc1, self.APP_ID, self.API_KEY, self.SECRECT_KEY)
            except:
                print("can't parse material's name")
                back()
                return True
            if (name.find("技巧概要") != -1 or name.find("芯片助剂") != -1 or name.find("芯片") != -1 or name.find("信物") != -1):
                print("finding completes")
                back()
                return False
            if (name.find("作战记录") != -1):
                back()
                return True
            try:
                number = baiduOCR(loc2, self.APP_ID, self.API_KEY, self.SECRECT_KEY)
            except:
                print("can't parse material's number")
                back()
                return True
            list.append({"name": name, "need": 0, "have": int(number)})
            back()
            return True

        def writeToTable(s):
            file.write(s)
            file.close()

        def convertList(list):
            s = str(list)
            s = s.replace("'", "\"")
            s = s.replace(" ", "")
            return s

        x = 1712
        y = 283
        self.backToMenu()
        self.to("cangku", "cangku")
        self.to("yangchengcailiao")
        self.delay(1)
        for i in range(0, 8):
            for j in range(0, 3):
                getInfo(x - i * 200, y + j * 250)
                self.delay(0.5)
        while True:
            drag()
            self.delay(1)
            for j in range(0, 3):
                if (getInfo(x, y + j * 250) == False):
                    res = convertList(list)
                    writeToTable(res)
                    return res
                self.delay(0.5)

    def getIntellect(self):
        self.foucusOnTheWindow()
        self.backToMenu()
        loc = r"output\\wordsImgs\\Intellect.jpg"
        auto.screenshot(region=(1118, 210, 1278 - 1118, 310 - 210)).save(loc)
        interllect = baiduOCR(loc, self.APP_ID, self.API_KEY, self.SECRECT_KEY)
        print(interllect)
        return interllect

    def getScreenShot(self):
        loc = r"output\\screenshot\\screenshot.jpg"
        auto.screenshot().save(loc)


if __name__ == "__main__":
    # win32api.LoadKeyboardLayout('00000409', 1)
    ark = Arknights()
    # ark.foucusOnTheWindow()
    #     # ark.generateMaterialList()
    # print(ark.getIntellect())
    # Ark.drag(xdistance=300,speed=500)
    # Ark.zhuxian("ercihuxi","S3-3",1)
    # Ark.mumuInit()
    # Ark.wuzichoubei("huowuyunsong","CE-5",4)
    # jiaomiemoshi("longmenwaihuan",1)
    # xinpiansousuo("shenxianshizu","PR-D-1",4)

    # ark.log('kkkkkkk')
    # ark.getTag('1-7')

    # hwnd_title = dict()
    #
    #
    # def get_all_hwnd(hwnd, mouse):
    #     if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
    #         hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    #
    #
    # win32gui.EnumWindows(get_all_hwnd, 0)
    #
    # for h, t in hwnd_title.items():
    #     if t is not "":
    #         print(h, t)
    # pass

    # for process in psutil.process_iter():
    #     try:
    #         # get the memory usage in bytes
    #         memory_usage = process.memory_full_info().uss
    #     except psutil.AccessDenied:
    #         memory_usage = 0
    #     print(process.name()+process.status()+str(memory_usage))

    # ark.generateMaterialList()
