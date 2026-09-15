from day23_login_system.dao.data_manager import DataManager, DataKey


class LoginService:
    dm = DataManager()
    state = False
    user = ""

    def login(self, user, password):
        if password == self.dm.get_data_user(user)[DataKey.password()]:
            self.state = True
            self.user = user
            print("登录成功", self.user)
            return True
        print("登录失败")
        return False

    def register_user(self, username, password):
        if self.dm.add_data(username, password):
            print("注册成功，请登录")
        else:
            print("注册失败")

    def update_password(self, password):
        if not self.state:
            print("暂未登录，请登录")
            return
        else:
            if self.dm.update_password(self.user, password):
                print("更改密码成功，请重新登录")
                self.__clear_state__()

    def logout(self):
        if not self.state:
            print("暂未登录")
        else:
            self.__clear_state__()

    def get_users(self):
        if not self.state:
            print("暂未登录，请登录")
            return None
        return self.dm.get_usernames()

    def __clear_state__(self):
        self.state = False
        self.user = None
