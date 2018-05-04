#!/usr/bin/env python
# -*- coding=utf-8 -*-

# --------------------------------------------------------
# Python Templet
# Copyright (c) 2017 CB
# Written by Leal Cheng
# --------------------------------------------------------
'''
�Զ����б��
'''

from wx import *
########################################################################
textColorForeGround = "#E9EBFE"  # �ı�ǰ��
textColorBackGround = "black"  # �ı�����
########################################################################
class MyCustomListPopup(ListCtrl, wx.combo.ComboPopup):
    def __init__(self):
        # Since we are using multiple inheritance, and don't know yet
        # which window is to be the parent, we'll do 2-phase create of
        # the ListCtrl instead, and call its Create method later in
        # our Create method.  (See Create below.)
        self.PostCreate(wx.PreListCtrl())

        # Also init the ComboPopup base class.
        wx.combo.ComboPopup.__init__(self)

    def ConfigureListCtrl(self):
        # �б������ú������ڶ������б�����֮����е��������ö�Ӧ�����б��
        # ��д����������Զ����б��
        pass

    def OnMotion(self, evt):
        # ��׽���λ�ã�������ǰ������ڵ��б���е�һ��
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:  # ���item>= 0,���ʾѡ����һ����Ч��item
            # self.Select(item, 1)
            for i in range(self.GetItemCount()): # �ҵ�����������0��ʼ����
                self.Select(i, 1 if i == item else 0)  # ����ǵ�ǰ���ͣ����λ����item���������item
            self.curitem = item  # ����ǰitem������Ϊ��ǰѡ�е�item

    def OnLeftDown(self, evt):
        # ��׽��궯���������������±�ʾѡ�����б���ĳһ��
        # ���б����йرգ�Dismiss--���أ�����д������ĳ�ֲ�����
        # self.value = self.curitem
        # self.GetControl().SetValue(self.GetItemText(self.curitem))
        self.Dismiss()

    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    # def Init(self):
    #     self.value = -1
    #     self.curitem = -1


    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        # ��ʼ���б����󣬱�����д�ĵ���������
        wx.ListCtrl.Create(self, parent,
                           style=wx.LC_REPORT)
        self.curitem = -1
        self.Bind(wx.EVT_MOTION, self.OnMotion)  # ���б�����껬���¼�
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)  # ���б��������������¼�
        return True  # ����True��ʾ�����б��ɹ�

    # Return the widget that is to be used for the popup
    def GetControl(self):
        # ������д�ĺ���֮һ�����ڴ�����Ͽ��е��б����Ѱ���Լ��ĸ�����
        # self.log.write("ListCtrlComboPopup.GetControl")
        return self

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    # def SetStringValue(self, val):
    #     print("ListCtrlComboPopup.SetStringValue")
    #     idx = self.FindItem(-1, val)
    #     if idx != wx.NOT_FOUND:
    #         self.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        # ������д�ĵڶ�������
        # �����Ҫ��ѡ�е��б���ֵ���õ���Ͽ���ı����ڣ����б��رպ󽫻���ô˺���
        if self.curitem >= 0:
            return self.GetItemText(self.curitem)
        return ""
    #
    # Called immediately after the popup is shown
    # def OnPopup(self):
    #     print("ListCtrlComboPopup.OnPopup")
    #     wx.combo.ComboPopup.OnPopup(self)
    #     # self.SetFocus()
    #
    # # Called when popup is dismissed
    # def OnDismiss(self):
    #     print("ListCtrlComboPopup.OnDismiss")
    #     wx.combo.ComboPopup.OnDismiss(self)
