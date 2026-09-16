# count_words(text: str) -> dict
def count_words(text: str) -> dict:
    """统计单词出现的次数"""
    if not isinstance(text, str):
        return {}
    elif text == "":
        return {}

    dic = dict()
    words = text.split()
    for word in words:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    return dic


assert count_words("hello world hello") == {"hello": 2, "world": 1}, "count_words测试用例1测试失败"
assert count_words("") == {}, "count_words测试用例2测试失败"
assert count_words(1) == {}, "count_words测试用例3测试失败"
assert count_words(" ") == {}, "count_words测试用例4测试失败"


# unique_sorted(items: list) -> list
def unique_sorted(items: list) -> list:
    if not isinstance(items, list):
        return []
    res = list({v for v in items})
    res.sort()
    return res


assert unique_sorted([3, 1, 3, 2, 5, 1, 1, 1, 1, 1, 2]) == [1, 2, 3, 5], "unique_sorted测试用例1测试失败"
assert unique_sorted([]) == [], "unique_sorted测试用例2测试失败"
assert unique_sorted(3) == [], "unique_sorted测试用例3测试失败"


# merge_dicts(a: dict, b: dict) -> dict
def merge_dicts(a: dict, b: dict) -> dict:
    if not isinstance(a, dict) or not isinstance(b, dict):
        return dict()
    return {**a, **b}


assert merge_dicts({'k': 5}, {'k': 6}) == {'k': 6}, "merge_dicts测试用例1测试失败"
assert merge_dicts({}, {}) == {}, "merge_dicts测试用例2测试失败"
assert merge_dicts(1, 2) == {}, "merge_dicts测试用例3测试失败"
