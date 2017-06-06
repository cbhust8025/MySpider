#!/usr/bin/env python
# encoding: gbk
'''
爬虫主窗口
'''
import wx
import re
from bs4 import BeautifulSoup
from HtmlDownloader import HtmlDownloader
from MyCustomListPopup import MyCustomListPopup
########################################################################
textColorForeGround = "#E9EBFE"  # 文本前景
textColorBackGround = "black"  # 文本背景
combocontrolButtonWidth = 35  # 下拉框按钮的宽度
########################################################################
class MyCustomLP(MyCustomListPopup):
    # 自定义列表框
    def ConfigureListCtrl(self):
        # 重写此函数来进行自定义配置
        # 插入三列进行初始化
        self.InsertColumn(1, "小说名")
        self.InsertColumn(2, "榜单")
        self.InsertColumn(3, "链接")
        # 调整每一列的宽度
        self.SetColumnWidth(0, 200)
        self.SetColumnWidth(1, 150)
        self.SetColumnWidth(2, 300)
        # # 添加三行用作调试，完成后进行注释
        # list.Append(["asa1", "asa2", "asa3", "asa4"])  # 超过当前的列数，触发中断错误
        # self.Append(["asa1", "asa2", "asa3"])
        # self.Append(["asb1", "asb2", "asb3"])
        # self.Append(["asc1", "asc2", "asc3"])
        # self.Append(["asd1asdsadasdsadsadsadasd", "asd2", "asd3"])
        self.SetBackgroundColour(textColorForeGround)  # 设置列表框的文字背景
    # def Append(self, txt):
    #     # 添加一行，以列表形式添加，长度小于等于列数
    #     # self.Append(["asa1", "asa2", "asa3"])
    #     self.Append(txt)
    def GetSelection(self):
        for i in range(self.GetItemCount()):
            if(self.IsSelected(i)):
                return i
        return -1

