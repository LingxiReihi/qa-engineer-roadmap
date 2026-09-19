from decimal import Decimal, ROUND_HALF_UP


def un_require_number(*args, match_type, not_match_type) -> bool:
    """
    判断数字是否符合类型
    :param args: 需要判断的参数
    :param match_type:需要符合的类型
    :param not_match_type:不需要符合的类型
    :return:不满足条件返回True，满足返回False
    """
    for arg in args:
        if not isinstance(arg, match_type) or isinstance(arg, not_match_type):
            return True
    return False


def clamp(value, low=0, high=100) -> float:
    """
    获取输入值在范围内的值
    :param value: 输入值
    :param low: 下边界值，默认=0
    :param high: 上边界值，默认=100
    :return: 输入值在范围内的值，输入类型错误或 low > high 抛出异常
    """
    if un_require_number(value, low, high, match_type=(int, float), not_match_type=bool):
        raise TypeError(
            f"clamp() 只接受 int/float，实际收到 "
            f"value={value!r} ({type(value).__name__}), low={low!r} ({type(low).__name__}),  high={high!r} ({type(high).__name__})"
        )
    if high < low:
        raise ValueError(
            f"clamp() 参数错误，high应该大于low，实际收到 "
            f"low={low!r},  high={high!r}"
        )
    return max(min(value, high), low)


def round2(value) -> float:
    """
    获得四舍五入后的小数
    :param value: 输入值
    :return: 返回四舍五入后的值，输入类型错误抛出异常
    """
    if un_require_number(value, match_type=(int, float), not_match_type=bool):
        raise TypeError(
            f"round2() 只接受 int/float，实际收到 "
            f"value={value!r} ({type(value).__name__})"
        )
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )
