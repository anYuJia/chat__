import wx


class FriendDetail(wx.Frame):
    def __init__(self, parent, data):
        super().__init__(parent=None, title="好友信息", size=(300, 300))
        self.group_parent = parent
        self.group_Center()
        self.group_SetBackgroundColour((220, 220, 220, 0.1))
        # 设置好友信息
        self.group_friend_info_uid = wx.StaticText(self, 1, label="uid:" + str(data["uid"]), pos=(10, 10),
                                             size=(100, -1))
        self.group_friend_info_uid.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.group_friend_info_username = wx.StaticText(self, 2, label="username:" + str(data["username"]),
                                                  pos=(10, 40), size=(100, -1))
        self.group_friend_info_username.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.group_friend_info_head_img = wx.StaticText(self, 3, label="head_img:" + str(data["head_img"]),
                                                  pos=(10, 70), size=(100, -1))
        self.group_friend_info_head_img.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.group_friend_info_sex = wx.StaticText(self, 2, label="sex:" + str(data["sex"]),
                                             pos=(10, 100), size=(100, -1))
        self.group_friend_info_sex.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.group_friend_info_age = wx.StaticText(self, 2, label="age:" + str(data["age"]),
                                             pos=(10, 130), size=(100, -1))
        self.group_friend_info_age.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.group_friend_info_phone = wx.StaticText(self, 2, label="phone:" + str(data["phone"]),
                                               pos=(10, 160), size=(100, -1))
        self.group_friend_info_phone.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.group_friend_info_email = wx.StaticText(self, 2, label="email:" + str(data["email"]),
                                               pos=(10, 190), size=(100, -1))
        self.group_friend_info_email.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))


class GroupDetail(wx.Frame):
    def __init__(self, parent, data):
        super().__init__(parent=None, title="群聊信息", size=(300, 150))
        self.group_parent = parent
        self.group_Center()
        self.group_SetBackgroundColour((220, 220, 220, 0.1))
        self.group_show_gid = wx.StaticText(self, 1, label="gid:" + str(data["gid"]), pos=(10, 10),
                                      size=(250, 50))
        self.group_show_group_name = wx.StaticText(self, 2, label="group_name:" + str(data["group_name"]),
                                             pos=(10, 30), size=(250, 50))
        self.group_show_head_img = wx.StaticText(self, 3, label="head_img:" + str(data["head_img"]),
                                           pos=(10, 50), size=(250, 50))
        self.group_show_introduction = wx.StaticText(self, 2, label="introduction:" + str(data["introduction"]),
                                               pos=(10, 70), size=(250, 50))

