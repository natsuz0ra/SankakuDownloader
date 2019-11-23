# -*- coding: utf-8 -*-
import time,requests,sys,datetime
import math,re,os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import *
from subprocess import Popen,PIPE,STDOUT
from bs4 import BeautifulSoup as bs

requests.adapters.DEFAULT_RETRIES = 5
this_page_count = this_page_downloaded = 0 #当前页图片数和已下载数
count = downloaded_count = 0 #总图片数和已下载数

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}

class Worker(QThread):
    log_append = pyqtSignal(str)
    set_processbar = pyqtSignal(int)
    set_process = pyqtSignal(str,int)
    log_moveCursor = pyqtSignal()
    enable_start_button = pyqtSignal()
    disable_start_button = pyqtSignal()
    enable_stop_button = pyqtSignal()
    disable_stop_button = pyqtSignal()
    set_infolabel = pyqtSignal(str)
    set_speedlabel = pyqtSignal(str)
    set_startbutton_text = pyqtSignal(str)
    info_message = pyqtSignal(str,str)
    notifications = pyqtSignal(int,int)
    save_failed_list = pyqtSignal()

    def __init__(self,tags,path,start_page,token,chan_cookies):
        super(Worker, self).__init__(None)
        self.tags = tags
        self.path = path
        self.start_page = int(start_page)
        self.token = token
        self.chan_cookies = chan_cookies

    ##调用aria2下载
    def get_img(self,img_list):
        order = ('aria2c_sd --dir=%s --input-file=url.txt --continue=true --enable-rpc=true --rpc-listen-port=7865 --rpc-secret=123654' % self.path)
        
        ##保存链接并调用aria2下载
        with open('url.txt','w') as url_list:
            for img_url in img_list:
                url_list.write(img_url+'\n')
        process = Popen(order,shell=True,stdin=PIPE,stdout=PIPE,stderr=STDOUT)
        time.sleep(0.1)
        self.notifications.emit(this_page_count,count)

        ##获取aria2的信息
        while process.poll() is None:
            process.stdout.readline()

    ##获取当前页所有的图片地址
    def get_url(self,page_url):
        ##如果登录成功，使用带token的headers
        if self.token != 'failed':
            ##获取图片地址
            login_headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134','authorization':'Bearer '+self.token}
            try:
                page = requests.get(page_url,headers=login_headers).text
            except:
                return ['error']
        else:
            try:
                page = requests.get(page_url,headers=headers).text
            except:
                 return ['error']
        url_list = re.findall(r'"file_url":"(.*?)"',str(page))
        return url_list

    ##获取tags下图片的数量
    def get_count(self):
        url_for_count = 'https://chan.sankakucomplex.com/?tags=' + self.tags
        if self.token != 'failed':##检查是否登录
            try:
                text = bs(requests.get(url_for_count,headers=headers,cookies=self.chan_cookies).text,'lxml')
            except:
                return -2
        else:##如果没有登录，那么就会有搜索限制
            try:
                text = bs(requests.get(url_for_count,headers=headers).text,'lxml')
            except:
                return -2

        ##获取总图片数
        if re.findall(r'\+',self.tags)==[] and re.findall(r'\+-',self.tags)==[]:#单tag时
            img_count = re.findall(r'">(.*?)</',str(text.find('span',{'class':'tag-count'})))[0]
            return int(img_count.replace(',',''))
        else:#多tag或过滤条件时
            try:
                img_count = re.findall(r'Post Count: (.*?)"><',str(text.find('span',{'class':'tag-type-none'})))[0]
            except:
                return -1
            return int(img_count.replace(',',''))

    ##获取当前页的图片地址
    def one_page_process(self,i):
        img_list = self.get_url(url+str(i))
        if img_list == ['error']:
            return 1
        global this_page_count
        this_page_count = len(img_list)
        self.log_append.emit('下载第%d页，%d张图片' % (i,this_page_count))
        self.log_moveCursor.emit()
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        #if len(img_list) > 5:
        #    if len(img_list)%5 == 0:
        #        for k in range(0,int(len(img_list)/5)):
        #            self.get_img(img_list[k*5:k*5+5])
        #    else:
        #        for k in range(0,math.ceil(len(img_list)/5)-1):
        #            self.get_img(img_list[k*5:k*5+5])
        #        self.get_img(img_list[(math.ceil(len(img_list)/5)-1)*5:])
        #else:
        #    self.get_img(img_list)
        self.get_img(img_list)
        return 0

    ##开始
    def run(self):
        self.set_processbar.emit(0)#进度条初始化
        self.disable_start_button.emit()
        self.enable_stop_button.emit()
        
        ##开始页码不能为0
        if self.start_page == 0:
            self.info_message.emit('错误','开始页码错误')
            self.enable_start_button.emit()
            self.disable_stop_button.emit()
            return

        ##检查path和tags是否为空
        if self.path == '':
            self.info_message.emit('错误','请设定保存路径')
            self.enable_start_button.emit()
            self.disable_stop_button.emit()
            return
        if self.tags == '':
            self.info_message.emit('错误','请设定标签')
            self.enable_start_button.emit()
            self.disable_stop_button.emit()
            return

        start = datetime.datetime.now()##计时
        global url
        url = 'https://capi-v2.sankakucomplex.com/posts?limit=40&tags='+self.tags+'&page='
        self.set_infolabel.emit('正在开始...')
        sys.setrecursionlimit(1000000)

        global count
        count = self.get_count()
        page_count = math.ceil(count/40)
        if count == -1 or count == 0:#如果不能获取正确页数则终止
            self.log_append.emit("错误：无法获取图片总数，可能是标签错误或者未登入")
            self.log_moveCursor.emit()
            self.enable_start_button.emit()
            self.disable_stop_button.emit()
            return
        elif count == -2:
            self.info_message.emit('错误',"网络错误，请检查网络状况")
            self.enable_start_button.emit()
            self.disable_stop_button.emit()
            return

        if self.start_page != 1 and self.start_page > page_count: #如果开始页数大于总页数则终止
            self.info_message.emit('错误','开始页码不能大于总页数')
            self.enable_start_button.emit()
            self.disable_stop_button.emit()
            return
        elif self.start_page != 1 and self.start_page <= page_count: #计算中途开始时的页数和图片数
            count -= ((self.start_page -1) * 40)
            page_count = (page_count - self.start_page + 1)

        self.log_append.emit('标签下找到%d张图片，共%d页' % (count,page_count))
        self.log_moveCursor.emit()

        self.set_process.emit('0',count)

        ##开始获取链接并下载
        for i in range(self.start_page, (page_count+self.start_page)):
            self.set_startbutton_text.emit('(%d/%d)' % (i,page_count+self.start_page-1))
            result = self.one_page_process(i)
            if result == 1:
                self.info_message.emit('错误',"网络错误，你可以从第%d页重新开始"%i)
                self.log_append.emit("网络错误，你可以从第%d页重新开始"%i)
                self.log_moveCursor.emit()
                self.save_failed_list.emit()
                self.set_startbutton_text.emit('开始')
                self.enable_start_button.emit()
                self.disable_stop_button.emit()
                return

        self.save_failed_list.emit()
        self.enable_start_button.emit()
        self.disable_stop_button.emit()
        self.set_startbutton_text.emit('开始')
        end = datetime.datetime.now()
        used_time = str(end-start).split('.', 2)[0]
        self.log_append.emit('用时：%s' % used_time)
        self.log_moveCursor.emit()
