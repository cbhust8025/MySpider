#!/usr/bin/env python
# -*- coding=utf-8 -*-

# --------------------------------------------------------
# Python Templet
# Copyright (c) 2017 CB
# Written by Leal Cheng
# --------------------------------------------------------
'''
������ ��ڣ������￪ʼִ������������
'''
import sys
import wx
from SpiderFrame import Spider


# ��ڣ������￪ʼִ������������
if __name__ == "__main__":
    app = wx.App()
    frame = Spider()
    frame.Show()
    app.MainLoop()