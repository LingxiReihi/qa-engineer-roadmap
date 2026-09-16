# 获取从1到6的所有平方数，并作为列表
squares = [n * n for n in range(1, 6)]
# 获取20以内的所有偶数，并作为列表
evens = [n for n in range(20) if n % 2 == 0]
# 获取列表中单词长度，并作为字典
lengths = {w: len(w) for w in ["apple", "pear"]}

print("squares: ", squares)
print("evens: ", evens)
print("lengths: ", lengths)
