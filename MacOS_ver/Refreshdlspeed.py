# -*- coding: utf-8 -*-
import requests,json,sys,os,time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import *

##刷新下载速度
class Refreshdlspeed(QThread):
    set_speedlabel = pyqtSignal(str)

    def __init__(self):
        super(Refreshdlspeed, self).__init__(None)

    def run(self):
        def bytes_conversion(number):
            symbols = ('K','M','G','T','P','E','Z','Y')
            prefix = dict()
            for i,s in enumerate(symbols):
                prefix[s] = 1<<(i+1) *10
            for s in reversed(symbols):
                if int(number) >= prefix[s]:
                    value = float(number) / prefix[s]
                    return '%.2f%s' %(value,s)
            return "%sB" %number
        jsonreq = json.dumps({'jsonrpc':'2.0','id':'qwer','method':'aria2.getGlobalStat','params': ['token:123654']})
        while True:
            try:
                c = requests.post('http://localhost:7865/jsonrpc', data=jsonreq)
                speed = int(eval(c.text)['result']['downloadSpeed'])
                self.set_speedlabel.emit(bytes_conversion(speed)+'b/s')
                time.sleep(1.2)##避免刷新太快
            except:
                speed = '0Bb/s'
                self.set_speedlabel.emit(speed)
