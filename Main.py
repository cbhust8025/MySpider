# -*- coding=utf-8 -*-

# --------------------------------------------------------
# Python Templet
# Copyright (c) 2017 CB
# Written by lealcheng
# --------------------------------------------------------
'''
主程序 入口，从这里开始执行爬虫主窗口
'''

import wx
from wx import App
# from SpiderFrame import Spider
from NewSpiderFrame import Spider

# 入口，从这里开始执行爬虫主窗口
if __name__ == "__main__":
    app = App()
    frame = Spider()
    frame.Show()
    app.MainLoop()
