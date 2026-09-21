from retry import retry


def make_flaky(failures, exception, calls=None):
    states = {"times": 0}

    def fn(*a, **k):

        states["times"] += 1
        if calls is not None:
            calls.append((a, k))
        if states["times"] <= failures:
            raise exception
        return "OK"

    return fn, states


def test_error(attempts=3, delay=0, exceptions=(Exception,), catch_exc=Exception, label=""):
    try:
        retry(attempts=attempts, delay=delay, exceptions=exceptions)(flaky)  # 装饰时（这一行执行时）就该抛
        assert False, f"{label}：预期抛出 {catch_exc.__name__}，实际未抛出"
    except catch_exc:
        return


if __name__ == "__main__":
    # region 测试用例1 第一次就成功
    flaky, state = make_flaky(failures=0, exception=ValueError("x"), calls=None)
    wrapped = retry(attempts=3)(flaky)
    result = wrapped()
    assert result == "OK", "测试用例1测试失败，运行没有成功"
    assert state["times"] == 1, "测试用例1测试失败，调用次数不为1"
    # endregion

    # region 测试用例2 第3次成功
    flaky, state = make_flaky(failures=2, exception=ValueError("x"), calls=None)
    wrapped = retry(attempts=3)(flaky)
    result = wrapped()
    assert result == "OK", "测试用例2测试失败，运行没有成功"
    assert state["times"] == 3, "测试用例2测试失败，调用次数不为3"
    # endregion

    # region 测试用例3 一直失败
    err = ValueError("x")
    flaky, state = make_flaky(failures=99, exception=err, calls=None)
    wrapped = retry(attempts=3, exceptions=(ValueError,))(flaky)
    catch = None
    try:
        wrapped()
    except ValueError as e:
        catch = e
    assert state["times"] == 3, "测试用例3测试失败，调用次数不为3"
    assert catch is err, "测试用例3测试失败，抛出异常不符"
    # endregion

    # region 测试用例4 单次尝试
    flaky, state = make_flaky(failures=1, exception=err, calls=None)
    wrapped = retry(attempts=1, exceptions=(ValueError,))(flaky)
    catch = None
    try:
        wrapped()
    except ValueError as e:
        catch = e
    assert state["times"] == 1, "测试用例4测试失败，调用次数不为1"
    assert catch is err, "测试用例4测试失败，抛出异常不符"
    # endregion

    # region 测试用例5 非目标异常不重试
    err = TypeError()
    flaky, state = make_flaky(failures=1, exception=err)
    wrapped = retry(attempts=2, exceptions=(ValueError,))(flaky)
    catch = None
    try:
        wrapped()
    except TypeError as e:
        catch = e
    assert state["times"] == 1, "测试用例5测试失败，调用次数不为1"
    assert catch is err, "测试用例5测试失败，抛出异常不符"


    # endregion

    # region 测试用例6 子类算目标
    class MyValueError(ValueError):
        pass


    err = MyValueError()
    flaky, state = make_flaky(failures=2, exception=err)
    wrapped = retry(attempts=3, exceptions=(ValueError,))(flaky)
    result = wrapped()
    assert state["times"] == 3, "测试用例6测试失败，调用次数不为3"
    assert result == "OK", "测试用例6测试失败，运行未成功"
    # endregion

    # region 测试用例7 参数转发
    ps = []
    flaky, state = make_flaky(failures=2, exception=ValueError(), calls=ps)
    wrapped = retry(attempts=3, exceptions=(ValueError,))(flaky)
    result = wrapped(5, key='v')
    assert state["times"] == 3, "测试用例7测试失败，调用次数不为3"
    assert result == "OK", "测试用例7测试失败，运行未成功"
    assert all(item == ((5,), {'key': 'v'}) for item in ps), "测试用例7测试失败，每次调用参数不一致"


    # endregion

    # region 测试用例8 wraps元数据
    def flaky_doc():
        """doc 123"""
        pass


    wrapped = retry()(flaky_doc)
    assert wrapped.__name__ == "flaky_doc", "测试用例8测试失败，名称不为原函数名称"
    assert wrapped.__doc__ == "doc 123", "测试用例8测试失败，注释内容不为原函数内容"
    # endregion

    # region 测试用例9 attempts边界值测试
    test_error(attempts=0, catch_exc=ValueError, label="测试用例9")
    # endregion

    # region 测试用例10 attempts异常值值测试
    test_error(attempts=-3, catch_exc=ValueError, label="测试用例10")
    # endregion

    # region 测试用例11,12,13 attempts异常类型值测试
    test_error(attempts="3", catch_exc=TypeError, label="测试用例11")
    test_error(attempts=True, catch_exc=TypeError, label="测试用例12")
    test_error(attempts=3.0, catch_exc=TypeError, label="测试用例13")
    # endregion

    # region 测试用例14 delay异常值测试
    test_error(delay=-1, catch_exc=ValueError, label="测试用例14")
    # endregion

    # region 测试用例15,16 delay异常类型值测试
    test_error(delay=True, catch_exc=TypeError, label="测试用例15")
    test_error(delay="0.5", catch_exc=TypeError, label="测试用例16")
    # endregion

    # region 测试用例17 exceptions异常值测试
    test_error(exceptions=(), catch_exc=ValueError, label="测试用例17")
    # endregion

    # region 测试用例18,19,20 exceptions异常类型值测试
    test_error(exceptions=[], catch_exc=TypeError, label="测试用例18")
    test_error(exceptions=(1,), catch_exc=TypeError, label="测试用例19")
    test_error(exceptions=(ValueError, 'a'), catch_exc=TypeError, label="测试用例20")

    # endregion

    # region 测试用例21 裸用@retry装饰器

    try:
        @retry
        def test():
            pass


        assert False, "测试用例21 裸用@retry装饰器，测试失败"
    except TypeError:
        pass

    # endregion
