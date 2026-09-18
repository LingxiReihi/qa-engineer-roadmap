# 01 · Python 语言基础（测试视角）

> **阶段时长**：3 周（21 天，每天 2~3 小时）
> **当前进度**：Day 4 / 21（20%）
> **前置**：懂一点 Python 基础语法即可；不懂也没关系，本阶段会从零讲
> **核心目标**：把「能写 Python」变成「能为 Python 代码写测试」
> **教学数据库**：categories "Python 测试开发"，topics #9（阶段级）+ #52~#55（Day 级）

---

## 一、本阶段为什么重要

测试开发 ≠ 写测试脚本的人。**测试开发的第一课是「读懂被测代码」**。

如果你连别人的业务代码都看不懂，你写的测试就是「对着黑盒点鼠标」，永远做不出自动化框架。

本阶段不追求「把 Python 学透」，而是**用测试的视角把关键知识点串起来**。

---

## 二、学习目标（可验收）

完成本阶段后，你应该能做到：

- [ ] 读懂一份 100 行的 Python 模块，能说出它的功能、入口、依赖
- [ ] 写出带**类型注解**和**文档字符串**的函数
- [ ] 处理异常（try/except/else/finally），并写出对应的测试
- [ ] 用 `unittest.mock` 或 `unittest` 给一个简单函数写测试
- [ ] 用 pytest 重写上面的测试，并让覆盖率达到 80%
- [ ] 看懂并写出一个「上下文管理器」（`with` 语句）
- [ ] 能解释装饰器的基本作用，看懂一个带 `@pytest.fixture` 的测试

---

## 三、周计划总览

### 第 1 周：语法补强 + 第一个测试

| 天 | 主题 | 训练 | 状态 |
|---|---|---|---|
| D0 | 工程环境准备 | — | ✅ 9/16 |
| D1 | 变量、数据类型、容器（list/dict/set/tuple） | T1-1 | ✅ B+ |
| D2 | 控制流（if/for/while）+ 列表推导式 | T1-2 | ✅ A- |
| D3 | 函数（参数、返回值、`*args`/`**kwargs`、默认参数） | T1-3 | ✅ A- |
| D4 | 模块与包（`import`、`__init__.py`、`__main__`） | T1-4 | ◐ 进行中 |
| D5 | 文件读写、`with` 上下文管理器 | T1-5 | ⏳ |
| D6 | **第一个测试**：用 `unittest` 写一个函数的测试 | T1-6 | ⏳ |
| D7 | 复盘 + 小项目：写一个"命令行用户管理"并为其写测试 | 项目 A | ⏳ |

### 第 2 周：进阶语法 + pytest 入门

| 天 | 主题 | 训练 | 状态 |
|---|---|---|---|
| D8 | 类与对象（`__init__`、实例方法、类方法、静态方法） | T1-7 | ⏳ |
| D9 | 异常体系（`Exception` 层次、自定义异常、断言） | T1-8 | ⏳ |
| D10 | 装饰器（`@decorator`、`functools.wraps`） | T1-9 | ⏳ |
| D11 | 生成器与迭代器（`yield`、`itertools`） | T1-10 | ⏳ |
| D12 | 类型注解与 `dataclasses` | T1-11 | ⏳ |
| D13 | **pytest 入门**：`assert`、`pytest.raises`、命令行 | T1-12 | ⏳ |
| D14 | 复盘 + 小项目：用 pytest 测试"登录模块" | 项目 B | ⏳ |

### 第 3 周：工具与工程化

| 天 | 主题 | 训练 | 状态 |
|---|---|---|---|
| D15 | 虚拟环境（`venv`）、`pip`、`requirements.txt` | T1-13 | ⏳ |
| D16 | IDE 配置（VSCode / PyCharm）、调试器使用 | T1-14 | ⏳ |
| D17 | 常用标准库（`os`、`pathlib`、`json`、`datetime`、`logging`） | T1-15 | ⏳ |
| D18 | 字符串与正则表达式（`re` 模块） | T1-16 | ⏳ |
| D19 | **阶段小项目**：一个完整的工具库 + 测试套件 | 项目 C | ⏳ |
| D20 | 复盘、自检、进入阶段 02 | 验收 | ⏳ |

