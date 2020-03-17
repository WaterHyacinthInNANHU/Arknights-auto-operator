import pyautogui as auto
import time
from getWords import baiduOCR
import win32gui,win32api
class Arknights():
    def __init__(self,password='',APP_ID='',API_KEY='',SECRECT_KEY='',path=''):
        self.logfilepath = "output\\log.txt"
        self.log("Welcome back, doctor!")
        self.password = password
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRECT_KEY = SECRECT_KEY
        self.path = path
    def log(self,str,end="\n"):
        with open(self.logfilepath,"w+") as file:
            file.write(str+end)
            print(str+end)

    def delay(self,t):
        time.sleep(t)

    def getTag(self,name,confidence=0.9):
        return auto.locateCenterOnScreen("imgs\\"+name+".jpg",grayscale=False,confidence=confidence)

    def click(self,pos):
        auto.click(pos.x, pos.y)
        self.delay(1.5)

    def typeStr(self,str):
        for char in str:
            auto.keyDown(char)
            auto.keyUp(char)

    def drag(self,xstart = 1020,ystart = 160,xdistance=0,ydistance=0,speed=250):
        auto.moveTo(xstart, ystart)  # move mouse to the start position
        auto.dragTo(xstart+xdistance,ystart+ydistance, button='left',duration=pow(pow(xdistance,2)+pow(ydistance,2),0.5)/speed)  # drag
        auto.click(xstart+xdistance,ystart+ydistance)
        self.delay(0.5)

    def to(self,name,targetname=None,timeoutforname=10,timeoutfortarget=10):
        self.log("name:"+str(name)+" targetname:"+str(targetname)+'\n')
        cnt = 0
        while True:
            cnt+=1
            pos = self.getTag(name)
            if(pos != None):break
            self.delay(1)
            if(cnt>=timeoutforname):
                self.log("can't find : "+name)
                return False
        cnt = 0
        while True:
            cnt+=1
            self.click(pos)
            self.delay(1)
            if(targetname == None):break
            elif(targetname == name):
                if (self.getTag(name) == None): break
            else:
                if(self.getTag(targetname) != None):break
            if(cnt>=timeoutfortarget):
                self.log("no reaction by pressing : " + name)
                return False
        return True

    def backToMenu(self):
        self.foucusOnTheWindow()
        if (self.getTag("maximizemumu") != None):
            self.to("maximizemumu", "maximizemumu", timeoutfortarget=120)
        if (self.getTag("zuozhan") == None):
            self.to("navigator","navigator_shouye")
            self.to("navigator_shouye","navigator_shouye")

    def onMission(self,scantime):#等待任务结束，scantime扫描间隔
        self.log("running",end='')
        while True:
            self.log(".", end=' ')
            self.delay(scantime)
            self.foucusOnTheWindow()
            if (self.getTag("xingdongjieshu") != None):
                self.to("xingdongjieshu", "xingdongjieshu")
                return
            if (self.getTag("dengjitisheng") != None):
                self.to("dengjitisheng", "dengjitisheng")
                self.to("xingdongjieshu", "xingdongjieshu")
                return
            if (self.getTag("zuozhanjianbao") != None):
                self.to("zuozhanjianbao", "zuozhanjianbao")
                self.to("meizhoubaochoujindu", "meizhoubaochoujindu")
                return

    def forTest(self):
        self.log("Arknight test")

    def foucusOnTheWindow(self):
        hwnd = win32gui.FindWindow(None, "MuMu模拟器")
        if(hwnd == 0):
            self.log("can't find Mumu window")
            return False
        win32gui.SetForegroundWindow(hwnd)
        return True
    def exitMumu(self):
        self.foucusOnTheWindow()
        self.to("exitmumu","exitmumu_confirm")
        self.to("exitmumu_confirm","exitmumu_confirm")

    def exitArknights(self):
        self.foucusOnTheWindow()
        self.to("exitarknights", "exitarknights")

    def mumuInit(self):
        win32api.ShellExecute(0, 'open', self.path,'', '', 1)
        while(self.foucusOnTheWindow()==False):self.delay(1)
        self.log("waiting for mumu being ready",end="")
        while True:
            self.log(".",end="")
            if(self.getTag("maximizemumu")!=None):
                self.to("maximizemumu","maximizemumu",timeoutfortarget=120)
                break
            if(self.getTag("minimizemumu")!=None):
                break
        self.log("start operating")
        self.to("arknight_launcher","arknight_launcher",timeoutforname=120,timeoutfortarget=30)
        self.to("login_start","login_start",timeoutforname=120)
        while True:
            if(self.getTag("login_kaishihuanxing")!=None):
                self.to("login_kaishihuanxing","login_kaishihuanxing",timeoutfortarget=60)
                while True:
                    if(self.getTag("login_arknights")==None):break
                if (self.getTag("login_relogconfirm") != None):
                    self.to("login_relogconfirm", "login_relogconfirm")
                    self.to("login_zhanghaodenglu", "login_zhanghaodenglu")
                    self.to("login_focuspassword")
                    self.delay(3)
                    self.typeStr(self.password)
                    self.to("login_denglu", "login_denglu", timeoutfortarget=60)
                break
            if(self.getTag("login_zhanghaodenglu")!=None):
                self.to("login_zhanghaodenglu","login_zhanghaodenglu")
                self.to("login_focuspassword")
                self.delay(3)
                self.typeStr(self.password)
                self.to("login_denglu","login_denglu",timeoutfortarget=60)
                break
        while True:
            if(self.getTag("zuozhan")!=None):
                self.delay(3)
                if(self.getTag("zuozhan")!=None):
                    break
            if(self.getTag("close_message")!=None):
                self.to("close_message","close_message")
                break
        self.log("login successfully")

    def zhuxian(self,part,level,times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan","zhuxian")
        self.to("zhuxian")
        while True:#find part
            if(cnt>=20):
                break
            cnt+=1
            if(self.getTag(part)==None):
                self.drag(xdistance=500,speed=500)
            else:
                self.to(part,part)
                break
        if(cnt>=20):
            cnt=0
            while True:  # find part
                if (cnt >= 20):
                    return
                cnt += 1
                if (self.getTag(part) == None):
                    self.drag(xdistance=-500, speed=500)
                else:
                    self.to(part, part)
                    break
        cnt=0
        while True:#find level
            if(cnt>=20):
                break
            cnt+=1
            if(self.getTag(level)==None):
                self.drag(xdistance=-500,speed=500)
            else:
                break
        if(cnt>=20):
            cnt=0
            while True:  # find level
                if (cnt >= 20):
                    return
                cnt += 1
                if (self.getTag(level) == None):
                    self.drag(xdistance=500, speed=500)
                else:
                    break
        cnt=0
        while True:
            cnt += 1
            self.to(level,"kaishixingdong")
            if(self.getTag("dailizhihui_ON")==None):
                self.to("dailizhihui_OFF","dailizhihui_ON")
            self.to("kaishixingdong","kaishixingdong")
            if(self.getTag("lizhihaojin")!=None):
                self.to("lizhihaojin","lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1","kaishixingdong_1")
            self.log("round "+str(cnt)+" begins")
            self.onMission(5)
            self.log("round " + str(cnt) + " finished")
            if(cnt >= times):
                self.log("mission complete")
                return

    def wuzichoubei(self,part,level,times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan","wuzichoubei")
        self.to("wuzichoubei",part)
        self.to(part,level)
        while True:
            cnt += 1
            self.to(level,"kaishixingdong")
            if(self.getTag("dailizhihui_ON")==None):
                self.to("dailizhihui_OFF","dailizhihui_ON")
            self.to("kaishixingdong","kaishixingdong")
            if(self.getTag("lizhihaojin")!=None):
                self.to("lizhihaojin","lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1","kaishixingdong_1")
            self.log("round "+str(cnt)+" begins")
            self.onMission(5)
            self.log("round " + str(cnt) + " finished")
            if(cnt >= times):
                self.log("mission complete")
                return

    def xinpiansousuo(self,part,level,times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan","xinpiansousuo")
        self.to("xinpiansousuo",part)
        self.to(part,level)
        while True:
            cnt += 1
            self.to(level,"kaishixingdong")
            if(self.getTag("dailizhihui_ON")==None):
                self.to("dailizhihui_OFF","dailizhihui_ON")
            self.to("kaishixingdong","kaishixingdong")
            if(self.getTag("lizhihaojin")!=None):
                self.to("lizhihaojin","lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1","kaishixingdong_1")
            self.log("round "+str(cnt)+" begins")
            self.onMission(5)
            self.log("round " + str(cnt) + " finished")
            if(cnt >= times):
                self.log("mission complete")
                return

    def jiaomiemoshi(self,part,times):
        self.foucusOnTheWindow()
        cnt = 0
        self.backToMenu()
        self.to("zuozhan","jiaomiezuozhan")
        self.to("jiaomiezuozhan",part)
        while True:
            cnt += 1
            self.to(part,"kaishixingdong")
            if(self.getTag("dailizhihui_ON")==None):
                self.to("dailizhihui_OFF","dailizhihui_ON")
            self.to("kaishixingdong","kaishixingdong")
            if(self.getTag("lizhihaojin")!=None):
                self.to("lizhihaojin","lizhihaojin")
                self.log("run out of itellect")
                # sys.exit()
                return
            self.to("kaishixingdong_1","kaishixingdong_1")
            self.log("round "+str(cnt)+" begins")
            self.onMission(5)
            self.log("round " + str(cnt) + " finished")
            if(cnt >= times):
                self.log("mission complete")
                return

    def generateMaterialList(self):
        self.foucusOnTheWindow()
        loc1 = r"imgs\\wordsImgs\\MaterialName.jpg"
        loc2 = r"imgs\\wordsImgs\\MatrerialNumber.jpg"
        outputloc = r"output\\MaterialList.txt"
        file = open(outputloc, "w+",encoding="utf-8")
        list = []
        def back():
            auto.click(1498,164)
        def drag():
            self.drag(xstart=1706, ystart=403, speed=500, xdistance=-240, ydistance=0)
        def getInfo(x,y):
            auto.click(x,y)
            self.delay(1)
            auto.screenshot(region=(424, 262, 672 - 424, 307 - 262)).save(loc1)
            auto.screenshot(region=(1352, 262, 1499 - 1352, 307 - 262)).save(loc2)
            name = baiduOCR(loc1,self.APP_ID,self.API_KEY,self.SECRECT_KEY)
            if(name.find("技巧概要")!=-1 or name.find("芯片助剂")!=-1 or name.find("芯片")!=-1 or name.find("信物")!=-1):
                print("finding completes")
                back()
                return False
            if(name.find("作战记录")!=-1):
                back()
                return True
            number = baiduOCR(loc2,self.APP_ID,self.API_KEY,self.SECRECT_KEY)
            list.append({"name":name,"need":0,"have":int(number)})
            back()
            return True
        def writeToTable(s):
            file.write(s)
            file.close()
        def convertList(list):
            s = str(list)
            s = s.replace("'","\"")
            s = s.replace(" ","")
            return s
        x = 1712
        y = 283
        self.backToMenu()
        self.to("cangku","cangku")
        self.to("yangchengcailiao")
        self.delay(1)
        for i in range(0,8):
            for j in range(0,3):
                getInfo(x-i*200,y+j*250)
                self.delay(0.5)
        while True:
            drag()
            self.delay(1)
            for j in range(0,3):
                if(getInfo(x, y + j * 250) == False):
                    res = convertList(list)
                    writeToTable(res)
                    return res
                self.delay(0.5)

    def getIntellect(self):
        self.foucusOnTheWindow()
        self.backToMenu()
        loc = r"imgs\\wordsImgs\\Intellect.jpg"
        auto.screenshot(region=(1118, 210, 1278 - 1118, 310 - 210)).save(loc)
        interllect = baiduOCR(loc, self.APP_ID, self.API_KEY, self.SECRECT_KEY)
        print(interllect)
        return interllect

if __name__ == "__main__":
    ark = Arknights()
    # ark.foucusOnTheWindow()
    #     # ark.generateMaterialList()
    print(ark.getIntellect())
    # Ark.drag(xdistance=300,speed=500)
    # Ark.zhuxian("ercihuxi","S3-3",1)
    # Ark.mumuInit()
    # Ark.wuzichoubei("huowuyunsong","CE-5",4)
    # jiaomiemoshi("longmenwaihuan",1)
    # xinpiansousuo("shenxianshizu","PR-D-1",4)

    pass
