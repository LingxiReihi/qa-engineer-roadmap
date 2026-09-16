# 01 · Python 语言基础（测试视角）

> **阶段时长**：3 周（每天 2~3 小时）
> **前置**：懂一点 Python 基础语法即可；不懂也没关系，本阶段会从零讲。
> **核心目标**：把「能写 Python」变成「能为 Python 代码写测试」。

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

## 三、Day 0：工程环境准备（开始正式学习前）

> **目标**：建好作品集仓库、虚拟环境、第一次 Git 提交。
> **耗时**：30~60 分钟。
> **参考**：[11_作品集仓库指南.md](./11_作品集仓库指南.md)。

### 任务 1：检查 Python

```bash
python --version        # Windows 没有 python 时用 py --version
pip --version
```

### 任务 2：建作品集仓库

```bash
cd ~
mkdir qa-engineer-roadmap
cd qa-engineer-roadmap
git init
```

### 任务 3：创建目录结构

**git-bash / macOS / Linux**：

```bash
mkdir -p 01-python/day01 01-python/projects \
         02-software-testing/case-design \
         03-linux-git \
         04-pytest 05-api-automation 06-ci-cd \
         07-web-mobile 08-performance 09-engineering-basics \
         10-final-project .github/workflows
```

**Windows PowerShell**（`mkdir` 是 `New-Item` 的别名，语法不同）：

```powershell
New-Item -ItemType Directory -Path "01-python\day01","01-python\projects",".github\workflows" -Force
New-Item -ItemType Directory -Path "02-software-testing\case-design","03-linux-git","04-pytest","05-api-automation","06-ci-cd","07-web-mobile","08-performance","09-engineering-basics","10-final-project" -Force
```

> ⚠️ **踩坑记录**：bash 的 `mkdir -p a b` 中 `a`、`b` 是两个参数；若在 PowerShell 里把整条命令**用一个引号括起来**，会创建一个名字带空格的目录（如 `day01 01-python`）。参数逐个写，别整体加引号。

#### 3.1 空目录占位（.gitkeep）——必须做，否则结构推不上 GitHub

git 只跟踪**文件**、不跟踪**目录**。上面建的目录全是空的，直接 `git add .` 后它们**不会进入提交**，push 到 GitHub 后结构会整个消失。给每个空目录放一个空占位文件：

```powershell
$dirs = @("01-python\day01","01-python\projects","02-software-testing\case-design","03-linux-git","04-pytest","05-api-automation","06-ci-cd","07-web-mobile","08-performance","09-engineering-basics","10-final-project",".github\workflows")
foreach ($d in $dirs) { New-Item -ItemType File -Path "$d\.gitkeep" -Force | Out-Null }
```

> 自查：`git status` 里能看到 `.gitkeep`，才说明结构真的会进仓库（`git ls-files` 列出的是真正入库的文件，磁盘上有 ≠ 仓库里有）。

### 任务 4：虚拟环境

```bash
python -m venv .venv
# Windows 激活：.venv\Scripts\activate
# macOS/Linux：source .venv/bin/activate
```

### 任务 5：.gitignore

**别用 heredoc**：`cat > file <<'EOF' ... EOF` 是 bash 语法，在 PowerShell 里粘贴会连 `EOF` 结束标记一起写进文件。用编辑器在仓库根目录新建 `.gitignore`，内容如下：

```
__pycache__/
*.py[cod]
.venv/
venv/
.env
*.env
.pytest_cache/
.coverage
htmlcov/
allure-results/
allure-report/
reports/
.idea/
.vscode/
.DS_Store
```

> ⚠️ **踩坑记录**：`.gitignore` 只对**未跟踪**文件生效。如果 `.idea/` 已被历史提交跟踪（比如复用了旧仓库），光写 ignore 没用，还要 `git rm -r --cached .idea` 把它移出索引，再提交一次。

### 任务 6：第一次提交

先建根目录 `README.md`（作品集门面）：标题 + 一句话定位即可。如果从 `11_作品集仓库指南.md` 复制模板，**务必删掉模板里的示例数据**——评分历史、阶段状态那些"占位内容"是例子，没发生过的不要写进去，作品集要诚实。

```bash
git add .
git commit -m "chore: init repository"
git log --oneline
```

### 任务 7：推送到 GitHub（可选，推荐）

