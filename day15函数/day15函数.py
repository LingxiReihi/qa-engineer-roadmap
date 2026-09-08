import random
import string

ALL_CHARS = string.digits + string.ascii_letters


def generate_code(*, code_len=4):
    """
    生成随机验证码
    :param code_len: 验证码长度，默认为4
    :return: 验证码
    """
    return ''.join(random.choices(ALL_CHARS, k=code_len))


def is_prime(num: int) -> bool:
    """
    判断一个正整数是不是质数
    :param num: 大于1的正整数
    :return: 如果num是质数返回True，否则返回False
    """
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def lcm(x: int, y: int) -> int:
    """
    求最小公倍数
    :param x: 整数
    :param y: 整数
    :return: 最小公倍数
    """
    return x * y // gcd(x, y)


def gcd(x: int, y: int) -> int:
    """
    求最大公约数
    :param x: 整数
    :param y: 整数
    :return: 最大公约数
    """
    while y % x != 0:
        x, y = y % x, x
    return x
