#!/usr/bin/env python
# encoding: gbk
'''
������ main���������
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