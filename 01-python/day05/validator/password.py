import re

from utils import un_require_type

_password_error = [
    "长度需要大于等于8",
    "需要包含至少一个大写字母",
    "需要包含至少一个数字",
    "需要包含至少一种非字母数字符号"
]


def validate_password(pwd: str) -> list[str]:
    """
    判断密码有效性，将会根据密码中所含有的字符数量及类型进行判断
    :param pwd: 密码字符串，输入非字符串将会报 TypeError
    :return: 问题列表，可能同时包含多个问题，没有问题将会返回空列表
        问题清单：
            "长度需要大于等于8",
            "需要包含至少一个大写字母",
            "需要包含至少一个数字",
            "需要包含至少一种非字母数字符号"
    :raise TypeError: 只能传入字符串作为参数
    """
    if un_require_type(pwd, match_type=str): raise TypeError("只能传入字符串作为参数")
    res = [v for v in _password_error]
    if len(pwd) >= 8: res.remove(_password_error[0])
    if bool(re.search(r"[A-Z]", pwd)): res.remove(_password_error[1])
    if bool(re.search(r"[0-9]", pwd)): res.remove(_password_error[2])
    if bool(re.search(r"[^A-Za-z0-9]", pwd)): res.remove(_password_error[3])
    return res


def parse_score(raw: str) -> int:
    """
    从字符串中获取分数
    :param raw: 原始字符串，输入非字符串会抛出 TypeError ，不符合条件的字符串会抛出 ValueError
    :return: 最终得到的分数
    :raise TypeError: 只能接受字符串，不接受其他类型的数据
    :raise ValueError: 只能接受0~100的代表分数的字符串，不接受分母不为100或数值超过的数据 | 当前数据超出允许范围，或输入包含重复字符(-/分)
    """
    if un_require_type(raw, match_type=str): raise TypeError(
        "只能接受字符串，不接受其他类型的数据")
    if any(c not in set("0123456789/分") for c in raw):
        raise ValueError("只能接受0~100的代表分数的字符串，不接受分母不为100或数值超过的数据")
    else:
        score = -1
        if raw.isdigit():
            score = int(raw)
        elif raw.find('/') != -1:
            s = raw.split('/')
            for c in s:
                if c.find('/') != -1 or c.find('分') != -1:
                    raise ValueError("只能接受0~100的代表分数的字符串，不接受分母不为100或数值超过的数据")
            if len(s) == 2 and s[0].isdigit() and s[1].isdigit():
                if int(s[1]) == 100:
                    score = int(s[0])
        elif raw.find('分') != -1 and raw.find('分') == len(raw) - 1 and len(raw) > 1:
            score = int(raw[:raw.find('分')])

        if 0 <= score <= 100:
            return score
        raise ValueError("当前数据超出允许范围，或输入包含重复字符(-/分)")
