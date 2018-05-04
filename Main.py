#!/usr/bin/env python
# -*- coding=utf-8 -*-

# --------------------------------------------------------
# Python Templet
# Copyright (c) 2017 CB
# Written by Leal Cheng
# --------------------------------------------------------
'''
主程序 入口，从这里开始执行爬虫主窗口
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