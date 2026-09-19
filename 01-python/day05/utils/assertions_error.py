def expect_type_error(fn, *args, error_type, label):
    """
    类型错误断言检查
    :param fn: 检查函数
    :param args: 传入参数列表
    :param error_type: 检测错误类型
    :param label: 提示语
    """
    try:
        fn(*args)
    except error_type:
        return
    raise AssertionError(f"{label}：预期抛出 {error_type.__name__}，实际未抛出")
