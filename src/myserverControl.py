from websocket import create_connection
import threading
import time
from arkOperator import Arknights
import re
import traceback
import os
import queue
from MyWebServerClient import MyWebServerClient

class Arknights_Myserver(object):
    def __init__(self):
        self.ws = MyWebServerClient('ws://101.132.147.44:2000', None, None, 'python', 5, self.onmessage)
        self.ark = Arknights()
        # 配置文件写入
        with open(r"userconfig/commonconfig.txt", mode='r') as file:
            for order in file.readlines():
                order = order.replace("\\", "\\\\")
                exec(order, {'ark': self.ark, 'ws': self.ws})
        with open(r"userconfig/myserverconfig.txt", mode='r') as file:
            for order in file.readlines():
                order = order.replace("\\", "\\\\")
                exec(order, {'ark': self.ark, 'ws': self.ws})
    # 逻辑部分
    def orderByInner(self,ws,msg,workstate):
        orderlist = ["getcailiao","getlog","flist","ilist","hi"]
        try:
            if(msg.find('*') == -1):
                msg = msg+'*1'
            if(msg.find(orderlist[0])!=-1):
                self.send(ws,'message',u'Arkights operator:收到,打印材料清单')
                outputloc = r"output\\MaterialList.txt"
                with open(outputloc, "r",encoding="utf-8") as file:
                    self.send(ws,'material',file.read().replace('"','\''))
                    self.send(ws,'message',u'Arkights operator:执行完毕')
            if(msg.find(orderlist[1])!=-1):
                self.send(ws,'message',u'Arkights operator:收到,打印程序log信息')
                outputloc = r"output\\log.txt"
                with open(outputloc, "r",encoding="utf-8") as file:
                    self.send(ws,'message',file.read())
                    self.send(ws,'message',u'Arkights operator:执行完毕')
            if(msg.find(orderlist[2])!=-1):
                filelist = os.listdir("myserverOrders")
                self.send(ws,'message',u'Arkights operator:收到,所有命令文件如下')
                for item in filelist:
                    self.send(ws,'message',os.path.splitext(item)[0])
            if(msg.find(orderlist[3])!=-1):
                self.send(ws,'message',u'Arkights operator:收到,所有内置命令如下')
                for item in orderlist:
                    self.send(ws,'message',str(item))
            if(msg.find(orderlist[4])!=-1):
                self.send(ws,'message',u'Arkights operator:在')
            # if(msg.find(orderlist[5])!=-1):
            #     loc = r"imgs\\screenshot\\screenshot.jpg"
            #     self.send(ws,'message',u'Arkights operator:收到，截屏上传中')
            #     ws.ark.getScreenShot()
            #     mediaid = ws.upload_file(loc,isPicture=True)['MediaId']
            #     ws.send_image(loc,'filehelper',mediaid)
        except:
            self.send(ws,'message',traceback.format_exc())
            workstate += ['执行过程中发生错误']
            self.send(ws,'message',u'Arkights Operator:执行过程中发生错误')

    def orderByFile(self,ws,msg,workstate):
        try:
            if(msg.find('*') == -1):
                msg = msg+'*1'
            self.send(ws,'message',u'Arkights operator:收到')
            pattern = re.compile(r'(.*)\*')  # 用于匹配order
            order = pattern.match(msg).groups()[0]
            pattern = re.compile(r'.*\*(.*)')  # 匹配次数
            times = pattern.match(msg).groups()[0]
            self.send(ws,'message',u'Arkights operator:将开始执行'+str(times)+"次文件"+str(order))
        except:
            workstate += ['执行过程中发生错误']
            self.send(ws,'message',u'Arkights operator:语法错误')
            return
        try:
            for i in range(int(times)):
                self.execTXT(ws,order)
                if(int(times)!=1):
                    # itchat.send(u'第'+str(i+1)+"轮执行完毕")
                    print('round '+str(i+1)+" has completed")
            self.send(ws,'message',u'Arkights operator:全部执行完毕')
        except FileNotFoundError or NotADirectoryError:
            workstate += ['执行过程中发生错误']
            self.send(ws,'message',u'Arkights operator:没有对应命令')
        except:
            # self.send(ws,'message',traceback.format_exc())
            workstate += ['执行过程中发生错误']
            self.send(ws,'message',u'Arkights Operator:执行过程中发生错误')

    def execTXT(self,ws,order):
        with open(r"myserverOrders\\"+order+".txt",mode='r') as file:
            for order in file.readlines():
                exec(order,{'ark': self.ark,'ws': ws})

    def orderByRaw(self,ws,msg,workstate):
        try:
            self.send(ws,'message',u'Arkights Operator:开始执行命令' + str(msg))
            exec(msg, {'ark': self.ark, 'ws': ws})
            self.send(ws,'message',u'Arkights Operator:执行完毕')
        except:
            workstate += ['执行过程中发生错误']
            self.send(ws,'message',u'Arkights Operator:执行过程中发生错误')

    def onmessage(self,ws,data,workstate):
        invalid_list = ['invalid message','None']
        for item in invalid_list:
            if(item==str(data)):
                return
        workstate += ['正在执行：'+data]
        try:
            pattern = re.compile(r'(.*):')
            type = pattern.match(data).groups()[0]
            pattern = re.compile(r'.*:(.*)')
            order = pattern.match(data).groups()[0]
        except:
            self.send(ws,'message',u'Arkights operator:请输入正确的命令格式')
            workstate += ['请输入正确的命令格式']
            return
        try:
            if(type == 'r'):
                self.orderByRaw(ws,order,workstate)
            elif(type == 'f'):
                self.orderByFile(ws,order,workstate)
            elif(type == 'i'):
                self.orderByInner(ws,order,workstate)
            else:
                self.send(ws,'message',u'Arkights operator:请设置正确的命令类型')
                workstate += ['请设置正确的命令类型']
        except:
            # self.send(ws,'message',traceback.format_exc())
            workstate += ['执行过程中发生错误']
        workstate += ['空闲中，等待命令']

    def send(self,ws,type,data):
        ws.send(str(type)+'&&&'+data)

    def run(self):
        self.ws.run()

if __name__ == '__main__':
    Arknights_Myserver = Arknights_Myserver()
    Arknights_Myserver.run()