class Spider(wx.Frame):
    # 爬虫主窗口的构造函数，绑定了右上角的关闭按钮
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title=u"不仅仅是一个爬虫",
                          size=(1200, 900),
                          style=wx.DEFAULT_FRAME_STYLE)
        # 初始化一些窗口内的属性值
        self.namelink = {}  # 保存已经爬取的小说名：[分类，链接] 键值对，用于自动补全后的小说索引链接

        # 绑定右上角关闭窗口
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # 初始化各类对象，用于下载、解析
        self.downloader = HtmlDownloader()  # 初始化下载器

        # 在主窗口放置两个面板
        self.Panel1 = wx.Panel(self)
        self.Panel2 = wx.Panel(self)

        # 面板颜色设置  界面设计完后删除
        self.Panel1.SetBackgroundColour('#FFF2E2')
        self.Panel2.SetBackgroundColour('White')

        # 按钮描述--panel1
        RecommandButton = wx.Button(self.Panel1, label=u'推荐')
        TestButton = wx.Button(self.Panel1, label=u"测试")


        # 按钮功能绑定
        RecommandButton.Bind(wx.EVT_BUTTON, self.recommand)
        TestButton.Bind(wx.EVT_BUTTON, self.test)


        # 文本框控件描述--panel2
        # 初始化组合框
        self.combocontrol = wx.combo.ComboCtrl(parent=self.Panel1, style=wx.CB_SORT)  # 初始化只读格式的组合框
        self.mcListPopup = MyCustomLP()  # 初始化组合框里面的列表框
        self.combocontrol.SetPopupControl(self.mcListPopup)  # 配置组合框中的列表框
        self.combocontrol.SetButtonPosition(width=combocontrolButtonWidth)  # 配置组合框的下拉按钮的宽度
        self.mcListPopup.ConfigureListCtrl()  # 配置列表框
        self.combotext = self.combocontrol.GetTextCtrl()  # 获取组合框中的文本域
        self.combocontrol.Bind(wx.EVT_TEXT, self.ChangeText)
        self.combocontrol.Bind(wx.EVT_KEY_DOWN, self.OnBtnBackButton)
        self.combocontrol.Bind(wx.EVT_CHAR, self.OnChar)
        # wx.TE_PROCESS_ENTER 、wx.TE_PROCESS_TAB 文本框接受tab键（下一项）和回车键（选中当前项）的功能
        self.inputText = wx.TextCtrl(self.Panel1, -1,
                style=wx.TE_RICH2 | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.PROCESS_DEFAULT | wx.TE_AUTO_URL) # 输入文本框
        self.inputText.Bind(wx.EVT_TEXT_ENTER, self.showbookdetail)  # 绑定回车事件到showbookdetail上
        self.MainText = wx.TextCtrl(self.Panel2, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)  # 主要文本显示
        self.MainText.SetOwnBackgroundColour(textColorForeGround)
        self.BarText = wx.StaticText(self.Panel2, -1, style=wx.TE_MULTILINE | wx.TE_RICH2)  # 状态栏显示

        # 窗口设计
        self.InputBox = wx.BoxSizer()  # 横向包含控件--按钮box，放置所有按钮
        self.TextBox = wx.BoxSizer(wx.VERTICAL)  # 横向包含控件--文本框box，放置文本框
        self.Panel1Box = wx.BoxSizer()  # 横向包含控件--面板1box，放置面板1中包含的所有box
        self.Panel2Box = wx.BoxSizer(wx.VERTICAL)  # 纵向包含控件--面板2box，放置面板2中包含的所有box
        self.MainBox = wx.BoxSizer(wx.VERTICAL)  # 纵向包含控件--窗口总box

        # 输入、按钮界面box
        self.InputBox.Add(self.inputText, proportion=10, flag=wx.ALL | wx.EXPAND, border=10)
        self.InputBox.Hide(self.inputText)  # 先隐藏起来，使用组合下拉框
        self.InputBox.Add(self.combocontrol, proportion=10, flag=wx.ALL | wx.EXPAND, border=10)
        self.InputBox.Add(RecommandButton, proportion=1, flag=wx.ALL, border=10)
        self.InputBox.Add(TestButton, proportion=1, flag=wx.ALL, border=10)

        # 文本域界面box
            # wx.EXPAND 参数表示文本框尽可能占满box的剩余空间
        self.TextBox.Add(self.MainText, proportion=25, flag=wx.ALL | wx.EXPAND, border=10)
        self.TextBox.Add(self.BarText, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        # self.TextBox.Hide(self.BarText)

        # 面板1--box设置
        self.Panel1Box.Add(self.InputBox, flag=wx.ALL | wx.EXPAND, border=0)
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

    def SetTextForPopup(self, text):  # 设置下拉框中的文本
        for txt in text:
            self.namelink[txt[0]] = [txt[-2], txt[-1]]
            self.mcListPopup.Append(txt)  # 利用Append方法添加一行文本
        # self.combocontrol.GetTextCtrl().AutoComplete(self.namelink.keys())  # 添加小说名自动补全功能
        # self.combocontrol.GetTextCtrl().Bind(wx.EVT_KEY_DOWN, self.ShowBookDetail)  # 绑定回车事件到showbookdetail上

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
        popuptext = []
        # LinkNum = []
        # regex = re.compile(r"\d{9,20}")
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
            # LinkNum.append(Link.getText() + " " + str(int(regex.findall(Link.get('href'))[0])))
            popuptext.append([Link.getText(), title, Link.get('href')])
        # self.inputText.AutoComplete(choices=LinkNum)  # 原始版本的自动补全功能
        self.SetTextForPopup(popuptext)
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
        print "call the showbookdetail!"
        # 展示书籍详情按钮
        regex = re.compile(r"\S+\d{9,20}$") # 匹配，当输入框输入的满足我们要求的书籍格式，我们进行显示书籍详情
        # print re.match(regex, self.inputText.GetValue())
        print self.namelink[self.inputText.GetValue()]
        if(re.match(regex, self.namelink[self.inputText.GetValue()])):
            self.MainTextValueSet(self.inputText.GetValue())

    def OnChar(self, event):  #
        print "call the OnChar!"
        print event.GetKeyCode()

    def OnBtnBackButton(self, event):  # 自定义按键响应
        print "call the OnBtnBackButton!"
        print event.GetKeyCode()
        if event.GetKeyCode() == 8:  # 如果是退格键
            self.combotext.SetValue(self.combotext.GetValue()[:-1])  # 删除一个字符
            self.combotext.SetInsertionPointEnd()  # 将光标移动最后
        elif 32 <= event.GetKeyCode() <= 126:
            print event.GetKeyCode()
            self.combotext.AppendText(chr(event.GetKeyCode()))
        elif event.GetKeyCode() == 9:  # 如果是Tab键
            if self.combocontrol.IsPopupShown():
                # 选中第一个，如果没有item被选中或者已经选中了最后一个item
                if(self.mcListPopup.GetSelectedItemCount() == 0
                   or self.mcListPopup.GetSelection() == self.mcListPopup.GetItemCount() - 1):
                    self.mcListPopup.Select(0)
                else:
                    print self.mcListPopup.GetItemCount()
                    print self.mcListPopup.GetSelection()
                    # 选中下一个
                    self.mcListPopup.Select(self.mcListPopup.GetSelection() + 1, True)
                    self.mcListPopup.Select(self.mcListPopup.GetSelection(), False)  # 将当前选中的取消选中
            elif not self.combocontrol.IsPopupShown():
                self.combocontrol.ShowPopup()
        elif event.GetKeyCode() == 13:  # 如果是回车键
            if self.combocontrol.IsPopupShown():  # 如果已经打开下拉框
                print self.mcListPopup.GetSelection()
                if self.mcListPopup.GetSelection() == -1:
                    text = ""
                elif self.combocontrol.IsPopupShown():
                    # 设置当前选中的文本内容
                    text = self.mcListPopup.GetItemText(self.mcListPopup.GetSelection())
                self.combocontrol.HidePopup()  # 隐藏下拉框
                self.combotext.SetValue(text)  # 设置文本域的词条
                self.combotext.SetInsertionPointEnd()  # 将光标移动文本域末尾

        elif event.GetKeyCode() == 32:  # 如果是空格键
            print "press the kong ge key"
            pass

    def ChangeText(self, event):  # 组合框文本变动事件触发函数
        print "call the ChangeText!"
        print self.combotext.GetValue()
        if(self.combotext.GetValue() == ""):  # 如果当前组合框文本为空，则下拉推荐列表显示
            self.mcListPopup.DeleteAllItems()
            names = sorted(self.namelink, key=lambda a: self.namelink[a][0])
            for name in names:
                self.mcListPopup.Append([name, self.namelink[name][-2], self.namelink[name][-1]])  # 利用Append方法添加一行文本
            if not self.combocontrol.IsPopupShown():
                self.combocontrol.ShowPopup()
            return
        else:  # 如果不为空，则进行匹配，匹配成功，显示匹配成功的条目，不成功则不显示下拉框
            Find = False
            Result = []
            for name in self.namelink.keys():
                if name.startswith(self.combotext.GetValue()):  # 如果以当前文本域内的文字开头的名称我们认为是匹配成功的结果
                    Find = True
                    Result.append([name, self.namelink[name][-2], self.namelink[name][-1]])  # 将匹配到的文字存入匹配结果
            if Find and len(Result) != 1:  # 如果找到匹配文本的数量大于1，则显示下拉框
                self.mcListPopup.DeleteAllItems()  # 清楚当前下拉框的所有文本
                for res in Result:  # 初始化下拉框的匹配文本
                    self.mcListPopup.Append(res)
                if not self.combocontrol.IsPopupShown():  # 如果下拉框未显示，则显示下拉框
                    self.combocontrol.ShowPopup()
            elif self.combocontrol.IsPopupShown():
                self.combocontrol.HidePopup()


    def test(self, evt):
        # 测试按钮功能
        # self.prefix = "http://book.qidian.com/info/" # 起点每一本书籍网页地址的前缀 加上ID即为当前书籍的页面地址
        # soup = BeautifulSoup(
        #     markup=self.downloader.download(self.prefix + self.combocontrol.GetValue().split()[-1]),
        #     features='html.parser', from_encoding='utf-8' # 解析当前选中的书籍页面，生成BeautifulSoup对象
        # )
        # print soup
        # print help(wx.TextAttr)
        self.inputText.SetDefaultStyle(self.combocontrol.GetTextCtrl().GetDefaultStyle())
        self.InputBox.Hide(self.combocontrol)
        self.InputBox.Show(self.inputText)
        print self.inputText.IsShownOnScreen()
        self.Layout()


    def MainTextValueSet(self, value):
        self.MainText.SetValue(value)  # 设置主要文本域的文本
        f = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)  # 设置字体格式：18号 罗曼字体，不倾斜、不加粗
        self.MainText.SetStyle(0, self.MainText.GetLastPosition(),
            wx.TextAttr(textColorBackGround, textColorForeGround, f))  # 设置前景、背景色（wx.TextAttr）

    def BarTextValueSet(self, value):
        self.BarText.SetLabel(value)  # 设置状态栏文本
        f = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD, False)  # 设置状态栏文本字体：15号 罗曼字体， 不倾斜、加粗
        self.BarText.SetFont(f)  # 进行设置
