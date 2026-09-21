# Day 07 · 函数式数据变换（闭包 / 生成器 / 惰性求值）

> 本规格所有用例值均已由教练参考实现验证（25 项全部通过）。
> 规格只描述**行为**，不包含实现——你需要自己写出满足这些行为的代码。

## 一、学习目标

1. **闭包**：内层函数捕获外层函数的变量；每次调用工厂函数都创建**独立**的环境（实例之间互不干扰）
2. **生成器函数 vs 返回生成器的普通函数**：前者函数体要等第一次迭代才执行（**校验也会被推迟**），后者校验即时、产出惰性——本课题强迫你在两者之间做出选择
3. **惰性求值**：大范围不占内存；`fn`/`pred` 的调用在**产出时逐个发生**，不是一次全做完
4. **函数式组合**：`lazy_map` → `lazy_filter` → 列表推导，对照内置 `map`/`filter`/`range` 验证行为一致
5. **QA 视角**：测试数据的生成与清洗——生成用例 ID（计数器）、采样取值（区间）、批量转换（map）、过滤无效行（filter），真实测试脚手架的基本件

## 二、项目结构

```
01-python/day07/
├── test_transform.py       # 数据驱动测试 + 负向验证（day07 根目录！）
└── transform/
    ├── __init__.py         # from .tools import make_counter, gen_range, lazy_map, lazy_filter
    └── tools.py            # 四个函数实现
```

- 测试文件必须在 `day07` 根目录（Day 5 教训：断言写包内导致 sys.path 陷阱）
- 禁止 import `day05` / `day06` 的任何代码（跨 day 目录 import 陷阱）
- 断言自包含，不引入外部辅助

## 三、规格

### 3.1 `make_counter(start=0, step=1)` —— 闭包工厂

**行为**：返回一个**无参函数** `counter`；第一次调用返回 `start`，之后每次返回「上一次返回值 + `step`」。每次调用 `make_counter` 都创建全新的独立计数器。

| 参数 | 类型 | 默认 | 约束 |
|------|------|------|------|
| `start` | int | 0 | 不接受 bool、float、str |
| `step` | int | 1 | 不接受 bool；**必须 `!= 0`**（`step=0` 每次返回同一值，无意义） |

**校验（调用 `make_counter` 时即抛，fail fast）**：

| 条件 | 异常 |
|------|------|
| `start` 非 int（含 bool） | `TypeError` |
| `step` 非 int（含 bool） | `TypeError` |
| `step == 0` | `ValueError` |

**用例表**：

| # | 设置 | 预期 |
|---|------|------|
| C1 | `make_counter()` | 依次返回 `0, 1, 2, ...` |
| C2 | `make_counter(5)` | `5, 6, 7, ...` |
| C3 | `make_counter(0, 2)` | `0, 2, 4, ...` |
| C4 | `make_counter(10, -3)` | `10, 7, 4, ...` |
| C5 | 两个独立实例 `a, b = make_counter(), make_counter()` | `a` 与 `b` 互不干扰：`[a(),a(),b(),b(),a()] == [0,1,0,1,2]` |
| C6 | `make_counter(True)` | `TypeError` |
| C7 | `make_counter(step=True)` | `TypeError` |
| C8 | `make_counter(step=0)` | `ValueError` |
| C9 | `make_counter("1")` | `TypeError` |
| C10 | `make_counter(1.5)` | `TypeError` |

> ⚠️ **counter 是无参函数，不是迭代器**：取下一个值用 `counter()`，**不是** `next(counter)`。前者返回下一个计数，后者抛 `TypeError: 'function' object is not an iterator`（这是验证过程中实际踩过的坑，已修正）。

### 3.2 `gen_range(start, end, step=1)` —— 生成器

**行为**：惰性产出 `[start, end)` 区间（**end 开区间**），步进 `step`。`step > 0` 递增、`step < 0` 递减。自己用 `yield` 实现，**不用内置 `range`**。

| 参数 | 类型 | 默认 | 约束 |
|------|------|------|------|
| `start` | int | — | 不接受 bool |
| `end` | int | — | 不接受 bool |
| `step` | int | 1 | 不接受 bool；**必须 `!= 0`** |

**校验（调用 `gen_range` 时即抛，fail fast）**：

| 条件 | 异常 |
|------|------|
| `start` / `end` / `step` 非 int（含 bool） | `TypeError` |
| `step == 0` | `ValueError` |

**返回类型必须是真的生成器**：`isinstance(g, types.GeneratorType)` 为 True（不是 list、不是普通迭代器对象）。

**用例表**：

| # | 设置 | 预期 |
|---|------|------|
| G1 | `list(gen_range(0, 5))` | `[0, 1, 2, 3, 4]`（end 开区间） |
| G2 | `list(gen_range(0, 5, 2))` | `[0, 2, 4]` |
| G3 | `list(gen_range(5, 0, -1))` | `[5, 4, 3, 2, 1]` |
| G4 | `list(gen_range(5, 0, 1))` | `[]`（方向不符，空） |
| G5 | `list(gen_range(3, 3))` | `[]`（start == end） |
| G6 | `gen_range(0, 10**9)` 取前 3 个 | `[0, 1, 2]`，不 OOM（惰性） |
| G7 | `type` 检查 | `types.GeneratorType` |
| G8 | `gen_range(0, 5, 0)` | 调用时 `ValueError` |
| G9 | `gen_range(0, 5, True)` | `TypeError` |
| G10 | `gen_range(True, 5)` | `TypeError` |

**惰性验证**（G11/G12）：生成器函数体到**第一次迭代**才执行。用带副作用的哨兵验证：迭代前 `executed == False`，`list(...)` 后才变 True。

