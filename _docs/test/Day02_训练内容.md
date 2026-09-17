# Day 2：控制流（if/for/while）+ 列表推导式 —— 训练内容

> 日期：2026-09-16 ｜ 阶段 01：Python 语言基础（测试视角） ｜ 对应 `_docs/01_Python基础与测试入门.md` 周计划 D2 / 训练 T1-2

---

## 一、今日目标

- [ ] 掌握 if / elif / else 分支，理解 **truthy / falsy**（`0`、`""`、`[]`、`None` 都是假）
- [ ] 掌握 for / while：遍历容器、`break` / `continue`，知道 **while 必须有出口**（防死循环）
- [ ] 列表推导式进阶：带条件的推导式 vs 显式 for 循环，两种都写得出来
- [ ] 理解**不可信输入**：用户输入必须校验，非法输入不能炸（今天用 `str.isdigit()`）
- [ ] 验收：T1-2 猜数字三个验收点全过

## 二、理论要点（测试视角）

### 1. 条件分支

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

- 测试视角：**边界值**就是 if 的临界点（90 / 89 / 60 / 59 / -1），每个边界都要有用例
- 顺序：先处理"退出 / 非法 / 空"，再处理业务分支

### 2. for 循环（遍历容器的主力）

```python
for item in items:      # 遍历
for i, item in enumerate(items):   # 带下标
for k, v in my_dict.items():       # 遍历字典
```

### 3. while 循环（条件循环，必须有出口）

```python
while condition:
    ...
    # 必须有语句改变 condition，否则死循环
```

- 测试视角：**死循环 = 挂死**，是稳定性的头号问题；写 while 先想"什么条件下退出"

### 4. 循环控制

- `break`：跳出整个循环
- `continue`：跳过本次，进入下一次
- `for ... else`：循环**没被 break** 才执行 else（找不找得到一类的场景很好用）

### 5. 推导式 vs 显式循环

```python
evens = [n for n in nums if n % 2 == 0]     # 推导式：一行，可读
evens = []
for n in nums:
    if n % 2 == 0:
        evens.append(n)                      # 显式：可读性差但能加复杂逻辑
```

- 原则：简单转换用推导式；逻辑复杂（多条语句）用显式循环

### 6. 不可信输入（今天第一次正式接触）

- 命令行 `input()` 返回的是 **str**，什么都可能进来：`"abc"`、`""`、`"12.5"`、`"-3"`
- 校验手段：`s.isdigit()`（纯数字字符串）→ `int(s)` 转换
- 测试视角：**输入校验是防御式编程**；把"判断大了小了"这种纯逻辑抽成独立函数，才能用 assert 测

## 三、示例代码（教学用，亲手敲）

```python
# demo_control.py
def first_even(nums):
    """返回第一个偶数，没有则返回 None（for + return 等价 break）"""
    for n in nums:
        if n % 2 == 0:
            return n
    return None

def sum_while(n: int) -> int:
    """1+2+...+n；n=0 返回 0（while 版）"""
    total, i = 0, 1
    while i <= n:
        total += i
        i += 1
    return total

def compare(guess: int, target: int) -> str:
    """猜数字的核心逻辑：'大了' / '小了' / '猜中了' —— 纯逻辑，可 assert"""
    if guess > target:
        return "大了"
    if guess < target:
        return "小了"
    return "猜中了"
```

```python
# 交互输入校验（isdigit 版）
def get_number() -> int:
    while True:
        s = input("请输入一个数字：")
        if s.isdigit():
            return int(s)
        print("不是合法数字，请重试")
```

## 四、今日练习（`01-python/day02/`）

1. `classify_score(score) -> str`：≥90 优秀 / ≥60 及格 / <60 不及格；非法类型返回"非法输入"
   - 边界自己定：90 / 89 / 60 / 59 / -1 / "abc" —— 每条写一个 assert
2. `sum_while(n: int) -> int`：while 算 `1+2+...+n`；`n=0` 边界返回 0；`n=5` 返回 15
3. `find_all_even(nums: list) -> list`：显式 for 收集所有偶数，再写一行推导式版本对照

> 老规矩：每个函数写完，`assert` 覆盖 正常 / 边界 / 异常，消息写"预期是什么"。

## 五、今日实战任务（T1-2 猜数字）

```python
def guess_number(target: int, max_attempts: int = 5) -> bool:
    """让用户猜数字，返回是否在 max_attempts 次内猜中。"""
    ...
```

**验收**：
- [ ] 猜中返回 `True`（含最后一次机会猜中）
- [ ] 超出 `max_attempts` 次返回 `False`
- [ ] 非法输入（`"abc"`、空串、负数）**不崩溃**，重新读取

**加分设计（测试思维）**：把核心逻辑抽成独立函数再拼装——例如：

```python
def compare(guess: int, target: int) -> str: ...   # 纯逻辑，可 assert
def guess_number(target, max_attempts=5) -> bool:  # 只负责 input + 循环 + 计数
```

> 这样 `compare` 能用 assert 测（大/小/中三态），`guess_number` 只留交互壳。**输入与逻辑分离**是可测试性的第一步。

## 六、提交要求

```
01-python/day02/
├── exercises.py        # 练习 1~3
├── t1_2_guess.py       # 猜数字（含 compare + guess_number）
└── （demo 文件可留可删）
```

```powershell
git add 01-python/day02
git commit -m "day(02): control flow and guess number"
git push
```

## 七、Review 关注点（明天我按这个查）

- **边界值**：90/89/60/59/0/负数有没有断言
- **循环出口**：while 会不会死循环
- **非法输入**：真的不崩溃吗（空串、字母、负数、超长）
- **可测试性**：`compare` 是否独立、被 assert 覆盖
- 命名 / 可读性 / commit 规范
