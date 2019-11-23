# -*- coding: utf-8 -*-
import sys,os,json
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMessageBox,QFileDialog,QLineEdit
from PyQt5.QtCore import *
from subprocess import call,PIPE,STDOUT
from Refreshdlspeed import Refreshdlspeed
from Login import Login
from Notifications import Notifications
from Worker import Worker
from Stop import Stop

##初始化全局变量
token = 'failed'
start_page = 1
chan_cookies = None
failed_list = []
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}

class Ui_SankakuDownloader(object):
    def setupUi(self, SankakuDownloader):
        SankakuDownloader.setObjectName("SankakuDownloader")
        SankakuDownloader.resize(521, 427)
        SankakuDownloader.setFixedSize(521, 427)
        self.centralwidget = QtWidgets.QWidget(SankakuDownloader)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(10, 190, 93, 28))
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(113, 190, 93, 28))
        self.pushButton_stop.setObjectName("pushButton_start")
        self.pushButton_stop.setEnabled(False)
        self.logBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logBrowser.setGeometry(QtCore.QRect(10, 260, 501, 141))
        self.logBrowser.setObjectName("logBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 70, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 227, 501, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(130, 10, 72, 15))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(310, 70, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 402, 291, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(380, 402, 131, 21))
        self.label_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(240, 31, 93, 28))
        self.pushButton_login.setObjectName("pushButton_login")
        self.lineEdit_tags = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_tags.setGeometry(QtCore.QRect(10, 90, 291, 31))
        self.lineEdit_tags.setObjectName("lineEdit_tags")
        self.lineEdit_savepath = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_savepath.setGeometry(QtCore.QRect(10, 150, 291, 31))
        self.lineEdit_savepath.setObjectName("lineEdit_savepath")
        self.lineEdit_username = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_username.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(130, 30, 101, 31))
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_startpage = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_startpage.setGeometry(QtCore.QRect(310, 90, 91, 31))
        self.lineEdit_startpage.setObjectName("lineEdit_username")
        self.pushButton_selectpath = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_selectpath.setGeometry(QtCore.QRect(310, 150, 51, 31))
        self.pushButton_selectpath.setObjectName("pushButton_selectpath")
        self.statusBar = QtWidgets.QStatusBar(SankakuDownloader)
        self.statusBar.setObjectName("statusBar")
        self.lineEdit_startpage.setValidator(QtGui.QIntValidator(1,2147483647))

        if os.path.exists('user.ini'):
            with open('user.ini','r') as user:
                user_info = user.readlines()
                try:
                    self.lineEdit_username.setText(user_info[0].split('\n')[0])
                    self.lineEdit_password.setText(user_info[1])
                except:
                    pass

        ##开始监控下载速度
        self.refreshdlspeed()

        ##按钮事件
        self.pushButton_selectpath.clicked.connect(self.set_path)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_stop.clicked.connect(self.stop)
        self.pushButton_login.clicked.connect(self.login)
        app.aboutToQuit.connect(self.closeEvent)

        self.retranslateUi(SankakuDownloader)
        QtCore.QMetaObject.connectSlotsByName(SankakuDownloader)

    def retranslateUi(self, SankakuDownloader):
        _translate = QtCore.QCoreApplication.translate
        SankakuDownloader.setWindowTitle(_translate("SankakuDownloader", "SankakuDownloader v2.0"))
        SankakuDownloader.setWindowIcon(QtGui.QIcon('icon.png'))
        self.pushButton_start.setText("开始")
        self.pushButton_stop.setText("停止")
        self.logBrowser.setHtml(_translate("SankakuDownloader", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText("标签：")
        self.label_2.setText("保存路径：")
        self.label_3.setText("用户名：")
        self.label_4.setText("密码：")
        self.label_5.setText("开始页码：")
        self.label_6.setText("等待中")
        self.pushButton_login.setText("登入")
        self.pushButton_selectpath.setText("...")

    ##关闭程序时关闭aria2c
    def closeEvent(self):
        #os.system('taskkill /f /im aria2c_sd.exe')
        call("kill -9 $(ps -ef|grep aria2c_sd |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')",shell=True,stdin=PIPE,stdout=PIPE,stderr=STDOUT)
        #process.send_signal(signal.CTRL_C_EVENT)
        global failed_list
        if failed_list != []:
            with open('failed.txt','w') as failed:
                for failed_url in failed_list:
                    failed.write(failed_url+'\n')
        sys.exit(0)

    ##设置图片保存目录
    def set_path(self):
        get_directory_path = QFileDialog.getExistingDirectory(None,'请选择保存路径','')
        self.lineEdit_savepath.setText(str(get_directory_path))

    ##设置start按钮字样
    def set_startbutton_text(self,info):
        self.pushButton_start.setText(info)

    ##调整进度条
    def set_processbar(self,int):
        self.progressBar.setProperty('value',int)

    ##添加log信息
    def log_append(self,log):
        self.logBrowser.append(log)

    ##将log移动到最下面
    def log_moveCursor(self):
        self.logBrowser.moveCursor(self.logBrowser.textCursor().End)

    ##获取开始下载的页数
    def get_start_page(self):
        global start_page
        if self.lineEdit_startpage.text() != '':
            start_page = int(self.lineEdit_startpage.text())

    ##关闭和开启开始键
    def enable_start_button(self):
        self.pushButton_start.setEnabled(True)

    def disable_start_button(self):
        self.pushButton_start.setEnabled(False)

    ##设置登录键是否可用
    def enable_login_button(self):
        self.pushButton_login.setEnabled(True)

    def disable_login_button(self):
        self.pushButton_login.setEnabled(False)

    ##设置停止键是否可用
    def enable_stop_button(self):
        self.pushButton_stop.setEnabled(True)

    def disable_stop_button(self):
        self.pushButton_stop.setEnabled(False)

    ##设置用户名密码栏为不可用
    def set_usernameedit_disable(self):
        self.lineEdit_username.setEnabled(False)

    def set_passwordedit_disable(self):
        self.lineEdit_password.setEnabled(False)

    def set_process(self,info,count):
        if info == '+1':
            now_info = int(self.label_6.text().split('/')[0].split('(')[-1])
            self.label_6.setText('(%d/%d)' % (now_info+1,count))
            self.progressBar.setProperty('value',round((now_info+1)*100/count))
        elif info == '0':
            self.label_6.setText('(%d/%d)' % (0,count))

    ##提示框
    def info_message(self,title,info):
        QMessageBox.information(None,title,info,QMessageBox.Yes)

    ##刷新信息提示
    def set_infolabel(self,info):
        self.label_6.setText(info)
        return info

    ##添加failed信息
    def add_failed_info(self,info):
        global failed_list
        failed_list.append(info)

    ##结束后处理failed_list
    def save_failed_list(self):
        ##保存失败列表
        global failed_list
        if failed_list != []:
            with open('failed.txt','w') as failed:
                for failed_url in failed_list:
                    failed.write(failed_url+'\n')
            self.label_6.setText('下载完成，%d个文件下载失败' % len(failed_list))
            failed_list = []
        else:
            self.label_6.setText('下载完成')

    ##刷新下载速度
    def set_speedlabel(self,speed):
        self.label_7.setText(speed)

    ##设置token和cookies
    def set_token(self,into_token):
        global token
        token = into_token

    def set_cookies(self,into_cookies):
        global chan_cookies
        chan_cookies = into_cookies

    ##终止主进程
    def stop_worker(self):
        self.thread.terminate()
        try:
            self.thread_notifications.stop()
        except:
            self.label_6.setText('下载已停止')
            return
        global failed_list
        if failed_list != []:
            with open('failed.txt','w') as failed:
                for failed_url in failed_list:
                    failed.write(failed_url+'\n')
            self.label_6.setText('下载已停止，%d个文件下载失败' % len(failed_list))
            failed_list = []
        else:
            self.label_6.setText('下载已停止')

    ##刷新下载速度
    def refreshdlspeed(self):
        self.thread_refreshdlspeed = Refreshdlspeed()
        self.thread_refreshdlspeed.set_speedlabel.connect(self.set_speedlabel)
        self.thread_refreshdlspeed.start()

    ##消息监控
    def notifications(self,this_page_count,count):
        self.thread_notifications = Notifications(this_page_count,count)

        self.thread_notifications.log_append.connect(self.log_append)
        self.thread_notifications.log_moveCursor.connect(self.log_moveCursor)
        self.thread_notifications.set_process.connect(self.set_process)
        self.thread_notifications.add_failed_info.connect(self.add_failed_info)

        self.thread_notifications.start()

    ##用户登录
    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        self.thread_login = Login(username,password)
        self.thread_login.log_append.connect(self.log_append)
        self.thread_login.log_moveCursor.connect(self.log_moveCursor)
        self.thread_login.set_infolabel.connect(self.set_infolabel)
        self.thread_login.enable_login_button.connect(self.enable_login_button)
        self.thread_login.disable_login_button.connect(self.disable_login_button)
        self.thread_login.set_usernameedit_disable.connect(self.set_usernameedit_disable)
        self.thread_login.set_passwordedit_disable.connect(self.set_passwordedit_disable)
        self.thread_login.info_message.connect(self.info_message)
        self.thread_login.set_token.connect(self.set_token)
        self.thread_login.set_cookies.connect(self.set_cookies)

        self.pushButton_login.setEnabled(False)
        self.thread_login.start()

    ##结束进程
    def stop(self):
        now_page = int(self.pushButton_start.text().split('/')[0].split('(')[-1])
        self.thread_stop = Stop(now_page)

        self.thread_stop.log_append.connect(self.log_append)
        self.thread_stop.log_moveCursor.connect(self.log_moveCursor)
        self.thread_stop.enable_start_button.connect(self.enable_start_button)
        self.thread_stop.disable_stop_button.connect(self.disable_stop_button)
        self.thread_stop.set_startbutton_text.connect(self.set_startbutton_text)
        self.thread_stop.stop_worker.connect(self.stop_worker)

        self.thread_stop.start()

    ##开始进程
    def start(self):
        tags = self.lineEdit_tags.text()
        path = self.lineEdit_savepath.text()
        start_page = self.lineEdit_startpage.text()
        if start_page == '':
            start_page = 1

        self.thread = Worker(tags,path,start_page,token,chan_cookies)
        self.thread.set_processbar.connect(self.set_processbar)
        self.thread.log_append.connect(self.log_append)
        self.thread.log_moveCursor.connect(self.log_moveCursor)
        self.thread.enable_start_button.connect(self.enable_start_button)
        self.thread.disable_start_button.connect(self.disable_start_button)
        self.thread.enable_stop_button.connect(self.enable_stop_button)
        self.thread.disable_stop_button.connect(self.disable_stop_button)
        self.thread.set_infolabel.connect(self.set_infolabel)
        self.thread.set_speedlabel.connect(self.set_speedlabel)
        self.thread.set_startbutton_text.connect(self.set_startbutton_text)
        self.thread.info_message.connect(self.info_message)
        self.thread.notifications.connect(self.notifications)
        self.thread.set_process.connect(self.set_process)
        self.thread.save_failed_list.connect(self.save_failed_list)

        self.thread.start()

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_SankakuDownloader()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())