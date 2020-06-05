import itchat
from arkOperator import Arknights
import re
import traceback
import os
def orderByInner(msg):
    global ark
    orderlist = ["zhuxian","getcailiao","getlog","flist","ilist","hi","screen"]
    try:
        if(msg.find('*') == -1):
            msg = msg+'*1'
        if(msg.find(orderlist[0])!=-1):
            pattern = re.compile(r'zhuxian(.*)')  # 用于匹配order
            level = pattern.match(msg).groups()[0]
            pattern = re.compile(r'S?(.*)-')
            chapter = pattern.match(level).groups()[0]
            pattern = re.compile(r'(.*)\*')
            section = pattern.match(level).groups()[0]
            pattern = re.compile(r'.*\*(.*)')
            times = pattern.match(level).groups()[0]
            order = 'ark.zhuxian(' + "\"" + "chapter" + chapter + "\"" + "," + "\"" + section + "\"" + "," + times + ')'
            itchat.send(u'Arkights operator:收到', 'filehelper')
            itchat.send(u'Arkights operator:将开始执行命令' + str(order), 'filehelper')
            exec(order, {'ark': ark, 'itchat': itchat})
            itchat.send(u'Arkights operator:执行完毕', 'filehelper')
        if(msg.find(orderlist[1])!=-1):
            itchat.send(u'Arkights operator:收到,打印材料清单', 'filehelper')
            outputloc = r"output\\MaterialList.txt"
            with open(outputloc, "r",encoding="utf-8") as file:
                itchat.send(file.read(), 'filehelper')
                itchat.send(u'Arkights operator:执行完毕', 'filehelper')
        if(msg.find(orderlist[2])!=-1):
            itchat.send(u'Arkights operator:收到,打印log信息', 'filehelper')
            outputloc = r"output\\log.txt"
            with open(outputloc, "r",encoding="utf-8") as file:
                itchat.send(file.read(), 'filehelper')
                itchat.send(u'Arkights operator:执行完毕', 'filehelper')
        if(msg.find(orderlist[3])!=-1):
            filelist = os.listdir("wechatOrders")
            itchat.send(u'Arkights operator:收到,所有命令文件如下', 'filehelper')
            for item in filelist:
                itchat.send(os.path.splitext(item)[0], 'filehelper')
        if(msg.find(orderlist[4])!=-1):
            itchat.send(u'Arkights operator:收到,所有内置命令如下', 'filehelper')
            for item in orderlist:
                itchat.send(str(item), 'filehelper')
        if(msg.find(orderlist[5])!=-1):
            itchat.send(u'Arkights operator:干啥', 'filehelper')
        if(msg.find(orderlist[6])!=-1):
            loc = r"output\\screenshot\\screenshot.jpg"
            itchat.send(u'Arkights operator:收到，截屏上传中', 'filehelper')
            ark.getScreenShot()
            mediaid = itchat.upload_file(loc,isPicture=True)['MediaId']
            itchat.send_image(loc,'filehelper',mediaid)

    except:
        itchat.send(traceback.format_exc(), 'filehelper')
def orderByFile(msg):
    global ark
    try:
        if(msg.find('*') == -1):
            msg = msg+'*1'
        itchat.send(u'Arkights operator:收到', 'filehelper')
        pattern = re.compile(r'(.*)\*')  # 用于匹配order
        order = pattern.match(msg).groups()[0]
        pattern = re.compile(r'.*\*(.*)')  # 匹配次数
        times = pattern.match(msg).groups()[0]
        itchat.send(u'Arkights operator:将开始执行'+str(times)+"次文件"+str(order), 'filehelper')
    except:
        itchat.send(u'Arkights operator:语法错误', 'filehelper')
        return
    try:
        for i in range(int(times)):
            execTXT(order)
            if(int(times)!=1):
                # itchat.send(u'第'+str(i+1)+"轮执行完毕", 'filehelper')
                print('round '+str(i+1)+" has completed")
        itchat.send(u'Arkights operator:全部执行完毕', 'filehelper')
    except FileNotFoundError or NotADirectoryError:
        itchat.send(u'Arkights operator:没有对应命令', 'filehelper')
    except:
        itchat.send(traceback.format_exc(), 'filehelper')
    pass
def orderByRaw(msg):
    global ark
    try:
        itchat.send(u'Arkights operator:收到', 'filehelper')
        itchat.send(u'Arkights operator:将开始执行命令' + str(msg), 'filehelper')
        exec(msg, {'ark': ark, 'itchat': itchat})
        itchat.send(u'Arkights operator:执行完毕', 'filehelper')
    except:
        itchat.send(traceback.format_exc(), 'filehelper')

def execTXT(order):
    global ark
    with open(r"wechatOrders\\"+order+".txt",mode='r') as file:
        for order in file.readlines():
            exec(order,{'ark': ark,'itchat': itchat})

@itchat.msg_register(itchat.content.TEXT)
def msgcallback(msg):
    str = msg['Text']
    pattern = re.compile(r'(.*):')
    type = pattern.match(str).groups()[0]
    pattern = re.compile(r'.*:(.*)')
    order = pattern.match(str).groups()[0]
    try:
        if(type == 'r'):
            orderByRaw(order)
        elif(type == 'f'):
            orderByFile(order)
        elif(type == 'i'):
            orderByInner(order)
        else:
            itchat.send(u'Arkights operator:请设置正确的命令类型', 'filehelper')
    except:
        itchat.send(traceback.format_exc(), 'filehelper')




def exitCallback():
    print("log out,relog")
    itchat.run()
    print("reloged")

if __name__ == "__main__":
    ark = Arknights()
    with open(r"userconfig/commonconfig.txt", mode='r') as file:
        for order in file.readlines():
            order = order.replace("\\", "\\\\")
            exec(order,{'ark': ark})
    print(ark.path)
    itchat.auto_login(exitCallback=exitCallback(),hotReload=True)
    itchat.send(u'Arkights operator:已连接', 'filehelper')
    itchat.run()