---

## 四、Day 0~4 详细记录（已完成）

### Day 0 · 工程环境准备 ✅（9/16）

**目标**：建好作品集仓库、虚拟环境、第一次 Git 提交。耗时 30~60 分钟。

#### 任务清单

| 任务 | 内容 | 踩坑记录 |
|------|------|----------|
| 1. 检查 Python | `python --version` / `py --version` + `pip --version` | Windows 没有 `python` 时用 `py` |
| 2. 建作品集仓库 | `mkdir qa-engineer-roadmap && cd && git init` | — |
| 3. 创建目录结构 | 01~10 + `.github/workflows` | ⚠️ PowerShell 的 `mkdir` 语法与 bash 不同，参数逐个写，别整体加引号 |
| 4. `.gitkeep` 占位 | 每个空目录放 `.gitkeep` | git 只跟踪文件不跟踪目录，没 `.gitkeep` push 后结构消失 |
| 5. 虚拟环境 | `python -m venv .venv` | Windows 激活：`.venv\Scripts\activate` |
| 6. `.gitignore` | 用编辑器写，别用 heredoc | ⚠️ heredoc 是 bash 语法，PowerShell 会连 `EOF` 一起写进文件 |
| 7. 第一次提交 | `git add . && git commit && git log` | 旧仓库内容移入 `old/`，历史保留 |
| 8. 推送到 GitHub | `git remote add && git push -u origin main` | 复用旧仓库时想清楚作品集想让别人看到什么 |

**验收**：
- [x] Python 版本已确认
- [x] `qa-engineer-roadmap` 仓库已建立
- [x] 虚拟环境已创建并激活
- [x] `.gitignore` 已写好
- [x] 每个空目录有 `.gitkeep`
- [x] `.idea/` 等 IDE 文件没进仓库
- [x] 第一次 commit 完成
- [x] 已推送到 GitHub

**数据库**：topic #51「Day0 作品集仓库初始化」→ mastered（1.0）

---

### Day 1 · 变量 / 数据类型 / 容器（测试视角）✅（9/16）

#### 今日目标

- [x] 分清 4 种基本类型（int / float / str / bool）与 4 种容器（list / dict / set / tuple）
- [x] 理解**可变 vs 不可变**，认识**别名**陷阱
- [x] 会写列表 / 字典 / 集合**推导式**
- [x] 认识**类型注解**，会用 **assert 断言**做自检
- [x] 验收：T1-1 三题全部跑通，每个函数回答"正常 / 异常 / 边界"三问

#### 学习笔记

**变量与别名**：
- 变量是"标签"不是"盒子"：`b = a` 不复制，两个标签指向同一对象
- 别名陷阱：`b.append(3)` 后 `a` 也变了——测试里做数据隔离时是头号坑
- **动态类型**：类型跟着值走，不跟变量走；接口 JSON 里的 `"1"`（str）和 `1`（int）是两个世界

**容器四兄弟**：

| 容器 | 有序 | 可修改 | 可重复 | 典型场景 |
|------|------|--------|--------|----------|
| `list` | ✅ | ✅ | ✅ | 有序数据、批量测试参数 |
| `tuple` | ✅ | ❌ | ✅ | 不可变数据、多返回值 |
| `dict` | 插入序 | ✅ | 键唯一 | **接口 JSON 就是 dict** |
| `set` | ❌ | ✅ | ❌ 自动去重 | 去重、成员判断 |

**推导式**：
```python
[表达式 for x in 可迭代对象 if 条件]   # 列表
{键: 值 for x in 可迭代对象}            # 字典
{x for x in 可迭代对象}                 # 集合
```

