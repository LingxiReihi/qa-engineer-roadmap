# 控制台指令系统
from day23_login_system.user.services import LoginService


class ComSystem:
    def __init__(self):
        self.login_service = LoginService()

    def cmd_start(self):
        print("""
        控制台登陆系统v0.1
        """)
        while True:
            input_cmd = input("@: ")
            match input_cmd:
                case "login":
                    self.__login__()
                case "register":
                    self.__register__()
                case "update_password":
                    self.__update_password__()
                case "get_users":
                    self.__get_users__()
                case "exit":
                    self.__exit_system__()
                    break
                case "remove_user":
                    self.__remove_user__()
                case "help":
                    self.__help__()
                case _:
                    print("无效的指令，请输入help获取帮助")

    def __login__(self):
        if not self.login_service.state:
            username = input("请输入用户名：").replace(" ", "")
            password = input("请输入密码：").replace(" ", "")
            self.login_service.login(username, password)
        else:
            print("用户已登录")

    def __register__(self):
        if not self.login_service.state:
            username = input("请输入用户名：").replace(" ", "")
            password_1 = input("请输入密码：").replace(" ", "")
            password_2 = input("请再次输入密码：").replace(" ", "")
            if password_1 == password_2:
                self.login_service.register_user(username, password_1)
            else:
                print("两次输入的密码不一致")
        else:
            print("用户已登录，请先退出")

    def __update_password__(self):
        if not self.login_service.state:
            print("暂未登录，请登录")
        else:
            password = input("请输入新密码：").replace(" ", "")
            self.login_service.update_password(password)

    def __get_users__(self):
        if not self.login_service.state:
            print("暂未登录，请登录")
        else:
            print(self.login_service.get_users())

    def __remove_user__(self):
        if not self.login_service.state:
            print("暂未登录，请登录")
        else:
            username = input("请输入要删除的用户名：").replace(" ", "")
            if self.login_service.remove_user(username):
                print("删除成功")
            else:
                print("删除失败")

    def __exit_system__(self):
        print(f"感谢使用，{self.login_service.user}")

    def __help__(self):
        print("""
        login               登录
        register            注册
        update_password     修改密码
        get_users           获取用户列表
        remove_user         删除用户
        exit                退出系统
        """)
