import wx

import config.config as config
import res.func as res
import ui_design.home as home
import ui_design.register as register


def login(user, password):
    if user == "" or password == "":
        message = "用户名或密码不能为空"
        wx.MessageBox(message)
    else:
        message = "登录成功"
        wx.MessageBox(message)


class LoginFrame(wx.Frame):
    def __init__(self, superion, uid=None, password=None):
        wx.Frame.__init__(self, parent=superion, title="登录界面", size=(config.WIDTH, config.HEIGHT))
        # 设置窗口居中
        self.Center()
        self.panel = wx.Panel(self)
        # 设置欢迎使用的字体
        self.label = wx.StaticText(self.panel, label="欢迎使用", pos=(0, int(config.HEIGHT * 0.15)),
                                   size=(config.WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.label.SetFont(font=wx.Font(int(config.HEIGHT * 0.08), wx.ROMAN, wx.ITALIC, wx.NORMAL))
        # 设置用户名
        self.label_user = wx.StaticText(self.panel, label="uid/手机号/邮箱",
                                        pos=(int(config.WIDTH * 0.25), int(config.HEIGHT * 0.46)),
                                        size=(int(config.WIDTH * 0.3), -1))
        self.label_user.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.user = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.45)),
                                size=(int(config.WIDTH * 0.25), int(config.HEIGHT * 0.05)))
        self.user.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 限制用户名的长度
        self.user.SetMaxLength(30)
        # 设置用户名检测提示
        self.label_user_check = wx.StaticText(self.panel, label="",
                                              pos=(int(config.WIDTH * 0.65), int(config.HEIGHT * 0.46)),
                                              size=(int(config.WIDTH * 0.3), -1))
        self.label_user_check.SetFont(
            font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 绑定检测事件
        self.user.Bind(wx.EVT_TEXT, self.check_user_event)

        # 设置密码
        self.label_password = wx.StaticText(self.panel, label="密码",
                                            pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.605)),
                                            size=(100, -1))
        self.label_password.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.password = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.59)),
                                    size=(int(config.WIDTH * 0.25), int(config.HEIGHT * 0.05)), style=wx.TE_PASSWORD)
        self.password.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 限制密码的长度
        self.password.SetMaxLength(16)
        # 设置密码检测提示
        self.label_password_check = wx.StaticText(self.panel, label="",
                                                  pos=(int(config.WIDTH * 0.65), int(config.HEIGHT * 0.605)),
                                                  size=(int(config.WIDTH * 0.3), -1))
        self.label_password_check.SetFont(
            font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 绑定检测事件
        self.password.Bind(wx.EVT_TEXT, self.check_password_event)

        # 设置登录按钮
        self.button_login = wx.Button(self.panel, label="登录",
                                      pos=(int(config.WIDTH * 0.48), int(config.HEIGHT * 0.7)),
                                      size=(int(config.WIDTH * 0.1), int(config.HEIGHT * 0.05)))
        self.button_login.SetFont(font=wx.Font(int(config.HEIGHT * 0.03), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 给登录按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.login, self.button_login)

        # 设置注册按钮
        self.button_register = wx.StaticText(self.panel, label="没有账户？点击注册",
                                             pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.8)),
                                             size=(int(config.WIDTH * 0.1), int(config.HEIGHT * 0.02)))
        self.button_register.SetFont(font=wx.Font(int(config.HEIGHT * 0.02), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.button_register.Bind(wx.EVT_LEFT_DOWN, self.register)
        self.init_user_password(uid, password)

    def init_user_password(self, uid, password):
        if uid is not None and password is not None:
            self.user.SetValue(str(uid))
            self.password.SetValue(str(password))

    # 设置登录按钮的事件
    def login(self, event):
        user = self.user.GetValue()
        password = self.password.GetValue()
        R = res.Login(user, password)
        if R[0]:
            wx.MessageBox("登录成功", "提示", wx.OK | wx.ICON_INFORMATION)
            self.Close(True)
            app = wx.App()
            frame = home.HomeFrame(None, R[1])
            frame.Show()
            app.MainLoop()
        else:
            wx.MessageBox("登录失败,请检查一下账号密码", "提示", wx.OK | wx.ICON_INFORMATION)

    # 关闭窗口
    def close(self, event):
        self.Close(True)

    # 设置注册按钮的事件
    def register(self, event):
        self.Close(True)
        app = wx.App()
        frame = register.RegisterFrame(None)
        frame.Show(True)
        app.MainLoop()

    def check_user_event(self, event):
        for i in self.user.GetValue():
            if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@.":
                self.label_user_check.SetForegroundColour("red")
                self.label_user_check.SetLabel("只能包含数字、字母、@、.")
                return False
        if self.user.GetValue() == "":
            self.label_user_check.SetLabel("")
            return False
        elif len(self.user.GetValue()) > 30:
            self.label_user_check.SetForegroundColour("red")
            self.label_user_check.SetLabel("长度不能超过30")
            return False
        else:
            self.label_user_check.SetForegroundColour("green")
            self.label_user_check.SetLabel("ok")
            return True

    def check_password_event(self, event):
        for i in self.password.GetValue():
            if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
                self.label_password_check.SetForegroundColour("red")
                self.label_password_check.SetLabel("密码只能包含数字和字母")
                return False
        if self.password.GetValue() == '':
            self.label_password_check.SetLabel("")
            return False
        elif len(self.password.GetValue()) > 16 or len(self.password.GetValue()) < 6:
            self.label_password_check.SetForegroundColour("red")
            self.label_password_check.SetLabel("密码不能超过16个字符或少于6个字符")
            return False
        else:
            self.label_password_check.SetForegroundColour("green")
            self.label_password_check.SetLabel("ok!")
            return True
