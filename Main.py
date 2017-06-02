#!/usr/bin/env python
# encoding: gbk
'''
主程序， main（），入口
'''
import sys
import wx
from SpiderFrame import Spider


# 入口，从这里开始执行爬虫主窗口
if __name__ == "__main__":
    app = wx.App()
    frame = Spider()
    frame.Show()
    app.MainLoop()