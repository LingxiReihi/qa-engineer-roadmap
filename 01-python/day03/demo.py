def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart


assert add_item("a") == ["a"]
assert add_item("b") == ["b"], "修复后两次调用互不污染"


def total(*nums):
    """可变位置参数，返回总和"""
    return sum(nums)


assert total(1, 2, 3) == 6
assert total() == 0, "空参数边界"


def describe(**info):
    """可变关键字参数"""
    return ", ".join(f"{k}={v}" for k, v in info.items())


assert describe(name="测试", level=1) == "name=测试, level=1"
