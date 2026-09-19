from .utils import un_require_number


def add(a: float, b: float) -> float:
    """
    加法运算
    :param a: 第一个加数
    :param b: 第二个加数
    :return: 和，加数出现格式错误时抛出异常
    """
    if un_require_number(a, b, match_type=(int, float), not_match_type=bool):
        raise TypeError(
            f"add() 只接受 int/float，实际收到 "
            f"a={a!r} ({type(a).__name__}), b={b!r} ({type(b).__name__})"
        )
    return a + b


def subtract(a: float, b: float) -> float:
    """
    减法运算
    :param a: 被减数
    :param b: 减数
    :return: 差，参数出现格式错误时抛出异常
    """
    if un_require_number(a, b, match_type=(int, float), not_match_type=bool):
        raise TypeError(
            f"subtract() 只接受 int/float，实际收到 "
            f"a={a!r} ({type(a).__name__}), b={b!r} ({type(b).__name__})"
        )
    return a - b


def multiply(a: float, b: float) -> float:
    """
    乘法运算
    :param a: 乘数
    :param b: 乘数
    :return: 积，乘数出现格式错误时抛出异常
    """
    if un_require_number(a, b, match_type=(int, float), not_match_type=bool):
        raise TypeError(
            f"multiply() 只接受 int/float，实际收到 "
            f"a={a!r} ({type(a).__name__}), b={b!r} ({type(b).__name__})"
        )
    return a * b
