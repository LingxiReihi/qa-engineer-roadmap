# Day 06 · 重试装饰器（装饰器 / 闭包）

> 本规格所有用例值均已由教练参考实现验证（22 个用例全部通过），可直接作为验收依据。
> 规格只描述**行为**，不包含实现——你需要自己写出满足这些行为的代码。

## 一、学习目标

1. **闭包**：内层函数捕获并读取外层函数的变量（`attempts`、`delay`、`exceptions`）
2. **装饰器语法糖**：`@retry(attempts=3)` 等价于 `fn = retry(attempts=3)(fn)`
3. **装饰器工厂**：带参数的装饰器 = 「返回装饰器的函数」
4. **`functools.wraps`**：为什么需要它（否则 `__name__` / `__doc__` 会变成 `wrapper`）
5. **`*args, **kwargs` 转发**：包装函数必须把参数原样传给被包装函数
6. **异常传播**：重试耗尽后要抛**同一个异常对象**，而不是新造一个
7. **fail fast**：参数校验放在**装饰时**（`@retry(...)` 执行那一刻），而不是调用时
8. **QA 视角**：重试的真实场景——flaky 测试重跑、接口调用重试、且重试只对**幂等操作**安全

## 二、项目结构

```
01-python/day06/
├── test_retry.py          # 数据驱动测试 + 负向验证（放在 day06 根目录！）
└── retry/
    ├── __init__.py        # from .decorator import retry
    └── decorator.py       # retry 装饰器实现
```

- **测试文件必须在 `day06` 根目录**，不要在 `retry/` 包内部写断言块（Day 5 的教训：断言写在包内部会导致直接运行时 `sys.path[0]` 变成包目录，兄弟包 import 失败）
- **禁止 import `day05` 的任何代码**（跨 day 目录 import 是 sys.path 陷阱，已在 Day 5 记录）
- 断言辅助自包含：用内联 `try/except` 即可，不要引入 Day 5 的 `utils`

## 三、规格

### 3.1 函数签名

```python
def retry(attempts=3, delay=0, exceptions=(Exception,)):
```

`retry` 是**装饰器工厂**：它返回一个装饰器，该装饰器接受一个函数 `fn`，返回包装后的 `wrapper`。

### 3.2 参数（输入域声明）

| 参数 | 类型 | 默认值 | 约束 |
|------|------|--------|------|
| `attempts` | int | 3 | **必须 `>= 1`**。不接受 bool（`True`/`False` 是 int 子类，必须显式拒绝）、不接受 float、不接受 str |
| `delay` | int / float | 0 | **必须 `>= 0`**。不接受 bool |
| `exceptions` | tuple | `(Exception,)` | **非空**元组，每个元素必须是异常类（`issubclass(exc, BaseException)` 为真） |

**默认值语义**：`exceptions=(Exception,)` 捕获所有 `Exception` 及其子类，但**不捕获**直接继承 `BaseException` 的 `KeyboardInterrupt` / `SystemExit` / `GeneratorExit`。

### 3.3 行为契约

`retry(attempts, delay, exceptions)` 返回的装饰器包装函数 `fn` 后，wrapper 的行为：

1. **调用转发**：`wrapper(*args, **kwargs)` 把收到的参数**原样**传给 `fn(*args, **kwargs)`
2. **成功即返回**：`fn` 正常返回 → wrapper 返回同一个值（不加工、不替换）
3. **目标异常重试**：`fn` 抛出的异常是 `exceptions` 中某类型的**实例**（`isinstance` 语义，**子类也算**）→ 若 `attempts` 次尝试未用完，等待 `delay` 秒后重试
4. **非目标异常不重试**：`fn` 抛出的异常不属于 `exceptions` → **立即向上抛出，不重试**
5. **耗尽重抛**：`attempts` 次全部失败 → 抛出**最后一次尝试抛出的那个异常对象本身**（不包装、不替换、不新建；调用方可以用 `is` 判断同一性）
6. **元数据保留**：包装后的函数 `__name__`、`__doc__` 必须等于原函数（用 `functools.wraps`）

**不支持**：`@retry` 裸用（不带括号）。裸用时 `fn` 会被当作 `attempts` 参数传入，因类型校验在装饰时执行，会抛 `TypeError`。这不是 bug，是规格声明的行为。

### 3.4 参数校验（fail fast，装饰时执行）

以下情况在**执行 `retry(...)` 那一刻**（即写 `@retry(...)` 时）就抛错，**不等到函数被调用**：

