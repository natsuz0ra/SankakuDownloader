# -*- coding: utf-8 -*-
import requests,sys,re,os,json,time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import *

requests.adapters.DEFAULT_RETRIES = 5
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}

##用户登录处理
class Login(QThread):
    log_append = pyqtSignal(str)
    log_moveCursor = pyqtSignal()
    set_infolabel = pyqtSignal(str)
    enable_login_button = pyqtSignal()
    disable_login_button = pyqtSignal()
    set_usernameedit_disable = pyqtSignal()
    set_passwordedit_disable = pyqtSignal()
    info_message = pyqtSignal(str,str)
    set_token = pyqtSignal(str)
    set_cookies = pyqtSignal(dict)

    def __init__(self,username,password):
        super(Login, self).__init__(None)
        self.username = username
        self.password = password

    ##用户登录
    def run(self):
        time.sleep(0.1) ##睡眠0.1s同步数据

        self.set_infolabel.emit('登入中...')

        login_headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','content-type':'application/json'}
        login_url = "https://capi-v2.sankakucomplex.com/auth/token"
        login_data = {'login':self.username,'password':self.password}
        try:
            login_response = requests.post(login_url,data=json.dumps(login_data),headers=login_headers)
        except:
            self.info_message.emit('登入','登入失败，请检查网络状况')
            self.enable_login_button.emit()
            self.set_infolabel.emit('登入失败')
            self.log_append.emit('登入信息：失败，可能是网络状况不佳')
            self.log_moveCursor.emit()
            return

        ##登录chan主站，用于获取图片数
        chan_login_data = {'user[name]':self.username,'user[password]':self.password}
        chan_login_url = 'https://chan.sankakucomplex.com/user/authenticate'
        chan_login_session = requests.session()
        try:
            chan_login_response = chan_login_session.post(chan_login_url,headers=headers,data=chan_login_data)
        except:
            self.info_message.emit('登入','登入失败，请检查网络状况')
            self.enable_login_button.emit()
            self.set_infolabel.emit('登入失败')
            self.log_append.emit('登入信息：失败，可能是网络状况不佳')
            self.log_moveCursor.emit()
            return

        if login_response.status_code == 200 and chan_login_response.status_code == 200:
            token = re.findall(r'"access_token":"(.*?)"',login_response.text)[0]
            self.set_token.emit(token)
            self.set_cookies.emit(requests.utils.dict_from_cookiejar(chan_login_session.cookies))
            ##禁止更改用户信息和登录按钮
            self.disable_login_button.emit()
            self.set_usernameedit_disable.emit()
            self.set_passwordedit_disable.emit()

            ##成功提示
            self.info_message.emit('登入','登入成功')
            self.set_infolabel.emit('登入成功')
            self.log_append.emit('登入信息：登入成功')
            self.log_moveCursor.emit()

            ##关闭过滤器
            disable_filter_headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','content-type':'application/json','authorization':'Bearer '+token}
            disable_filter_url = "https://capi-v2.sankakucomplex.com/users/724964"
            disable_filter_data = {'user':{'filter_content':'false'}}
            disable_filter_request = requests.put(disable_filter_url,data=json.dumps(disable_filter_data),headers=disable_filter_headers)

            ##保存账号信息
            with open('user.ini','w') as user:
                user.write(self.username+'\n')
                user.write(self.password)
        else:
            ##失败提示
            self.info_message.emit('登入','登入失败，请检查账号密码是否正确')
            self.enable_login_button.emit()
            self.set_infolabel.emit('登入失败')
            self.log_append.emit('登入信息：失败，可能是账号密码有误')
            self.log_moveCursor.emit()