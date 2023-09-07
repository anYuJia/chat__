import wx

import config.config as config
import res.func as res
import ui_design.login as login


class RegisterFrame(wx.Frame):
    def __init__(self, superion):
        wx.Frame.__init__(self, parent=superion, title="注册界面", size=(config.WIDTH, config.HEIGHT))
        self.Center()
        self.panel = wx.Panel(self)
        # 设置欢迎注册的字体
        self.label = wx.StaticText(self.panel, label="欢迎注册", pos=(0, int(config.HEIGHT * 0.02)),
                                   size=(config.WIDTH, -1), style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.label.SetFont(font=wx.Font(int(config.HEIGHT * 0.05), wx.ROMAN, wx.ITALIC, wx.NORMAL))
        # 设置用户名框
        self.label_user = wx.StaticText(self.panel, label="用户名",
                                        pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.15)),
                                        size=(int(config.WIDTH * 0.3), -1))
        self.label_user.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.text_user = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.15)),
                                     size=(int(config.WIDTH * 0.3), -1))
        # 绑定用户名框的事件
        self.text_user.Bind(wx.EVT_TEXT, self.user_check_event)
        # 设置用户名检测
        self.user_check = wx.StaticText(self.panel, label="", pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.15)),
                                        size=(int(config.WIDTH * 0.3), -1))
        self.user_check.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 设置密码框
        self.label_password = wx.StaticText(self.panel, label="密码",
                                            pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.25)),
                                            size=(int(config.WIDTH * 0.3), -1))
        self.label_password.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.text_password = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.25)),
                                         size=(int(config.WIDTH * 0.3), -1), style=wx.TE_PASSWORD)
        # 绑定密码框的事件
        self.text_password.Bind(wx.EVT_TEXT, self.password_check_event)
        # 限制密码框的输入
        self.text_password.SetMaxLength(16)
        # 设置密码检测
        self.password_check = wx.StaticText(self.panel, label="",
                                            pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.25)),
                                            size=(int(config.WIDTH * 0.3), -1))
        self.password_check.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        # 设置确认密码框
        self.label_password_confirm = wx.StaticText(self.panel, label="确认密码",
                                                    pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.35)),
                                                    size=(int(config.WIDTH * 0.3), -1))
        self.label_password_confirm.SetFont(
            font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.text_password_confirm = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.35)),
                                                 size=(int(config.WIDTH * 0.3), -1), style=wx.TE_PASSWORD)
        # 绑定确认密码框的事件
        self.text_password_confirm.Bind(wx.EVT_TEXT, self.password_confirm_check_event)
        # 限制确认密码框的输入
        self.text_password_confirm.SetMaxLength(16)
        # 设置确认密码检测
        self.password_confirm_check = wx.StaticText(self.panel, label="",
                                                    pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.35)),
                                                    size=(int(config.WIDTH * 0.3), -1))
        self.password_confirm_check.SetFont(
            font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 设置性别框
        sex_list = ['男', '女']
        self.label_sex = wx.StaticText(self.panel, label="性别",
                                       pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.45)),
                                       size=(int(config.WIDTH * 0.1), -1))
        self.label_sex.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.box_sex = wx.ComboBox(self.panel, -1, value="男", choices=sex_list,
                                   pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.45)),
                                   size=(int(config.WIDTH * 0.03 + 20), -1), style=wx.CB_DROPDOWN)
        self.box_sex.SetFont(font=wx.Font(int(config.HEIGHT * 0.015 + 5), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 设置邮箱框
        self.label_email = wx.StaticText(self.panel, label="邮箱",
                                         pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.55)),
                                         size=(int(config.WIDTH * 0.3), -1))
        self.label_email.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.text_email = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.55)),
                                      size=(int(config.WIDTH * 0.3), -1))
        # 绑定邮箱框的事件
        self.text_email.Bind(wx.EVT_TEXT, self.email_check_event)
        # 设置邮箱检测
        self.email_check = wx.StaticText(self.panel, label="", pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.55)),
                                         size=(int(config.WIDTH * 0.3), -1))
        self.email_check.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        # 设置电话框
        self.label_phone = wx.StaticText(self.panel, label="电话",
                                         pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.65)),
                                         size=(int(config.WIDTH * 0.3), -1))
        self.label_phone.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        self.text_phone = wx.TextCtrl(self.panel, pos=(int(config.WIDTH * 0.4), int(config.HEIGHT * 0.65)),
                                      size=(int(config.WIDTH * 0.3), -1))
        # 绑定电话框的事件
        self.text_phone.Bind(wx.EVT_TEXT, self.phone_check_event)
        # 设置电话检测
        self.phone_check = wx.StaticText(self.panel, label="", pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.65)),
                                         size=(int(config.WIDTH * 0.3), -1))
        self.phone_check.SetFont(font=wx.Font(int(config.HEIGHT * 0.025), wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        # 设置注册按钮
        self.button_register = wx.Button(self.panel, label="注册",
                                         pos=(int(config.WIDTH * 0.3), int(config.HEIGHT * 0.75)),
                                         size=(int(config.WIDTH * 0.1), -1))
        self.button_register.Bind(wx.EVT_BUTTON, self.register)
        # 设置返回按钮
        self.button_back = wx.Button(self.panel, label="返回", pos=(int(config.WIDTH * 0.6), int(config.HEIGHT * 0.75)),
                                     size=(int(config.WIDTH * 0.1), -1))
        self.button_back.Bind(wx.EVT_BUTTON, self.back_to_login)

    def register(self, event):
        message = ''
        if not self.user_check_event(event):
            message = '用户名不合法\n'
            wx.MessageBox(message)
        elif not self.password_check_event(event):
            message = '密码不合法\n'
            wx.MessageBox(message)
        elif not self.password_confirm_check_event(event):
            message = '确认密码不合法\n'
            wx.MessageBox(message)
        elif not self.email_check_event(event):
            message = '邮箱不合法\n'
            wx.MessageBox(message)
        elif not self.phone_check_event(event):
            message = '电话不合法\n'
            wx.MessageBox(message)
        else:
            user = {'username': self.text_user.GetValue(), 'password': self.text_password.GetValue(),
                    'email': self.text_email.GetValue(), 'phone': self.text_phone.GetValue(),
                    'sex': self.box_sex.GetValue()}
            R = res.Register(user)
            if R[0]:
                message = '注册成功\n你的uid为' + str(R[1])
                wx.MessageBox(message)
                self.Close(True)
                a = wx.App()
                f = login.LoginFrame(None, R[1], user['password'])
                f.Show(True)
                a.MainLoop()
            else:
                message = "电话或者邮箱已经绑定了别的账号，先取消绑定再来注册\n"
                wx.MessageBox(message)

    def back_to_login(self, event):
        self.Close(True)
        app = wx.App()
        frame = login.LoginFrame(None)
        frame.Show(True)
        app.MainLoop()

    def user_check_event(self, event):
        if self.text_user.GetValue() == '':
            self.user_check.SetLabel("")
            return False
        elif len(self.text_user.GetValue()) > 10:
            self.user_check.SetForegroundColour("red")
            self.user_check.SetLabel("用户名不能超过10个字符")
            return False
        else:
            self.user_check.SetForegroundColour("green")
            self.user_check.SetLabel("ok!")
            return True

    def password_check_event(self, event):
        for i in self.text_password.GetValue():
            if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
                self.password_check.SetForegroundColour("red")
                self.password_check.SetLabel("密码只能包含数字和字母")
                return False
        if self.text_password.GetValue() == '':
            self.password_check.SetLabel("")
            return False
        elif len(self.text_password.GetValue()) > 16 or len(self.text_password.GetValue()) < 6:
            self.password_check.SetForegroundColour("red")
            self.password_check.SetLabel("密码不能超过16个字符或少于6个字符")
            return False
        else:
            self.password_check.SetForegroundColour("green")
            self.password_check.SetLabel("ok!")
            return True

    def password_confirm_check_event(self, event):
        if self.text_password_confirm.GetValue() == '':
            self.password_confirm_check.SetLabel("")
            return False
        elif self.text_password_confirm.GetValue() != self.text_password.GetValue():
            self.password_confirm_check.SetForegroundColour("red")
            self.password_confirm_check.SetLabel("两次密码不一致")
            return False
        else:
            self.password_confirm_check.SetForegroundColour("green")
            self.password_confirm_check.SetLabel("ok!")
            return True

    def email_check_event(self, event):
        for i in self.text_email.GetValue():
            if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.':
                self.email_check.SetForegroundColour("red")
                self.email_check.SetLabel("邮箱只能包含数字、字母、@和.")
                return False
        if self.text_email.GetValue() == '':
            self.email_check.SetLabel("")
            return False
        elif len(self.text_email.GetValue()) > 30:
            self.email_check.SetForegroundColour("red")
            self.email_check.SetLabel("邮箱不能超过30个字符")
            return False
        elif '@' not in self.text_email.GetValue() \
                or '.' not in self.text_email.GetValue() \
                or self.text_email.GetValue()[-1] == '.' \
                or self.text_email.GetValue().index('@') > self.text_email.GetValue().index('.'):
            self.email_check.SetForegroundColour("red")
            self.email_check.SetLabel("邮箱格式错误")
            return False
        else:
            self.email_check.SetForegroundColour("green")
            self.email_check.SetLabel("ok!")
            return True

    def phone_check_event(self, event):
        for i in self.text_phone.GetValue():
            if i not in '0123456789':
                self.phone_check.SetForegroundColour("red")
                self.phone_check.SetLabel("电话只能包含数字")
                return False
        if self.text_phone.GetValue() == '':
            self.phone_check.SetLabel("")
            return False
        elif len(self.text_phone.GetValue()) != 11:
            self.phone_check.SetForegroundColour("red")
            self.phone_check.SetLabel("电话只能为11个字符")
            return False
        else:
            self.phone_check.SetForegroundColour("green")
            self.phone_check.SetLabel("ok!")
            return True


if __name__ == '__main__':
    app = wx.App()
    frame = RegisterFrame(None)
    frame.Show(True)
    app.MainLoop()
