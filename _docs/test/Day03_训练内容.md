# Day 3：函数（测试视角）——训练内容

> 日期：2026-09-17 ｜ 阶段 01：Python 语言基础（测试视角） ｜ 对应 `_docs/01_Python基础与测试入门.md` 周计划 D3 / 训练 T1-3

---

## 一、今日目标

- [ ] 理解函数签名：参数、返回值、**默认参数**
- [ ] 掌握 `*args` / `**kwargs` 收集参数
- [ ] 认识并避开**可变默认参数陷阱**（`def f(x=[])`）——今天最值钱的一课
- [ ] 理解**纯函数**（同输入同输出、无副作用）——测试开发最爱的函数形态
- [ ] 验收：T1-3 四条验收 + 自加边界断言

## 二、理论要点

### 1. 函数签名全家桶

```python
def f(a, b=1, *args, **kwargs):
    ...
```

- `a`：位置参数（必填）
- `b=1`：默认参数（可省略；有默认行为）
- `*args`：收集多余位置参数 → **元组**
- `**kwargs`：收集多余关键字参数 → **字典**

### 2. 可变默认参数陷阱（面试高频）

```python
def add_item(item, cart=[]):      # ❌ 默认 [] 只创建一次！
    cart.append(item)
    return cart

add_item("a")   # ['a']
add_item("b")   # ['a', 'b']  ← 竟然共享了同一个 list
```

默认参数在**函数定义时求值一次**，之后所有调用共用同一个对象。修复：

```python
def add_item(item, cart=None):    # ✅ 默认 None，内部再建
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```

- 测试视角：这也是"函数隐藏状态"的教训——**纯函数不该有跨调用的记忆**

### 3. 纯函数（测试友好的函数）

- 同样的输入 → 永远同样的输出
- 不改外部状态（无副作用）
- 好处：**可以直接 assert**，不需要搭环境

> `discount(price, rate, coupon)` 就是一个典型纯函数——T1-3 的测试就是直接断言它。

## 三、示例代码（教学用，亲手敲）

```python
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart

assert add_item("a") == ["a"]
assert add_item("b") == ["b"], "修复后两次调用互不污染"

def total(*nums):
    """可变位置参数，返回总和"""
    return sum(nums)

assert total(1, 2, 3) == 6
assert total() == 0, "空参数边界"

def describe(**info):
    """可变关键字参数"""
    return ", ".join(f"{k}={v}" for k, v in info.items())

assert describe(name="测试", level=1) == "name=测试, level=1"
```

## 四、今日练习（`01-python/day03/exercises.py`）

1. `mean(*nums) -> float`：平均值。边界自己定：空参数返回什么？单参数？写断言
2. `make_user(name, age, **extra) -> dict`：返回 `{"name": name, "age": age, **extra}`，断言多个额外关键字
3. `add_item(item, cart=None)`：修复版，断言两次调用**不共享**列表

> 一个隐藏考点：`mean()` 空参数时 `sum([]) / len([])` 会 `ZeroDivisionError`——你怎么处理？自己定义并写进断言。

## 五、今日实战任务（T1-3 订单折扣）

```python
def discount(price: float, discount_rate: float = 1.0, coupon: float = 0.0) -> float:
    """计算折后价：price * discount_rate - coupon，结果不为负。"""
    ...
```

**验收（四条 assert）**：
- `discount(100)` → 100
- `discount(100, 0.8)` → 80
- `discount(100, 0.5, 50)` → 0（不为负）
- `discount(100, 0.5, 80)` → 0

**加分**：结果不为负怎么实现（`max(0, ...)`？）；非法输入（负数 price / 字符串 / rate>1？）怎么处理——自己定义规则并断言。

> 测试思维：这就是一个纯函数的用例设计——每个参数组合都是用例（正常 / 边界 0 / 异常）。

## 六、提交要求

```
01-python/day03/
├── exercises.py        # 练习 1~3
└── t1_3_discount.py    # discount + 断言
```

```powershell
git add 01-python/day03
git commit -m "day(03): functions, defaults and discount"
git push
```

## 七、Review 关注点

- **可变默认参数陷阱**有没有避开（`cart=None` 模式）
- `discount` 负结果钳位（`max(0, ...)`）
- 边界：`coupon > price*rate`、`rate=0`、`price=0`、空 `*args`
- `*args` / `**kwargs` 使用是否准确
- 断言覆盖：正常 / 边界 / 异常