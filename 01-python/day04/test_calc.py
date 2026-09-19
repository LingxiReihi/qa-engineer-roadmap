# from calc import multiply # 直接通过包名导入函数需要 __init.py__ 中已有的导出方法(包对外的API)才可，否则将会导出错误
from math import isclose

from calc.arithmetic import multiply  # 这个方法通过 包名.文件名 导入，直接定位到对应文件，不属于包API
from calc import add, subtract, clamp
from calc.utils import round2


def expect_typeerror(fn, *args, label):
    """
    类型错误断言检查
    :param fn:检查函数
    :param args:传入参数列表
    :param label:提示语
    """
    try:
        fn(*args)
    except TypeError:
        return
    raise AssertionError(f"{label}：预期抛出 TypeError，实际未抛出")


if __name__ == "__main__":
    assert add(1, 2) == 3, "add测试用例1：(1,2)，预期结果：3，测试失败"
    assert add(1, -1) == 0, "add测试用例2：(1, -1)，预期结果：0，测试失败"
    assert add(1.0, -0.5) == 0.5, "add测试用例3：(1.0, -0.5)，预期结果：0.5，测试失败"
    assert isclose(add(0.1, 0.2), 0.3), "add测试用例4：(0.1, 0.2)，预期结果：0.3，测试失败"
    expect_typeerror(add, "0.1", 0.2, label="add测试用例5")

    assert subtract(1, 2) == -1, "subtract测试用例1：(1,2)，预期结果：-1，测试失败"
    assert subtract(1, -1) == 2, "subtract测试用例2：(1, -1)，预期结果：2，测试失败"
    assert isclose(subtract(1.0, -0.5), 1.5), "subtract测试用例3：(1.0, -0.5)，预期结果：1.5，测试失败"
    assert isclose(subtract(0.1, 0.2), -0.1), "subtract测试用例4：(0.1, 0.2)，预期结果：-0.1，测试失败"
    expect_typeerror(subtract, "0.1", 0.2, label="subtract测试用例5")

    assert multiply(1, 2) == 2, "multiply测试用例1：(1,2)，预期结果：2，测试失败"
    assert multiply(1, -1) == -1, "multiply测试用例2：(1, -1)，预期结果：-1，测试失败"
    assert isclose(multiply(1.0, -0.5), -0.5), "multiply测试用例3：(1.0, -0.5)，预期结果：-0.5，测试失败"
    assert isclose(multiply(0.1, 0.2), 0.02), "multiply测试用例4：(0.1, 0.2)，预期结果：0.02，测试失败"
    expect_typeerror(multiply, "0.1", 0.2, label="multiply测试用例5")

    assert clamp(50) == 50, "clamp测试用例1：(50)，预期结果：50，测试失败"
    assert clamp(-10) == 0, "clamp测试用例2：(-10)，预期结果：0，测试失败"
    assert clamp(150) == 100, "clamp测试用例3：(150)，预期结果：100，测试失败"
    assert clamp(50, 10, 20) == 20, "clamp测试用例4：(50, 10, 20)，预期结果：20，测试失败"
    assert clamp(9.23, 10, 100) == 10, "clamp测试用例5：(9.23, 10, 100)，预期结果：10，测试失败"
    expect_typeerror(clamp, "9.23", 10, 100, label="clamp测试用例6")
    try:
        clamp(10, 20, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("clamp测试用例7：预期抛出 ValueError，实际未抛出")

    # round函数四舍五入在 python2 时，舍去位为5时会前一位+1，但 python3 末位为5时更新保留前一位靠近偶数方，即0.5~0，-0.5~0
    assert isclose(round2(3.14156), 3.14), "round2测试用例1：(3.14156)，预期结果：3.14，测试失败"
    assert isclose(round2(2.675), 2.68), "round2测试用例2：(2.675)，预期结果：2.68，测试失败"
    assert isclose(round2(1.336), 1.34), "round2测试用例3：(1.336)，预期结果：1.34，测试失败"
    assert isclose(round2(-2.005), -2.01), "round2测试用例4：(-2.005)，预期结果：-2.01，测试失败"
    expect_typeerror(round2, "-2.005", label="round2测试用例5")

    print("calc 包全部通过")