### 3.3 `lazy_map(fn, iterable)` —— 惰性 map

**行为**：对 `iterable` 的每个元素产出 `fn(x)`。自己用 `yield` 实现，对照内置 `map` 验证行为一致。

**函数形态（本课题核心教学点）**：`lazy_map` 必须是「**返回生成器的普通函数**」，**不是**生成器函数。原因：如果直接写 `def lazy_map(...)` 且内部有 `yield`，整个函数体（含 `fn` 的 `callable` 校验）都会推迟到第一次迭代——`lazy_map(123, [1,2])` 调用时不抛错、迭代时才抛，校验失去 fail fast 意义。

```python
# 正确形态：
def lazy_map(fn, iterable):
    if not callable(fn):
        raise TypeError(...)          # 调用时即抛
    def _map():
        for item in iterable:
            yield fn(item)
    return _map()                     # 返回生成器，fn 逐个惰性调用
```

**用例表**：

| # | 设置 | 预期 |
|---|------|------|
| M1 | `list(lazy_map(lambda x: x*2, [1,2,3]))` | `[2, 4, 6]` |
| M2 | `list(lazy_map(lambda x: x, []))` | `[]` |
| M3 | `lazy_map(123, [1,2])` | **调用时** `TypeError` |
| M4 | `lazy_map(None, [1])` | **调用时** `TypeError` |
| M5/M6 | 带副作用 fn（记录每次入参）| `next` 一次 → `calls == [1]`；再 `next` → `calls == [1,2]`（惰性：产出几个才调几次） |
| M7 | 与内置 `map` 一致 | `list(lazy_map(str, [3,-1,7,0,9])) == list(map(str, ...))` |

### 3.4 `lazy_filter(pred, iterable)` —— 惰性 filter

**行为**：产出 `iterable` 中满足 `pred(x)` 的元素。自己用 `yield` 实现，对照内置 `filter` 验证行为一致。

**形态要求与 `lazy_map` 相同**：返回生成器的普通函数，`callable(pred)` 校验在调用时即抛。

**用例表**：

| # | 设置 | 预期 |
|---|------|------|
| F1 | `list(lazy_filter(lambda x: x%2==0, [1,2,3,4]))` | `[2, 4]` |
| F2 | `list(lazy_filter(lambda x: True, []))` | `[]` |
| F3 | `lazy_filter(123, [1])` | **调用时** `TypeError` |
| F4 | 带副作用 pred | `pred` 对每个元素恰好调用一次（惰性，产出时逐个） |
| F5 | 与内置 `filter` 一致 | 对照结果相同 |

### 3.5 组合用例（QA 场景：测试数据生成 + 清洗）

| # | 步骤 | 预期 |
|---|------|------|
| Z1 | `counter = make_counter(1000)`；`data = list(lazy_map(lambda x: x*10, gen_range(1, 4)))`；`rows = [(counter(), d) for d in data]` | `rows == [(1000, 10), (1001, 20), (1002, 30)]` |
| Z2 | `list(lazy_filter(lambda t: t[0] % 2 == 0, rows))` | `[(1000, 10), (1002, 30)]` |

## 四、测试要求

### 4.0 三个新断言技巧（沿用 Day 6 脚手架互证）

1. **实例独立性**（C5）：两个计数器交替取值，证明每次调用工厂创建新闭包环境
2. **惰性验证**（M5/M6、F4）：用带副作用的 `fn`/`pred`，验证「产出几个才调用几次」——这是 `yield` 惰性的直接证据
3. **GeneratorType 断言**（G7）：`isinstance(g, types.GeneratorType)`，需要 `import types`

### 4.1 负向验证清单（逐条改坏，测试必须失败）

1. 把 `make_counter` 的状态改成**模块级变量** → C5（实例独立）必须失败
2. 把 `gen_range` 改成**返回 list**（不用 yield）→ G6（10**9 不 OOM）、G7（GeneratorType）必须失败
3. 把 `lazy_map`/`lazy_filter` 改回**生成器函数**（yield 直接写在函数体）→ M3/M4/F3（调用时校验）必须失败
4. 删掉 `lazy_map` 的惰性（先 `list(iterable)` 再处理）→ M5/M6（副作用计次）必须失败
5. 把 `step=0` 校验删掉 → C8/G8 必须失败

### 4.2 对照验证（本课题独有）

对每个手写函数，加一条「与内置对照」的断言（M7/F5 已有）——这不是多余的，是证明你的实现语义正确的**基准测试**。

## 五、运行方式与注意事项

```bash
cd 01-python/day07
python test_transform.py     # 期望 exit 0
```

- 测试脚本在 `day07` 根目录直接运行，`from transform import ...` 即可解析
- 断言消息格式沿用 Day 5/6：`函数名()测试用例N：输入，预期结果X，测试不通过`
- **编号连续**：提交前 grep 检查（Day 5/6 教训）
- 用 `next(g)` 做惰性验证时，注意验证完的生成器已消耗部分元素，**不要在同一生成器上继续断言剩余元素**（惰性的副作用）——需要重新创建生成器

## 六、验收条件

1. `python test_transform.py` → exit 0
2. 规格 3.1~3.5 的全部用例有对应断言，且预期值与你代码实际行为一致（含 `types.GeneratorType` 与惰性副作用断言）
3. 4.1 的 5 项负向验证逐条做一遍，全部 exit 非 0
4. 编号连续（grep 检查）
5. 提交后贴 `python test_transform.py` 输出 + 负向验证结果

## 七、打卡

| 项目 | 状态 | 日期 | Review |
|------|------|------|--------|
| T2-2 transform 数据变换 | ⬜ 待开始 | — | — |