def discount(price: float, discount_rate: float = 1.0, coupon: float = 0.0) -> float:
    """计算折后价：price * discount_rate - coupon，结果不为负。"""

    if not isinstance(price, (float, int)) or price < 0:
        return 0

    real_price = price
    if isinstance(discount_rate, (float, int)) and 0 <= discount_rate <= 1:
        real_price = price * discount_rate
        if real_price < 0: real_price = 0
    if isinstance(coupon, (int, float)) and coupon >= 0:
        real_price -= coupon
        if real_price < 0:
            real_price = 0
    return real_price


assert discount(100) == 100, 'discount测试用例1：(100)，预期结果为100'
assert discount(100, 0.8) == 80, 'discount测试用例2：(100, 0.8)，预期结果为80'
assert discount(100, 0.5, 50) == 0, 'discount测试用例3：(100, 0.5, 50)，预期结果为0'
assert discount(100, 0.5, 80) == 0, 'discount测试用4：(100, 0.5, 80)，预期结果为0'
assert discount(-100, 0.5, 30) == 0, 'discount测试用5：(-100, 0.5, 30)，预期结果为0'
assert discount(100, -0.5, 30) == 70, 'discount测试用6：(100, -0.5, 30)，预期结果为70'
assert discount(100, 0.5, -30) == 50, 'discount测试用7：(100, 0.5, -30)，预期结果为50'
assert discount("100", 0.5, 30) == 0, 'discount测试用8：("100", 0.5, 30)，预期结果为0'
assert discount(100, "0.5", 30) == 70, 'discount测试用9：(100, "0.5", 30)，预期结果为70'
assert discount(100, 0.5, "30") == 50, 'discount测试用10：(100, 0.5, "30")，预期结果为50'
assert discount(100) == 100, 'discount测试用11：(100)，预期结果为100'
