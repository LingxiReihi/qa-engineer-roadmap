# 03 · pytest 核心与进阶

> **阶段时长**：4 周（建议每天 2~3 小时，本阶段是整条路径的核心）
> **前置**：完成阶段 01、02
> **核心目标**：把 pytest 从"会写 assert"练到"能设计测试框架"。

---

## 一、为什么 pytest 是核心

pytest 是 Python 测试生态的事实标准：

- 断言简洁（`assert` 就是它）
- fixture 强大（解决 90% 的测试代码复用问题）
- 插件生态丰富（coverage、allure、xdist、rerunfailures 等）
- 接口测试、UI 测试、性能测试都能用它做框架

**学会 pytest = 学会测试开发的"母语"**。

---

## 二、学习目标

- [ ] 熟练使用 `assert` 与 `pytest.raises`
- [ ] 写出带 `@pytest.fixture` 的测试（含 yield、scope、参数化）
- [ ] 理解 `conftest.py` 的作用与加载规则
- [ ] 用 `@pytest.mark.parametrize` 写数据驱动测试
- [ ] 使用 `mark`（skip、xfail、skipif、参数）
- [ ] 用 `unittest.mock` 和 `pytest.MonkeyPatch` 做依赖替换
- [ ] 用 `coverage` 测覆盖率并解读报告
- [ ] 输出 Allure 或 pytest-html 报告
- [ ] 写一个自定义 pytest 插件

---

## 三、周计划

### 第 1 周：pytest 基础 + fixture

| 天 | 主题 | 训练 |
|---|---|---|
| D1 | pytest 安装、断言、命令行、收集机制 | T3-1 |
| D2 | `pytest.raises`、近似断言（`pytest.approx`） | T3-2 |
| D3 | fixture 基础（局部、类级、`request` 对象） | T3-3 |
| D4 | fixture 高级（`yield`、`scope`、`autouse`、`indirect`） | T3-4 |
| D5 | `conftest.py` 与 fixture 共享 | T3-5 |
| D6 | fixture 参数化（`params`、`indirect`） | T3-6 |
| D7 | 复盘 + 小项目：给一个模块写完整测试 | 项目 A |

### 第 2 周：parametrize + 标记 + 报告

| 天 | 主题 | 训练 |
|---|---|---|
| D8 | `@pytest.mark.parametrize` 基础 | T3-7 |
| D9 | parametrize 进阶（多参数、ids、间接参数化） | T3-8 |
| D10 | `mark` 体系（skip、xfail、skipif、自定义 mark） | T3-9 |
| D11 | pytest-html 报告 | T3-10 |
| D12 | Allure 报告 | T3-11 |
| D13 | 复盘 + 小项目：参数化数据驱动测试 | 项目 B |
| D14 | 缓冲 | — |

### 第 3 周：Mock + 覆盖率

| 天 | 主题 | 训练 |
|---|---|---|
| D15 | `unittest.mock` 基础（`patch`、`MagicMock`） | T3-12 |
| D16 | `Mock` 进阶（`side_effect`、`assert_called`、`patch.object`） | T3-13 |
| D17 | `pytest.MonkeyPatch` | T3-14 |
| D18 | `coverage` 安装、运行、报告解读 | T3-15 |
| D19 | 覆盖率门禁（`--cov-fail-under`） | T3-16 |
| D20 | 复盘 + 小项目：Mock 外部依赖 | 项目 C |
| D21 | 缓冲 | — |

### 第 4 周：插件 + Hook + 综合

| 天 | 主题 | 训练 |
|---|---|---|
| D22 | 内置 hook（`pytest_runtest_setup` 等） | T3-17 |
| D23 | 写自定义 pytest 插件 | T3-18 |
| D24 | `pytest-xdist` 并行执行 | T3-19 |
| D25 | `pytest-rerunfailures` 不稳定用例处理 | T3-20 |
| D26 | **阶段大项目**：完整测试框架设计 | 项目 D |
| D27 | 答辩与复盘 | 验收 |
| D28 | 缓冲 | — |

---

## 四、关键知识点

### 4.1 断言

```python
# 简单
assert 1 + 1 == 2

# 浮点
assert 0.1 + 0.2 == pytest.approx(0.3)

# 异常
with pytest.raises(ValueError, match="除数不能为 0"):
    divide(1, 0)

# 列表/字典比较
assert [1, 2, 3] == [1, 2, 3]
assert {"a": 1} == {"a": 1}

# 集合
assert {1, 2, 3} >= {1, 2}  # 子集
```

### 4.2 Fixture

```python
@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

def test_hello(sample_data):
    assert sample_data["name"] == "Alice"
```

