def un_require_type(*args, match_type, not_match_type=None) -> bool:
    """
    判断参数是否符合类型
    :param args: 需要判断的参数
    :param match_type: 需要符合的类型
    :param not_match_type: 不需要符合的类型
    :return: 不满足条件返回True，满足返回False
    """
    for arg in args:
        if not isinstance(arg, match_type) or (not_match_type is not None and isinstance(arg, not_match_type)):
            return True
    return False


def require_type(*args, match_type, not_match_type=None) -> bool:
    """
    判断参数是否符合类型
    :param args: 需要判断的参数
    :param match_type: 需要符合的类型
    :param not_match_type: 不需要符合的类型
    :return: 满足条件返回True，不满足返回False
    :raise TypeError: match_type当前未赋值，请显式赋值
    """
    if match_type is None:
        raise TypeError("match_type当前未赋值，请显式赋值")
    # (v for v in args)传参传入的是生成器，需要解包后传入才是正常运行
    return not un_require_type(*args, match_type=match_type, not_match_type=not_match_type)