**断言（assert）**：
```python
assert 条件, "条件不成立时显示的消息"
```
- 三步心法：算出结果 → 写下预期 → `assert 实际 == 预期`
- **关键**：预期来自**需求**，不是来自实现

#### 实战任务 T1-1

| 函数 | 要求 | 实现要点 |
|------|------|----------|
| `count_words(text)` | 统计单词频次 | 处理非字符串 → `{}`；空串/空格边界；`split()` 按任意空白切分 |
| `unique_sorted(items)` | 去重 + **升序** | 集合去重后 `res.sort()`（首提漏排序） |
| `merge_dicts(a, b)` | 合并，b 覆盖 a | `{**a, **b}` 返回新字典，不污染原数据（首提用 `a.update(b)` 有副作用） |

推导式三题：
1. `[n ** 2 for n in nums if n % 2 == 0]` → 偶数的平方
2. `{word: len(word) for word in words}` → 字长字典
3. `{x for x in items}` → 集合去重

#### Review 复盘

| 轮次 | 评分 | 发现的问题 | 修正 |
|------|------|-----------|------|
| 首提 | **C** | ① set 去重后未排序，测试碰巧通过 ② `a.update(b)` 污染原字典 ③ 推导式漏偶数条件 | — |
| 修正后 | **B+（通过）** | — | 补 `if n % 2 == 0`；`res.sort()`；改 `{**a, **b}`；`split()` 无参；新增 `count_words(" ")` 边界用例 |

**今天最值钱的一课**：测试全绿 ≠ 需求满足——断言预期必须来自需求，而不是"代码碰巧输出什么"。

**数据库**：topic #52 → mastered（0.85）

---

### Day 2 · 控制流（if/for/while）+ 列表推导式 ✅（9/17）

#### 今日目标

- [x] 掌握 if / elif / else 分支，理解 **truthy / falsy**（`0`、`""`、`[]`、`None` 都是假）
- [x] 掌握 for / while：遍历容器、`break` / `continue`，知道 **while 必须有出口**
- [x] 列表推导式进阶：带条件的推导式 vs 显式 for 循环
- [x] 理解**不可信输入**：用户输入必须校验，非法输入不能炸
- [x] 验收：T1-2 猜数字三个验收点全过

#### 理论要点

**条件分支**：先处理"退出 / 非法 / 空"，再处理业务分支。**边界值**就是 if 的临界点（90/89/60/59/-1），每个边界都要有用例。

**for 循环**：
```python
for item in items:
for i, item in enumerate(items):
for k, v in my_dict.items():
```

**while 循环**：必须有语句改变 condition，否则死循环。**死循环 = 挂死**，是稳定性的头号问题。

**循环控制**：
- `break`：跳出整个循环
- `continue`：跳过本次
- `for ... else`：循环没被 break 才执行 else

**推导式 vs 显式循环**：简单转换用推导式；逻辑复杂（多条语句）用显式循环。

**不可信输入**：命令行 `input()` 返回 str，什么都可能进来。校验手段：`s.isdigit()` → `int(s)`。**输入与逻辑分离**是可测试性的第一步。

#### 实战任务 T1-2

```python
def guess_number(target: int, max_attempts: int = 5) -> bool:
    """让用户猜数字，返回是否在 max_attempts 次内猜中。"""
```

**验收**：
- 猜中返回 `True`（含最后一次机会猜中）
- 超出 `max_attempts` 次返回 `False`
- 非法输入（`"abc"`、空串、负数）**不崩溃**，重新读取

**加分设计**：把核心逻辑抽成独立函数再拼装：
```python
def compare(guess: int, target: int) -> str: ...   # 纯逻辑，可 assert
def guess_number(target, max_attempts=5) -> bool:   # 只负责 input + 循环 + 计数
```

**Review**：**A-（通过）**

**数据库**：topic #53 → mastered（0.88）

---

### Day 3 · 函数（测试视角）✅（9/17）

#### 今日目标

