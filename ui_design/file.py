import os
import socket

# 创建套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定端口
server.bind(("localhost", 16600))
# 监听
server.listen()

while True:
    # 接收连接请求
    conn, addr = server.accept()
    print("连接成功", addr)
    while True:
        try:
            # 接收数据
            data = conn.recv(1024)
            if not data:
                print("客户端已断开连接")
                break
        except Exception as e:
            print("客户端已断开连接")
            break
        cmd, filename = data.decode().split()
        if os.path.isfile(filename):
            f = open(filename, "rb")
            # 获取文件大小
            size = os.stat(filename).st_size
            conn.send(str(size).encode())
            conn.recv(1024)
            for line in f:
                conn.send(line)
            f.close()
            print("文件下载成功")
            conn.send("not file".encode())
server.close()
