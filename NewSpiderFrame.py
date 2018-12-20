# -*- coding=utf-8 -*-

# --------------------------------------------------------
# Python Templet
# Copyright (c) 2017 CB
# Written by Leal Cheng
# --------------------------------------------------------
'''
爬虫主窗口
'''
import re
import sys
import wx
from bs4 import BeautifulSoup
from HtmlDownloader import HtmlDownloader
########################################################################
textColorForeGround = "#E9EBFE"  # 文本前景
textColorBackGround = "black"  # 文本背景
combocontrolButtonWidth = 35  # 下拉框按钮的宽度
########################################################################
_DEBUG = True

class Spider(wx.Frame):
    # 爬虫主窗口的构造函数
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title="不仅仅是一个爬虫",
                          size=(1200, 900),
                          style=wx.DEFAULT_FRAME_STYLE)
        # 初始化爬虫窗口
        self._init_window()

    def _init_window(self):
        # 绑定右上角关闭窗口
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # 在主窗口放置两个面板
        self.panel_top = wx.Panel(self)
        self.panel_bottom = wx.Panel(self)

        # 面板颜色设置  界面设计完后删除
        self.panel_top.SetBackgroundColour('#FFF2E2')
        self.panel_bottom.SetBackgroundColour('White')

        # 初始化放置在窗口上面的控件
        main_box = self._init_boxer()

        self.SetSizer(main_box)

    def _init_boxer(self):
        # 窗口设计
        input_box = wx.BoxSizer()  # 横向包含控件--按钮box，放置所有按钮
        text_box = wx.BoxSizer(wx.VERTICAL)  # 横向包含控件--文本框box，放置文本框
        panel1_box = wx.BoxSizer()  # 横向包含控件--面板1box，放置面板1中包含的所有box
        panel2_box = wx.BoxSizer(wx.VERTICAL)  # 纵向包含控件--面板2box，放置面板2中包含的所有box
        main_box = wx.BoxSizer(wx.VERTICAL)  # 纵向包含控件--窗口总box
        ################################panel_top########################################
        # 按钮描述--panel1
        recommand_button = wx.Button(self.panel_top, label='推荐')
        test_button = wx.Button(self.panel_top, label="测试")

        # 按钮功能绑定
        recommand_button.Bind(wx.EVT_BUTTON, self.recommand)
        test_button.Bind(wx.EVT_BUTTON, self.test)

        # 文本框控件描述
        input_text = wx.TextCtrl(self.panel_top, -1,
                style=wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_AUTO_URL) # 输入文本框
        # 输入、按钮界面box
        input_box.Add(input_text, proportion=10, flag=wx.ALL | wx.EXPAND, border=10)
        # input_box.Hide(input_text)  # 先隐藏起来，使用组合下拉框
        # self.InputBox.Add(self.combocontrol, proportion=10, flag=wx.ALL | wx.EXPAND, border=10)
        input_box.Add(recommand_button, proportion=1, flag=wx.ALL, border=10)
        input_box.Add(test_button, proportion=1, flag=wx.ALL, border=10)

        # 面板1--box设置
        panel1_box.Add(input_box, flag=wx.ALL | wx.EXPAND, border=0)
        self.panel_top.SetSizer(panel1_box)

        ################################panel_bottom########################################
        content_text = wx.TextCtrl(self.panel_bottom, -1, u"正常", style=wx.TE_MULTILINE | wx.TE_RICH2)  # 主要文本显示
        content_text.SetOwnBackgroundColour(textColorForeGround)
        content_text.SetStyle(0,
            content_text.GetLastPosition(),
            wx.TextAttr(textColorBackGround, textColorForeGround,
            wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)))  # 设置前景、背景色（wx.TextAttr）
        bar_text = wx.StaticText(self.panel_bottom, -1, u"正常", style=wx.TE_MULTILINE | wx.TE_RICH2)  # 状态栏显示
        bar_text.SetFont(wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD, False))  # 进行设置

        # 文本域界面box
            # wx.EXPAND 参数表示文本框尽可能占满box的剩余空间
        text_box.Add(content_text, proportion=25, flag=wx.ALL | wx.EXPAND, border=10)
        text_box.Add(bar_text, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        # self.TextBox.Hide(self.BarText)

        # 面板2--box设置
        panel2_box.Add(text_box, proportion=0, flag=wx.ALL | wx.EXPAND, border=0)
        self.panel_bottom.SetSizer(panel2_box)
        ################################main_box########################################
        # 窗口总box，放置两个panel
        main_box.Add(self.panel_top, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        main_box.Add(self.panel_bottom, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        return main_box

    def OnClose(self, evt):
        if _DEBUG:
            evt.Skip()
            return
        ret = wx.MessageBox(u'你真的确认要关闭么？？？',
            u'我是一个小说爬虫阅读器', wx.OK | wx.CANCEL)
        if ret == wx.OK:
            # do something here...
            evt.Skip()

    def recommand(self, evt):
        pass

    def test(self, evt):
        pass

# 入口，从这里开始执行测试程序
if __name__ == "__main__":
    app = wx.App()
    frame = Spider()
    frame.Show()
    app.MainLoop()