**关键点**：

- fixture 通过**参数名**注入，不是 `return` 出来
- fixture 函数可以是一个普通的函数（不需要 `@pytest.fixture` 装饰）
- fixture 的 setup 在测试前执行，teardown 在测试后执行
- `yield` 后是 teardown 代码：

```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn        # 测试用 conn
    conn.close()      # teardown
```

### 4.3 Fixture Scope

```python
@pytest.fixture(scope="function")   # 默认：每个测试新建
@pytest.fixture(scope="class")      # 每个类共享
@pytest.fixture(scope="module")     # 每个模块共享
@pytest.fixture(scope="package")
@pytest.fixture(scope="session")    # 整个测试会话共享
```

**典型场景**：
- DB 连接用 `session`（避免重复建立）
- 临时数据用 `function`（隔离）

### 4.4 conftest.py

- 放在项目根或测试目录
- 自动加载，无需 import
- 可以放共享 fixture、共享配置、自定义 plugin
- 子目录的 `conftest.py` 只对该目录生效

### 4.5 Parametrize

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (3, 4, 7),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

**进阶**：
- `ids`：给每个 case 起名
- 多 fixture 参数化：`pytest_generate_tests` hook
- 间接参数化：`indirect=True`

### 4.6 Mark 体系

```python
@pytest.mark.skip(reason="not implemented yet")
@pytest.mark.xfail(reason="known bug, will fix in v2")
@pytest.mark.skipif(sys.version_info < (3, 9), reason="needs 3.9+")
@pytest.mark.slow  # 自定义 mark，配合 -m slow 使用
```

**pytest.ini** 里声明自定义 mark：

```ini
[pytest]
markers =
    slow: 慢测试
    api: 接口测试
    ui: UI 测试
```

### 4.7 Mock

```python
from unittest.mock import patch, MagicMock

@patch("my_module.requests.get")
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {"name": "Alice"}
    result = fetch_user()
    assert result["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### 4.8 覆盖率

```bash
pip install coverage pytest-cov
pytest --cov=my_package --cov-report=term-missing --cov-report=html
```

**报告解读**：
- **Statements**：总语句数
- **Missing**：未覆盖
- **Coverage**：覆盖率百分比
- **Missing**：未覆盖的行号

---

## 五、训练任务

### T3-1：pytest 安装与命令行

**任务**：
```bash
pip install pytest
pytest --version
```

写一个最小测试文件 `test_demo.py`：

```python
def test_add():
    assert 1 + 1 == 2

def test_fail():
    assert 1 + 1 == 3  # 故意失败
```

**运行**：
- `pytest`（默认）
- `pytest -v`（详细）
- `pytest --tb=short`（短回溯）
- `pytest -x`（首个失败即停）
- `pytest -k "add"`（按名字过滤）
- `pytest --collect-only`（只看收集）

**验收**：能解释上述每个参数的作用。

### T3-2：断言与异常

**任务**：

```python
import math
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b

def test_divide():
    assert divide(6, 3) == 2

def test_divide_zero():
    with pytest.raises(ValueError, match="除数不能为 0"):
        divide(1, 0)

def test_sqrt_approx():
    assert math.sqrt(2) == pytest.approx(1.4142, rel=1e-4)

def test_list():
    assert [1, 2, 3] == [1, 2, 3]
    assert [1, 2, 3] != [1, 2, 4]
```

**验收**：4 个测试全部通过。

### T3-3：fixture 基础

**任务**：

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "age": 30}

@pytest.fixture
def another_user():
    return {"name": "Bob", "age": 25}

def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"

def test_user_age(sample_user):
    assert sample_user["age"] == 30

def test_two_users(sample_user, another_user):
    assert sample_user["name"] != another_user["name"]
```

**训练**：
- 给 fixture 改名，测试自动跟随
- 多个 fixture 在同一个测试里组合使用

**验收**：3 个测试全部通过，fixture 被自动注入。

### T3-4：fixture 高级（yield、scope、autouse）

**任务 A**：用 yield 写数据库连接 fixture

```python
import sqlite3
import pytest

@pytest.fixture(scope="session")
def db_path(tmp_path_factory):
    return tmp_path_factory.mktemp("data") / "test.db"

@pytest.fixture
def db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    yield conn
    conn.close()
```

**任务 B**：用 `autouse` 清理全局状态

```python
@pytest.fixture(autouse=True)
def cleanup_env():
    import os
    os.environ.pop("API_KEY", None)
    yield
    os.environ.pop("API_KEY", None)
```

**任务 C**：用 `scope` 控制 fixture 生命周期

