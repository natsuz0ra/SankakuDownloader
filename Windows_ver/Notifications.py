# -*- coding: utf-8 -*-
import requests,sys,os,json,websocket
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import *
from subprocess import call,PIPE,STDOUT

this_page_downloaded = 0

##监控下载消息
class Notifications(QThread):
    log_append = pyqtSignal(str)
    log_moveCursor = pyqtSignal()
    set_process = pyqtSignal(str,int)
    add_failed_info = pyqtSignal(str)

    def __init__(self,this_page_count,count):
        super(Notifications, self).__init__(None)
        self.this_page_count = this_page_count
        self.count = count

    def run(self):
        def on_message(ws, message):
            method = eval(message)['method']
            gid = eval(message)['params'][0]['gid']
            jsonreq = json.dumps({'jsonrpc':'2.0','id':'qwer','method':'aria2.tellStatus','params':['token:123654',gid]})
            
            ##下载成功或失败时打印log，失败后还会记录
            if method == 'aria2.onDownloadComplete':
                c = requests.post('http://localhost:7865/jsonrpc', data=jsonreq)
                file_name = eval(c.text)['result']['files'][0]['path'].split('/')[-1]
                self.log_append.emit('下载成功：%s' % file_name)
                self.log_moveCursor.emit()
            elif method == 'aria2.onDownloadError':
                c = requests.post('http://localhost:7865/jsonrpc', data=jsonreq)
                file_name = eval(c.text)['result']['files'][0]['uris'][0]['uri'].replace('\\','').split('/')[-1].split('?')[0]
                file_url = eval(c.text)['result']['files'][0]['uris'][0]['uri'].replace('\\','')
                self.add_failed_info.emit(file_url)
                self.log_append.emit('下载失败：%s' % file_name)
                self.log_moveCursor.emit()
            else:
                return
            global this_page_downloaded
            this_page_downloaded += 1
            self.set_process.emit('+1',self.count)

            if this_page_downloaded == self.this_page_count:#如果当页下载完毕则关闭aria2
                call('taskkill /f /im aria2c_sd.exe',shell=True,stdin=PIPE,stdout=PIPE,stderr=STDOUT)
                this_page_downloaded = 0
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://127.0.0.1:7865/jsonrpc",on_message=on_message)
        ws.run_forever()

    def stop(self):
        global this_page_downloaded
        this_page_downloaded = 0
