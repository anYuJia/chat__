import config.config as config
import database_control.database as db
import res.MD5 as MD5


# 注册 返回值: (是否注册成功, uid)
def Register(user) -> (bool, int):
    DB = db.connect_mysql()
    cursor = DB[1]
    # 检测电话邮箱是否用过
    check_email_phone_sql = "select * from user_detail where phone = %s or email = %s"
    cursor.execute(check_email_phone_sql, (user["phone"], user["email"]))
    if cursor.fetchone() is not None:
        db.close_cursor(DB)
        return False, 0
    # 插入用户uid和password到user表
    insert_user_sql = "insert into user(password) values(%s)"
    cursor.execute(insert_user_sql, (MD5.encrypt(user["password"]),))
    DB[0].commit()
    # 获取uid
    get_uid_sql = "select uid from user where password = %s"
    cursor.execute(get_uid_sql, (MD5.encrypt(user["password"]),))
    uid = cursor.fetchone()[0]
    # 插入用户详细信息到user_detail表
    insert_user_detail_sql = "insert into user_detail(uid,username,head_img,sex,age,phone,email) values(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_user_detail_sql, (
        uid, user["username"], config.DEFAULT_HEAD_IMG, user["sex"], 0, user["phone"], user["email"]))
    DB[0].commit()
    return True, uid

    # 登录 返回值: (是否登录成功, uid)


def Login(user, password) -> (bool, int):
    # 获取数据库句柄
    DB = db.connect_mysql()
    cursor = DB[1]
    # 通过user作为uid查询password进行校验
    get_password_sql = "select password from user where uid = %s"
    cursor.execute(get_password_sql, (user,))
    pd = cursor.fetchone()
    if pd is None:
        # 通过电话或邮箱查询uid
        get_uid_sql = "select uid from user_detail where phone = %s or email = %s"
        cursor.execute(get_uid_sql, (user, user))
        uid = cursor.fetchone()
        if uid is None:
            db.close_cursor(DB)
            return False, 0
        else:
            uid = uid[0]
            cursor.execute(get_password_sql, (uid,))
            pd = cursor.fetchone()
            if pd is None:
                db.close_cursor(DB)
                return False, 0
            else:
                pd = pd[0]
                if MD5.confirm(password, pd):
                    db.close_cursor(DB)
                    return True, uid
                else:
                    db.close_cursor(DB)
                    return False, 0
    else:
        pd = pd[0]
        if MD5.confirm(password, pd):
            db.close_cursor(DB)
            return True, user
        else:
            db.close_cursor(DB)
            return False, 0


def refresh_left_list(uid) -> [list, list]:
    # 获取数据库句柄
    DB = db.connect_mysql()
    cursor = DB[1]
    # 通过uid查询好友列表
    get_friend_list_sql = "select * from user_user where uid1 = %s or uid2 = %s"
    cursor.execute(get_friend_list_sql, (uid, uid))
    friend_list = cursor.fetchall()
    friend_List = []
    for i in range(len(friend_list)):
        if friend_list[i][0] == int(uid):
            friend_List.append(friend_list[i][1])
        else:
            friend_List.append(friend_list[i][0])
    friend_info_list = []
    for i in friend_List:
        get_friend_info_sql = "select * from user_detail where uid = %s"
        cursor.execute(get_friend_info_sql, (i,))
        try:
            user_detail = config.UserDetail(*cursor.fetchone())
        except TypeError:
            continue
        if user_detail.uid == int(uid):
            continue
        friend_info_list.append(obj_to_dict(user_detail))
    friend_list = list(friend_info_list)
    # 通过uid查询群列表
    get_group_list_sql = "select group_detail.gid,group_name,head_img,introduction from group_detail,user_group where user_group.gid = group_detail.gid and uid = %s"
    cursor.execute(get_group_list_sql, (uid,))
    group_list = cursor.fetchall()
    group_info_list = list([obj_to_dict(config.GroupDetail(*i)) for i in group_list])
    return [friend_list, group_info_list]


def story_send_message(message) -> bool:
    DB = db.connect_mysql()
    try:
        # 获取数据库句柄
        cursor = DB[1]
        # 插入消息
        insert_message_sql = "insert into user_message(uid1,uid2,message,time) values(%s,%s,%s,%s)"
        cursor.execute(insert_message_sql, (message.uid1, message.uid2, message.message, message.time))
        DB[0].commit()
        db.close_cursor(DB)
        return True
    except Exception as e:
        print(e)
        db.close_cursor(DB)
        return False


def story_send_group_message(message) -> bool:
    DB = db.connect_mysql()
    try:
        # 获取数据库句柄
        cursor = DB[1]
        # 插入消息
        insert_message_sql = "insert into group_message(gid,uid,message,time) values(%s,%s,%s,%s)"
        cursor.execute(insert_message_sql, (message.gid, message.uid, message.message, message.time))
        DB[0].commit()
        db.close_cursor(DB)
        return True
    except Exception as e:
        print(e)
        db.close_cursor(DB)
        return False


def get_user_message(uid1, uid2) -> list:
    DB = db.connect_mysql()
    cursor = DB[1]
    get_message_sql = "select * from user_message where uid1 = %s and uid2 = %s or uid1 = %s and uid2 = %s order by time asc"
    cursor.execute(get_message_sql, (uid1, uid2, uid2, uid1))
    message_list = cursor.fetchall()
    message_list = list([obj_to_dict(config.UserMessage(*i)) for i in message_list])
    # 将时间datetime.datetime(*******)转换为字符串
    for message in message_list:
        message['time'] = message['time'].strftime("%Y-%m-%d %H:%M:%S")
    db.close_cursor(DB)
    return message_list


def get_group_message(gid) -> list:
    DB = db.connect_mysql()
    cursor = DB[1]
    get_message_sql = "select * from group_message where gid = %s order by time asc"
    cursor.execute(get_message_sql, (gid,))
    message_list = cursor.fetchall()
    message_list = list([obj_to_dict(config.GroupMessage(*i)) for i in message_list])
    # 将时间datetime.datetime(*******)转换为字符串
    for message in message_list:
        message["time"] = message["time"].strftime("%Y-%m-%d %H:%M:%S")
        message["username"] = get_user_name(message["uid"])
    db.close_cursor(DB)
    return message_list


def get_user_name(uid) -> str:
    DB = db.connect_mysql()
    cursor = DB[1]
    get_user_name_sql = "select username from user_detail where uid = %s"
    cursor.execute(get_user_name_sql, (uid,))
    username = cursor.fetchone()[0]
    db.close_cursor(DB)
    return username


def get_group_name(gid) -> str:
    DB = db.connect_mysql()
    cursor = DB[1]
    get_group_name_sql = "select group_name from group_detail where gid = %s"
    cursor.execute(get_group_name_sql, (gid,))
    group_name = cursor.fetchone()[0]
    db.close_cursor(DB)
    return group_name


# 获取群聊成员
def get_group_member(gid) -> tuple:
    DB = db.connect_mysql()
    cursor = DB[1]
    get_online_group_member_sql = "select uid from user_group where gid = %s"
    cursor.execute(get_online_group_member_sql, (gid,))
    online_group_member = cursor.fetchall()
    online_group_member = tuple([i[0] for i in online_group_member])
    db.close_cursor(DB)
    return online_group_member


# 将对象转化为字典
def obj_to_dict(obj):
    obj_dict = {}
    for i in obj.__dict__:
        obj_dict[i] = obj.__dict__[i]
    return obj_dict