```python
@pytest.fixture(scope="module")
def config():
    return {"base_url": "https://api.example.com", "timeout": 5}
```

**验收**：能解释每个 fixture 的作用、scope 选择的理由。

### T3-5：conftest.py

**任务**：把 T3-4 的 fixture 移到 `tests/conftest.py`，验证跨文件可用。

```
project/
├── src/
│   └── my_module.py
└── tests/
    ├── conftest.py          # 放 fixture
    ├── test_a.py
    └── test_b.py
```

**验收**：`test_a.py` 和 `test_b.py` 都能用 `conftest.py` 里的 fixture。

### T3-6：fixture 参数化

**任务**：用 fixture 参数化生成多组数据。

```python
import pytest

@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_number_is_positive(number):
    assert number > 0

@pytest.fixture(params=["Alice", "Bob"])
def username(request):
    return request.param

@pytest.fixture(params=[18, 25, 60])
def age(request):
    return request.param

def test_user(username, age):
    # 会跑 2 * 3 = 6 个组合
    assert username
    assert age > 0
```

**进阶**：用 `indirect` 参数化 fixture

```python
@pytest.mark.parametrize("number", [4, 5, 6])
def test_number(number):
    assert number > 0
```

**验收**：理解 fixture 参数化的运行次数计算。

### T3-7：parametrize 基础

**任务**：

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (3, 4, 7),
    (0, 0, 0),
    (-1, 1, 0),
    (1.5, 2.5, 4.0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

**验收**：能看到 5 个 case 分别运行。

### T3-8：parametrize 进阶

**任务 A**：用 `ids` 给 case 起名

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3, "small"),
    (100, 200, 300, "large"),
], ids=["small", "large"])
```

**任务 B**：多参数间接化

```python
@pytest.fixture(params=[("Alice", 30), ("Bob", 25)])
def user(request):
    return request.param

def test_user(user):
    name, age = user
    assert name
    assert age > 0
```

**任务 C**：parametrize 与 fixture 组合

```python
@pytest.mark.parametrize("endpoint", ["/users", "/orders"])
def test_endpoint(endpoint, api_client):
    response = api_client.get(endpoint)
    assert response.status_code == 200
```

**验收**：能解释每个 case 的运行逻辑。

### T3-9：mark 体系

**任务**：

```python
import sys
import pytest

@pytest.mark.skip(reason="not implemented")
def test_future():
    pass

@pytest.mark.xfail(reason="known bug", strict=True)
def test_known_bug():
    assert False

@pytest.mark.skipif(sys.version_info < (3, 10), reason="needs 3.10+")
def test_new_feature():
    pass

@pytest.mark.slow
def test_slow():
    import time
    time.sleep(2)
```

**pytest.ini**：

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
```

**运行**：
- `pytest -m "not slow"`（跳过慢测试）
- `pytest -m slow`（只跑慢测试）
- `pytest -ra`（显示所有 skip/xfail 原因）

**验收**：能解释每个 mark 的作用。

### T3-10：pytest-html 报告

**任务**：

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

**输出**：`report.html` 是一个可交互的 HTML 报告。

**验收**：报告能展示测试详情、截图、备注。

### T3-11：Allure 报告

**任务**：

```bash
pip install allure-pytest
# 安装 allure 命令行（https://allure-framework.io/）
pytest --alluredir=allure-results
allure serve allure-results
```

**在测试里加步骤**：

```python
import allure

def test_login():
    allure.attach("user", "Alice", allure.attachment_type.TEXT)
    with allure.step("输入用户名"):
        # ...
        pass
    with allure.step("输入密码"):
        # ...
        pass
```

**验收**：报告能展示步骤、附件、环境信息。

### T3-12：Mock 基础

**任务**：

```python
from unittest.mock import patch, MagicMock
import requests

def fetch_user():
    resp = requests.get("https://api.example.com/users/1")
    return resp.json()

@patch("requests.get")
def test_fetch_user(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"name": "Alice"}
    mock_get.return_value = mock_resp

    result = fetch_user()
    assert result["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

**验收**：能解释为什么 patch 的是 `requests.get` 而不是 `my_module.requests.get`。

### T3-13：Mock 进阶

**任务 A**：用 `side_effect` 模拟异常

```python
mock_get.side_effect = requests.exceptions.ConnectionError("timeout")
with pytest.raises(requests.exceptions.ConnectionError):
    fetch_user()
```

**任务 B**：用 `assert_called_with` 验证参数

```python
mock_get.assert_called_with(url, params={"q": "python"})
```

**任务 C**：用 `patch.object` patch 类方法

```python
with patch.object(MyClass, "method") as mock_method:
    mock_method.return_value = 42
    assert MyClass().method() == 42
