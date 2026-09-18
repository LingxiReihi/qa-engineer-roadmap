# Day 4：模块与包（测试视角）——训练计划

> 日期：2026-09-18 ｜ 阶段 01：Python 语言基础（测试视角） ｜ 对应 `_docs/01_Python基础与测试入门.md` 周计划 D4 / 训练 T1-4

---

## 一、今日目标

- [ ] 分清**模块**（一个 .py 文件）与**包**（目录 + `__init__.py`）
- [ ] 掌握 import 三种形态：`import x` / `from x import y` / `from x import y as z`
- [ ] 理解 `if __name__ == "__main__":` 守卫的作用（直接运行 vs 被导入）
- [ ] 理解**被测代码的组织方式 = 测试的组织方式**（模块化是测试的前提）
- [ ] 验收：T1-4 的 `calc/` 包在外部能 `from calc import add` 并调用

## 二、理论要点

### 1. 模块 vs 包

```text
calc/                   ← 包（目录）
├── __init__.py         ← 包标记（可写导出语句）
├── arithmetic.py       ← 模块（文件）
└── utils.py            ← 模块（文件）
```

- **模块** = 一个 `.py` 文件
- **包** = 目录 + `__init__.py`；`__init__.py` 里写"这个包对外暴露什么"
- 测试视角：**包结构 = 被测系统的骨架**，测试从外部 import 包，就是"黑盒测试"的入口

### 2. import 三种形态

```python
import calc.arithmetic            # 用全名 calc.arithmetic.add(...)
from calc import add              # 直接拿 add
from calc import add as plus      # 别名（避免重名）
```

- import 会**执行被导入模块的顶层代码**——所以顶层别放"会跑的东西"（这正是 `__main__` 守卫的意义）

### 3. `if __name__ == "__main__":`

```python
def say_hi():
    return "hi"

if __name__ == "__main__":        # 只有"直接运行本文件"才执行
    print(say_hi())
```

- 被 `import` 时 `__name__` 是模块名，**不会**执行演示代码
- 测试视角：没有这个守卫，测试导入被测模块时会冒出演示输出，污染测试

### 4. 导入路径

- Python 从 `sys.path` 找模块：当前目录、标准库、site-packages
- 包内用**相对导入**：`from .arithmetic import add`（`.` 表示当前包）

## 三、示例代码（教学用，亲手敲——注意：不是 T1-4 的答案，练手包）

```text
greeting/
├── __init__.py
└── hello.py
```

```python
# greeting/hello.py
def say_hi(name: str) -> str:
    return f"hi, {name}"

def say_bye(name: str) -> str:
    return f"bye, {name}"
```

```python
# greeting/__init__.py
from .hello import say_hi, say_bye
```

```python
# 外部使用（在 greeting/ 的上一级目录运行）
from greeting import say_hi
assert say_hi("tester") == "hi, tester"
```

```python
# __main__ 守卫演示
def f():
    return 1

if __name__ == "__main__":
    print("只有直接运行时才打印这行")
```

## 四、今日练习（`01-python/day04/`）

1. 建 `greeting/` 包（**不是 calc**）：`say_hi` / `say_bye` 两个函数，`__init__.py` 导出，包外写断言调用
2. 写一个带 `if __name__ == "__main__"` 的模块，**验证被导入时不执行演示代码**（例如模块里 `RUN = "demo"`，main 块里改成 `"run"`，导入后断言 `RUN == "demo"`）
3. 三种 import 形态各写一次，分别调用

## 五、今日实战任务（T1-4：`calc/` 包——详细规格）

### 5.1 目标结构

```text
01-python/day04/
├── calc/                     # 包
│   ├── __init__.py           # 对外导出（API 门面）
│   ├── arithmetic.py         # 四则运算（纯函数）
│   └── utils.py              # 工具函数
└── test_calc.py              # 包外测试脚本（验收入口）
```

### 5.2 `arithmetic.py` —— 3 个纯函数，带类型注解和 docstring

| 函数 | 行为 | 必测断言 |
|---|---|---|
| `add(a: float, b: float) -> float` | a + b | `add(1, 2) == 3`；`add(-1, 1) == 0` |
| `subtract(a: float, b: float) -> float` | a - b | `subtract(5, 3) == 2`；`subtract(3, 5) == -2`（负数边界） |
| `multiply(a: float, b: float) -> float` | a * b | `multiply(4, 0.5) == 2.0`；`multiply(0, 9) == 0` |

> ⚠️ **浮点坑 1（真实测试陷阱）**：`0.1 + 0.2 == 0.3` 是 `False`（实际是 `0.30000000000000004`）。浮点断言**不要用裸 `==`**，用 `round(x, 2) == 0.3` 或 `abs(x - 0.3) < 1e-9`。在 test_calc.py 里给 `add(0.1, 0.2)` 写一条**能通过**的断言，并用注释说明为什么。

### 5.3 `utils.py` —— 至少 2 个工具函数

| 函数 | 行为 | 必测断言 |
|---|---|---|
| `clamp(value, low=0, high=100) -> float` | 超下界取下界、超上界取上界、否则原值 | `clamp(50) == 50`；`clamp(-10) == 0`；`clamp(150) == 100`；`clamp(50, 10, 20) == 20` |
| `round2(value) -> float` | 四舍五入保留 2 位小数（价格场景） | `round2(3.14159) == 3.14` |

> ⚠️ **浮点坑 2**：`round(2.675, 2)` 返回 `2.67` 而不是 `2.68`（二进制浮点表示所致）。亲手试一下，把这个发现写进注释——这是断言最容易翻车的地方。

### 5.4 `__init__.py` —— 导出策略（含思考题）

```python
from .arithmetic import add, subtract
from .utils import clamp
```

- **故意不导出 `multiply`**，然后在 test_calc.py 里实测并注释结论：
  - `from calc import multiply` → ？（预期 `ImportError`）
  - `from calc.arithmetic import multiply` → ✅ 成功
- 这个实验证明：**包的对外 API 由 `__init__.py` 决定**，内部模块文件不是 API。

### 5.5 `test_calc.py` —— 包外测试脚本（验收入口）

要求：
1. 全部断言通过、exit 0；运行方式：在 `01-python/day04/` 目录下执行 `.venv\Scripts\python.exe test_calc.py`
2. 覆盖：每个函数 ≥3 条（正常 / 边界 / 负数或浮点）
3. 每条断言消息写**预期是什么**，编号连续（Day 1~3 的教训）
4. 注释写清：两个浮点坑的结论、`multiply` 导出实验的结论
5. 全部通过后打印 `print("calc 包全部通过")`

### 5.6 验收清单

- [ ] `from calc import add, subtract, clamp` 全部可用
- [ ] `from calc.arithmetic import multiply` 可用；`from calc import multiply` 的行为已实测并注释
- [ ] 浮点断言用 `round` / 误差比较，而不是裸 `==`
- [ ] 全部断言通过、exit 0、`print("calc 包全部通过")` 出现
- [ ] 包内没有"导入即打印"的代码（`__main__` 守卫意识）

## 六、提交要求

```powershell
git add 01-python/day04
git commit -m "day(04): modules and calc package"
git push
```

## 七、Review 关注点

- `from calc import add` 真的能跑（导入路径）
- `__init__.py` 导出是否干净、有没有多余副作用
- `if __name__ == "__main__"` 用得对不对
- 包外测试文件的组织（测试与被测的目录关系）
- 相对导入 `from .` 是否用对