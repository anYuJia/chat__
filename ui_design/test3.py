import wx

def loadframe():
    app = wx.App()

    mywindow = myframe()

    mywindow.Show()

    app.MainLoop()


class myframe(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'saintdingsFrame', size=(1200, 800))

        mypanel = wx.Panel(self, -1, size=(1200, 800))

        # 声明图片对象

        image = wx.Image("D:\desk\docment\me\3_1\python_program_design\file\head_img\user\default_head_img.jpg", wx.BITMAP_TYPE_JPEG)

        print('图片的尺寸为{0}x{1}'.format(image.GetWidth(), image.GetHeight()))

        portion = 0.75

        w = image.GetWidth() * portion

        h = image.GetHeight() * portion

        image.Rescale(w, h)

        mypic = image.ConvertToBitmap()

        # 显示图片

        wx.StaticBitmap(mypanel, -1, bitmap=mypic, pos=(2, 2))

        # 菜单 原则自上至下

        menubar = wx.MenuBar()

        filemenu = wx.Menu()

        menubar.Append(filemenu, '&文件')

        filemenu.Append(wx.ID_NEW, '&新建', '新建文件')

        filemenu.Append(wx.ID_OPEN, '&打开', '打开文件')

        filemenu.Append(wx.ID_SAVE, '&保存', '保存文件')

        filemenu.Append(wx.ID_EXIT, '&退出', '退出程序')

        # 虽然\'编辑\'菜单的结构和\'\文件'菜单的结构大同小异，但必须另实例化Menu类对象

        # 否则将提示C++错误

        editmenu = wx.Menu()

        menubar.Append(editmenu, '&编辑')

        editmenu.Append(wx.ID_OPEN, '&复制', '复制文本')

        editmenu.Append(wx.ID_SAVE, '&粘贴', '粘贴文本')

        editmenu.Append(wx.ID_EXIT, '&剪切', '剪切选中内容')

        editmenu.Append(wx.ID_NEW, '&全选', '文本框内容全选')

        self.SetMenuBar(menubar)

        # 简易文本框

        mytxt = wx.TextCtrl(mypanel, size=(600, 700), pos=(550, 2), style=wx.TE_MULTILINE | wx.HSCROLL)

        mytxt.SetInsertionPoint(0)


if __name__ == '__main__':
    loadframe()