```

**验收**：能解释每个 mock 操作的语义。

### T3-14：MonkeyPatch

**任务**：

```python
def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    import os
    assert os.environ["API_KEY"] == "test-key"

def test_chdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    import os
    assert os.getcwd() == str(tmp_path)

def test_attr(monkeypatch):
    import math
    original = math.sqrt
    monkeypatch.setattr(math, "sqrt", lambda x: x * 2)
    assert math.sqrt(4) == 8
    monkeypatch.undo()
```

**验收**：理解 MonkeyPatch 会自动回滚。

### T3-15：覆盖率

**任务**：

```bash
pip install pytest-cov
pytest --cov=my_module --cov-report=term-missing
```

**解读报告**：

```
Name           Stmts   Miss  Cover   Missing
--------------------------------------------
my_module.py      50      5    90%   20-22, 30
```

**验收**：能解释每一列的含义。

### T3-16：覆盖率门禁

**任务**：在 `pytest.ini` 里设置：

```ini
[pytest]
addopts = --cov=my_module --cov-fail-under=80
```

**运行**：`pytest`，覆盖率不足 80% 时测试失败。

**验收**：能强制 CI 通过覆盖率门禁。

### T3-17：Hook

**任务**：写一个 hook 在测试前后打印日志。

```python
# conftest.py
def pytest_runtest_setup(item):
    print(f"\n=== SETUP: {item.name} ===")

def pytest_runtest_teardown(item):
    print(f"=== TEARDOWN: {item.name} ===")
```

**运行**：能看到每个测试前后的日志。

**验收**：能解释 hook 的调用时机。

### T3-18：自定义 pytest 插件

**任务**：写一个"测试耗时统计"插件。

```python
# my_plugin.py
import time

def pytest_runtest_setup(item):
    item._start_time = time.perf_counter()

def pytest_runtest_teardown(item):
    elapsed = time.perf_counter() - item._start_time
    print(f"{item.name}: {elapsed:.4f}s")
```

**注册插件**：在 `pytest.ini` 里 `testpaths` + `pythonpath`，或用 `entry_points` 发布。

**验收**：能解释插件的加载机制。

### T3-19：pytest-xdist 并行

**任务**：

```bash
pip install pytest-xdist
pytest -n 4  # 4 进程并行
```

**注意**：并行测试需要 fixture 隔离（避免共享状态）。

**验收**：能解释并行带来的问题（共享资源、顺序依赖）。

### T3-20：pytest-rerunfailures

**任务**：

```bash
pip install pytest-rerunfailures
pytest --reruns 2  # 失败重试 2 次
```

**验收**：理解何时用重试（网络抖动 vs 真 bug）。

---

## 六、4 个项目

### 项目 A：给模块写完整测试（第 1 周）

**任务**：为下面这个模块写完整测试。

```python
# utils.py
class StringHelper:
    @staticmethod
    def is_palindrome(s: str) -> bool:
        s = s.lower().replace(" ", "")
        return s == s[::-1]

    @staticmethod
    def count_vowels(s: str) -> int:
        return sum(1 for c in s.lower() if c in "aeiou")

    @staticmethod
    def reverse_words(s: str) -> str:
        return " ".join(s.split()[::-1])
```

**要求**：
- 用 pytest 写测试
- 覆盖正常、边界、异常
- 用 parametrize 参数化
- 覆盖率 > 85%

### 项目 B：数据驱动测试（第 2 周）

**任务**：为「用户注册」写数据驱动测试。

**业务规则**：
- 用户名：4~20 字符，字母开头
- 密码：8~16 字符，含大小写字母 + 数字
- 邮箱：合法格式

```python
@pytest.mark.parametrize("username,password,email,expected", [
    # 正常
    ("Alice", "Passw0rd!", "a@b.com", True),
    # 边界
    ("abcd", "Passw0rd!", "a@b.com", True),
    ("abcdefghij", "Passw0rd!", "a@b.com", True),
    # 异常
    ("Ab", "Passw0rd!", "a@b.com", False),  # 太短
    ("1lice", "Passw0rd!", "a@b.com", False),  # 数字开头
    ("Alice", "short", "a@b.com", False),  # 密码太短
    ("Alice", "Password", "a@b.com", False),  # 缺数字
    ("Alice", "Passw0rd!", "invalid", False),  # 邮箱非法
])
def test_register(username, password, email, expected):
    result = register(username, password, email)
    assert result == expected
