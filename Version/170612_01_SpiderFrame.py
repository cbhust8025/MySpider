#!/usr/bin/env python
# -*- coding=utf-8 -*-

# --------------------------------------------------------
# Python Templet
# Copyright (c) 2017 CB
# Written by Leal Cheng
# --------------------------------------------------------
'''
����������
'''
import wx
import re
from bs4 import BeautifulSoup
from HtmlDownloader import HtmlDownloader
from MyCustomListPopup import MyCustomListPopup
########################################################################
textColorForeGround = "#E9EBFE"  # �ı�ǰ��
textColorBackGround = "black"  # �ı�����
combocontrolButtonWidth = 35  # ������ť�Ŀ��
########################################################################


class MyCustomLP(MyCustomListPopup):
    # �Զ����б��

    def ConfigureListCtrl(self):
        # ��д�˺����������Զ�������
        # �������н��г�ʼ��
        self.InsertColumn(1, "С˵��")
        self.InsertColumn(2, "��")
        self.InsertColumn(3, "����")
        # ����ÿһ�еĿ��
        self.SetColumnWidth(0, 200)
        self.SetColumnWidth(1, 150)
        self.SetColumnWidth(2, 300)
        # # ��������������ԣ���ɺ����ע��
        # list.Append(["asa1", "asa2", "asa3", "asa4"])  # ������ǰ�������������жϴ���
        # self.Append(["asa1", "asa2", "asa3"])
        # self.Append(["asb1", "asb2", "asb3"])
        # self.Append(["asc1", "asc2", "asc3"])
        # self.Append(["asd1asdsadasdsadsadsadasd", "asd2", "asd3"])
        self.SetBackgroundColour(textColorForeGround)  # �����б������ֱ���
    # def Append(self, txt):
    #     # ���һ�У����б���ʽ��ӣ�����С�ڵ�������
    #     # self.Append(["asa1", "asa2", "asa3"])
    #     self.Append(txt)

    def GetSelection(self):
        for i in range(self.GetItemCount()):
            if(self.IsSelected(i)):
                return i
        return -1


