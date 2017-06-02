#!/usr/bin/env python
# encoding: gbk
'''
爬虫主窗口
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
    # 爬虫主窗口的构造函数，绑定了右上角的关闭按钮
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title=u"不仅仅是一个爬虫",
                          size=(1200, 900),
                          style=wx.DEFAULT_FRAME_STYLE)
        # 绑定右上角关闭窗口
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # 初始化各类对象，用于下载、解析
        self.downloader = HtmlDownloader()  # 初始化下载器

        # 在主窗口放置两个面板
        self.Panel1 = wx.Panel(self)
        self.Panel2 = wx.Panel(self)

        # 面板颜色设置
        self.Panel1.SetBackgroundColour('#FFF2E2')
        self.Panel2.SetBackgroundColour('White')

        # 按钮描述--panel1
        RecommandButton = wx.Button(self.Panel1, label=u'推荐')


        # 按钮功能绑定
        RecommandButton.Bind(wx.EVT_BUTTON, self.recommand)

        # 文本框控件描述--panel2
        self.MainText = wx.TextCtrl(self.Panel2, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)  # 主要文本显示
        self.MainText.SetOwnBackgroundColour(textColorForeGround)
        self.BarText = wx.StaticText(self.Panel2, -1,style=wx.TE_MULTILINE | wx.TE_RICH2)  # 状态栏显示

        # 窗口设计
        self.ButtonBox = wx.BoxSizer()  # 横向包含控件--按钮box，放置所有按钮
        self.TextBox = wx.BoxSizer(wx.VERTICAL)  # 横向包含控件--文本框box，放置文本框
        self.Panel1Box = wx.BoxSizer()  # 横向包含控件--面板1box，放置面板1中包含的所有box
        self.Panel2Box = wx.BoxSizer(wx.VERTICAL)  # 纵向包含控件--面板2box，放置面板2中包含的所有box
        self.MainBox = wx.BoxSizer(wx.VERTICAL)  # 纵向包含控件--窗口总box

        # 按钮box
        self.ButtonBox.Add(RecommandButton, proportion=0, flag=wx.ALL, border=10)

        # 文本框box
            # wx.EXPAND 参数表示文本框尽可能占满box的剩余空间
        self.TextBox.Add(self.MainText, proportion=25, flag=wx.ALL | wx.EXPAND, border=10)
        self.TextBox.Add(self.BarText, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        # self.TextBox.Hide(self.BarText)

        # 面板1--box设置
        self.Panel1Box.Add(self.ButtonBox, proportion=0, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel1.SetSizer(self.Panel1Box)

        # 面板2--box设置
        self.Panel2Box.Add(self.TextBox, proportion=0, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel2.SetSizer(self.Panel2Box)

        # 窗口总box
        self.MainBox.Add(self.Panel1, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        self.MainBox.Add(self.Panel2, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # 将box都放到窗口上
        self.SetSizer(self.MainBox)

    def OnClose(self, evt):
        ret = wx.MessageBox('确认关闭?', '关闭', wx.OK | wx.CANCEL)
        if ret == wx.OK:
            # do something here...
            evt.Skip()

    def TitleBookForRecommand(self, LinksRes, targetLink):
        others = [u"其他推荐"]
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
            "qd_A103": [u"本周强推"],
            "qd_A110": [u"编辑推荐"],
            "qd_A113": [u"三江·网文新风"],
            "qd_A147": [u"新人·签约新书榜"],
            "qd_A138": [u"新书推荐"]
        }
        self.MainText.SetEditable(False)
        self.MainTextValueSet(self.GetLinksForRecommand(soup, targetlink))
        self.BarTextValueSet("推荐")  # 设置状态栏

    def MainTextValueSet(self, value):
        self.MainText.SetValue(value)  # 设置主要文本域的文本
        f = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)  # 设置字体格式：18号 罗曼字体，不倾斜、不加粗
        self.MainText.SetStyle(0, self.MainText.GetLastPosition(),
            wx.TextAttr(textColorBackGround, textColorForeGround, f))  # 设置前景、背景色（wx.TextAttr）

    def BarTextValueSet(self, value):
        self.BarText.SetLabel(value)  # 设置状态栏文本
        f = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD, False)  # 设置状态栏文本字体：15号 罗曼字体， 不倾斜、加粗
        self.BarText.SetFont(f)  # 进行设置