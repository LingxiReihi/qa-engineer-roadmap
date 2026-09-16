nums = [n for n in range(1, 11)]
res1 = [n ** 2 for n in nums]
assert res1 == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], "res1测试用例1测试失败"

words = ["hello", "world", "python"]
res2 = {w: len(w) for w in words}
assert res2 == {"hello": 5, "world": 5, "python": 6}, "res2测试用例1测试失败"

nums_with_dup = [1, 1, 2, 2, 3, 3]
res3 = {n for n in nums_with_dup}
assert res3 == {1, 2, 3}, "res3测试用例1测试失败"