class Spider(wx.Frame):
    # ���������ڵĹ��캯�����������ϽǵĹرհ�ť

    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title=u"��������һ������",
                          size=(1200, 900),
                          style=wx.DEFAULT_FRAME_STYLE)
        # ��ʼ��һЩ�����ڵ�����ֵ
        self.namelink = {}  # �����Ѿ���ȡ��{С˵����[���࣬����]} ��ֵ�ԣ������Զ���ȫ��С˵��������

        # �����Ͻǹرմ���
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # ��ʼ����������������ء�����
        self.downloader = HtmlDownloader()  # ��ʼ��������

        # �������ڷ����������
        self.Panel1 = wx.Panel(self)
        self.Panel2 = wx.Panel(self)

        # �����ɫ����  ����������ɾ��
        self.Panel1.SetBackgroundColour('#FFF2E2')
        self.Panel2.SetBackgroundColour('White')

        # ��ť����--panel1
        RecommandButton = wx.Button(self.Panel1, label=u'�Ƽ�')
        TestButton = wx.Button(self.Panel1, label=u"����")

        # ��ť���ܰ�
        RecommandButton.Bind(wx.EVT_BUTTON, self.recommand)
        TestButton.Bind(wx.EVT_BUTTON, self.test)

        # �ı���ؼ�����--panel2
        # ��ʼ����Ͽ�
        self.combocontrol = wx.combo.ComboCtrl(
            parent=self.Panel1, style=wx.CB_SORT)  # ��ʼ��ֻ����ʽ����Ͽ�
        self.mcListPopup = MyCustomLP()  # ��ʼ����Ͽ�������б��
        self.combocontrol.SetPopupControl(self.mcListPopup)  # ������Ͽ��е��б��
        self.combocontrol.SetButtonPosition(
            width=combocontrolButtonWidth)  # ������Ͽ��������ť�Ŀ��
        self.mcListPopup.ConfigureListCtrl()  # �����б��
        self.combotext = self.combocontrol.GetTextCtrl()  # ��ȡ��Ͽ��е��ı���
        self.combocontrol.Bind(wx.EVT_TEXT, self.ChangeText)
        self.combocontrol.Bind(wx.EVT_KEY_DOWN, self.OnBtnBackButton)
        # self.combocontrol.Bind(wx.EVT_CHAR, self.OnChar)
        # wx.TE_PROCESS_ENTER ��wx.TE_PROCESS_TAB �ı������tab������һ��ͻس�����ѡ�е�ǰ��Ĺ���
        self.inputText = wx.TextCtrl(self.Panel1, -1,
                                     style=wx.TE_RICH2
                                     | wx.TE_PROCESS_ENTER
                                     | wx.TE_PROCESS_TAB
                                     | wx.PROCESS_DEFAULT
                                     | wx.TE_AUTO_URL)  # �����ı���
        # �󶨻س��¼���showbookdetail��
        self.inputText.Bind(wx.EVT_TEXT_ENTER, self.showbookdetail)
        self.MainText = wx.TextCtrl(
            self.Panel2, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)  # ��Ҫ�ı���ʾ
        self.MainText.SetOwnBackgroundColour(textColorForeGround)
        self.BarText = wx.StaticText(
            self.Panel2, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)  # ״̬����ʾ

        # �������
        self.InputBox = wx.BoxSizer()  # ��������ؼ�--��ťbox���������а�ť
        self.TextBox = wx.BoxSizer(wx.VERTICAL)  # ��������ؼ�--�ı���box�������ı���
        self.Panel1Box = wx.BoxSizer()  # ��������ؼ�--���1box���������1�а���������box
        # ��������ؼ�--���2box���������2�а���������box
        self.Panel2Box = wx.BoxSizer(wx.VERTICAL)
        self.MainBox = wx.BoxSizer(wx.VERTICAL)  # ��������ؼ�--������box

        # ���롢��ť����box
        self.InputBox.Add(self.inputText, proportion=10,
                          flag=wx.ALL | wx.EXPAND, border=10)
        self.InputBox.Hide(self.inputText)  # ������������ʹ�����������
        self.InputBox.Add(self.combocontrol, proportion=10,
                          flag=wx.ALL | wx.EXPAND, border=10)
        self.InputBox.Add(RecommandButton, proportion=1,
                          flag=wx.ALL, border=10)
        self.InputBox.Add(TestButton, proportion=1, flag=wx.ALL, border=10)

        # �ı������box
        # wx.EXPAND ������ʾ�ı��򾡿���ռ��box��ʣ��ռ�
        self.TextBox.Add(self.MainText, proportion=25,
                         flag=wx.ALL | wx.EXPAND, border=10)
        self.TextBox.Add(self.BarText, proportion=1,
                         flag=wx.ALL | wx.EXPAND, border=10)
        # self.TextBox.Hide(self.BarText)

        # ���1--box����
        self.Panel1Box.Add(self.InputBox, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel1.SetSizer(self.Panel1Box)

        # ���2--box����
        self.Panel2Box.Add(self.TextBox, proportion=0,
                           flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel2.SetSizer(self.Panel2Box)

        # ������box
        self.MainBox.Add(self.Panel1, proportion=1,
                         flag=wx.ALL | wx.EXPAND, border=10)
        self.MainBox.Add(self.Panel2, proportion=1,
                         flag=wx.ALL | wx.EXPAND, border=10)

        # ��box���ŵ�������
        self.SetSizer(self.MainBox)
        self.recommand(wx.wxEVT_COMMAND_BUTTON_CLICKED)  # ��ʼ�����һ��������һ���Ƽ�ϵͳ

    def OnClose(self, evt):
        ret = wx.MessageBox('ȷ�Ϲر�?', '�ر�', wx.OK | wx.CANCEL)
        if ret == wx.OK:
            # do something here...
            evt.Skip()

    def SetTextForPopup(self, text):  # �����������е��ı�
        for txt in text:
            self.namelink[txt[0]] = [txt[-2], txt[-1]]
            self.mcListPopup.Append(txt)  # ����Append�������һ���ı�
        # self.combocontrol.GetTextCtrl().AutoComplete(self.namelink.keys())  # ���С˵���Զ���ȫ����
        # self.combocontrol.GetTextCtrl().Bind(wx.EVT_KEY_DOWN,
        # self.ShowBookDetail)  # �󶨻س��¼���showbookdetail��

    def GetTextForRecommand(self, titledic):
        text = ""
        titlel = sorted(titledic.keys(), key=lambda a: len(a),
                        reverse=True)  # ���շ������ĳ��̽�������
        for title in titlel:  # ��ʽ������ı�
            text += title + ":\n"
            num = 1
            for book in titledic[title]:
                text += str(num) + ". " + book + "\n"
                num += 1
            text += "\n"
        return text

    def GetLinksForRecommand(self, soup):  # ��ȡ�����ҳ������С˵����
        LinksRes = soup.find_all('a', {  # С˵��������Tag��ǩ��Ϊa
            "class": "name",  # С˵��������Tag��class����Ϊ��name��
            # С˵��������Tag�ġ�data-eid����ʽΪqd_A110������ʽ��ʹ��������ʽ����ƥ��
            "data-eid": re.compile("qd_A\d{3}"),
            "href": re.compile("//book.qidian.com/info/\d{9,20}")})  # ����bs4��soup�����find_all������ƥ������С˵�������ڵ�Tag
        titledic = {}  # ����ȡ����С˵���������Ͻ��ֵ䣬��ֵΪ��ǰС˵���ڵķ�����
        popuptext = []
        # LinkNum = []
        # regex = re.compile(r"\d{9,20}")
        for Link in LinksRes:
            # ��С˵�����ǰ��Tag��Ϊ'h3'��Tag��Ϊ��ǰС˵���ڵķ��࣬��NO.1�������ǩ����
            linkprevious = Link.find_previous('h3')
            while(linkprevious.getText() == "NO.1"):
                linkprevious = linkprevious.find_previous('h3')
            # ȥ���������л�ȡ���ġ����ࡱ��"24Сʱ�ڸ���15163��"����������
            title = linkprevious.getText().rstrip(u'\u66f4\u591a\ue621')\
                .rstrip(u'24\u5c0f\u65f6\u5185\u66f4\u65b015163\u672c')
            if(titledic.has_key(title)):
                titledic[title].append(
                    Link.getText() + "    " + Link.get('href'))
            else:
                titledic[title] = [Link.getText() + "    " + Link.get('href')]
            # LinkNum.append(Link.getText() + " " + str(int(regex.findall(Link.get('href'))[0])))
            popuptext.append([Link.getText(), title, Link.get('href')])
        # self.inputText.AutoComplete(choices=LinkNum)  # ԭʼ�汾���Զ���ȫ����
        self.SetTextForPopup(popuptext)
        return self.GetTextForRecommand(titledic)  # �����ɵķ����ֵ��ʽ���������ʽ�����з�����ʾ

    def recommand(self, event):
        soup = BeautifulSoup(
            markup=self.downloader.download("http://www.qidian.com/"),
            features='html.parser', from_encoding='utf-8')  # ����www.qidian.com��վ��ҳ�棬����BeautifulSoup����
        self.MainText.SetEditable(False)  # ���Ƽ�״̬�µ���Ҫ�ı������óɲ��ɱ༭״̬
        self.MainTextValueSet(self.GetLinksForRecommand(soup))  # �����Ƽ�С˵�ı�
        self.BarTextValueSet("�Ƽ�")  # ����״̬��
        # �Ƽ��ı������˸�ʽ�����������ɻ���Ҫ��

    def showbookdetail(self, event):
        print "call the showbookdetail!"
        # չʾ�鼮���鰴ť
        regex = re.compile(r"\S+\d{9,20}$")  # ƥ�䣬��������������������Ҫ����鼮��ʽ�����ǽ�����ʾ�鼮����
        # print re.match(regex, self.inputText.GetValue())
        print self.namelink[self.inputText.GetValue()]
        if(re.match(regex, self.namelink[self.inputText.GetValue()])):
            self.MainTextValueSet(self.inputText.GetValue())

    def OnChar(self, event):  #
        print "call the OnChar!"
        print event.GetKeyCode()

    def OnBtnBackButton(self, event):  # �Զ��尴����Ӧ
        # print type(event)
        print "call the OnBtnBackButton!"
        print event.GetKeyCode()
        if event.GetKeyCode() == 8:  # ������˸��
            self.combotext.SetValue(self.combotext.GetValue()[:-1])  # ɾ��һ���ַ�
            self.combotext.SetInsertionPointEnd()  # ������ƶ����
        elif 32 <= event.GetKeyCode() <= 126:
            print event.GetKeyCode()
            self.combotext.AppendText(chr(event.GetKeyCode()))
        elif event.GetKeyCode() == 9 or event.GetKeyCode() == 317:  # �����Tab�� ���߷�����е�down��
            # print self.mcListPopup.GetFocusedItem()
            if self.combocontrol.IsPopupShown():
                # ѡ�е�һ�������û��item��ѡ�л����Ѿ�ѡ�������һ��item
                if(self.mcListPopup.GetSelectedItemCount() == 0
                   or self.mcListPopup.GetSelection() == self.mcListPopup.GetItemCount() - 1):
                    self.mcListPopup.Select(0)
                    while(self.mcListPopup.ScrollPages(-1)):
                        # ����Ѿ�ѡ�������һ��item��Ȼ����Tab������һֱ���Ϸ�ҳֱ��������
                        pass
                else:
                    print self.mcListPopup.GetItemCount()
                    print self.mcListPopup.GetSelection()
                    self.mcListPopup.ScrollLines(1)
                    # ѡ����һ��
                    self.mcListPopup.Select(
                        self.mcListPopup.GetSelection() + 1, True)
                    self.mcListPopup.Select(
                        self.mcListPopup.GetSelection(), False)  # ����ǰѡ�е�ȡ��ѡ��
            elif not self.combocontrol.IsPopupShown():
                self.combocontrol.ShowPopup()
        elif event.GetKeyCode() == 13:  # ����ǻس���
            if self.combocontrol.IsPopupShown():  # ����Ѿ���������
                print self.mcListPopup.GetSelection()
                if self.mcListPopup.GetSelection() == -1:
                    text = ""
                elif self.combocontrol.IsPopupShown():
                    # ���õ�ǰѡ�е��ı�����
                    text = self.mcListPopup.GetItemText(
                        self.mcListPopup.GetSelection())
                self.combocontrol.HidePopup()  # ����������
                self.combotext.SetValue(text)  # �����ı���Ĵ���
                self.combotext.SetInsertionPointEnd()  # ������ƶ��ı���ĩβ
        elif event.GetKeyCode() == 27:  # �����ǰ���µļ�ΪESC������ر�������
            if self.combocontrol.IsPopupShown():  # ����Ѿ���������
                self.combocontrol.HidePopup()  # ����������
                self.combotext.ChangeValue("")  # ��յ�ǰ�ı����ڵ���������,���Ҳ�����text chhange event
        elif event.GetKeyCode() == 32:  # ����ǿո��
            print "press the kong ge key"
            pass

    def ChangeText(self, event):  # ��Ͽ��ı��䶯�¼���������
        print "call the ChangeText!"
        print self.combotext.GetValue()
        # print event.GetPreviousHandler()
        if(self.combotext.GetValue() == ""):  # �����ǰ��Ͽ��ı�Ϊ�գ��������Ƽ��б���ʾ
            self.mcListPopup.DeleteAllItems()
            names = sorted(self.namelink, key=lambda a: self.namelink[a][0])
            for name in names:
                self.mcListPopup.Append(
                    [name, self.namelink[name][-2], self.namelink[name][-1]])  # ����Append�������һ���ı�
            if not self.combocontrol.IsPopupShown():
                self.combocontrol.ShowPopup()
                # print self.combocontrol.FindFocus()
                # self.combocontrol.Release()
            return
        else:  # �����Ϊ�գ������ƥ�䣬ƥ��ɹ�����ʾƥ��ɹ�����Ŀ�����ɹ�����ʾ������
            Find = False
            Result = []
            for name in self.namelink.keys():
                # ����Ե�ǰ�ı����ڵ����ֿ�ͷ������������Ϊ��ƥ��ɹ��Ľ��
                if name.startswith(self.combotext.GetValue()):
                    Find = True
                    Result.append([name, self.namelink[name][-2],
                                   self.namelink[name][-1]])  # ��ƥ�䵽�����ִ���ƥ����
            if Find and len(Result) != 1:  # ����ҵ�ƥ���ı�����������1������ʾ������
                self.mcListPopup.DeleteAllItems()  # �����ǰ������������ı�
                for res in Result:  # ��ʼ���������ƥ���ı�
                    self.mcListPopup.Append(res)
                if not self.combocontrol.IsPopupShown():  # ���������δ��ʾ������ʾ������
                    self.combocontrol.ShowPopup()
            elif self.combocontrol.IsPopupShown():
                self.combocontrol.HidePopup()

    def test(self, evt):
        # ���԰�ť����
        # self.prefix = "http://book.qidian.com/info/" # ���ÿһ���鼮��ҳ��ַ��ǰ׺ ����ID��Ϊ��ǰ�鼮��ҳ���ַ
        # soup = BeautifulSoup(
        #     markup=self.downloader.download(self.prefix + self.combocontrol.GetValue().split()[-1]),
        #     features='html.parser', from_encoding='utf-8' # ������ǰѡ�е��鼮ҳ�棬����BeautifulSoup����
        # )
        # print soup
        # print help(wx.TextAttr)
        self.inputText.SetDefaultStyle(
            self.combocontrol.GetTextCtrl().GetDefaultStyle())
        self.InputBox.Hide(self.combocontrol)
        self.InputBox.Show(self.inputText)
        print self.inputText.IsShownOnScreen()
        self.Layout()

    def MainTextValueSet(self, value):
        self.MainText.SetValue(value)  # ������Ҫ�ı�����ı�
        f = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                    False)  # ���������ʽ��18�� �������壬����б�����Ӵ�
        self.MainText.SetStyle(0, self.MainText.GetLastPosition(),
                               wx.TextAttr(textColorBackGround, textColorForeGround, f))  # ����ǰ��������ɫ��wx.TextAttr��

    def BarTextValueSet(self, value):
        self.BarText.SetLabel(value)  # ����״̬���ı�
        f = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD,
                    False)  # ����״̬���ı����壺15�� �������壬 ����б���Ӵ�
        self.BarText.SetFont(f)  # ��������
