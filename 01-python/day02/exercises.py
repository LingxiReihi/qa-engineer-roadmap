def classify_score(score) -> str:
    if not isinstance(score, int) or score < 0: return "非法输入"
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


assert classify_score(90) == "优秀", "classify_score测试用例1：score=90，return=\"优秀\"，预期正常通过"
assert classify_score(89) == "及格", "classify_score测试用例2：score=89，return=\"及格\"，预期正常通过"
assert classify_score(60) == "及格", "classify_score测试用例3：score=60，return=\"及格\"，预期正常通过"
assert classify_score(59) == "不及格", "classify_score测试用例4：score=59，return=\"不及格\"，预期正常通过"
assert classify_score(0) == "不及格", "classify_score测试用例5：score=0，return=\"不及格\"，预期正常通过"
assert classify_score(-1) == "非法输入", "classify_score测试用例6：score=-1，return=\"非法输入\"，预期正常通过"


def sum_while(n: int) -> int:
    if isinstance(n, int) and n >= 0:
        sum = 0
        while n >= 0:
            sum += n
            n -= 1
        return sum
    return 0


assert sum_while(3) == 6, "sum_while测试用例1：n=3，return=6，预期正常通过"
assert sum_while(0) == 0, "sum_while测试用例2：n=0，return=0，预期正常通过"
assert sum_while(5) == 15, "sum_while测试用例3：n=5，return=15，预期正常通过"
assert sum_while(-1) == 0, "sum_while测试用例4：n=-1，return=0，预期正常通过"


def find_all_even(nums: list) -> list:
    if not isinstance(nums, list): return []
    # return [v for v in nums if v % 2 == 0]
    res = list()
    for v in nums:
        if v % 2 == 0:
            res.append(v)
    return res


assert find_all_even([1, 2, 3, 4, 5, 6]) == [2, 4, 6], (
    "find_all_even测试用例1：nums=[1,2,3,4,5,6]，return=[2,4,6]，预期正常通过")
assert find_all_even([1, 3, 5]) == [], ("find_all_even测试用例2：nums=[1,3,5]，return=[]，预期正常通过")
assert find_all_even([2, 4, 6]) == [2, 4, 6], ("find_all_even测试用例3：nums=[2,4,6]，return=[2,4,6]，预期正常通过")
assert find_all_even((1, 2, 3, 4, 5, 6)) == [], "find_all_even测试用例4：nums=(1,2,3,4,5,6)，return=[]，预期正常通过"
