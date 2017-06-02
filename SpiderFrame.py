#!/usr/bin/env python
# encoding: gbk
'''
����������
'''
import wx
import re
from bs4 import BeautifulSoup
from HtmlDownloader import HtmlDownloader
########################################################################
textColorForeGround = "#E9EBFE"
textColorBackGround = "black"
########################################################################
class Spider(wx.Frame):
    # ���������ڵĹ��캯�����������ϽǵĹرհ�ť
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title=u"��������һ������",
                          size=(1200, 900),
                          style=wx.DEFAULT_FRAME_STYLE)
        # �����Ͻǹرմ���
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # ��ʼ����������������ء�����
        self.downloader = HtmlDownloader()  # ��ʼ��������

        # �������ڷ����������
        self.Panel1 = wx.Panel(self)
        self.Panel2 = wx.Panel(self)

        # �����ɫ����
        self.Panel1.SetBackgroundColour('#FFF2E2')
        self.Panel2.SetBackgroundColour('White')

        # ��ť����--panel1
        RecommandButton = wx.Button(self.Panel1, label=u'�Ƽ�')


        # ��ť���ܰ�
        RecommandButton.Bind(wx.EVT_BUTTON, self.recommand)

        # �ı���ؼ�����--panel2
        self.MainText = wx.TextCtrl(self.Panel2, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)  # ��Ҫ�ı���ʾ
        self.MainText.SetOwnBackgroundColour(textColorForeGround)
        self.BarText = wx.StaticText(self.Panel2, -1,style=wx.TE_MULTILINE | wx.TE_RICH2)  # ״̬����ʾ

        # �������
        self.ButtonBox = wx.BoxSizer()  # ��������ؼ�--��ťbox���������а�ť
        self.TextBox = wx.BoxSizer(wx.VERTICAL)  # ��������ؼ�--�ı���box�������ı���
        self.Panel1Box = wx.BoxSizer()  # ��������ؼ�--���1box���������1�а���������box
        self.Panel2Box = wx.BoxSizer(wx.VERTICAL)  # ��������ؼ�--���2box���������2�а���������box
        self.MainBox = wx.BoxSizer(wx.VERTICAL)  # ��������ؼ�--������box

        # ��ťbox
        self.ButtonBox.Add(RecommandButton, proportion=0, flag=wx.ALL, border=10)

        # �ı���box
            # wx.EXPAND ������ʾ�ı��򾡿���ռ��box��ʣ��ռ�
        self.TextBox.Add(self.MainText, proportion=25, flag=wx.ALL | wx.EXPAND, border=10)
        self.TextBox.Add(self.BarText, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        # self.TextBox.Hide(self.BarText)

        # ���1--box����
        self.Panel1Box.Add(self.ButtonBox, proportion=0, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel1.SetSizer(self.Panel1Box)

        # ���2--box����
        self.Panel2Box.Add(self.TextBox, proportion=0, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel2.SetSizer(self.Panel2Box)

        # ������box
        self.MainBox.Add(self.Panel1, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        self.MainBox.Add(self.Panel2, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # ��box���ŵ�������
        self.SetSizer(self.MainBox)

    def OnClose(self, evt):
        ret = wx.MessageBox('ȷ�Ϲر�?', '�ر�', wx.OK | wx.CANCEL)
        if ret == wx.OK:
            # do something here...
            evt.Skip()

    def TitleBookForRecommand(self, LinksRes, targetLink):
        others = [u"�����Ƽ�"]
        for Link in LinksRes:
            print Link
            if(targetLink.has_key(Link['data-eid'])):
                targetLink[Link['data-eid']].append(
                    Link['title'] if (Link.has_attr('title'))
                        else (Link.get_text() if Link.get_text() != "" else Link.findChildren('img')[0]['alt']))
            else:
                others.append(Link['title'] if (Link.has_attr('title')) else Link.get_text())
        return others

    def GetLinksForRecommand(self, soup, targetLink):
        LinksRes = soup.find_all('a', {
            # "class": "name",
            "data-eid": re.compile("qd_A\d{3}"),
            "href": re.compile("//book.qidian.com/info/\d{9,20}")})
        print help(BeautifulSoup)
        others = self.TitleBookForRecommand(LinksRes, targetLink)
        targetLink["qd_A000"] = others
        target = sorted(targetLink, reverse=True)
        # print help(re)
        temp = ""
        for qdA in target:
            if(len(targetLink[qdA]) == 1):
                continue
            temp += targetLink[qdA][0] + ":" + "\n"
            num = 1
            for title in targetLink[qdA][1:]:
                if(title == ""):
                    continue
                temp += str(num) + ". " + title + "\n"
                num += 1
            temp += "\n"
        temp += "\n"
        return temp

    def recommand(self, event):
        soup = BeautifulSoup(
            markup=self.downloader.download("http://www.qidian.com/"),
            features='html.parser', from_encoding='utf-8')
        # print help(soup.find_all)
        targetlink = {
            "qd_A103": [u"����ǿ��"],
            "qd_A110": [u"�༭�Ƽ�"],
            "qd_A113": [u"�����������·�"],
            "qd_A147": [u"���ˡ�ǩԼ�����"],
            "qd_A138": [u"�����Ƽ�"]
        }
        self.MainText.SetEditable(False)
        self.MainTextValueSet(self.GetLinksForRecommand(soup, targetlink))
        self.BarTextValueSet("�Ƽ�")  # ����״̬��

    def MainTextValueSet(self, value):
        self.MainText.SetValue(value)  # ������Ҫ�ı�����ı�
        f = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)  # ���������ʽ��18�� �������壬����б�����Ӵ�
        self.MainText.SetStyle(0, self.MainText.GetLastPosition(),
            wx.TextAttr(textColorBackGround, textColorForeGround, f))  # ����ǰ��������ɫ��wx.TextAttr��

    def BarTextValueSet(self, value):
        self.BarText.SetLabel(value)  # ����״̬���ı�
        f = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD, False)  # ����״̬���ı����壺15�� �������壬 ����б���Ӵ�
        self.BarText.SetFont(f)  # ��������