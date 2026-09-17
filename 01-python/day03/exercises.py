def means(*nums) -> float:
    if nums and len(nums) > 0:
        sum_nums = .0
        for num in nums:
            if isinstance(num, (float, int)):
                sum_nums += num
            else:
                return 0
        return sum_nums / len(nums)
    else:
        return 0


assert means(1, 2, 3, 4) == 2.5, "means测试用例1：(1, 2, 3, 4)，预期结果为2.5"
assert means(1.0, 1.0, 2.0, 2.0) == 1.5, "means测试用例2：(1.0, 1.0, 2.0, 2.0)，预期结果为1.5"
assert means(1) == 1, "means测试用例3：(1)，预期结果为1"
assert means() == 0, "means测试用例4：()，预期结果为0"
assert means("1", "2") == 0, 'means测试用例5：("1", "2")，预期结果为0'


def make_user(name, age, **extra) -> dict:
    if name and age:
        return {"name": name, "age": age, **extra}
    else:
        return dict()


make_user_res1 = dict()
make_user_res2 = {'name': 'Bob', 'age': 25}
make_user_res3 = {
    "name": "tom",
    "age": 18,
    "study": "测试",
    "friend": "me",
}
assert make_user("", "") == make_user_res1, f'make_user测试用例1：("","")，预期结果为{make_user_res1}'
assert make_user("Bob", 25) == make_user_res2, f'make_user测试用例2：("Bob", 25)，预期结果为{make_user_res2}'
assert make_user("tom", 18, study="测试",
                 friend="me") == make_user_res3, f'make_user测试用例3：("tom", 18, study="测试", friend="me")，预期结果为{make_user_res3}'


def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart


assert add_item("") == [""], 'add_item测试用例1：("")，预期结果为[""]'
assert add_item("a") == ["a"], 'add_item测试用例2：("a")，预期结果为["a"]'
assert add_item("b") == ["b"], 'add_item测试用例3：("b")，预期结果为["b"]'
assert add_item("b", ["a", "c"]) == ["a", "c", "b"], 'add_item测试用例4：("b",["a","c"])，预期结果为["a","c","b"]'
