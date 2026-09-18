# Day 3：函数与默认参数（测试视角）

> **日期**：2026-09-17 ｜ 训练 T1-3 ｜ Review：A-（修正后）
> **对应文件**：`01-python/day03/exercises.py`、`01-python/day03/t1_3_discount.py`
> **数据库**：topic #54 → in_progress（0.7）

---

## 一、今日目标

- [x] 理解函数签名：参数、返回值、**默认参数**
- [x] 掌握 `*args` / `**kwargs` 收集参数
- [x] 认识并避开**可变默认参数陷阱**（`def f(x=[])`）
- [x] 理解**纯函数**（同输入同输出、无副作用）
- [x] 验收：T1-3 四条验收 + 自加边界断言

---

## 二、理论要点

### 2.1 函数签名全家桶

```python
def f(a, b=1, *args, **kwargs):
    ...
```

| 参数类型 | 示例 | 说明 |
|----------|------|------|
| 位置参数 | `a` | 必填 |
| 默认参数 | `b=1` | 可省略，有默认值 |
| 可变位置参数 | `*args` | 收集多余位置参数 → **元组** |
| 可变关键字参数 | `**kwargs` | 收集多余关键字参数 → **字典** |

### 2.2 可变默认参数陷阱（面试高频）

```python
def add_item(item, cart=[]):      # ❌ 默认 [] 只创建一次！
    cart.append(item)
    return cart

add_item("a")   # ['a']
add_item("b")   # ['a', 'b']  ← 竟然共享了同一个 list
```

默认参数在**函数定义时求值一次**，之后所有调用共用同一个对象。

**修复**：
```python
def add_item(item, cart=None):    # ✅ 默认 None，内部再建
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```

> 测试视角：这也是"函数隐藏状态"的教训——**纯函数不该有跨调用的记忆**。

### 2.3 纯函数（测试友好的函数）

- 同样的输入 → 永远同样的输出
- 不改外部状态（无副作用）
- 好处：**可以直接 assert**，不需要搭环境

> `discount(price, rate, coupon)` 就是一个典型纯函数——T1-3 的测试就是直接断言它。

---

## 三、练习：`exercises.py`

### 3.1 `means(*nums) -> float`

平均值。边界：空参数返回 0；非数字参数返回 0。

```python
def means(*nums) -> float:
    if nums and len(nums) > 0:
        sum_nums = .0
        for num in nums:
            if isinstance(num, (float, int)):
                sum_nums += num
            else:
                return 0
        return sum_nums / len(nums)
    else:
        return 0


assert means(1, 2, 3, 4) == 2.5, "means测试用例1"
assert means(1.0, 1.0, 2.0, 2.0) == 1.5, "means测试用例2"
assert means(1) == 1, "means测试用例3"
assert means() == 0, "means测试用例4"
assert means("1", "2") == 0, "means测试用例5"
```

### 3.2 `make_user(name, age, **extra) -> dict`

```python
def make_user(name, age, **extra) -> dict:
    if name and isinstance(age, int) and age >= 0:
        return {"name": name, "age": age, **extra}
    else:
        return dict()


assert make_user("", "") == {}, "make_user测试用例1"
assert make_user("Bob", 0) == {'name': 'Bob', 'age': 0}, "make_user测试用例2"
assert make_user("tom", 18, study="测试", friend="me") == \
    {"name": "tom", "age": 18, "study": "测试", "friend": "me"}, "make_user测试用例3"
```

### 3.3 `add_item(item, cart=None)`

可变默认参数陷阱的修复版。

```python
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart


assert add_item("") == [""], "add_item测试用例1"
assert add_item("a") == ["a"], "add_item测试用例2"
assert add_item("b") == ["b"], "add_item测试用例3"
assert add_item("b", ["a", "c"]) == ["a", "c", "b"], "add_item测试用例4"
```

> 两次连续调用 `add_item("a")` 和 `add_item("b")` 各自返回 `["a"]` 和 `["b"]`——没有共享状态。

---

## 四、训练任务 T1-3：订单折扣

### 4.1 目标

```python
def discount(price: float, discount_rate: float = 1.0, coupon: float = 0.0) -> float:
    """计算折后价：price * discount_rate - coupon，结果不为负。"""
```

### 4.2 验收要求

- `discount(100)` → 100
- `discount(100, 0.8)` → 80
- `discount(100, 0.5, 50)` → 0（不为负）
- `discount(100, 0.5, 80)` → 0

### 4.3 实际代码

```python
# 01-python/day03/t1_3_discount.py
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


assert discount(100) == 100, 'discount测试用例1'
assert discount(100, 0.8) == 80, 'discount测试用例2'
assert discount(100, 0.5, 50) == 0, 'discount测试用例3'
assert discount(100, 0.5, 80) == 0, 'discount测试用例4'
assert discount(-100, 0.5, 30) == 0, 'discount测试用例5'
assert discount(100, -0.5, 30) == 70, 'discount测试用例6'
assert discount(100, 0.5, -30) == 50, 'discount测试用例7'
assert discount("100", 0.5, 30) == 0, 'discount测试用例8'
assert discount(100, "0.5", 30) == 70, 'discount测试用例9'
assert discount(100, 0.5, "30") == 50, 'discount测试用例10'
assert discount(100) == 100, 'discount测试用例11'
```

### 4.4 扩展断言（超出基本要求）

| 断言 | 输入 | 预期 | 考点 |
|------|------|------|------|
| 用例5 | `(-100, 0.5, 30)` | 0 | 负数 price → 直接返回 0 |
| 用例6 | `(100, -0.5, 30)` | 70 | 负数 rate → 忽略折扣，只减券 |
| 用例7 | `(100, 0.5, -30)` | 50 | 负数 coupon → 忽略券，只打折 |
| 用例8 | `("100", 0.5, 30)` | 0 | 字符串 price → 非数字返回 0 |
| 用例9 | `(100, "0.5", 30)` | 70 | 字符串 rate → 忽略折扣 |
| 用例10 | `(100, 0.5, "30")` | 50 | 字符串 coupon → 忽略券 |

> 11 条断言覆盖：正常路径 + 边界值 + 非法类型输入。

---

## 五、Review 复盘

| 轮次 | 评分 | 发现的问题 | 修正 |
|------|------|-----------|------|
| 首提 | **B+** | 未处理负数钳位；非法输入处理不完善 | — |
| 修正后 | **A-** | — | 加 `max(0, ...)` 钳位；补非法类型判断；补 6 条扩展断言 |

**Day 3 要点**：
- 可变默认参数只创建一次——用 `None` + 内部初始化
- 纯函数 = 可直接 assert = 测试开发最爱的函数形态
- 非法输入不是"假设不会发生"，而是要显式处理

---

## 六、打卡

| 项目 | 状态 | 日期 | Review |
|------|------|------|--------|
| 练习：means / make_user / add_item | ✅ | 2026-09-17 | — |
| T1-3 订单折扣（11 条断言） | ✅ | 2026-09-17 | A-（修正后） |
| 数据库更新 | ✅ | 2026-09-17 | topic #54 in_progress (0.7) |