| 条件 | 异常 |
|------|------|
| `attempts` 非 int（含 bool、float、str） | `TypeError` |
| `attempts` 是 int 但 `< 1` | `ValueError` |
| `delay` 非 int/float（含 bool） | `TypeError` |
| `delay` 是数值但 `< 0` | `ValueError` |
| `exceptions` 不是 tuple | `TypeError` |
| `exceptions` 是空元组 `()` | `ValueError` |
| `exceptions` 含非异常类元素（如 `(1,)`、`(ValueError, "x")`） | `TypeError` |

### 3.5 用例表（每个值均已验证）

**行为用例**：

| # | 场景 | 设置 | 预期 |
|---|------|------|------|
| 1 | 第一次就成功 | `failures=0`，`attempts=3` | 返回 `"ok"`，调用次数 == 1 |
| 2 | 失败 2 次后成功 | `failures=2`，`attempts=3` | 返回 `"ok"`，调用次数 == 3 |
| 3 | 一直失败 | `failures=99`，`attempts=3` | 调用次数 == 3；抛出的是**最后一次**那个异常对象（`is` 同一） |
| 4 | 单次尝试 | `failures=1`，`attempts=1` | 调用次数 == 1；抛 `ValueError` |
| 5 | 非目标异常不重试 | 抛 `TypeError`，`exceptions=(ValueError,)` | 调用次数 == 1；抛 `TypeError`（同一个对象） |
| 6 | 子类算目标 | 抛 `MyValueError(ValueError 子类)`，`exceptions=(ValueError,)` | 触发重试，调用次数 == 3，返回 `"ok"` |
| 7 | 参数转发 | `wrapper(5, key="v")` | 每次调用 fn 都收到 `(5,)` 和 `{"key": "v"}` |
| 8 | wraps 元数据 | 包装 `def flaky_doc(): """doc 内容"""` | `__name__ == "flaky_doc"`，`__doc__ == "doc 内容"` |

**参数校验用例（都在装饰时抛）**：

| # | 调用 | 预期异常 |
|---|------|----------|
| 9 | `retry(attempts=0)` | `ValueError` |
| 10 | `retry(attempts=-3)` | `ValueError` |
| 11 | `retry(attempts="3")` | `TypeError` |
| 12 | `retry(attempts=True)` | `TypeError` |
| 13 | `retry(attempts=3.0)` | `TypeError` |
| 14 | `retry(delay=-1)` | `ValueError` |
| 15 | `retry(delay=True)` | `TypeError` |
| 16 | `retry(delay="0.5")` | `TypeError` |
| 17 | `retry(exceptions=())` | `ValueError` |
| 18 | `retry(exceptions=[])` | `TypeError` |
| 19 | `retry(exceptions=(1,))` | `TypeError` |
| 20 | `retry(exceptions=(ValueError, "x"))` | `TypeError` |
| 21 | 裸用 `@retry` 装饰函数 | 装饰时 `TypeError` |

**计时语义**：`delay` 表示**每次重试前**等待的秒数（第 1 次调用前不等待）。用例 22：`delay=0`、`failures=2`、`attempts=3` → 返回 `"ok"`、调用 3 次。

> ⚠️ **不要求测真实等待时间**（如「delay=0.01 时总耗时 >= 0.02」）。依赖真实时间的断言是 flaky 测试的经典来源（机器负载会让它随机失败）。验证 `delay` 逻辑：`delay=0` 时行为正确 + `delay` 的参数校验两条即可。

## 四、测试要求

### 4.0 如何测试装饰器（先读这一节，再谈用例）

**核心认识**：`@retry(attempts=3)` 写在 `def fn` 上面，等价于后面有一行 `fn = retry(attempts=3)(fn)`。也就是说——

> **你测的不是「装饰器」，你测的是「被包装后的那个函数」`retry(attempts=3)(fn)`。**

所以测试脚手架只有三步，和测普通函数几乎一样，只是多了「把函数套一层」：

```python
def make_flaky(failures, exc, calls=None):
    """前 failures 次抛 exc、之后返回 ok；state.n 计调用次数，calls 收每次参数。"""
    state = {"n": 0}
    def fn(*a, **k):
        state["n"] += 1
        if calls is not None:
            calls.append((a, k))
        if state["n"] <= failures:
            raise exc
        return "ok"
    return fn, state


# 1) 造一个「前 2 次必失败」的目标函数
flaky, state = make_flaky(failures=2, exc=ValueError("x"), calls=None)

# 2) 手动套装饰器 —— 不要在测试里写 @ ！直接调用 retry(...)(fn)
wrapped = retry(attempts=3)(flaky)

# 3) 调用包装后的函数，断言结果 + 调用次数
result = wrapped()
assert result == "ok"          # 失败 2 次后成功了
assert state["n"] == 3          # 总共试了 3 次 == attempts
```

