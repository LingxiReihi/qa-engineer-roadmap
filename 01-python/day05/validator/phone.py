import re


def normalize_phone(raw: str) -> str:
    """
    格式化手机号
    :param raw: 原始手机号数据，只接受str类型且只包含+-()以及数字0~9，否则提示值错误
    :return: 格式化后的手机号码
    :raise ValueError: 输入号码错误，只接受包含 +-()0~9 ，且以1开头的号码
    :raise TypeError: 输入号码错误，只接受str类型
    """
    if isinstance(raw, str):
        text = re.sub(r'[-() ]', '', raw)  # 批量替换 '-() ' 为 ''
        text = re.sub(r'^(?:\+86|0086|86)', '', text)
        if len(text) == 11 and text.isdigit() and text[0] == '1':
            return text
        else:
            raise ValueError('输入号码错误，只接受包含+-()0~9，且以1开头的号码')
    raise TypeError('输入号码错误，只接受str类型')


# 因为 normalize_phone 中已经有对数据的判断检测，且返回必定为这里不再重复检测数据类型及合规性
def mask_phone(phone: str) -> str:
    """
    为号码生成掩码
    :param phone: 手机号数据，只接受str类型且只包含+-()以及数字0~9，且以1开头的号码，否则提示值错误
    :return: 号码掩盖后的手机号
    :raise ValueError: 输入号码错误，只接受包含 +-()0~9，且以1开头的号码
    :raise TypeError: 输入号码错误，只接受str类型
    """
    phone = normalize_phone(phone)
    return phone[:3] + '****' + phone[7:]
