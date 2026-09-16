nums = [1, 2, 3]  # 列表，别名指向同一个对象地址
alias = nums  # 添加新别名，但指向地址相同
alias.append(99)  # 为同一地址添加数据
print(nums, id(nums) == id(alias))  # 输出: [1, 2, 3, 99] True


def kind_of(value):
    '''返回 (类型名，是否可变)'''
    mutable = isinstance(value, (list, dict, set))  # isinstance判断value是否是list、dict、set的实例
    return type(value).__name__, mutable


# 测试数据
for v in [42, 3.14, 'abc', [1], (1,), {'k': 1}, {1, 2}]:
    print(repr(v), "->", kind_of(v))
