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
        TestButton = wx.Button(self.Panel1, label=u"测试")


        # 按钮功能绑定
        RecommandButton.Bind(wx.EVT_BUTTON, self.recommand)
        TestButton.Bind(wx.EVT_BUTTON, self.test)

        # 文本框控件描述--panel2
        # wx.TE_PROCESS_ENTER 、wx.TE_PROCESS_TAB 文本框接受tab键（下一项）和回车键（选中当前项）的功能
        self.inputText = wx.TextCtrl(self.Panel1, -1,
                style=wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.PROCESS_DEFAULT | wx.TE_AUTO_URL) # 输入文本框
        self.inputText.Bind(wx.EVT_TEXT, self.showbookdetail)
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
        self.ButtonBox.Add(self.inputText, proportion=10, flag=wx.ALL | wx.EXPAND, border=10)
        self.ButtonBox.Add(RecommandButton, proportion=1, flag=wx.ALL, border=10)
        self.ButtonBox.Add(TestButton, proportion=1, flag=wx.ALL, border=10)

        # 文本框box
            # wx.EXPAND 参数表示文本框尽可能占满box的剩余空间
        self.TextBox.Add(self.MainText, proportion=25, flag=wx.ALL | wx.EXPAND, border=10)
        self.TextBox.Add(self.BarText, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        # self.TextBox.Hide(self.BarText)

        # 面板1--box设置
        self.Panel1Box.Add(self.ButtonBox, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel1.SetSizer(self.Panel1Box)

        # 面板2--box设置
        self.Panel2Box.Add(self.TextBox, proportion=0, flag=wx.ALL | wx.EXPAND, border=0)
        self.Panel2.SetSizer(self.Panel2Box)

        # 窗口总box
        self.MainBox.Add(self.Panel1, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        self.MainBox.Add(self.Panel2, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # 将box都放到窗口上
        self.SetSizer(self.MainBox)
        self.recommand(wx.wxEVT_COMMAND_BUTTON_CLICKED)  # 开始程序第一步先运行一下推荐系统

    def OnClose(self, evt):
        ret = wx.MessageBox('确认关闭?', '关闭', wx.OK | wx.CANCEL)
        if ret == wx.OK:
            # do something here...
            evt.Skip()

    def GetTextForRecommand(self, titledic):
        text = ""
        titlel = sorted(titledic.keys(), key=lambda a : len(a), reverse=True)  # 按照分类名的长短进行排序
        for title in titlel:  # 格式化输出文本
            text += title + ":\n"
            num = 1
            for book in titledic[title]:
                text += str(num) + ". " + book + "\n"
                num += 1
            text += "\n"
        return text

    def GetLinksForRecommand(self, soup):  # 获取起点主页的所有小说链接
        LinksRes = soup.find_all('a', {  # 小说链接所在Tag标签名为a
            "class": "name",  # 小说链接所在Tag的class属性为“name”
            "data-eid": re.compile("qd_A\d{3}"),  # 小说链接所在Tag的“data-eid”形式为qd_A110这种样式，使用正则表达式进行匹配
            "href": re.compile("//book.qidian.com/info/\d{9,20}")})  # 利用bs4中soup对象的find_all方法，匹配所有小说链接所在的Tag
        titledic = {}  # 将获取到的小说链接名整合进字典，键值为当前小说所在的分类名
        LinkNum = []
        regex = re.compile(r"\d{9,20}")
        for Link in LinksRes:
            linkprevious =  Link.find_previous('h3')  # 离小说最近的前置Tag名为'h3'的Tag即为当前小说所在的分类，“NO.1”这个标签除外
            while(linkprevious.getText() == "NO.1"):
                linkprevious = linkprevious.find_previous('h3')
            # 去除分类名中获取到的“更多”、"24小时内更新15163本"这两个字样
            title = linkprevious.getText().rstrip(u'\u66f4\u591a\ue621')\
                .rstrip(u'24\u5c0f\u65f6\u5185\u66f4\u65b015163\u672c')
            if(titledic.has_key(title)):
                titledic[title].append(Link.getText() + "    " + Link.get('href'))
            else:
                titledic[title] = [Link.getText() + "    " + Link.get('href')]
            LinkNum.append(Link.getText() + " " + str(int(regex.findall(Link.get('href'))[0])))
        self.inputText.AutoComplete(choices=LinkNum)
        return self.GetTextForRecommand(titledic)  # 将生成的分类字典格式化成输出格式，进行返回显示

    def recommand(self, event):
        soup = BeautifulSoup(
            markup=self.downloader.download("http://www.qidian.com/"),
            features='html.parser', from_encoding='utf-8')  # 解析www.qidian.com网站的页面，生成BeautifulSoup对象
        self.MainText.SetEditable(False)  # 将推荐状态下的主要文本框设置成不可编辑状态
        self.MainTextValueSet(self.GetLinksForRecommand(soup))  # 设置推荐小说文本
        self.BarTextValueSet("推荐")  # 设置状态栏
        # 推荐文本进行了格式化输出，已完成基本要求

    def showbookdetail(self, event):
        # 展示书籍详情按钮
        regex = re.compile(r"\S+\s\d{9,20}$") # 匹配，当输入框输入的满足我们要求的书籍格式，我们进行显示书籍详情
        # print re.match(regex, self.inputText.GetValue())
        if(re.match(regex, self.inputText.GetValue())):
            self.MainTextValueSet(self.inputText.GetValue())

    def test(self, evt):
        # 测试按钮功能
        self.prefix = "http://book.qidian.com/info/" # 起点每一本书籍网页地址的前缀 加上ID即为当前书籍的页面地址
        soup = BeautifulSoup(
            markup=self.downloader.download(self.prefix + self.inputText.GetValue().split()[-1]),
            features='html.parser', from_encoding='utf-8' # 解析当前选中的书籍页面，生成BeautifulSoup对象
        )
        print soup

    def MainTextValueSet(self, value):
        self.MainText.SetValue(value)  # 设置主要文本域的文本
        f = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)  # 设置字体格式：18号 罗曼字体，不倾斜、不加粗
        self.MainText.SetStyle(0, self.MainText.GetLastPosition(),
            wx.TextAttr(textColorBackGround, textColorForeGround, f))  # 设置前景、背景色（wx.TextAttr）

    def BarTextValueSet(self, value):
        self.BarText.SetLabel(value)  # 设置状态栏文本
        f = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD, False)  # 设置状态栏文本字体：15号 罗曼字体， 不倾斜、加粗
        self.BarText.SetFont(f)  # 进行设置