```bash
# 1. 在 GitHub 网页创建空仓库（不勾 README），仓库名 qa-engineer-roadmap
# 2. 关联远程（二选一）
git remote add origin git@github.com:<你的用户名>/qa-engineer-roadmap.git   # SSH
# 或 git remote add origin https://github.com/<你的用户名>/qa-engineer-roadmap.git
# 3. 推送
git branch -M main
git push -u origin main
```

> 如果已有旧仓库（如之前的练习仓库）：可以复用——把旧内容移进 `old/` 目录再提交，历史保留、作品集长在新结构上；也可以新建仓库只保留新内容。两种都行，想清楚"作品集链接"想让别人看到什么。

### Day 0 验收

- [x] Python 版本已确认
- [x] `qa-engineer-roadmap` 仓库已建立
- [x] 虚拟环境已创建并激活
- [x] `.gitignore` 已写好（无 heredoc 残留的 `EOF` 行）
- [x] 每个空目录有 `.gitkeep`，`git ls-files` 能看到 01~10 目录
- [x] `.idea/` 等 IDE 文件没进仓库（已跟踪则先 `git rm -r --cached` 移出）
- [x] 第一次 commit 完成，`git log` 能看到
- [x] （推荐）已推送到 GitHub

> Day 0 完成后，说一句「**开始 Day 1**」，进入陪练流程。

---

## 四、周计划

### 第 1 周：语法补强 + 第一个测试

| 天 | 主题 | 训练 |
|---|---|---|
| D1 | 变量、数据类型、容器（list/dict/set/tuple） | T1-1 |
| D2 | 控制流（if/for/while）+ 列表推导式 | T1-2 |
| D3 | 函数（参数、返回值、`*args`/`**kwargs`、默认参数） | T1-3 |
| D4 | 模块与包（`import`、`__init__.py`、`__main__`） | T1-4 |
| D5 | 文件读写、`with` 上下文管理器 | T1-5 |
| D6 | **第一个测试**：用 `unittest` 写一个函数的测试 | T1-6 |
| D7 | 复盘 + 小项目：写一个"命令行用户管理"并为其写测试 | 项目 A |

### 第 2 周：进阶语法 + pytest 入门

| 天 | 主题 | 训练 |
|---|---|---|
| D8 | 类与对象（`__init__`、实例方法、类方法、静态方法） | T1-7 |
| D9 | 异常体系（`Exception` 层次、自定义异常、断言） | T1-8 |
| D10 | 装饰器（`@decorator`、`functools.wraps`） | T1-9 |
| D11 | 生成器与迭代器（`yield`、`itertools`） | T1-10 |
| D12 | 类型注解与 `dataclasses` | T1-11 |
| D13 | **pytest 入门**：`assert`、`pytest.raises`、命令行 | T1-12 |
| D14 | 复盘 + 小项目：用 pytest 测试"登录模块" | 项目 B |

### 第 3 周：工具与工程化

| 天 | 主题 | 训练 |
|---|---|---|
| D15 | 虚拟环境（`venv`）、`pip`、`requirements.txt` | T1-13 |
| D16 | IDE 配置（VSCode / PyCharm）、调试器使用 | T1-14 |
| D17 | 常用标准库（`os`、`pathlib`、`json`、`datetime`、`logging`） | T1-15 |
| D18 | 字符串与正则表达式（`re` 模块） | T1-16 |
| D19 | **阶段小项目**：一个完整的工具库 + 测试套件 | 项目 C |
| D20 | 复盘、自检、进入阶段 02 | 验收 |

---

## 五、关键知识点（精简版）

