# Day 1：变量、数据类型、容器（测试视角）

> **日期**：2026-09-16 ｜ 训练 T1-1 ｜ Review：B+（修正后通过）
> **对应文件**：`01-python/day01/containers.py`、`01-python/day01/t1_1_comprehensions.py`
> **数据库**：topic #52 → mastered（0.85）

---

## 一、今日目标

- [x] 分清 4 种基本类型（int / float / str / bool）与 4 种容器（list / dict / set / tuple）
- [x] 理解**可变 vs 不可变**，认识**别名**陷阱
- [x] 会写列表 / 字典 / 集合**推导式**
- [x] 认识**类型注解**，会用 **assert 断言**做自检
- [x] 验收：T1-1 三题全部跑通，每个函数回答"正常 / 异常 / 边界"三问

---

## 二、理论要点

### 2.1 变量与别名

变量是"标签"不是"盒子"：`b = a` 不复制，两个标签指向同一对象。

**别名陷阱**：`b.append(3)` 后 `a` 也变了——测试里做数据隔离时是头号坑。

```python
a = [1, 2]
b = a            # b 和 a 指向同一个 list
b.append(3)
print(a)         # [1, 2, 3] ← a 也变了！
```

**动态类型**：类型跟着值走，不跟变量走。接口 JSON 里的 `"1"`（str）和 `1`（int）是两个世界。

### 2.2 容器四兄弟

| 容器 | 有序 | 可修改 | 可重复 | 典型场景 |
|------|------|--------|--------|----------|
| `list` `[1,2]` | ✅ | ✅ | ✅ | 有序数据、批量测试参数 |
| `tuple` `(1,2)` | ✅ | ❌ | ✅ | 不可变数据、多返回值 |
| `dict` `{"k":1}` | 插入序 | ✅ | 键唯一 | **接口 JSON 就是 dict** |
| `set` `{1,2}` | ❌ | ✅ | ❌ 自动去重 | 去重、成员判断 |

> 记忆锚：接口返回的 JSON 几乎总是当 dict 处理——阶段 04 接口自动化的地基。

### 2.3 推导式

```python
[表达式 for x in 可迭代对象 if 条件]   # 列表推导式
{键: 值 for x in 可迭代对象}            # 字典推导式
{x for x in 可迭代对象}                 # 集合推导式
```

> 测试场景：批量造测试数据、过滤日志行、把接口列表转成可断言的结构。

### 2.4 类型注解

```python
def add(a: int, b: int) -> int:
    return a + b
```

运行时不生效，是写给人、IDE、mypy 看的"合同"。

### 2.5 断言（assert）

```python
assert 条件, "条件不成立时显示的消息"
```

- 条件为 True → 静默通过；False → 抛 `AssertionError` 带消息中止
- **三步心法**：算出结果 → 写下预期 → `assert 实际 == 预期`
- **关键**：预期来自**需求**，不是来自实现

---

## 三、训练任务 T1-1：容器三函数

### 3.1 `count_words(text) -> dict`

统计单词频次。处理非字符串 → `{}`；空串/空格边界；`split()` 按任意空白切分。

```python
# 01-python/day01/containers.py
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
```

### 3.2 `unique_sorted(items) -> list`

去重 + **升序**。集合去重后 `res.sort()`。

```python
def unique_sorted(items: list) -> list:
    if not isinstance(items, list):
        return []
    res = list({v for v in items})
    res.sort()
    return res


assert unique_sorted([3, 1, 3, 2, 5, 1, 1, 1, 1, 1, 2]) == [1, 2, 3, 5], "unique_sorted测试用例1测试失败"
assert unique_sorted([]) == [], "unique_sorted测试用例2测试失败"
assert unique_sorted(3) == [], "unique_sorted测试用例3测试失败"
```

### 3.3 `merge_dicts(a, b) -> dict`

合并，b 覆盖 a。`{**a, **b}` 返回新字典，不污染原数据。

```python
def merge_dicts(a: dict, b: dict) -> dict:
    if not isinstance(a, dict) or not isinstance(b, dict):
        return dict()
    return {**a, **b}


assert merge_dicts({'k': 5}, {'k': 6}) == {'k': 6}, "merge_dicts测试用例1测试失败"
assert merge_dicts({}, {}) == {}, "merge_dicts测试用例2测试失败"
assert merge_dicts(1, 2) == {}, "merge_dicts测试用例3测试失败"
```

---

## 四、推导式三题

```python
# 01-python/day01/t1_1_comprehensions.py

# 题1：偶数的平方
nums = [n for n in range(1, 11) if n % 2 == 0]
res1 = [n ** 2 for n in nums]
assert res1 == [4, 16, 36, 64, 100], "res1测试用例1测试失败"

# 题2：字长字典
words = ["hello", "world", "python"]
res2 = {w: len(w) for w in words}
assert res2 == {"hello": 5, "world": 5, "python": 6}, "res2测试用例1测试失败"

# 题3：集合去重
nums_with_dup = [1, 1, 2, 2, 3, 3]
res3 = {n for n in nums_with_dup}
assert res3 == {1, 2, 3}, "res3测试用例1测试失败"
```

---

## 五、Review 复盘

| 轮次 | 评分 | 发现的问题 | 修正 |
|------|------|-----------|------|
| 首提 | **C** | ① set 去重后未排序，测试碰巧通过（`[10,1,2]` → `[1,10,2]`）② `a.update(b)` 污染调用方原字典 ③ T1-1 第 1 题漏"偶数"条件，断言预期被实现带着走 | — |
| 修正后 | **B+（通过）** | — | 补 `if n % 2 == 0` 筛选；`res.sort()`；改 `{**a, **b}`；`split()` 无参；新增 `count_words(" ")` 边界用例 |

**今天最值钱的一课**：测试全绿 ≠ 需求满足——断言预期必须来自需求，而不是"代码碰巧输出什么"。

---

## 六、打卡

| 项目 | 状态 | 日期 | Review |
|------|------|------|--------|
| T1-1 容器三函数 | ✅ | 2026-09-16 | B+（修正后） |
| T1-1 推导式三题 | ✅ | 2026-09-16 | B+（修正后） |
| 数据库更新 | ✅ | 2026-09-16 | topic #52 mastered (0.85) |
