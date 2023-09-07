import wx

TOOL_TITLE = u'游戏打渠道包工具'


# 显示主页面
class GuiMainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1080, 786))

        self.sp = wx.SplitterWindow(self)
        # 创建左子面板
        self.Panel_Left = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        # 创建右子面板
        self.Panel_Right = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        # 创建一个子分割窗，parent是Panel_Right
        self.Right = wx.SplitterWindow(self.Panel_Right)
        # 创建一个水平布局
        self.box = wx.BoxSizer(wx.VERTICAL)
        # 将子分割窗布局延伸至整个空间
        self.box.Add(self.Right, 1, wx.EXPAND)
        self.Panel_Right.SetSizer(self.box)
        # 在子分割窗的基础上创建子画板
        self.Panel_Right_Top = wx.Panel(self.Right, style=wx.SUNKEN_BORDER)
        # 在子分割窗的基础上创建子画板
        self.Panel_Right_Bottom = wx.Panel(self.Right, style=wx.SUNKEN_BORDER)
        # 分割窗体
        self.sp.SplitHorizontally(self.Panel_Left, self.Panel_Right, 50)
        self.Right.SplitVertically(self.Panel_Right_Top, self.Panel_Right_Bottom, 100)
        # 在右底上画板添加聊天框listbox
        self.Text = wx.ListCtrl(self.Panel_Right_Bottom, -1,  style=wx.LC_REPORT, pos=(0,0), size=(900, 420))
        self.Text.InsertColumn(0, '', width=100)
        self.Text.InsertColumn(1, '', width=700)
        self.Text.InsertColumn(2, '', wx.LIST_FORMAT_RIGHT, 100)
        self.Text.SetBackgroundColour('white')
        self.Text.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 在右底下画板添加输入框
        self.Input = wx.TextCtrl(self.Panel_Right_Bottom, -1,pos=(0,420), size=(900, 180), style=wx.TE_MULTILINE)
        self.Input.SetBackgroundColour('white')
        self.Input.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 在右下画板添加发送按钮
        self.Button = wx.Button(self.Panel_Right_Bottom, -1, u'发送', pos=(860, 610), size=(60, 40))
        self.Button.SetBackgroundColour('white')
        self.Button.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # 窗口居中显示
        self.Center()
        # 调用窗口展示功能<br>
        self.Show(True)


if __name__ == "__main__":
    # 实例化一个主循环<br>
    app = wx.App()
    # 实例化一个窗口<br>
    frame = GuiMainFrame(None, 'Game')
    # 启动主循环
    app.MainLoop()
