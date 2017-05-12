# -*- coding: utf-8 -*-

import wx
import os
from time import ctime, sleep
import socket
import threading
import json


class Conn:
    def __init__(self, **values):
        self.values = values
        # self.mer = values.get('mer')
        # self.posId = values.get('posId')
        # self.insNo = values.get('insNo')
        # self.tmk = values.get('tmk')
        # self.tpk = values.get('tpk')

    def Start(self):
        print ("========================准备打开Android服务========================\r\n")
        # os.system("adb shell am broadcast -a NotifyServiceStop")
        # sleep(3)
        os.system("adb forward tcp:12580 tcp:10086")
        # sleep(3)
        # os.system("adb shell am broadcast -a NotifyServiceStart")
        print ("========================开始连接Android服务器========================\r\n")
        self.sk = socket.socket()
        self.sk.connect(("127.0.0.1", 12580))
        print ("========================准备写入数据========================\r\n")

        for param in self.values:
            print (
                "========================准备写入" + param +
                "========================\r\n")
            if self.SendParams(param) != 'OK':
                print ("========================数据写入错误========================\r\n")
                return
        print ("========================正在请求关闭数据通信========================\r\n")
        self.sk.send('exit')
        print ("========================通信关闭========================\r\n")

    def SendParams(self, value):
        self.sk.send(self.values.get(value).decode('utf-8'))
        ret_bytes = self.sk.recv(1024)
        ret_str = str(ret_bytes)
        print(ret_str)
        return ret_str


class ButtonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "江苏东大集成PC端".decode('utf-8'), size=(720, 350), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)

        wx.StaticText(panel, -1, "编号".decode('utf-8'), (0, 10), (80, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "参数名".decode('utf-8'), (80, 10), (100, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "参数标识".decode('utf-8'), (180, 10), (180, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "参数值".decode('utf-8'), (360, 10), (180, -1), style=wx.ALIGN_CENTER)

        # 编号
        wx.StaticText(panel, -1, "1".decode('utf-8'), (0, 50), (80, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "2".decode('utf-8'), (0, 100), (80, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "3".decode('utf-8'), (0, 150), (80, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "4".decode('utf-8'), (0, 200), (80, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "5".decode('utf-8'), (0, 250), (80, -1), style=wx.ALIGN_CENTER)
        # wx.StaticText(panel, -1, "6".decode('utf-8'), (0, 300), (180, -1), style=wx.ALIGN_CENTER)

        # 参数名
        wx.StaticText(panel, -1, "商户编号".decode('utf-8'), (80, 50), (100, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "终端号".decode('utf-8'), (80, 100), (100, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "机构号".decode('utf-8'), (80, 150), (100, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "主密钥密文".decode('utf-8'), (80, 200), (100, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "传输密钥明文".decode('utf-8'), (80, 250), (100, -1), style=wx.ALIGN_CENTER)
        # wx.StaticText(panel, -1, "xxx".decode('utf-8'), (180, 300), (180, -1), style=wx.ALIGN_CENTER)

        # 参数标识
        wx.StaticText(panel, -1, "MERCHANTID".decode('utf-8'), (180, 50), (180, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "POSID".decode('utf-8'), (180, 100), (180, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "INSNO".decode('utf-8'), (180, 150), (180, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "TMK".decode('utf-8'), (180, 200), (180, -1), style=wx.ALIGN_CENTER)
        wx.StaticText(panel, -1, "TPK".decode('utf-8'), (180, 250), (180, -1), style=wx.ALIGN_CENTER)
        # wx.StaticText(panel, -1, "XXX".decode('utf-8'), (360, 300), (180, -1), style=wx.ALIGN_CENTER)

        # 参数值
        self.merText = wx.TextCtrl(panel, -1, "0000".decode('utf-8'), (360, 50), (180, -1), style=wx.TE_LEFT)
        self.posIdText = wx.TextCtrl(panel, -1, "0000".decode('utf-8'), (360, 100), (180, -1), style=wx.TE_LEFT)
        self.insNoText = wx.TextCtrl(panel, -1, "0000".decode('utf-8'), (360, 150), (180, -1), style=wx.TE_LEFT)
        self.tmkText = wx.TextCtrl(panel, -1, "0000".decode('utf-8'), (360, 200), (180, -1), style=wx.TE_LEFT)
        self.tpkText = wx.TextCtrl(panel, -1, "0000".decode('utf-8'), (360, 250), (180, -1), style=wx.TE_LEFT)
        # self.xxxText = wx.TextCtrl(panel, -1, "0000".decode('utf-8'), (540, 300), (180, -1), style=wx.TE_LEFT)

        # 右侧
        wx.StaticText(panel, -1,
                      "\r\n步骤：\r\n\r\n1.打开Android端，点击参数下载按钮\r\n2.在PC端将需要下载的参数填写\r\n3.点击PC端下载按钮，等待下载完毕\r\n4.程序退出"
                      .decode('utf-8'), (560, 30), (140, 150), style=wx.TE_LEFT)
        self.button = wx.Button(panel, -1, "下载".decode('utf-8'), (555, 205), (140, 70))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

    def OnClick(self, event):
        mer = self.merText.GetValue()
        posId = self.posIdText.GetValue()
        insNo = self.insNoText.GetValue()
        tmk = self.tmkText.GetValue()
        tpk = self.tpkText.GetValue()

        # args = {'mer': mer, 'posId': posId, 'insNo': insNo, 'tmk': tmk, 'tpk': tpk}
        conn = Conn(mer=mer, posId=posId, insNo=insNo, tmk=tmk, tpk=tpk)
        t = threading.Thread(target=conn.Start)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    app = wx.App(False)
    frame = ButtonFrame()
    frame.Show()
    app.MainLoop()
