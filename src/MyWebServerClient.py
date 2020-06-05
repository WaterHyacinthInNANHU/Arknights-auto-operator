import inspect
import ctypes
from websocket import create_connection,WebSocketTimeoutException,WebSocketConnectionClosedException
import threading
import time
import queue
class MyWebServerClient(object):
    def __init__(self,url,email,password,role,pingtime,onmessage):
        self.ws_recieve = None
        self.ws_send = None
        self.ws_recieve_lock = threading.Lock()
        self.ws_send_lock = threading.Lock()
        self.url=url
        self.email = email
        self.password=password
        self.role=role
        self.queue = queue.Queue(100)
        self.work = onmessage
        self.pingtime = pingtime
        self.workstate = []

    def send(self,message):
        s = '{"type":"data","data":"' + message + '"}'
        # print(s)
        self.ws_send_lock.acquire()
        try:
            self.ws_send.send(s)##发送消息
        except:
            pass
        self.ws_send_lock.release()


    def recieve(self):
        while True:
            self.ws_recieve_lock.acquire()
            try:
                res = self.ws_recieve.recv()
            except:
                res = None
            self.ws_recieve_lock.release()
            print('',end='')
            if(res != None):
                print('message='+res)
                if(res == 'workstate'):
                    if(self.workstate == []):
                        word = '空闲中，等待命令'
                    else:
                        word = self.workstate[-1]
                    s = '{"type":"data","data":"' + str(word) + '"}'
                    self.ws_recieve.send(s)
                elif(res == 'workstatehistory'):
                    if(self.workstate == []):
                        word = '空闲中，等待命令'
                        s = '{"type":"data","data":"'+'运行日志：' + str(word).replace('"','\'') + '"}'
                        self.ws_recieve.send(s)
                    else:
                        s = '{"type":"data","data":"'+'运行日志：' + str(self.workstate).replace('"','\'') + '"}'
                        self.ws_recieve.send(s)
                    print(s)
                else:
                    if(self.queue.empty()):
                        word = '收到，即将开始执行命令'
                        s = '{"type":"data","data":"' + str(word) + '"}'
                        self.ws_recieve.send(s)
                    else:
                        word = '收到，命令已进入队列并等待处理'
                        s = '{"type":"data","data":"' + str(word) + '"}'
                        self.ws_recieve.send(s)
                    self.queue.put(res)


    def onmessage(self):
        while True:
            data = self.queue.get()
            self.work(self,data,self.workstate)

    def ping(self):
        s = '{"type":"ping"}'
        while True:
            # print('ping')
            self.ws_send_lock.acquire()
            try:
                self.ws_send.send(s)
            except:
                while self.ws_send_Init() == False: pass
            self.ws_send_lock.release()

            self.ws_recieve_lock.acquire()
            try:
                self.ws_recieve.send(s)
            except:
                while self.ws_recieve_Init() == False: pass
            self.ws_recieve_lock.release()
            time.sleep(self.pingtime)


    def ws_recieve_Init(self):
        try:
            print('reciever:trying to reconnect to server...')
            loginmessage = '{"type":"login","email":"' + self.email + '","password":"' + self.password + '", "role":"' + self.role + '"}'
            #接收连接
            self.ws_recieve = create_connection(self.url)
            self.ws_recieve.settimeout(1)
            self.ws_recieve.send(loginmessage)
            print(self.ws_recieve.recv())#接收连接成功信息
            # print(self.ws_recieve.recv())#接收登入信息
            print('reciever:connection established')
        # except (ConnectionRefusedError,WebSocketConnectionClosedException,ConnectionResetError,TimeoutError):
        except:
            print('reciever:connecting failed')
            return False
        return True

    def ws_send_Init(self):
        try:
            print('sender:trying to reconnect to server...')
            loginmessage = '{"type":"login","email":"' + self.email + '","password":"' + self.password + '", "role":"' + self.role + '"}'
            #发送连接
            self.ws_send = create_connection(self.url)
            self.ws_send.send(loginmessage)
            print(self.ws_send.recv())#接收连接成功信息
            # print(self.ws_send.recv())#接收登入信息
            print('sender:connections established')
        # except (ConnectionRefusedError,WebSocketConnectionClosedException,ConnectionResetError,TimeoutError):
        except:
            print('sender:connecting failed')
            return False
        return True

    def run(self):
        while self.ws_recieve_Init() == False:pass
        while self.ws_send_Init() == False: pass
        self.send('已连接')
        threading.Thread(target=self.recieve, args=()).start()
        threading.Thread(target=self.onmessage, args=()).start()
        # ThreadWithExc(target=self.onmessage, args=()).start()#可以强行退出的进程
        threading.Thread(target=self.ping, args=()).start()


class ThreadShutException(Exception):
    def __init__(self,ErrorInfo='This thread has been shut down'):
        super().__init__(self)
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

class ThreadWithExc(threading.Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
    def _get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

    def raiseExc(self, exctype):
        def _async_raise(tid, exctype):
            '''Raises an exception in the threads with id tid'''
            if not inspect.isclass(exctype):
                raise TypeError("Only types can be raised (not instances)")
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                             ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # "if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                t.raiseExc( SomeException )
                time.sleep( 0.1 )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        _async_raise( self._get_my_tid(), exctype )

if __name__=='__main__':
    # def work(self,data):
    #     self.send(data)
    #     print(data)
    # mws = MyWebServerClient('ws://101.132.147.44:2000',None,None,'python',5,work)
    # mws.run()
    # ws = create_connection('')
    def a():
        while True:
            time.sleep(0.5)
        # print('running')
            print('l')
            pass
    t = ThreadWithExc(target=a,args=())
    t.start()
    print('sleep for 2s')
    time.sleep(2)
    print('kill time')
    print(t.is_alive())
    while t.isAlive():
        t.raiseExc(ThreadShutException)
        time.sleep(0.1)

    print(t.is_alive())
    while True:
        time.sleep(1)
        print('running')