# Day 2：控制流与列表推导式

> **日期**：2026-09-17 ｜ 训练 T1-2 ｜ Review：A-（通过）
> **对应文件**：`01-python/day02/exercises.py`、`01-python/day02/t1_2_guess.py`
> **数据库**：topic #53 → mastered（0.88）

---

## 一、今日目标

- [x] 掌握 if / elif / else 分支，理解 **truthy / falsy**（`0`、`""`、`[]`、`None` 都是假）
- [x] 掌握 for / while：遍历容器、`break` / `continue`，知道 **while 必须有出口**
- [x] 列表推导式进阶：带条件的推导式 vs 显式 for 循环，两种都写得出来
- [x] 理解**不可信输入**：用户输入必须校验，非法输入不能炸
- [x] 验收：T1-2 猜数字三个验收点全过

---

## 二、理论要点

### 2.1 条件分支

```python
def classify(score):
    if not score:              # falsy：0 / None / "" 都进这里
        return "无成绩"
    elif score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    return "不及格"
```

- 测试视角：**边界值**就是 if 的临界点（90/89/60/59/-1），每个边界都要有用例
- 顺序：先处理"退出 / 非法 / 空"，再处理业务分支

### 2.2 for 循环（遍历容器的主力）

```python
for item in items:                  # 遍历
for i, item in enumerate(items):    # 带下标
for k, v in my_dict.items():        # 遍历字典
```

### 2.3 while 循环（条件循环，必须有出口）

```python
while condition:
    ...
    # 必须有语句改变 condition，否则死循环
```

- 测试视角：**死循环 = 挂死**，是稳定性的头号问题
- 写 while 先想"什么条件下退出"

### 2.4 循环控制

- `break`：跳出整个循环
- `continue`：跳过本次，进入下一次
- `for ... else`：循环**没被 break** 才执行 else

### 2.5 推导式 vs 显式循环

```python
evens = [n for n in nums if n % 2 == 0]     # 推导式：一行，可读
evens = []
for n in nums:
    if n % 2 == 0:
        evens.append(n)                      # 显式：可读性差但能加复杂逻辑
```

- 原则：简单转换用推导式；逻辑复杂（多条语句）用显式循环

### 2.6 不可信输入

- 命令行 `input()` 返回的是 **str**，什么都可能进来：`"abc"`、`""`、`"12.5"`、`"-3"`
- 校验手段：`s.isdigit()`（纯数字字符串）→ `int(s)` 转换
- **输入与逻辑分离**是可测试性的第一步

---

## 三、练习：`exercises.py`

### 3.1 `classify_score(score) -> str`

```python
def classify_score(score) -> str:
    if not isinstance(score, int) or score < 0: return "非法输入"
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


assert classify_score(90) == "优秀", "classify_score测试用例1"
assert classify_score(89) == "及格", "classify_score测试用例2"
assert classify_score(60) == "及格", "classify_score测试用例3"
assert classify_score(59) == "不及格", "classify_score测试用例4"
assert classify_score(0) == "不及格", "classify_score测试用例5"
assert classify_score(-1) == "非法输入", "classify_score测试用例6"
```

**边界值**：90 / 89 / 60 / 59 / 0 / -1 / "abc"

### 3.2 `sum_while(n: int) -> int`

```python
def sum_while(n: int) -> int:
    if isinstance(n, int) and n >= 0:
        total = 0
        while n >= 0:
            total += n
            n -= 1
        return total
    return 0


assert sum_while(3) == 6, "sum_while测试用例1"
assert sum_while(0) == 0, "sum_while测试用例2"
assert sum_while(5) == 15, "sum_while测试用例3"
assert sum_while(-1) == 0, "sum_while测试用例4"
```

### 3.3 `find_all_even(nums: list) -> list`

```python
def find_all_even(nums: list) -> list:
    if not isinstance(nums, list): return []
    res = list()
    for v in nums:
        if v % 2 == 0:
            res.append(v)
    return res


assert find_all_even([1, 2, 3, 4, 5, 6]) == [2, 4, 6], "find_all_even测试用例1"
assert find_all_even([1, 3, 5]) == [], "find_all_even测试用例2"
assert find_all_even([2, 4, 6]) == [2, 4, 6], "find_all_even测试用例3"
assert find_all_even((1, 2, 3, 4, 5, 6)) == [], "find_all_even测试用例4"
```

> 注释掉了推导式版本 `return [v for v in nums if v % 2 == 0]`——两种写法对照。

---

## 四、训练任务 T1-2：猜数字

### 4.1 目标

```python
def guess_number(target: int, max_attempts: int = 5) -> bool:
    """让用户猜数字，返回是否在 max_attempts 次内猜中。"""
```

**验收**：
- [x] 猜中返回 `True`（含最后一次机会猜中）
- [x] 超出 `max_attempts` 次返回 `False`
- [x] 非法输入（`"abc"`、空串、负数）**不崩溃**，重新读取

### 4.2 实际代码

```python
# 01-python/day02/t1_2_guess.py
from dataclasses import dataclass


@dataclass
class Options:
    bigger: str = "大了"
    smaller: str = "小了"
    correct: str = "恭喜你，猜对了！"
    error: str = "输入非法"


def compare(guess: int, target: int) -> str:
    """纯逻辑函数，可 assert"""
    if isinstance(guess, int) and isinstance(target, int):
        if guess > target:
            return Options.bigger
        elif guess < target:
            return Options.smaller
        else:
            return Options.correct
    return Options.error


assert compare(1, 2) == Options.smaller, f"compare测试用例1"
assert compare(100, 100) == Options.correct, f"compare测试用例2"
assert compare("1", 1) == Options.error, f"compare测试用例3"
assert compare(" ", 1) == Options.error, f"compare测试用例4"


def guess_number(target: int, max_attempts: int = 5) -> bool:
    """交互壳：只负责 input + 循环 + 计数"""
    while max_attempts > 0:
        guess = input(f"剩余{max_attempts}回合，请输入您猜的数字：")
        if guess.isdigit():
            guess = int(guess)
            res = compare(guess, target)
            if res == Options.correct:
                print(Options.correct)
                return True
            else:
                if res == Options.smaller:
                    print(Options.smaller)
                elif res == Options.bigger:
                    print(res)
                max_attempts -= 1
        else:
            print(Options.error)
    return False
```

### 4.3 设计亮点

- **输入与逻辑分离**：`compare()` 纯逻辑可 assert，`guess_number()` 只留交互壳
- **dataclass 管理消息**：`Options` 集中管理提示文案，不硬编码字符串
- **非法输入不消耗回合**：`isdigit()` 不通过时不减 `max_attempts`

---

## 五、Review 复盘

| 轮次 | 评分 | 说明 |
|------|------|------|
| 首提 | **A-** | 通过，无明显问题 |

**Day 2 要点**：
- 边界值 = if 的临界点，每个临界点都要有用例
- 输入与逻辑分离 = 可测试性的第一步
- while 必须有出口，死循环是头号稳定性问题

---

## 六、打卡

| 项目 | 状态 | 日期 | Review |
|------|------|------|--------|
| 练习：classify_score / sum_while / find_all_even | ✅ | 2026-09-17 | — |
| T1-2 猜数字 | ✅ | 2026-09-17 | A- |
| 数据库更新 | ✅ | 2026-09-17 | topic #53 mastered (0.88) |
