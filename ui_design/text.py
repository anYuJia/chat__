import wx

TOOL_TITLE = u'游戏打渠道包工具'


# 显示主页面
class GuiMainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1080, 786))
        # 窗体分割
        self.SplitWindow()
        # 窗口居中显示
        self.Center()
        # 调用窗口展示功能<br>
        self.Show(True)

    def SplitWindow(self):
        # 创建一个分割窗,parent是frame
        self.sp = wx.SplitterWindow(self)
        # 创建上子面板
        self.Panel_Top = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        # 创建上子面板
        self.Panel_Bottom = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        # 创建一个子分割窗，parent是Panel_Top
        self.Top = wx.SplitterWindow(self.Panel_Top)
        # 创建一个垂直布局
        self.box = wx.BoxSizer(wx.VERTICAL)
        # 将子分割窗布局延伸至整个空间
        self.box.Add(self.Top, 1, wx.EXPAND)
        self.Panel_Top.SetSizer(self.box)
        # 在子分割窗的基础上创建子画板
        self.Panel_Top_Left = wx.Panel(self.Top, style=wx.SUNKEN_BORDER)
        # 在子分割窗的基础上创建子画板
        self.Panel_Top_Right = wx.Panel(self.Top, style=wx.SUNKEN_BORDER)

        # 分割窗体
        self.sp.SplitHorizontally(self.Panel_Top, self.Panel_Bottom, 450)
        self.Top.SplitVertically(self.Panel_Top_Left, self.Panel_Top_Right, 500)


if __name__ == "__main__":
    # 实例化一个主循环<br>
    app = wx.App()
    # 实例化一个窗口<br>
    frame = GuiMainFrame(None, 'Game')
    # 启动主循环
    app.MainLoop()
