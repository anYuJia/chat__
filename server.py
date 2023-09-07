import json
import socket
import threading
import time

import config.config as config

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


def send_message(user_message):
    user = None
    user2 = False
    for user in user_list:
        if int(user.uid) == int(user_message['uid2']):
            user2 = True
            print(user.addr)
            print(user_message['uid1'], "给", user_message['uid2'], "发送消息：", user_message['message'])
            user.conn.send(json.dumps(user_message).encode('utf-8'))
            break
    if not user2:
        print("用户", user_message['uid2'], "不在线")


# 处理接收到的信息
def work(info_json):
    if info_json['type'] == 'user_message':
        send_message(info_json)


# 接收连接请求
def connect(my_socket):
    while True:
        conn, addr = my_socket.accept()
        print("连接成功", addr)
        # 创建线程处理连接
        t = threading.Thread(target=handle, args=(conn, addr))
        t.start()


def handle(conn, addr):
    while True:
        info = conn.recv(1024).decode('utf-8')
        info_json = json.loads(info)
        if info_json['type'] == 'login':
            login(conn, addr, info_json['uid'])
        work(info_json)


if __name__ == '__main__':
    main()
