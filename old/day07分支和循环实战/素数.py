"""
输出素数
"""

max_num = int(input("请输入最大范围："))

for num in range(2, max_num):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):  # 最大范围为平方根+1
        if num % i == 0:  # 判断是否能被整除
            is_prime = False
            break
    if is_prime:  # 如果是素数，则输出
        print(num)
