JSON_AS_ASCII = False
HEIGHT = 500
WIDTH = 800
DEFAULT_HEAD_IMG = "file/head_img/user/default_head_img.jpg"
HOST = "localhost"
PORT = 1600


class RegisterUser():
    def __init__(self, username, password, sex, email, phone):
        self.username = username
        self.password = password
        self.sex = sex
        self.email = email
        self.phone = phone


class UserDetail:
    def __init__(self, uid, username, head_img, sex, age, phone, email):
        self.uid = uid
        self.username = username
        self.head_img = head_img
        self.sex = sex
        self.age = age
        self.phone = phone
        self.email = email


class GroupDetail:
    def __init__(self, gid, group_name, head_img, introduction):
        self.gid = gid
        self.group_name = group_name
        self.head_img = head_img
        self.introduction = introduction


class UserMessage:
    def __init__(self, uid1, uid2, message, time):
        self.uid1 = uid1
        self.uid2 = uid2
        self.message = message
        self.time = time


class GroupMessage:
    def __init__(self, gid, uid, message, time):
        self.gid = gid
        self.uid = uid
        self.message = message
        self.time = time


class UserIp:
    def __init__(self, uid, conn,ip, port):
        self.uid = uid
        self.conn = conn
        self.ip = ip
        self.port = port
