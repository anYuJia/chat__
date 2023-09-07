# 循环左移n位
def shift(x, n):
    y = ""
    for i in range(0, len(x) - n):
        y += x[i + n]
    y += x[0:n]
    # print(len(y))
    return y


def F(X, Y, Z):
    return Or(And(X, Y), And(Not(X), Z))


def G(X, Y, Z):
    return Or(And(X, Z), And(Y, Not(Z)))


def H(X, Y, Z):
    return xor(xor(X, Y), Z)


def I(X, Y, Z):
    return xor(Y, Or(X, Not(Z)))


# 轮循环
def Go(a, b, c, d, fun, m, s, K):
    thesum = xor(xor(a, fun(b, c, d)), xor(m, K))
    return xor(b, shift(thesum, s))


# 二进制转16进制
def int32ToHex(a):
    '32位整型集合转16进制'
    md5 = ''
    for i in a:
        x = "{:08x}".format(int(i, 2))  # 整型【32位2】->8位16
        md5 += x[6:] + x[4:6] + x[2:4] + x[:2]  # 每两位切割, 切割4刀->逆序【大变小端】
    return md5


# 明文转二进制
def m_to_bin(string):
    return hex_to_bin(bytes(string, "utf-8").hex())


# 16进制转2进制
def hex_to_bin(int_16):
    int_16 = int_16.replace("0x", "").replace("0X", "")
    return (bin(int(int_16, 16)).replace("0b", "")).rjust(32, "0")


# 与
def And(bin_a, bin_b):
    bin_c = ""
    for i in range(len(bin_a)):
        if bin_a[i] == bin_b[i] and bin_a[i] == '1':
            bin_c += '1'
        else:
            bin_c += '0'
    return bin_c


# 或
def Or(bin_a, bin_b):
    bin_c = ""
    for i in range(len(bin_a)):
        if bin_a[i] == bin_b[i] and bin_a[i] == '0':
            bin_c += '0'
        else:
            bin_c += '1'
    return bin_c


# 非
def Not(bin_a):
    bin_c = ""
    for i in range(len(bin_a)):
        if bin_a[i] == '0':
            bin_c += '1'
        else:
            bin_c += '0'
    return bin_c


# 异或
def xor(bin_a, bin_b):
    bin_c = ""
    for i in range(len(bin_a)):
        if bin_a[i] == bin_b[i]:
            bin_c += '0'
        else:
            bin_c += '1'
    return bin_c


# 字节填充
def byte_stuffing(string_bin):
    string_len = len(str(string_bin))
    l = 512 - 64 - (string_len % 512 - 1)
    end_len = bin(string_len).rjust(64, "0")
    return string_bin + '1' + l * '0' + end_len.replace("0b", "")


# 将二进制每512bit分16组
def divide(text):
    text_range = []
    for i in range(int(len(text) / 512)):
        T = []
        for j in range(0, 16):
            T.append(text[i * 512 + j * 32:i * 512 + j * 32 + 32])
        text_range.append(T)
    return text_range


def encrypt(string):
    A = "0X67452301"
    B = "0XEFCDAB89"
    C = "0X98BADCFE"
    D = "0X10325476"
    K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
         0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
         0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
         0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
         0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
         0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
         0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
         0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
         0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
         0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
         0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
         0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
         0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
         0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
         0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, ]
    S = [7, 12, 17, 22, 7, 12, 17, 22,
         7, 12, 17, 22, 7, 12, 17, 22,
         5, 9, 14, 20, 5, 9, 14, 20,
         5, 9, 14, 20, 5, 9, 14, 20,
         4, 11, 16, 23, 4, 11, 16, 23,
         4, 11, 16, 23, 4, 11, 16, 23,
         6, 10, 15, 21, 6, 10, 15, 21,
         6, 10, 15, 21, 6, 10, 15, 21, ]
    S_bin = m_to_bin(string)  # 字符串转为2进制
    text_bin = byte_stuffing(S_bin)  # 填充
    M = divide(text_bin)  # 对M处理，用于加密截取使用
    A = hex_to_bin(A)
    B = hex_to_bin(B)
    C = hex_to_bin(C)
    D = hex_to_bin(D)
    for i in range(len(M)):
        for ii in range(64):
            if ii < 16:
                A, B, C, D = D, Go(A, B, C, D, F, str(M[i][ii]), S[ii], hex_to_bin(str(K[ii]))), B, C
            elif ii < 32:
                A, B, C, D = D, Go(A, B, C, D, G, str(M[i][(ii * 5 + 1) % 16]), S[ii], hex_to_bin(str(K[ii]))), B, C
            elif ii < 48:
                A, B, C, D = D, Go(A, B, C, D, H, str(M[i][((ii * 3) + 5) % 16]), S[ii], hex_to_bin(str(K[ii]))), B, C
            else:
                A, B, C, D = D, Go(A, B, C, D, I, str(M[i][ii * 7 % 16]), S[ii], hex_to_bin(str(K[ii]))), B, C
            # print("第" + str(i + 1) + "组 第" + str(ii) + "轮加密结果为：", int32ToHex([A, B, C, D]))
    md5 = int32ToHex([A, B, C, D])
    return md5


def confirm(string, md5):
    if md5 == encrypt(string):
        return True
    else:
        return False