- [x] 理解函数签名：参数、返回值、**默认参数**
- [x] 掌握 `*args` / `**kwargs` 收集参数
- [x] 认识并避开**可变默认参数陷阱**（`def f(x=[])`）
- [x] 理解**纯函数**（同输入同输出、无副作用）
- [x] 验收：T1-3 四条验收 + 自加边界断言

#### 理论要点

**函数签名全家桶**：
```python
def f(a, b=1, *args, **kwargs):
    ...
```
- `a`：位置参数（必填）
- `b=1`：默认参数（可省略）
- `*args`：收集多余位置参数 → **元组**
- `**kwargs`：收集多余关键字参数 → **字典**

**可变默认参数陷阱**（面试高频）：
```python
def add_item(item, cart=[]):      # ❌ 默认 [] 只创建一次！
    cart.append(item)
    return cart

def add_item(item, cart=None):    # ✅ 默认 None，内部再建
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```
默认参数在**函数定义时求值一次**，之后所有调用共用同一个对象。

**纯函数**：同样的输入 → 永远同样的输出；不改外部状态（无副作用）；好处：可以直接 assert。

#### 实战任务 T1-3

```python
def discount(price: float, discount_rate: float = 1.0, coupon: float = 0.0) -> float:
    """计算折后价：price * discount_rate - coupon，结果不为负。"""
```

**验收（四条 assert）**：
- `discount(100)` → 100
- `discount(100, 0.8)` → 80
- `discount(100, 0.5, 50)` → 0（不为负）
- `discount(100, 0.5, 80)` → 0

**隐藏考点**：`mean()` 空参数时 `sum([]) / len([])` 会 `ZeroDivisionError`。

**Review**：首提 **B+** → 修正后 **A-**

**数据库**：topic #54 → in_progress（0.7）

---

### Day 4 · 模块与包（测试视角）◐（9/18）

#### 今日目标

- [ ] 分清**模块**（一个 .py 文件）与**包**（目录 + `__init__.py`）
- [ ] 掌握 import 三种形态：`import x` / `from x import y` / `from x import y as z`
- [ ] 理解 `if __name__ == "__main__":` 守卫的作用
- [ ] 理解**被测代码的组织方式 = 测试的组织方式**
- [ ] 验收：T1-4 的 `calc/` 包在外部能 `from calc import add` 并调用

#### 理论要点

**模块 vs 包**：
```text
calc/                   ← 包（目录）
├── __init__.py         ← 包标记（可写导出语句）
├── arithmetic.py       ← 模块（文件）
└── utils.py            ← 模块（文件）
```

**import 三种形态**：
```python
import calc.arithmetic            # 用全名
from calc import add              # 直接拿
from calc import add as plus      # 别名
```
import 会**执行被导入模块的顶层代码**——所以顶层别放"会跑的东西"。

**`if __name__ == "__main__":`**：被 import 时 `__name__` 是模块名，不会执行演示代码。没有这个守卫，测试导入被测模块时会冒出演示输出，污染测试。

**包内相对导入**：`from .arithmetic import add`（`.` 表示当前包）。

#### 练习

1. 建 `greeting/` 包：`say_hi` / `say_bye`，`__init__.py` 导出，包外写断言调用
2. 写一个带 `if __name__ == "__main__"` 的模块，验证被导入时不执行演示代码
3. 三种 import 形态各写一次

#### 实战任务 T1-4：`calc/` 包

**目标结构**：
```text
01-python/day04/
├── calc/
│   ├── __init__.py           # 对外导出（API 门面）
│   ├── arithmetic.py         # 四则运算（纯函数）
│   └── utils.py              # 工具函数
└── test_calc.py              # 包外测试脚本（验收入口）
```

**`arithmetic.py`** —— 3 个纯函数：

| 函数 | 行为 | 必测断言 |
|------|------|----------|
| `add(a, b)` | a + b | `add(1, 2) == 3`；`add(-1, 1) == 0` |
| `subtract(a, b)` | a - b | `subtract(5, 3) == 2`；`subtract(3, 5) == -2` |
| `multiply(a, b)` | a * b | `multiply(4, 0.5) == 2.0`；`multiply(0, 9) == 0` |