> 详细的语法参考可以查官方文档（[docs.python.org](https://docs.python.org/3/)），这里只列「测试开发最常用」的点。

### 4.1 函数：一切测试的对象

```python
def add(a: int, b: int) -> int:
    """两个整数相加。"""
    return a + b
```

- 参数、返回值、默认值、关键字参数：`f(x=1, y=2)`
- 可变参数：`*args`（位置）、`**kwargs`（关键字）
- 默认参数陷阱：**可变默认参数**（`def f(x=[])`）是新手最常被坑的地方

### 4.2 异常处理：测试反向用例的载体

```python
def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b
```

测试时：
- 正常情况：`divide(6, 3) == 2`
- 异常路径：`with pytest.raises(ValueError): divide(1, 0)`

### 4.3 上下文管理器：资源管理的标配

```python
with open("file.txt", "r") as f:
    data = f.read()
# 离开 with 块，文件自动关闭
```

> 测试时常见场景：数据库连接、HTTP 会话、临时文件。

### 4.4 类与继承：框架设计的基石

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"
```

> 测试框架（Selenium PO、pytest BaseClass）大量用类组织。

### 4.5 类型注解：团队协作的契约

```python
def login(username: str, password: str, remember: bool = False) -> dict:
    ...
```

> 注解不影响运行，但 `mypy`、`pyright` 能提前发现 bug。

### 4.6 装饰器：pytest 插件机制的底层

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper
```

> pytest 的 `@pytest.mark.parametrize` 就是一个装饰器。

---

## 六、训练任务

> 每个训练都遵循「小步快跑」原则：先读题、再写代码、再运行、再改进。

### T1-1：容器与推导式

**目标**：用列表推导式、字典推导式完成下列任务。

```python
# 1. 给定 nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#    写出所有偶数的平方：[4, 16, 36, 64, 100]
# 2. 给定 words = ["hello", "world", "python"]
#    写出 {word: len(word)} 形式的字典
# 3. 用集合去重：nums_with_dup = [1, 1, 2, 2, 3, 3] → {1, 2, 3}
```

**验收**：能写出三个推导式，运行结果符合预期。

### T1-2：控制流实战

**目标**：实现「猜数字」游戏（命令行版），并用函数封装。

```python
def guess_number(target: int, max_attempts: int = 5) -> bool:
    """让用户猜数字，返回是否在 max_attempts 次内猜中。"""
    ...
```

**验收**：
- 猜中返回 `True`
- 超出次数返回 `False`
- 输入非法字符不崩溃

### T1-3：函数与默认参数

**目标**：写一个「订单折扣」函数。

```python
def discount(price: float, discount_rate: float = 1.0, coupon: float = 0.0) -> float:
    """计算折后价：price * discount_rate - coupon，结果不为负。"""
    ...
```

**验收**：
- `discount(100)` → 100
- `discount(100, 0.8)` → 80
- `discount(100, 0.5, 50)` → 0（不为负）
- `discount(100, 0.5, 80)` → 0

### T1-4：模块与包

**目标**：在 `calc/` 目录下建包，包含：

```
calc/
├── __init__.py        # 导出 add, subtract
├── arithmetic.py      # add, subtract, multiply
└── utils.py           # 一些工具函数
```

**验收**：在外部能 `from calc import add` 并调用。

### T1-5：文件读写 + 上下文管理器

**目标**：写一个「CSV 读写」工具。

```python
def read_csv(path: str) -> list[dict]:
    """读取 CSV 返回 list of dict（第一行是表头）。"""
    ...

def write_csv(path: str, rows: list[dict]) -> None:
    """写入 CSV。"""
    ...
```

**验收**：
- 能读回刚写出的 CSV
- 文件不存在时抛出明确异常
- 用 `with` 管理文件

### T1-6：**第一个测试**（unittest）

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
        # 折后价为负时应返回 0
        self.assertEqual(discount(100, 0.5, 80), 0)

if __name__ == "__main__":
    unittest.main()
```

**运行**：`python -m unittest test_calc.py -v`

**验收**：3 个测试全部 PASS。

### T1-7：类与测试

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

### T1-8：异常体系

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

### T1-9：装饰器

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

### T1-10：生成器

**目标**：写一个「分页器」。

```python
def paginate(items: list, page_size: int):
    """生成器：每次返回一页。"""
    for i in range(0, len(items), page_size):
        yield items[i:i + page_size]

# 用法
for page in paginate([1, 2, 3, 4, 5], 2):
    print(page)  # [1,2] [3,4] [5]
```

**训练**：写测试验证分页逻辑（用 `list(paginate(...))` 比对）。

### T1-11：dataclass

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

### T1-12：**pytest 入门**

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

### T1-13：虚拟环境

**目标**：
- `python -m venv .venv` 创建虚拟环境
- `pip install pytest requests`
- `pip freeze > requirements.txt`

**验收**：新机器克隆项目后能 `pip install -r requirements.txt` 还原环境。

### T1-14：调试器

**目标**：在 VSCode 或 PyCharm 中：
- 打断点运行
- 查看变量
- 单步执行
- 条件断点

**训练**：故意写一个 bug，用调试器找到它。

### T1-15：标准库实战

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

### T1-16：正则表达式

**目标**：写几个常用正则。

```python
import re

# 1. 匹配邮箱：user@domain.com
email_pat = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# 2. 匹配手机号（中国大陆 11 位）
phone_pat = r"^1[3-9]\d{9}$"

# 3. 提取字符串中所有数字
nums = re.findall(r"\d+", "我有3个苹果和5个香蕉")
```

**训练**：写测试覆盖每种正则的合法/非法输入。

---

## 七、3 个小项目

### 项目 A：命令行用户管理 + unittest 测试（第 1 周）

**目标**：用 Python 实现一个命令行用户管理系统，覆盖"增删改查 + 文件持久化"，并用 unittest 写完整测试。这是本周所有知识点的综合应用。

**目录结构**：

```
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

**核心代码骨架**（供参考，请自己实现）：

```python
# models.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(**data)
```

```python
# storage.py
import json
from pathlib import Path

class Storage:
    def __init__(self, path: str):
        self.path = Path(path)
        self.users = []
        self.load()

    def load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        else:
            self.users = []

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
```

```python
# service.py
import hashlib
from models import User
from storage import Storage

class UserService:
    def __init__(self, storage: Storage):
        self.storage = storage
        self._next_id = max((u["id"] for u in storage.users), default=0) + 1

    def create(self, name: str, email: str, password: str) -> User:
        if not name or not email or not password:
            raise ValueError("name, email, password 不能为空")
        if "@" not in email:
            raise ValueError("邮箱格式非法")
        if self.find_by_email(email):
            raise ValueError("邮箱已存在")
        user = User(
            id=self._next_id,
            name=name,
            email=email,
            password_hash=hashlib.sha256(password.encode()).hexdigest(),
        )
        self._next_id += 1
        self.storage.users.append(user.to_dict())
        self.storage.save()
        return user

    def list(self) -> list[dict]:
        return self.storage.users

    def get(self, user_id: int) -> dict | None:
        for u in self.storage.users:
            if u["id"] == user_id:
                return u
        return None

    def find_by_email(self, email: str) -> dict | None:
        for u in self.storage.users:
            if u["email"] == email:
                return u
        return None

    def delete(self, user_id: int) -> bool:
        before = len(self.storage.users)
        self.storage.users = [u for u in self.storage.users if u["id"] != user_id]
        self.storage.save()
        return len(self.storage.users) < before
```

**功能要求**：

- [ ] **用户模型**：`User` 数据类，含 `id`、`name`、`email`、`password_hash`、`created_at`
- [ ] **存储层**：JSON 文件读写，文件不存在时自动初始化
- [ ] **业务层**：`create`、`list`、`get`、`find_by_email`、`delete`
- [ ] **输入校验**：空值、邮箱格式、重复邮箱
- [ ] **密码处理**：用 `hashlib.sha256` 哈希，不存明文
- [ ] **命令行入口**：`python -m user_mgr.cli` 交互式操作
- [ ] **unittest 测试**：覆盖所有函数，含正常 + 异常路径
- [ ] **覆盖率 > 80%**

**CLI 示例**（`cli.py`）：

```
$ python -m user_mgr.cli
用户管理系统 v0.1
1. 新增用户  2. 列出用户  3. 查看用户  4. 删除用户  0. 退出
> 1
姓名: 张三
邮箱: zhangsan@example.com
密码: (输入至少 2 次确认)
✓ 用户创建成功 (id=1)
> 2
ID  姓名  邮箱
1   张三  zhangsan@example.com
> 4
用户 ID: 1
✓ 用户已删除
> 0
再见
```

**测试要求**：

```python
# tests/test_service.py
import unittest
import tempfile
from pathlib import Path
from user_mgr.models import User
from user_mgr.storage import Storage
from user_mgr.service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.storage = Storage(str(Path(self.tmp) / "users.json"))
        self.service = UserService(self.storage)

    def test_create_user(self):
        user = self.service.create("Alice", "alice@example.com", "Passw0rd!")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Alice")
        self.assertNotIn("Passw0rd!", user.password_hash)  # 不存明文

    def test_create_user_empty_name(self):
        with self.assertRaises(ValueError):
            self.service.create("", "alice@example.com", "Passw0rd!")

    def test_create_user_invalid_email(self):
        with self.assertRaises(ValueError):
            self.service.create("Alice", "invalid", "Passw0rd!")

    def test_create_user_duplicate_email(self):
        self.service.create("Alice", "alice@example.com", "Passw0rd!")
        with self.assertRaises(ValueError):
            self.service.create("Bob", "alice@example.com", "Passw0rd!")

    def test_list_users(self):
        self.service.create("Alice", "alice@example.com", "Passw0rd!")
        self.service.create("Bob", "bob@example.com", "Passw0rd!")
        self.assertEqual(len(self.service.list()), 2)

    def test_get_user(self):
        created = self.service.create("Alice", "alice@example.com", "Passw0rd!")
        found = self.service.get(created.id)
        self.assertIsNotNone(found)
        self.assertEqual(found["email"], "alice@example.com")

    def test_get_user_not_found(self):
        self.assertIsNone(self.service.get(999))

    def test_find_by_email(self):
        self.service.create("Alice", "alice@example.com", "Passw0rd!")
        found = self.service.find_by_email("alice@example.com")
        self.assertIsNotNone(found)
        self.assertIsNone(self.service.find_by_email("nobody@example.com"))

    def test_delete_user(self):
        created = self.service.create("Alice", "alice@example.com", "Passw0rd!")
        self.assertTrue(self.service.delete(created.id))
        self.assertIsNone(self.service.get(created.id))

    def test_delete_user_not_found(self):
        self.assertFalse(self.service.delete(999))

if __name__ == "__main__":
    unittest.main()
```

**验收标准**：

- [ ] 模块结构清晰（models / storage / service / cli）
- [ ] 业务层不依赖 CLI，可独立测试
- [ ] 所有函数有 unittest 测试
- [ ] 测试覆盖正常 + 异常路径
- [ ] 运行 `python -m unittest discover tests -v` 全部 PASS
- [ ] 覆盖率 > 80%（用 `coverage run -m unittest` 验证）
- [ ] 数据持久化到 JSON 文件，重启后数据不丢

### 项目 B：登录模块 + pytest 测试（第 2 周）

```
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

### 项目 C：工具库 + 完整测试套件（第 3 周）

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

## 八、常见陷阱

| 陷阱 | 说明 | 解决 |
|---|---|---|
| 可变默认参数 | `def f(x=[])` 多次调用共享同一个 list | 用 `None` + 函数内初始化 |
| 浮点相等 | `0.1 + 0.2 == 0.3` 是 `False` | 用 `math.isclose` 或 pytest 的 `approx` |
| 异常吞掉 | `except: pass` | 至少 `except Exception as e: logging.error(e)` |
| 导入顺序混乱 | 模块相互引用导致循环导入 | 把共享代码抽到独立模块 |
| 时区 | `datetime.now()` 不带时区 | 用 `datetime.now(timezone.utc)` |
| 编码 | Windows 默认 GBK，读取 UTF-8 文件乱码 | `open(..., encoding="utf-8")` |
| 路径 | 相对路径在不同工作目录下失效 | 用 `pathlib.Path(__file__).parent` |

---

## 九、阶段验收

本阶段结束时，做以下自检：

- [ ] 我能用 pytest 给一个模块写测试，覆盖率 > 80%
- [ ] 我能解释「上下文管理器」「装饰器」「生成器」的用途
- [ ] 我能配置虚拟环境并导出 `requirements.txt`
- [ ] 我完成了至少 1 个「项目 A/B/C」级别的小项目
- [ ] 我有一份能展示的测试报告（HTML）
- [ ] 我能向别人解释一个 100 行的 Python 模块在做什么

> 全部打勾 → 进入 [02_测试理论与用例设计.md](./02_测试理论与用例设计.md)。
> 未全部打勾 → 补完再走，**不要带着坑进入下一阶段**。

---

## 十、打卡表（复制到你的笔记）

| 训练 | 完成日期 | 备注 |
|---|---|---|
| T1-1 容器与推导式 | 2026-09-16 | B+（修正后通过：set 排序 / 字典副作用 / 需求预期） |
| T1-2 猜数字 |  |  |
| T1-3 订单折扣 |  |  |
| T1-4 模块与包 |  |  |
| T1-5 CSV 读写 |  |  |
| T1-6 unittest 第一个测试 |  |  |
| T1-7 类与测试 |  |  |
| T1-8 异常体系 |  |  |
| T1-9 装饰器 |  |  |
| T1-10 生成器 |  |  |
| T1-11 dataclass |  |  |
| T1-12 pytest 入门 |  |  |
| T1-13 虚拟环境 |  |  |
| T1-14 调试器 |  |  |
| T1-15 标准库 |  |  |
| T1-16 正则 |  |  |
| 项目 A 用户管理 |  |  |
| 项目 B 登录 |  |  |
| 项目 C 工具库 |  |  |
