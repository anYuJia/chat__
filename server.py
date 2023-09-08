import json
import socket
import threading
import time
import config.config as config
import res.func as func

user_list = []


def main():
    # 创建tcp套接字
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口
    my_socket.bind(("localhost", 1600))
    # 监听
    my_socket.listen(10)
    # 创建线程接收连接请求
    t = threading.Thread(target=connect, args=(my_socket,))
    t.start()
    t1 = threading.Thread(target=not_die)
    t1.start()


def not_die():
    while True:
        time.sleep(100)


def login(conn, addr, uid, ):
    user_list.append(config.UserIp(uid, conn, addr))
    print("用户", uid, "已登录  ", "ip:", addr)


def logout(uid):
    for user in user_list:
        if user.uid == uid:
            user_list.remove(user)
            print("用户", func.get_user_name(uid), uid, "已退出登录")
            break


def send_message(user_message):
    for user in user_list:
        if int(user.uid) == int(user_message['uid2']):
            user.conn.send(json.dumps(user_message).encode('utf-8'))
            break
    print("{}({})给{}({})发送消息：{}".format(func.get_user_name(user_message['uid1']), user_message['uid1'],
                                             func.get_user_name(user_message['uid2']), user_message['uid2'],
                                             user_message['message']))
    # 将消息保存到数据库
    message = config.UserMessage(user_message['uid1'], user_message['uid2'], user_message['message'],
                                 user_message['time'])
    func.story_send_message(message)


def send_group_message(group_message):
    # 获取群聊的成员
    group_user_list = func.get_group_member(group_message['gid'])
    # 获取发消息人的用户名，添加到消息中
    group_message['username'] = func.get_user_name(group_message['uid'])
    # 获取群聊名字
    group_message['group_name'] = func.get_group_name(group_message['gid'])
    # 遍历群聊用户是否在线
    for user in user_list:
        # 如果是发消息的人就跳过
        if int(user.uid) == int(group_message['uid']):
            continue
        # 如果在线而且不是自己就发送消息
        if int(user.uid) in group_user_list:
            user.conn.send(json.dumps(group_message).encode('utf-8'))
    print("{}({})在群聊{}({})中发送消息：{}".format(group_message['username'], group_message['uid'],
                                                   group_message['group_name'], group_message['gid'],
                                                   group_message['message']))
    # 将群聊消息保存消息到数据库
    message = config.GroupMessage(group_message['gid'], group_message['uid'], group_message['message'], group_message[
        'time'])
    func.story_send_group_message(message)


def send_friend_group_list(info_json):
    info = func.refresh_left_list(info_json['uid'])
    message = {'type': 'friend_group_data', 'data': info}
    for user in user_list:
        if int(user.uid) == int(info_json['uid']):
            user.conn.sendall(json.dumps(message).encode('utf-8'))
            break


# 发送历史私聊消息
def send_user_message_list(info_json):
    message_list = func.get_user_message(info_json['uid1'], info_json['uid2'])
    message = {'type': 'user_message_list', 'data': message_list}
    for user in user_list:
        if int(user.uid) == int(info_json['uid1']):
            user.conn.sendall(json.dumps(message).encode('utf-8'))
            break


# 发送历史群聊消息
def send_group_message_list(info_json):
    group_message_list = func.get_group_message(info_json['gid'])
    message = {'type': 'group_message_list', 'data': group_message_list}
    for user in user_list:
        if int(user.uid) == int(info_json['uid']):
            print(message)
            user.conn.sendall(json.dumps(message).encode('utf-8'))
            break


# 处理接收到的信息
def work(info_json):
    # 如果是用户消息
    if info_json['type'] == 'user_message':
        send_message(info_json)
    # 如果是群聊消息
    elif info_json['type'] == 'group_message':
        send_group_message(info_json)
    elif info_json['type'] == 'get_friend_group_data':
        send_friend_group_list(info_json)
    elif info_json['type'] == 'get_user_message':
        send_user_message_list(info_json)
    elif info_json['type'] == 'get_group_message':
        send_group_message_list(info_json)


# 接收连接请求
def connect(my_socket):
    while True:
        try:
            conn, addr = my_socket.accept()
            print("连接成功", addr)
            # 创建线程处理连接
            t = threading.Thread(target=handle, args=(conn, addr))
            t.start()
        except:
            continue


def handle(conn, addr):
    while True:
        try:
            info = conn.recv(1024).decode('utf-8')
            info_json = json.loads(info)
            if info_json['type'] == 'login':
                login(conn, addr, info_json['uid'])
            elif info_json['type'] == 'logout':
                logout(info_json['uid'])
            work(info_json)
        except:
            continue


if __name__ == '__main__':
    main()