> ⚠️ **浮点坑 1**：`0.1 + 0.2 == 0.3` 是 `False`。浮点断言不要用裸 `==`，用 `round(x, 2) == 0.3` 或 `abs(x - 0.3) < 1e-9`。

**`utils.py`** —— 2 个工具函数：

| 函数 | 行为 | 必测断言 |
|------|------|----------|
| `clamp(value, low=0, high=100)` | 超下界取下界、超上界取上界 | `clamp(50) == 50`；`clamp(-10) == 0`；`clamp(150) == 100`；`clamp(50, 10, 20) == 20` |
| `round2(value)` | 四舍五入保留 2 位小数 | `round2(3.14159) == 3.14` |

> ⚠️ **浮点坑 2**：`round(2.675, 2)` 返回 `2.67` 而不是 `2.68`。亲手试一下，写进注释。

**`__init__.py`** —— 导出策略：
```python
from .arithmetic import add, subtract
from .utils import clamp
```
- **故意不导出 `multiply`**，然后在 test_calc.py 里实测并注释结论
- `from calc import multiply` → `ImportError`
- `from calc.arithmetic import multiply` → ✅ 成功
- 证明：**包的对外 API 由 `__init__.py` 决定**

**`test_calc.py`** —— 要求：
1. 全部断言通过、exit 0
2. 每个函数 ≥3 条（正常 / 边界 / 浮点）
3. 断言消息写**预期是什么**，编号连续
4. 注释写清：两个浮点坑的结论、`multiply` 导出实验的结论
5. 全部通过后打印 `print("calc 包全部通过")`

**当前状态**：
- ✅ `greeting/` 练习包已完成
- ◐ `calc/` 包结构已创建但文件为空
- 待完成：`arithmetic.py`、`utils.py`、`test_calc.py`

**数据库**：topic #55 → in_progress（0.4）

---

## 五、Day 5~21 详细计划

### Day 5 · 文件读写 + `with` 上下文管理器（T1-5）

**目标**：写一个「CSV 读写」工具。

```python
def read_csv(path: str) -> list[dict]:
    """读取 CSV 返回 list of dict（第一行是表头）。"""

def write_csv(path: str, rows: list[dict]) -> None:
    """写入 CSV。"""
```

**验收**：能读回刚写出的 CSV；文件不存在时抛出明确异常；用 `with` 管理文件。

**关键知识点**：
- `open()` 的 mode 参数（`"r"` / `"w"` / `"a"` / `"r+"`）
- `with` 语句自动关闭文件
- `csv` 模块 vs 手动解析
- 编码问题：Windows 默认 GBK，读取 UTF-8 文件乱码 → `encoding="utf-8"`
- 路径：用 `pathlib.Path` 替代字符串拼接

---

### Day 6 · 第一个测试：unittest（T1-6）

**目标**：用 `unittest` 给 `discount()` 写测试。

```python
import unittest
from calc import discount

class TestDiscount(unittest.TestCase):
    def test_default_no_discount(self):
        self.assertEqual(discount(100), 100)

    def test_with_discount_rate(self):
        self.assertEqual(discount(100, 0.8), 80)

    def test_coupon_lower_than_zero(self):
        self.assertEqual(discount(100, 0.5, 80), 0)
```

**运行**：`python -m unittest test_calc.py -v`

**验收**：3 个测试全部 PASS。

**关键知识点**：
- `unittest.TestCase` 结构
- `self.assertEqual` / `assertRaises` / `assertTrue`
- `setUp()` / `tearDown()` 生命周期
- `unittest.main()` 入口
- `tempfile` 模块做临时文件测试

---

### Day 7 · 项目 A：命令行用户管理（项目 A）

**目标**：实现一个命令行用户管理系统，覆盖"增删改查 + 文件持久化"，并用 unittest 写完整测试。

