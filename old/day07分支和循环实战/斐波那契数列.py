"""
前n个斐波那契数列

"""

max_range = int(input("请输入求取数量"))

a, b = 0, 1
for _ in range(max_range):
    a, b = b, a + b
    print(a)
