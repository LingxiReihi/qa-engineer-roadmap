from functools import wraps
from time import sleep


def retry(attempts=3, delay=0, exceptions=(Exception,)):
    """
    在函数抛弃指定异常时重试
    :param attempts: 出现异常时重试的次数，需要大于0，默认为3
    :param delay: 每次重试等待的时间，不能为负数
    :param exceptions: 非空元组，每个元素必须是异常类（issubclass(exc, BaseException) 为真）
    :raise TypeError: attempts只能是int类型，不包含子类型bool; delay必须为int或float，不接受int子类型bool;
        exceptions不能为空元组; exceptions每个元素必须是异常类
    :raise ValueError: attempts必须大于0; delay必须 >= 0; exceptions不能为空元组
    """
    # region retry参数类型判断块
    if not isinstance(attempts, int) or isinstance(attempts, bool):
        raise TypeError("attempts只能是int类型，不包含子类型bool")
    elif attempts < 1:
        raise ValueError("attempts必须大于0")

    if not isinstance(delay, (int, float)) or isinstance(delay, bool):
        raise TypeError("delay必须为int或float，不接受int子类型bool")
    elif delay < 0:
        raise ValueError("delay必须 >= 0")

    if not isinstance(exceptions, tuple):
        raise TypeError("exceptions必须为元组")
    elif len(exceptions) == 0:
        raise ValueError("exceptions不能为空元组")

    for exception in exceptions:
        if not issubclass(exception, BaseException):
            raise TypeError("exceptions每个元素必须是异常类")

    # endregion

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            catch = None
            for _ in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except exceptions as e:
                    catch = e
                    sleep(delay)
            raise catch

        return wrapper

    return decorator