**目录结构**：
```text
user_mgr/
├── __init__.py
├── models.py             # User 数据类
├── storage.py            # JSON 文件读写
├── service.py            # 用户管理业务逻辑
└── cli.py                # 命令行入口
tests/
├── test_models.py
├── test_storage.py
└── test_service.py
```

**核心模块**：

| 模块 | 职责 | 关键函数 |
|------|------|----------|
| `models.py` | User 数据类 | `to_dict()` / `from_dict()` |
| `storage.py` | JSON 文件持久化 | `load()` / `save()` |
| `service.py` | 业务逻辑 | `create()` / `list()` / `get()` / `find_by_email()` / `delete()` |
| `cli.py` | 命令行交互 | 交互式菜单 |

**功能要求**：
- [ ] 用户模型：`User` 数据类，含 `id`、`name`、`email`、`password_hash`、`created_at`
- [ ] 存储层：JSON 文件读写，文件不存在时自动初始化
- [ ] 业务层：`create`、`list`、`get`、`find_by_email`、`delete`
- [ ] 输入校验：空值、邮箱格式、重复邮箱
- [ ] 密码处理：用 `hashlib.sha256` 哈希，不存明文
- [ ] 命令行入口：交互式操作
- [ ] unittest 测试：覆盖所有函数，含正常 + 异常路径
- [ ] 覆盖率 > 80%

**验收标准**：
- [ ] 模块结构清晰（models / storage / service / cli）
- [ ] 业务层不依赖 CLI，可独立测试
- [ ] 所有函数有 unittest 测试
- [ ] 测试覆盖正常 + 异常路径
- [ ] 运行 `python -m unittest discover tests -v` 全部 PASS
- [ ] 覆盖率 > 80%
- [ ] 数据持久化到 JSON 文件，重启后数据不丢

---

### Day 8~9 · 类与对象（T1-7）

**目标**：写一个 `User` 类，并用 unittest 测试。

```python
class User:
    def __init__(self, name: str, age: int):
        if age < 0:
            raise ValueError("age cannot be negative")
        self.name = name
        self.age = age

    def is_adult(self) -> bool:
        return self.age >= 18
```

**验收**：
- 测试 `is_adult()` 在 17/18/19 三种情况下的行为
- 测试负年龄抛出 `ValueError`
- 测试 `name` 空字符串的处理

**关键知识点**：
- `__init__` 构造器与 `self`
- 实例属性 vs 类属性
- `@classmethod` / `@staticmethod`
- `__str__` / `__repr__` 魔术方法
- duck typing（鸭子类型）

---

### Day 10 · 异常体系（T1-8）

**目标**：定义一个异常层次结构，模拟业务场景。

```python
class AppError(Exception):
    """应用基础异常。"""
    pass

class AuthError(AppError):
    """认证相关异常。"""
    pass

class NotFoundError(AppError):
    """资源不存在。"""
    pass
```

**训练**：
- 写一个函数抛出 `AuthError`，用 unittest 捕获
- 测试 `isinstance(e, AppError)` 为 `True`

**关键知识点**：
- `Exception` 层次结构
- `raise` / `try` / `except` / `else` / `finally`
- `except Exception as e:` vs `except: pass`
- 异常链：`raise NewError from e`
- 自定义异常的最佳实践

---

### Day 11 · 装饰器（T1-9）

**目标**：写一个「耗时统计」装饰器。

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

**训练**：
- 用 `@timer` 装饰一个 sleep 1 秒的函数
- 测试装饰后函数名、文档字符串未丢失

**关键知识点**：
- 函数作为参数
- 闭包
- `functools.wraps` 保留原函数元数据
- `@decorator` 语法糖
- pytest 的 `@pytest.mark.parametrize` 就是一个装饰器

---

### Day 12 · 生成器（T1-10）

**目标**：写一个「分页器」。

```python
def paginate(items: list, page_size: int):
    """生成器：每次返回一页。"""
    for i in range(0, len(items), page_size):
        yield items[i:i + page_size]
```

