import json
from pathlib import Path

from day23_login_system.Exceptions.file_error import FileError


class DataKey:
    @classmethod
    def password(cls): return "password"


FILE_PATH = Path(__file__).resolve().parent / "data.json"

"""
数据管理器
"""


class DataManager:
    __slots__ = ('file_path', 'data')

    def __init__(self, file_path=FILE_PATH):
        self.file_path = file_path
        self.data = {}
        self.__load_data__()

    def __load_data__(self):
        """
        加载数据
        :return: bool
        """
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
                return True
        except FileError as e:
            print(e)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
        return False

    def __save_data__(self):
        """
        保存数据
        :return: bool
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file)
                return True
        except FileError as e:
            print(e)
        except OSError as e:
            print(f"保存失败: {e}")
        return False

    def add_data(self, user, password):
        """
        添加数据
        :param user: str
        :param password: str
        :return: bool
        """
        if user in self.data:
            print(f"用户已存在: {user}")
            return False

        self.data[user] = {
            DataKey.password(): password
        }
        return self.__save_data__()

    def get_data_user(self, username):
        if username in self.data:
            return self.data[username]
        else:
            print(f"用户不存在: {username}")
            return None

    def update_password(self, username, password):
        if username in self.data:
            self.data[username][DataKey.password()] = password
            return True
        else:
            print(f"用户不存在: {username}")
            return False

    def get_usernames(self):
        return list(self.data.keys())

    def remove_user(self, username):
        if username in self.data:
            del self.data[username]
            self.__save_data__()
            return True
        else:
            print(f"用户不存在: {username}")
            return False