```

**要求**：
- 至少 15 个 case
- 覆盖所有边界
- 用 `ids` 给 case 起名
- 输出 pytest-html 报告

### 项目 C：Mock 外部依赖（第 3 周）

**任务**：写一个"天气查询"模块并测试它。

```python
# weather.py
import requests

class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.weather.example.com"

    def get_weather(self, city: str) -> dict:
        resp = requests.get(
            f"{self.base_url}/current",
            params={"key": self.api_key, "city": city},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
```

**测试要求**：
- 用 Mock 模拟 HTTP 响应
- 测试成功、HTTP 错误、网络错误、超时
- 验证请求参数正确
- 用 fixture 管理 Mock 对象

### 项目 D：完整测试框架（第 4 周）

**任务**：设计一个分层测试框架。

**目录结构**：

```
test_framework/
├── pytest.ini
├── requirements.txt
├── conftest.py
├── plugins/
│   └── my_plugin.py
├── fixtures/
│   ├── conftest.py
│   ├── data_fixtures.py
│   └── env_fixtures.py
├── utils/
│   ├── reporter.py
│   ├── logger.py
│   └── helpers.py
├── tests/
│   ├── unit/
│   │   ├── conftest.py
│   │   └── test_*.py
│   ├── api/
│   │   ├── conftest.py
│   │   └── test_*.py
│   └── e2e/
│       ├── conftest.py
│       └── test_*.py
└── reports/
    ├── allure/
    └── html/
```

**要求**：
- 支持分层（unit / api / e2e）
- 共享 fixture 在 `fixtures/conftest.py`
- 自定义 mark（unit、api、e2e）
- 自定义插件（耗时统计、环境注入）
- 覆盖率门禁 80%
- Allure 报告
- README 文档

**验收标准**：
- 框架结构清晰
- 测试可按 mark 分组运行
- 报告完整
- 至少 30 个测试通过
- 覆盖率 > 80%

---

## 七、常见陷阱

| 陷阱 | 说明 | 解决 |
|---|---|---|
| fixture 命名冲突 | 同名 fixture 在不同 conftest 里 | 用更具体的名字，或用 `pytest.ini` 的 `norecursedirs` |
| 测试顺序依赖 | 测试 A 改了全局状态影响测试 B | 每个测试独立，用 `autouse` fixture 清理 |
| Mock patch 路径错 | patch 了错误的模块路径 | 在被测模块里 patch（`my_module.requests.get`） |
| parametrize 性能差 | case 太多导致收集慢 | 用 `indirect` 参数化，或拆分文件 |
| scope 选择错 | 用 `function` 但应该用 `session` | 根据资源开销选 scope |
| 浮点比较 | `assert 0.1 + 0.2 == 0.3` 失败 | 用 `pytest.approx` |
| 异步测试 | pytest 不支持 async | 用 `pytest-asyncio` |
| 报告里看不到中文 | 编码问题 | `export PYTHONIOENCODING=utf-8` |

---

## 八、阶段验收

- [ ] 我能写带 fixture、parametrize、mark 的 pytest 测试
- [ ] 我能写 conftest.py 共享 fixture
- [ ] 我能用 Mock 模拟外部依赖
- [ ] 我能输出覆盖率报告并解读
- [ ] 我能输出 Allure / HTML 报告
- [ ] 我设计了一个分层测试框架（项目 D）
- [ ] 我能向别人解释 pytest 的核心机制

> 全部打勾 → 进入 [04_接口自动化测试.md](./04_接口自动化测试.md)。

---

## 九、打卡表

| 训练 | 完成日期 | 备注 |
|---|---|---|
| T3-1 pytest 命令行 |  |  |
| T3-2 断言与异常 |  |  |
| T3-3 fixture 基础 |  |  |
| T3-4 fixture 高级 |  |  |
| T3-5 conftest.py |  |  |
| T3-6 fixture 参数化 |  |  |
| T3-7 parametrize 基础 |  |  |
| T3-8 parametrize 进阶 |  |  |
| T3-9 mark 体系 |  |  |
| T3-10 pytest-html |  |  |
| T3-11 Allure |  |  |
| T3-12 Mock 基础 |  |  |
| T3-13 Mock 进阶 |  |  |
| T3-14 MonkeyPatch |  |  |
| T3-15 覆盖率 |  |  |
| T3-16 覆盖率门禁 |  |  |
| T3-17 Hook |  |  |
| T3-18 自定义插件 |  |  |
| T3-19 pytest-xdist |  |  |
| T3-20 rerunfailures |  |  |
| 项目 A 模块测试 |  |  |
| 项目 B 数据驱动 |  |  |
| 项目 C Mock 外部依赖 |  |  |
| 项目 D 完整框架 |  |  |
