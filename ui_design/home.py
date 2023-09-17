import datetime
import json
import socket
import threading
import time

import wx

import config.config as config
import ui_design.detail as detail
import ui_design.login as login


class HomeFrame(wx.Frame):
    def __init__(self, parent, uid):
        super().__init__(parent=None, title="主界面", size=(800, 600))
        self.group_show_head_img = None
        self.group_show_introduction = None
        self.group_show_group_name = None
        self.group_show_gid = None
        self.friend_info_frame_phone = None
        self.friend_info_frame_email = None
        self.friend_info_frame_age = None
        self.friend_info_frame_sex = None
        self.friend_info_frame_head_img = None
        self.friend_info_frame_username = None
        self.friend_info_frame_uid = None
        self.friend_info_frame = None
        self.add_friend_frame = None
        friend_info_frame = None
        self.conn = None
        self.port = None
        self.id = 0
        self.uid = int(uid)
        self.client = None
        self.login_socket()
        self.Bind(wx.EVT_CLOSE, self.logout)
        self.chat_msg = []
        self.Center()
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
        self.sp.SplitVertically(self.Panel_Left, self.Panel_Right, int(config.WIDTH * 0.17))
        self.Right.SplitHorizontally(self.Panel_Right_Top, self.Panel_Right_Bottom, 50)
        # 在右底上画板添加聊天框listbox
        self.Text = wx.ListCtrl(self.Panel_Right_Bottom, -1, style=wx.LC_REPORT, pos=(0, 0),
                                size=(int(config.WIDTH * 0.8), int(config.HEIGHT * 0.7)))
        self.Text.InsertColumn(0, '', wx.LIST_FORMAT_RIGHT, width=int(config.WIDTH * 0.1))
        self.Text.InsertColumn(1, '', width=int(config.WIDTH * 0.6))
        self.Text.InsertColumn(2, '', width=int(config.WIDTH * 0.1))
        self.Text.SetBackgroundColour('white')
        self.Text.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 在右底下画板添加输入框
        self.Input = wx.TextCtrl(self.Panel_Right_Bottom, -1, pos=(0, int(config.HEIGHT * 0.7)),
                                 size=(int(config.WIDTH * 0.8), int(config.HEIGHT * 0.2)), style=wx.TE_MULTILINE)
        self.Input.SetBackgroundColour('white')
        self.Input.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 在右下画板添加发送按钮
        self.Button = wx.Button(self.Panel_Right_Bottom, -1, u'发送',
                                pos=(int(config.WIDTH * 0.7), int(config.HEIGHT * 0.9)), size=(60, 40))
        self.Button.SetBackgroundColour('white')
        self.Button.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.Button.Bind(wx.EVT_BUTTON, self.send_message)

        # 设置切换好友列表
        self.friend_button = wx.StaticText(self.Panel_Left, 1, label="好友", pos=(20, 13), size=(40, -1),
                                           style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.friend_button.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 绑定点击切换好友列表事件
        self.friend_button.Bind(wx.EVT_LEFT_DOWN, self.on_click_friend_button)
        # 设置好友群聊之间的分割线
        self.line = wx.StaticText(self.Panel_Left, 1, label="|", pos=(65, 13), size=(5, -1))

        # 设置切换群聊列表
        self.group_button = wx.StaticText(self.Panel_Left, 1, label="群聊", pos=(70, 13), size=(40, -1),
                                          style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.group_button.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 绑定点击切换群聊列表事件
        # self.Bind(wx.EVT_LEFT_DOWN, self.on_click_group_button, self.group_button)
        self.group_button.Bind(wx.EVT_LEFT_DOWN, self.on_click_group_button)
        # 展示列表
        self.showList = []
        self.SList = wx.ListBox(self.Panel_Left, 1, choices=self.showList, style=wx.LB_SINGLE,
                                pos=(10, 50),
                                size=(120, int(config.HEIGHT - 50)))
        self.SList.SetBackgroundColour((220, 220, 220, 0.1))
        self.SList.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.SList.Bind(wx.EVT_LISTBOX, self.on_click_list)
        # 设置退出登录按钮
        self.logout_button = wx.Button(self.Panel_Left, 1, label="退出登录", pos=(25, 510),
                                       size=(80, 30))
        self.logout_button.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 绑定退出登录事件
        self.logout_button.Bind(wx.EVT_BUTTON, self.back_to_login)

        # 设置查看好友信息按钮
        self.info_button = wx.Button(self.Panel_Right_Top, 1, label="", pos=(10, 18),
                                     size=(110, 30))
        self.info_button.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 绑定查看好友信息事件
        self.info_button.Bind(wx.EVT_BUTTON, self.show_detail_info)

        # 设置好友信息
        self.info = wx.StaticText(self.Panel_Right_Top, 2, label="", pos=(int(config.WIDTH * 0.3), 20), size=(100, -1))
        self.info.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.info.SetSize((100, 50))
        #
        # 设置添加好友按钮
        #
        self.add_friend_button = wx.Button(self.Panel_Right_Top, 1, label="添加好友", pos=(int(config.WIDTH * 0.6), 20),
                                           size=(100, 30))
        self.add_friend_button.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 绑定添加好友事件
        self.add_friend_button.Bind(wx.EVT_BUTTON, self.get_add_friend_window)
        #
        # 设置聊天状态True为与好友聊天，False为与群聊聊天
        self.chat_ing = True
        #
        # 加载数据
        self.friend_group_data = [[], []]
        self.load_friend_group_data()
        self.listen_receive_message()

    def show_friend_info(self, data):
        # 设置好友信息
        self.friend_info_frame_uid.SetLabel("uid: " + str(data["uid"]))
        self.friend_info_frame_age.SetLabel("age: " + str(data["age"]))
        self.friend_info_frame_sex.SetLabel("sex:" + str(data["sex"]))
        self.friend_info_frame_head_img.SetLabel("head_img: " + str(data["head_img"]))
        self.friend_info_frame_email.SetLabel("email: " + str(data["email"]))
        self.friend_info_frame_phone.SetLabel("phone: " + str(data["phone"]))

    def show_group_info(self, data):
        self.group_show_group_name.SetLabel("群聊名称: " + str(data["group_name"]))
        self.group_show_gid.SetLabel("群聊id: " + str(data["gid"]))
        self.group_show_head_img.SetLabel("群聊头像: " + str(data["head_img"]))
        self.group_show_introduction.SetLabel("群聊简介: " + str(data["introduction"]))

    # 加载添加好友窗口
    def get_add_friend_window(self, event):
        add_friend_frame = wx.Frame(None, title="添加好友和群聊", size=(300, 150))
        add_friend_frame.Center()
        add_friend_frame.SetBackgroundColour((220, 220, 220, 0.1))
        self.add_friend_uid = wx.TextCtrl(add_friend_frame, 1, pos=(40, 10), size=(150, 30))
        self.add_friend_btn = wx.Button(add_friend_frame, 2, label="添加好友uid/email/phone", pos=(10, 70),
                                        size=(150, 30))
        self.add_group_btn = wx.Button(add_friend_frame, 3, label="添加群聊", pos=(180, 70), size=(100, 30))
        self.add_friend_btn.Bind(wx.EVT_BUTTON, self.add_friend_btn_func)
        self.add_group_btn.Bind(wx.EVT_BUTTON, self.add_group_btn_func)
        add_friend_frame.Show()

    # 向服务器发送添加好友请求
    def add_friend_btn_func(self, event):
        if self.add_friend_uid.GetValue() == "":
            wx.MessageBox("好友ID不能为空", "提示")
            return
        message = {"uid": self.uid, "type": "add_friend", "uid1": self.add_friend_uid.GetValue()}
        self.client.send(json.dumps(message).encode("utf-8"))
        self.add_friend_uid.SetValue("")

    # 验证好友是否添加成功
    def check_add_friend(self, data):
        if data["code"]:
            wx.MessageBox("成功!" + data['username'], "提示")
            self.load_friend_group_data()
        else:
            wx.MessageBox("添加失败  " + data['data'], "提示")
        self.add_friend_frame.Close()

    # 验证群聊是否添加成功
    def check_add_group(self, data):
        if data["code"]:
            wx.MessageBox("成功" + data['group_name'], "提示")
            self.load_friend_group_data()
        else:
            wx.MessageBox("添加失败  " + data['data'], "提示")
        self.add_friend_frame.Close()

    # 向服务器发送添加群聊请求
    def add_group_btn_func(self, event):
        if self.add_friend_uid.GetValue() == "":
            wx.MessageBox("请输入群聊号", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        message = {"uid": self.uid, "type": "add_group", "gid": self.add_friend_uid.GetValue()}
        self.client.send(json.dumps(message).encode("utf-8"))
        self.add_friend_uid.SetValue("")

    def show_detail_info(self, event):
        if self.chat_ing:
            friend_info_frame = wx.Frame(None, title="好友信息", size=(300, 300))
            friend_info_frame.Center()
            friend_info_frame.SetBackgroundColour((220, 220, 220, 0.1))
            # 设置好友信息
            self.friend_info_frame_uid = wx.StaticText(friend_info_frame, 1, label="uid:", pos=(10, 10),
                                                       size=(100, -1))
            self.friend_info_frame_uid.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))

            self.friend_info_frame_username = wx.StaticText(friend_info_frame, 2, label="username:",
                                                            pos=(10, 40), size=(100, -1))
            self.friend_info_frame_username.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
            self.friend_info_frame_head_img = wx.StaticText(friend_info_frame, 3, label="head_img:",
                                                            pos=(10, 70), size=(100, -1))
            self.friend_info_frame_head_img.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
            self.friend_info_frame_sex = wx.StaticText(friend_info_frame, 2, label="sex:",
                                                       pos=(10, 100), size=(100, -1))
            self.friend_info_frame_sex.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
            self.friend_info_frame_age = wx.StaticText(friend_info_frame, 2, label="age:",
                                                       pos=(10, 130), size=(100, -1))
            self.friend_info_frame_age.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
            self.friend_info_frame_phone = wx.StaticText(friend_info_frame, 2, label="phone:",
                                                         pos=(10, 160), size=(100, -1))
            self.friend_info_frame_phone.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
            self.friend_info_frame_email = wx.StaticText(friend_info_frame, 2, label="email:",
                                                         pos=(10, 190), size=(100, -1))
            self.friend_info_frame_email.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
            friend_info_frame.Show()
            message = {"uid": self.uid, "type": "get_friend_info", "uid2": self.id}
            self.client.send(json.dumps(message).encode("utf-8"))
        else:
            group = wx.Frame(None,title="群聊信息", size=(300, 150))
            group.Center()
            self.group_show_gid = wx.StaticText(group, 1, label="gid:", pos=(10, 10),
                                                size=(250, -1))
            self.group_show_group_name = wx.StaticText(group, 2, label="group_name:",
                                                       pos=(10, 30), size=(250, -1))
            self.group_show_head_img = wx.StaticText(group, 3, label="head_img:",
                                                     pos=(10, 50), size=(250, -1))
            self.group_show_introduction = wx.StaticText(group, 2, label="introduction:",
                                                         pos=(10, 70), size=(250, -1))
            group.Show()
            message = {"uid": self.uid, "type": "get_group_info", "gid": self.id}
            self.client.send(json.dumps(message).encode("utf-8"))

    # 登录创建socket连接告诉服务器登录的用户ip,port
    def login_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((config.HOST, config.PORT))
        user = {"uid": self.uid, "type": "login"}
        self.client.send(json.dumps(user).encode("utf-8"))

    def on_click_friend_button(self, event):
        friend_username_list = []
        if self.friend_group_data[0] is not None:
            for i in range(len(self.friend_group_data[0])):
                friend_username_list.append(self.friend_group_data[0][i]["username"])
        friend_list = friend_username_list
        self.SList.Set(friend_list)

    def on_click_group_button(self, event):
        group_name_list = []
        if self.friend_group_data[1] is not None:
            for i in range(len(self.friend_group_data[1])):
                group_name_list.append(self.friend_group_data[1][i]["group_name"])
        group_list = group_name_list
        self.SList.Set(group_list)

    # 点击列表加载消息
    def on_click_list(self, event):
        # 设置好友信息
        self.info.SetLabel(event.GetString())
        # 获取好友id或者群聊id
        # 设置聊天状态True为与好友聊天，False为与群聊聊天
        for i in range(len(self.friend_group_data[0])):
            if self.friend_group_data[0][i]["username"] == event.GetString():
                self.id = self.friend_group_data[0][i]["uid"]
                self.load_friend_message()
                self.info_button.SetLabel("查看好友信息")
                self.chat_ing = True
                break

        for i in range(len(self.friend_group_data[1])):
            if self.friend_group_data[1][i]["group_name"] == event.GetString():
                self.id = self.friend_group_data[1][i]["gid"]
                self.load_group_message()
                self.info_button.SetLabel("查看群聊信息")
                self.chat_ing = False
                break
        # 加载消息

    def get_send_text(self):
        return self.Input.GetValue()

    def clear_send_text(self):
        self.Input.Clear()

    def listen_receive_message(self):
        # 创建子进程监听
        p = threading.Thread(target=self.receive_message)
        p.start()

    def send_message(self, event):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = self.get_send_text()
        self.clear_send_text()
        total = self.Text.GetItemCount()
        indexItem_time = self.Text.InsertItem(total, str(total + 1))
        indexItem = self.Text.InsertItem(total + 1, str(total + 2))
        self.Text.SetItem(indexItem_time, 0, "")
        self.Text.SetItem(indexItem_time, 1, time)
        self.Text.SetItem(indexItem_time, 2, "")
        self.Text.SetItem(indexItem, 0, "")
        self.Text.SetItem(indexItem, 1, message)
        self.Text.SetItem(indexItem, 2, "我")
        if self.chat_ing:
            send_message = {"type": "user_message", "uid1": self.uid, "uid2": self.id, "message": message,
                            "time": time}
            self.client.sendall(json.dumps(send_message).encode('utf-8'))
        else:
            send_message = {"type": "group_message", "gid": self.id, "uid": self.uid, "message": message,
                            "time": time}
            self.client.sendall(json.dumps(send_message).encode('utf-8'))

    def receive_message(self):
        while True:
            try:
                data = self.client.recv(1024 * 3).decode('utf-8')
                data = json.loads(data)
                # print(data)
                if data['type'] == 'user_message':
                    if int(data['uid1']) == self.id and int(data['uid2']) == int(self.uid):
                        total = self.Text.GetItemCount()
                        indexItem_time = self.Text.InsertItem(total, str(total + 1))
                        indexItem = self.Text.InsertItem(total + 1, str(total + 2))
                        self.Text.SetItem(indexItem_time, 0, "")
                        self.Text.SetItem(indexItem_time, 1, data['time'])
                        self.Text.SetItem(indexItem_time, 2, "")
                        self.Text.SetItem(indexItem, 0, "对方")
                        self.Text.SetItem(indexItem, 1, data['message'])
                        self.Text.SetItem(indexItem, 2, '')
                elif data['type'] == 'group_message':
                    if int(data['gid']) == self.id:
                        total = self.Text.GetItemCount()
                        indexItem_time = self.Text.InsertItem(total, str(total + 1))
                        indexItem = self.Text.InsertItem(total + 1, str(total + 2))
                        self.Text.SetItem(indexItem_time, 0, "")
                        self.Text.SetItem(indexItem_time, 1, data['time'])
                        self.Text.SetItem(indexItem_time, 2, "")
                        # 发消息的user的uid为data['uid']，此时还不知道有无有用，先留着
                        self.Text.SetItem(indexItem, 0, str(data["username"]))
                        self.Text.SetItem(indexItem, 1, data['message'])
                        self.Text.SetItem(indexItem, 2, "")
                elif data['type'] == 'friend_group_data':
                    self.friend_group_data = data['data']
                    self.on_click_friend_button(self.friend_button)
                elif data['type'] == 'user_message_list':
                    self.set_user_message(data['data'])
                elif data['type'] == 'group_message_list':
                    self.set_group_message(data['data'])
                elif data['type'] == 'friend_info':
                    self.show_friend_info(data['data'])
                elif data['type'] == 'group_info':
                    self.show_group_info(data['data'])
                elif data['type'] == 'add_friend_result':
                    self.check_add_friend(data)
                elif data['type'] == 'add_group_result':
                    self.check_add_group(data)
                time.sleep(0.5)
            except:
                continue

    # 加载好友群聊列表数据
    def load_friend_group_data(self):
        # 发送消息给服务器，获取好友列表
        message = {"type": "get_friend_group_data", "uid": self.uid}
        self.client.sendall(json.dumps(message).encode('utf-8'))

    # 请求私聊消息
    def load_friend_message(self):
        # 发送消息给服务器，获取聊天记录
        message = {"type": "get_user_message", "uid1": self.uid, "uid2": self.id}
        self.client.sendall(json.dumps(message).encode('utf-8'))

    # 加载用户聊天记录
    def set_user_message(self, message_list):
        self.Text.DeleteAllItems()
        for i in range(len(message_list)):
            total = self.Text.GetItemCount()
            indexItem_time = self.Text.InsertItem(total, str(total + 1))
            indexItem = self.Text.InsertItem(total + 1, str(total + 2))
            if int(message_list[i]["uid1"]) == int(self.uid):
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_list[i]["time"]))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, "")
                self.Text.SetItem(indexItem, 1, message_list[i]["message"])
                self.Text.SetItem(indexItem, 2, "我")
            else:
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_list[i]["time"]))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, "对方")
                self.Text.SetItem(indexItem, 1, message_list[i]["message"])
                self.Text.SetItem(indexItem, 2, "")

    def back_to_login(self, event):
        self.logout(event)
        app = wx.App()
        frame = login.LoginFrame(None, self.uid, None)
        frame.Show(True)
        app.MainLoop()

    def load_group_message(self):
        message = {"type": "get_group_message", "gid": self.id, "uid": self.uid}
        self.client.send(json.dumps(message).encode('utf-8'))

    def set_group_message(self, message_list):
        self.Text.DeleteAllItems()
        for i in range(len(message_list)):
            total = self.Text.GetItemCount()
            indexItem_time = self.Text.InsertItem(total, str(total + 1))
            indexItem = self.Text.InsertItem(total + 1, str(total + 2))
            if int(message_list[i]['uid']) == int(self.uid):
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_list[i]['time']))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, "")
                self.Text.SetItem(indexItem, 1, message_list[i]['message'])
                self.Text.SetItem(indexItem, 2, "我")
            else:
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_list[i]['time']))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, str(message_list[i]['username']))
                self.Text.SetItem(indexItem, 1, message_list[i]['message'])
                self.Text.SetItem(indexItem, 2, "")

    # 退出登录，告诉服务器此账号已下线
    def logout(self, event):
        self.client.sendall(json.dumps({"type": "logout", "uid": self.uid}).encode('utf-8'))
        self.client.close()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = HomeFrame(None, 1)
    frame.Show(True)
    app.MainLoop()