**为什么测试里不写 `@`，而是 `wrapped = retry(...)(fn)`**：

- `@` 是语法糖，绑定在 `def` 那行上，一个装饰器参数只能用一次；
- 手动调用能让你在一个 `def` 上套出**不同参数**的多个包装函数（`attempts=1`、`attempts=3`、`exceptions=(ValueError,)`……），用例才写得出来；
- 一行代码就还原了 `@` 做的事，等价且更灵活。

**三个必备手法**：

| 要验证什么 | 手法 | 为什么 |
|-----------|------|--------|
| 重试了几次 | 闭包变量 `state["n"]` 计数 | 这是包装函数调用**原函数**的次数，重试几次就看它 |
| 参数有没有原样传 | `calls` 列表记下每次 `(a, k)` | 比对转发是否漏参数 |
| 抛的是不是最后一次那个对象 | 先造 `err = ValueError("boom")`，原函数每次 `raise err`，断言 `caught is err` | `==` 比内容，`is` 比对象——只有 `is` 能证明「同一个对象被重新扔出来」 |

**异常同一性怎么断言**：

```python
err = ValueError("boom")
fn, state = make_flaky(failures=99, exc=err, calls=None)
wrapped = retry(attempts=3)(fn)
caught = None
try:
    wrapped()
except ValueError as e:
    caught = e
assert state["n"] == 3     # 试满 3 次
assert caught is err       # 抛的是最开始那个对象，不是新造的
```

**参数校验怎么断言（fail fast）**：

```python
try:
    retry(attempts=0)      # 装饰时（这一行执行时）就该抛
    assert False, "应抛 ValueError"
except ValueError:
    pass
```

> 把 `make_flaky`、`state`、`err` 这些脚手架写进你的 `test_retry.py`（这是**测试工具**，不是 retry 的实现，不算抄答案）。规格 §3.5 的 21 条用例 = 用这套脚手架把 §3.3 行为契约逐条落到断言。

### 4.1 断言技巧（两条新增）

1. **闭包计数器**：构造一个内部计数、前 `failures` 次抛异常的函数，用闭包变量记录调用次数——这是验证「重试了几次」的标准手法
2. **异常对象同一性**：预先创建异常对象 `err = ValueError("boom")`，让函数每次都 `raise err`；捕获后断言 `caught is err`——这是验证「抛出的是最后一次那个对象」的唯一可靠方式（`==` 比较的是内容，`is` 比较的是对象）

### 4.2 负向验证清单（逐条改坏，测试必须失败）

每改坏一处，跑一遍 `python test_retry.py`，确认 exit 非 0：

1. 把 wrapper 改成**只调用一次**（删掉重试循环）→ 用例 2、3 必须失败
2. 把 `raise last_error` 改成 `raise ValueError("wrong")`（新建异常）→ 用例 3 必须失败（`is` 同一性抓到的）
3. 删掉 `@functools.wraps(fn)` → 用例 8 必须失败
4. 删掉任一 fail-fast 校验分支 → 对应用例 9~21 必须失败
5. 忽略 `attempts`、恒重试 3 次 → 用例 4（`attempts=1` 只调用 1 次）必须失败

## 五、运行方式与注意事项

```bash
cd 01-python/day06
python test_retry.py        # 期望 exit 0，打印通过信息
```

- 测试脚本在 `day06` 根目录直接运行，`from retry import retry` 即可解析（cwd 在 sys.path 上）
- 断言消息格式沿用 Day 5：`函数名()测试用例N：输入，预期结果X，测试不通过`
- **编号连续**：同一函数内 `测试用例N` 不允许重复（Day 5 教训，已累计 8 次）；提交前用 grep 检查编号
- 不要在测试里 import `time` 做真实等待断言（见 3.5 计时语义）

## 六、验收条件

1. `python test_retry.py` → exit 0
2. 规格 3.5 的全部用例有对应断言，且每个预期值与你代码的实际行为一致
3. 4.2 的 5 项负向验证逐条做一遍，全部 exit 非 0
4. 编号连续（grep 检查）
5. 提交后贴 `python test_retry.py` 输出 + 负向验证结果

## 七、打卡

| 项目 | 状态 | 日期 | Review |
|------|------|------|--------|
| T2-1 retry 装饰器 | ✅ | 2026-09-21 | 三轮收口。规格 3.5 全部 21 用例 + 校验矩阵 12 条通过；负向验证 5/5；21 编号零重复（8 次连错后首次）；`caught is err` 断言当场抓住 `return catch` bug，`attempts=2` 恢复用例5 辨别力 |