**训练**：写测试验证分页逻辑（用 `list(paginate(...))` 比对）。

**关键知识点**：
- `yield` 暂停/恢复执行
- 生成器是迭代器的一种
- `next()` / `iter()` 协议
- `itertools` 常用函数（`chain` / `product` / `combinations` / `islice`）
- 生成器表达式 vs 列表推导式

---

### Day 13 · dataclass（T1-11）

**目标**：用 `@dataclass` 定义 `Order`，并写测试。

```python
from dataclasses import dataclass

@dataclass
class Order:
    id: int
    amount: float
    items: list[str]
    status: str = "pending"
```

**训练**：
- 测试默认 `status`
- 测试相等性（dataclass 自动实现 `__eq__`）
- 测试 `frozen=True` 的不可变性

**关键知识点**：
- `@dataclass` 自动生成 `__init__` / `__eq__` / `__repr__`
- `field(default_factory=...)` 可变默认值
- `frozen=True` 不可变
- `@property` 计算属性
- 与字典互转

---

### Day 14 · pytest 入门（T1-12）

**目标**：用 pytest 重写 T1-6 的测试。

```python
# test_discount.py
from calc import discount

def test_default_no_discount():
    assert discount(100) == 100

def test_with_discount_rate():
    assert discount(100, 0.8) == 80

def test_coupon_lower_than_zero():
    assert discount(100, 0.5, 80) == 0
```

**运行**：`pytest -v`

**训练**：
- 用 `pytest.raises` 测试异常
- 用命令行参数 `pytest -k "discount"` 过滤
- 用 `pytest --collect-only` 查看收集到哪些测试

**关键知识点**：
- pytest 的断言重写机制（比 unittest 更简洁）
- `pytest.raises` 上下文管理器
- `pytest.mark.parametrize` 参数化
- `pytest.approx` 浮点比较
- `conftest.py` 与 fixture
- 报告插件（pytest-html / Allure）

---

### Day 15 · 项目 B：登录模块（项目 B）

```text
login/
├── __init__.py
├── auth.py             # 登录、登出、会话管理
└── models.py           # User 类
tests/
├── test_auth.py
└── test_models.py
```

**要求**：
- 密码错误返回 False
- 密码正确返回 token
- 会话超时处理
- 用 pytest + 参数化测试覆盖

---

### Day 16 · 虚拟环境（T1-13）

**目标**：
- `python -m venv .venv` 创建虚拟环境
- `pip install pytest requests`
- `pip freeze > requirements.txt`

**验收**：新机器克隆项目后能 `pip install -r requirements.txt` 还原环境。

---

### Day 17 · 调试器（T1-14）

**目标**：在 VSCode 或 PyCharm 中：
- 打断点运行
- 查看变量
- 单步执行
- 条件断点

**训练**：故意写一个 bug，用调试器找到它。

---

### Day 18 · 标准库（T1-15）

**目标**：用 `json`、`datetime`、`logging` 完成一个小任务。

```python
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def save_user(name: str):
    logging.info(f"Saving user: {name}")
    user = {"name": name, "created_at": datetime.now().isoformat()}
    with open("users.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(user) + "\n")
```

**训练**：写测试验证 `save_user()` 写入的内容能被 `json.loads` 解析。

---

### Day 19 · 正则表达式（T1-16）

**目标**：写几个常用正则。

```python
import re

# 匹配邮箱
email_pat = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# 匹配手机号（中国大陆 11 位）
phone_pat = r"^1[3-9]\d{9}$"

# 提取字符串中所有数字
nums = re.findall(r"\d+", "我有3个苹果和5个香蕉")
```

**训练**：写测试覆盖每种正则的合法/非法输入。

---

### Day 20 · 项目 C：工具库（项目 C）

自选一个主题（建议：CSV 处理工具、文本处理工具、API 客户端），实现：
- 至少 5 个函数/类
- 完整的 pytest 测试
- Allure 或 pytest-html 报告
- README 文档

