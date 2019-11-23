# -*- coding: utf-8 -*-
import requests,json,sys,os,time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import *
from subprocess import call,PIPE,STDOUT

##终止下载
class Stop(QThread):
    log_append = pyqtSignal(str)
    log_moveCursor = pyqtSignal()
    enable_start_button = pyqtSignal()
    disable_stop_button = pyqtSignal()
    set_startbutton_text = pyqtSignal(str)
    stop_worker = pyqtSignal()

    def __init__(self,now_page):
        super(Stop, self).__init__(None)
        self.now_page = now_page

    def run(self):
        call('taskkill /f /im aria2c_sd.exe',shell=True,stdin=PIPE,stdout=PIPE,stderr=STDOUT)
        self.stop_worker.emit()
        self.set_startbutton_text.emit('开始')
        self.enable_start_button.emit()
        self.disable_stop_button.emit()
        self.log_append.emit('已停止下载，你可以从第%d页重新开始' % self.now_page)
        self.log_moveCursor.emit()
