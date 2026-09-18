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

## 五、今日实战任务（T1-4：`calc/` 包）

```text
01-python/day04/
├── calc/
│   ├── __init__.py        # 导出 add, subtract
│   ├── arithmetic.py      # add, subtract, multiply
│   └── utils.py           # 工具函数（如 clamp：把值限制在 [0, 100]）
└── test_calc.py           # 包外部的测试脚本
```

**验收**：在 `01-python/day04/` 下运行 `test_calc.py`，里面 `from calc import add` 能成功并断言。

**加分**：
- `multiply` 也加入导出
- `utils.py` 里的工具函数（如 clamp）也写断言
- 想想：`__init__.py` 只导出 add/subtract 时，`from calc import multiply` 会怎样？——这个"想"比写更重要

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