**验收标准**：
- 测试覆盖率 > 80%
- 全部测试通过
- 报告能展示

---

### Day 21 · 阶段验收

做以下自检：

- [ ] 我能用 pytest 给一个模块写测试，覆盖率 > 80%
- [ ] 我能解释「上下文管理器」「装饰器」「生成器」的用途
- [ ] 我能配置虚拟环境并导出 `requirements.txt`
- [ ] 我完成了至少 1 个「项目 A/B/C」级别的小项目
- [ ] 我有一份能展示的测试报告（HTML）
- [ ] 我能向别人解释一个 100 行的 Python 模块在做什么

> 全部打勾 → 进入 [02_测试理论与用例设计.md](./02_测试理论与用例设计.md)。
> 未全部打勾 → 补完再走，**不要带着坑进入下一阶段**。

---

## 六、常见陷阱

| 陷阱 | 说明 | 解决 |
|------|------|------|
| 可变默认参数 | `def f(x=[])` 多次调用共享同一个 list | 用 `None` + 函数内初始化 |
| 浮点相等 | `0.1 + 0.2 == 0.3` 是 `False` | 用 `math.isclose` 或 pytest 的 `approx` |
| 异常吞掉 | `except: pass` | 至少 `except Exception as e: logging.error(e)` |
| 导入顺序混乱 | 模块相互引用导致循环导入 | 把共享代码抽到独立模块 |
| 时区 | `datetime.now()` 不带时区 | 用 `datetime.now(timezone.utc)` |
| 编码 | Windows 默认 GBK，读取 UTF-8 文件乱码 | `open(..., encoding="utf-8")` |
| 路径 | 相对路径在不同工作目录下失效 | 用 `pathlib.Path(__file__).parent` |

---

## 七、阶段验收标准

| 维度 | 要求 | 验证方式 |
|------|------|----------|
| pytest 测试能力 | 能为一个模块写测试，覆盖率 > 80% | `coverage run -m pytest && coverage report` |
| 进阶语法理解 | 能解释上下文管理器/装饰器/生成器的用途 | 口头解释 + 代码示例 |
| 工程能力 | 能配置虚拟环境并导出 `requirements.txt` | 新环境还原测试 |
| 项目能力 | 完成至少 1 个项目 A/B/C 级别小项目 | 代码 + 测试 + README |
| 报告能力 | 有一份能展示的测试报告（HTML） | Allure 或 pytest-html |
| 沟通能力 | 能向别人解释一个 100 行 Python 模块在做什么 | 口头演示 |

**通过标准**：全部打勾 → 进入阶段 02。未全部打勾 → 补完再走。

---

## 八、打卡表

| 训练 | 完成日期 | Review 评分 | 数据库状态 | 备注 |
|------|----------|------------|-----------|------|
| D0 工程环境 | 2026-09-16 | ✅ | mastered (1.0) | |
| T1-1 容器与推导式 | 2026-09-16 | B+（修正后） | mastered (0.85) | set 排序 / 字典副作用 / 需求预期 |
| T1-2 猜数字 | 2026-09-17 | A- | mastered (0.88) | |
| T1-3 订单折扣 | 2026-09-17 | A-（修正后） | in_progress (0.7) | 负数钳位 / 非法输入 |
| T1-4 模块与包 | | | in_progress (0.4) | calc 包待完成 |
| T1-5 CSV 读写 | | | | |
| T1-6 unittest | | | | |
| T1-7 类与测试 | | | | |
| T1-8 异常体系 | | | | |
| T1-9 装饰器 | | | | |
| T1-10 生成器 | | | | |
| T1-11 dataclass | | | | |
| T1-12 pytest 入门 | | | | |
| T1-13 虚拟环境 | | | | |
| T1-14 调试器 | | | | |
| T1-15 标准库 | | | | |
| T1-16 正则 | | | | |
| 项目 A 用户管理 | | | | |
| 项目 B 登录 | | | | |
| 项目 C 工具库 | | | | |
