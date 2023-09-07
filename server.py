import json
import socket
import threading

import config.config as config


def main():
    # 创建tcp套接字
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口
    my_socket.bind(("localhost", 1600))
    # 监听
    my_socket.listen()
    user_list = []
    # 创建线程接收连接请求
    t = threading.Thread(target=accept_connect, args=(my_socket, user_list))
    t.start()


def login(conn, ip,port, uid, user_list):
    user_list.append(config.UserIp(uid, conn, ip, port))
    print("用户", uid, "已登录  ", "ip:", ip, "port:", port)
    pass


def send_message(user_message, user_list):
    for user in user_list:
        if user.uid == user_message['uid2']:
            user.conn.send(user_message["message"].encode('utf-8'))
            break
    else:
        print("用户", user_message['uid2'], "不在线")
    print("端口", user_message, "用户", user_message['uid1'], "给用户", user_message['uid2'], "发送了一条消息")


# 处理接收到的信息
def work(info_json, user_list):
    if info_json['type'] == 'user_message':
        send_message(info_json, user_list)


# 接收连接请求
def accept_connect(my_socket, user_list):
    conn, addr = my_socket.accept()
    while True:
        # 接收连接请求
        print("等待连接")
        info = conn.recv(1024).decode('utf-8')
        info_json = json.loads(info)
        if info_json['type'] == 'login':
            login(conn, info_json['ip'], info_json['port'], info_json['uid'], user_list)
        work(info_json, user_list)


if __name__ == '__main__':
    main()
