import datetime
import json
import socket
import threading
import time

import wx

import config.config as config
import res.func as res
import ui_design.login as login


class HomeFrame(wx.Frame):
    def __init__(self, parent, uid):
        super().__init__(parent=None, title="主界面", size=(800, 600))
        self.conn = None
        self.port = None
        self.id = 0
        self.uid = int(uid)
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

        # 设置好友信息
        self.info = wx.StaticText(self.Panel_Right_Top, 2, label="", pos=(int(config.WIDTH * 0.3), 20), size=(100, -1))
        self.info.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.info.SetSize((100, 50))
        #
        # 设置聊天状态True为与好友聊天，False为与群聊聊天
        self.chat_ing = True
        #
        # 加载数据
        self.friend_group_data = ()
        self.load_friend_group_data()
        self.client = None
        self.login_socket()
        self.listen_receive_message()

    # 登录创建socket连接告诉服务器登录的用户ip,port
    def login_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((config.HOST, config.PORT))
        user = {"uid": self.uid, "type": "login"}
        self.client.send(json.dumps(user).encode("utf-8"))

    def on_click_friend_button(self, event):
        friend_username_list = []
        for i in range(len(self.friend_group_data[0])):
            friend_username_list.append(self.friend_group_data[0][i].username)
        friend_list = friend_username_list
        self.SList.Set(friend_list)

    def on_click_group_button(self, event):
        group_name_list = []
        for i in range(len(self.friend_group_data[1])):
            group_name_list.append(self.friend_group_data[1][i].group_name)
        group_list = group_name_list
        self.SList.Set(group_list)

    # 点击列表加载消息
    def on_click_list(self, event):
        # 设置好友信息
        self.info.SetLabel(event.GetString())
        # 获取好友id或者群聊id
        # 设置聊天状态True为与好友聊天，False为与群聊聊天
        for i in range(len(self.friend_group_data[0])):
            if self.friend_group_data[0][i].username == event.GetString():
                self.id = self.friend_group_data[0][i].uid
                self.load_friend_message()
                self.chat_ing = True
                break

        for i in range(len(self.friend_group_data[1])):
            if self.friend_group_data[1][i].group_name == event.GetString():
                self.id = self.friend_group_data[1][i].gid
                self.load_group_message()
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
            message = config.UserMessage(self.uid, self.id, message, time)
            res.send_message(message)
            send_message = {"type": "user_message", "uid1": self.uid, "uid2": self.id, "message": message.message,
                            "time": time}
            self.client.sendall(json.dumps(send_message).encode('utf-8'))
        else:
            message = config.GroupMessage(self.id, self.uid, message, time)
            res.send_group_message(message)

    def receive_message(self):
        while True:
            time.sleep(1)
            data = self.client.recv(1024).decode('utf-8')
            data = json.loads(data)
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
                if data['gid'] == self.id and data['uid'] != self.uid:
                    total = self.Text.GetItemCount()
                    indexItem_time = self.Text.InsertItem(total, str(total + 1))
                    indexItem = self.Text.InsertItem(total + 1, str(total + 2))
                    self.Text.SetItem(indexItem_time, 0, "")
                    self.Text.SetItem(indexItem_time, 1, data['time'])
                    self.Text.SetItem(indexItem_time, 2, "")
                    self.Text.SetItem(indexItem, 0, "")
                    self.Text.SetItem(indexItem, 1, data['message'])
                    self.Text.SetItem(indexItem, 2, data['uid1'])

    # 加载好友群聊列表数据
    def load_friend_group_data(self):
        self.friend_group_data = res.refresh_left_list(self.uid)
        self.on_click_friend_button(self.friend_button)

    # 加载消息
    def load_friend_message(self):
        message_tuple = res.get_user_message(self.uid, self.id)
        self.Text.DeleteAllItems()
        for i in range(len(message_tuple)):
            total = self.Text.GetItemCount()
            indexItem_time = self.Text.InsertItem(total, str(total + 1))
            indexItem = self.Text.InsertItem(total + 1, str(total + 2))
            if int(message_tuple[i].uid1) == int(self.uid):
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_tuple[i].time))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, "")
                self.Text.SetItem(indexItem, 1, message_tuple[i].message)
                self.Text.SetItem(indexItem, 2, "我")
            else:
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_tuple[i].time))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, "对方")
                self.Text.SetItem(indexItem, 1, message_tuple[i].message)
                self.Text.SetItem(indexItem, 2, "")

    def back_to_login(self, event):
        self.Close(True)
        app = wx.App()
        frame = login.LoginFrame(None, self.uid, None)
        frame.Show(True)
        app.MainLoop()

    def load_group_message(self):
        message_tuple = res.get_group_message(self.id)
        self.Text.DeleteAllItems()
        for i in range(len(message_tuple)):
            total = self.Text.GetItemCount()
            indexItem_time = self.Text.InsertItem(total, str(total + 1))
            indexItem = self.Text.InsertItem(total + 1, str(total + 2))
            if int(message_tuple[i].uid) == int(self.uid):
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_tuple[i].time))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, "")
                self.Text.SetItem(indexItem, 1, message_tuple[i].message)
                self.Text.SetItem(indexItem, 2, "我")
            else:
                send_name = res.get_user_name(message_tuple[i].uid)
                self.Text.SetItem(indexItem_time, 0, "")
                self.Text.SetItem(indexItem_time, 1, str(message_tuple[i].time))
                self.Text.SetItem(indexItem_time, 2, "")
                self.Text.SetItem(indexItem, 0, send_name)
                self.Text.SetItem(indexItem, 1, message_tuple[i].message)
                self.Text.SetItem(indexItem, 2, "")


if __name__ == '__main__':
    app = wx.App()
    frame = HomeFrame(None, 1)
    frame.Show(True)
    app.MainLoop()
