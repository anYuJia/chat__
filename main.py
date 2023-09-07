import wx

import database_control.init_database as init_database
import ui_design.login as login

if __name__ == '__main__':
    # init_database.init_create_tables()  # 初始化数据库,通过脚本建立相关表
    app = wx.App()
    frame = login.LoginFrame(None)
    frame.Show(True)
    app.MainLoop()
