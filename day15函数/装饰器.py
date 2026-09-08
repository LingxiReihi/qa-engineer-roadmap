import random
import time


def record_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__}用时: {end_time - start_time}秒')
        return result

    return wrapper


def test(func):
    def wrapper(*args, **kwargs):
        print('测试开始.')
        result = func(*args, **kwargs)
        print('测试结束.')
        return result

    return wrapper


@test
@record_time
def download(filename):
    """下载文件"""
    print(f'开始下载{filename}.')
    time.sleep(random.random() * 6)
    print(f'{filename}下载完成.')


@test
@record_time
def upload(filename):
    """上传文件"""
    print(f'开始上传{filename}.')
    time.sleep(random.random() * 8)
    print(f'{filename}上传完成.')


# download = record_time(download)
# upload = record_time(upload)

download('MySQL从删库到跑路.avi')
upload('Python从入门到住院.pdf')
