# 05 · Web 与移动端自动化

> **阶段时长**：3 ~ 4 周
> **前置**：完成阶段 03、04
> **核心目标**：用 Playwright 写 Web 自动化，了解 Appium 移动端测试。

---

## 一、Web 与移动端自动化的定位

在测试金字塔中，UI 自动化属于"顶层"：

- **慢**：一次跑 10 分钟起
- **脆**：页面一改版就挂
- **贵**：维护成本高

**测试开发的目标**：
- 用接口测试覆盖业务逻辑
- UI 测试只覆盖**核心端到端流程**
- 能写能维护，比写得多更重要

---

## 二、为什么推荐 Playwright 优先

| 维度 | Selenium | Playwright |
|---|---|---|
| 速度 | 慢 | 快 3~5 倍 |
| API | 老式 | 现代 async |
| 等待 | 需要显式等待 | 自动等待 |
| 调试 | 一般 | 时间旅行调试 |
| 移动端 | 需要 Appium | 内置 mobile |
| 维护 | 老 | 活跃 |

**结论**：新项目用 Playwright，老项目用 Selenium。本路径以 Playwright 为主。

---

## 三、学习目标

- [ ] 理解 HTML/DOM 结构与元素定位
- [ ] 用 Playwright 写 Web 自动化（推荐）
- [ ] 了解 Selenium 的基本用法（兼容老项目）
- [ ] 掌握 Page Object Model（PO）模式
- [ ] 掌握等待策略（避免 flaky）
- [ ] 了解 Appium 移动端自动化
- [ ] 完成一个"登录 → 搜索 → 下单 → 登出"的端到端流程

---

## 四、周计划

### 第 1 周：HTML/DOM + Playwright 基础

| 天 | 主题 | 训练 |
|---|---|---|
| D1 | HTML 结构、DOM、CSS 选择器、XPath | T5-1 |
| D2 | Playwright 安装、浏览器启动 | T5-2 |
| D3 | 元素定位（text、role、css、testid） | T5-3 |
| D4 | 操作（click、fill、type、select） | T5-4 |
| D5 | 等待策略（auto-wait、显式等待） | T5-5 |
| D6 | 断言（expect） | T5-6 |
| D7 | 复盘 + 小项目：测试一个登录页 | 项目 A |

### 第 2 周：Playwright 进阶

| 天 | 主题 | 训练 |
|---|---|---|
| D8 | Page Object Model | T5-7 |
| D9 | 多标签页、弹窗、iframe | T5-8 |
| D10 | 文件上传、截图、PDF 导出 | T5-9 |
| D11 | API 请求拦截与 Mock | T5-10 |
| D12 | 测试数据与 fixture | T5-11 |
| D13 | 报告集成（Allure） | T5-12 |
| D14 | 复盘 + 小项目：端到端流程 | 项目 B |

### 第 3 周：移动端与 Selenium

| 天 | 主题 | 训练 |
|---|---|---|
| D15 | Appium 概念、Android/iOS 设备 | T5-13 |
| D16 | Appium Python Client 基础 | T5-14 |
| D17 | 移动端元素定位（Accessibility ID） | T5-15 |
| D18 | Playwright Mobile 模式 | T5-16 |
| D19 | Selenium 基础（兼容老项目） | T5-17 |
| D20 | 对比 Selenium vs Playwright | T5-18 |
| D21 | 复盘 + 小项目：Appium 登录测试 | 项目 C |
| D22 | 缓冲 | — |

### 第 4 周：综合项目（可选）

| 天 | 主题 | 训练 |
|---|---|---|
| D23 | 测试稳定性（重试、隔离） | T5-19 |
| D24 | 并行执行（pytest-xdist + Playwright） | T5-20 |
| D25 | 浏览器兼容（Chrome/Firefox/Safari） | T5-21 |
| D26 | **大项目**：完整 Web 自动化框架 | 项目 D |
| D27 | 答辩与复盘 | 验收 |
| D28 | 缓冲 | — |

---

## 五、关键知识点

### 5.1 HTML/DOM 结构

```html
<div class="login-form">
  <input id="username" type="text" />
  <input id="password" type="password" />
  <button id="login-btn">登录</button>
</div>
```

**定位策略**：
- `#id`：最稳定
- `[data-testid="xxx"]`：推荐（专为测试）
- `.class`：样式相关，可能变
- `tag`：太宽泛
- XPath：灵活但脆弱

### 5.2 CSS 选择器

```css
#username                 /* id */
.login-form               /* class */
.login-form #username     /* 后代 */
.login-form > #username   /* 子代 */
input[type="text"]        /* 属性 */
input[type="text"]:not(:disabled)  /* 伪类 */
```

### 5.3 XPath

```xpath
//*[@id="username"]
//input[@type="text"]
//button[text()="登录"]
//input[@id="username"]/following-sibling::button
```

### 5.4 Playwright 定位

```python
page.locator("#username")            # CSS
page.locator("text=登录")             # 文本
page.locator("role=button[name=登录]")  # ARIA
page.get_by_test_id("login-btn")     # data-testid
page.get_by_role("button", name="登录")
page.get_by_placeholder("请输入用户名")
```

### 5.5 Playwright 操作

```python
page.goto("https://example.com")
page.fill("#username", "alice")
page.type("#username", "alice")        # 逐字输入
page.click("#login-btn")
page.select_option("#country", "CN")
page.check("#agree")
page.hover(".menu")
page.press("#search", "Enter")
page.screenshot(path="shot.png")
```

### 5.6 等待策略

```python
# 自动等待（推荐）
page.click("#login-btn")  # 自动等待可点击

# 显式等待
page.wait_for_selector("#username")
page.wait_for_url("**/dashboard")
page.wait_for_load_state("networkidle")
page.wait_for_timeout(1000)  # 少用！
```

### 5.7 断言

```python
from playwright.sync_api import expect

expect(page).to_have_title("首页")
expect(page.locator("#username")).to_be_visible()
expect(page.locator("#username")).to_have_value("alice")
expect(page.locator("#login-btn")).to_be_enabled()
```

### 5.8 Page Object Model

```
pages/
├── base_page.py          # 基础操作
├── login_page.py         # 登录页
├── dashboard_page.py     # 首页
└── user_page.py          # 用户页
```

### 5.9 Appium 元素定位

```python
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "loginButton")
driver.find_element(AppiumBy.ID, "com.app:id/login_btn")
driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='登录']")
```

---

## 六、训练任务

### T5-1：HTML/DOM + CSS 选择器

**任务**：在 [W3Schools HTML 教程](https://www.w3schools.com/html/) 上练习定位。

```python
# 给定 HTML，写 CSS 选择器
# 1. 选择 id="username" 的输入框
# 2. 选择 class="btn btn-primary" 的按钮
# 3. 选择所有 input[type="text"]
# 4. 选择 form 下第一个按钮
```

**验收**：能写出正确选择器。

### T5-2：Playwright 安装与启动

**任务**：

```bash
pip install playwright
playwright install  # 安装浏览器
playwright install-deps  # Linux 需要
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    page.screenshot(path="example.png")
    browser.close()
```

**验收**：能截图成功。

### T5-3：元素定位

**任务**：在 [Playwright 官方测试页](https://playwright.dev/python/docs/intro) 上练习定位。

```python
page.get_by_role("link", name="Getting Started")
page.get_by_text("Learn")
page.get_by_test_id("my-button")
page.locator("css=div.button").first
```

**验收**：理解各种定位方式。

### T5-4：操作

**任务**：在 [示例登录页](https://playwright.dev/python/docs/intro#installation) 登录。

```python
page.goto("https://example.com/login")
page.fill("#username", "alice")
page.fill("#password", "Passw0rd!")
page.click("#login-btn")
```

**验收**：能完成登录流程。

### T5-5：等待策略

**任务**：

```python
page.goto("https://example.com/slow")
page.wait_for_selector("#data-loaded")  # 等待元素出现
page.wait_for_url("**/dashboard")       # 等待 URL 变化
page.wait_for_load_state("networkidle")  # 等待网络空闲
```

**陷阱训练**：故意用 `wait_for_timeout(1000)`，观察 flaky 现象。

**验收**：能解释为什么自动等待优于显式 sleep。

### T5-6：断言

**任务**：

```python
from playwright.sync_api import expect

expect(page).to_have_title("Dashboard")
expect(page.locator("#welcome")).to_have_text("Welcome, Alice")
expect(page.locator(".avatar")).to_be_visible()
expect(page.locator(".avatar")).to_have_count(1)
```

**验收**：能写 5+ 个断言。

### T5-7：Page Object Model

**任务**：为登录页写 PO。

```python
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".error")

    def open(self, url: str):
        self.page.goto(url)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_success(self):
        expect(self.page).to_have_url("**/dashboard")

    def expect_error(self, message: str):
        expect(self.error_message).to_have_text(message)
```

**测试**：

```python
from pages.login_page import LoginPage

def test_login_success(login_page: LoginPage, base_url):
    login_page.open(f"{base_url}/login")
    login_page.login("alice", "Passw0rd!")
    login_page.expect_success()

def test_login_fail(login_page: LoginPage, base_url):
    login_page.open(f"{base_url}/login")
    login_page.login("alice", "wrong")
    login_page.expect_error("密码错误")
```

**验收**：理解 PO 的优势。

### T5-8：多标签页与弹窗

**任务**：

```python
# 新标签页
page.get_by_text("Open in new tab").click()
pages = context.pages
new_page = pages[-1]

# 弹窗
page.on("dialog", lambda dialog: dialog.accept())
page.get_by_text("Click me").click()
```

**验收**：能处理多标签和弹窗。

### T5-9：文件上传、截图、PDF

**任务**：

```python
# 文件上传
page.locator("input[type=file]").set_input_files("path/to/file.pdf")

# 截图
page.screenshot(path="full.png", full_page=True)
page.locator(".widget").screenshot(path="widget.png")

# PDF
page.pdf(path="report.pdf", format="A4")
```

**验收**：能截图、上传文件、导出 PDF。

### T5-10：API 请求拦截与 Mock

**任务**：

```python
# 拦截请求
def handle_request(route):
    route.continue_()

page.route("**/api/users", handle_request)

# Mock 响应
def mock_response(route):
    route.fulfill(
        status=200,
        content_type="application/json",
        body='{"name": "Alice"}',
    )

page.route("**/api/users", mock_response)
```

**验收**：理解请求拦截的价值。

### T5-11：测试数据与 fixture

**任务**：

```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def logged_in_page(page, base_url):
    page.goto(f"{base_url}/login")
    page.fill("#username", "alice")
    page.fill("#password", "Passw0rd!")
    page.click("#login-btn")
    page.wait_for_url(f"**/dashboard")
    return page
```

**验收**：能用 fixture 管理浏览器、上下文、登录态。

### T5-12：Allure 报告集成

**任务**：

```python
import allure
from playwright.sync_api import expect

def test_login_with_allure(logged_in_page):
    page = logged_in_page
    with allure.step("验证 Dashboard"):
        expect(page).to_have_title("Dashboard")
        expect(page.locator(".avatar")).to_be_visible()

    with allure.step("截图"):
        page.screenshot(path="allure-screenshot.png")
        allure.attach.path("allure-screenshot.png", name="Dashboard", attachment_type=allure.attachment_type.PNG)
```

**验收**：Allure 报告能展示步骤、截图。

### T5-13：Appium 概念

**任务**：
- 阅读 [Appium 官方文档](https://appium.io/docs/en/)
- 理解 Appium 与 WebDriver 的关系
- 准备 Android 模拟器或真机（开启 USB 调试）
- 安装 Appium Server

**验收**：能启动 Appium Server。

### T5-14：Appium Python Client 基础

**任务**：

```bash
pip install Appium-Python-Client
```

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.app_package = "com.example.app"
options.app_activity = ".MainActivity"

driver = webdriver.Remote("http://localhost:4723", options=options)

# 操作
element = driver.find_element("accessibility id", "loginButton")
element.click()
```

**验收**：能驱动 Android 模拟器。

### T5-15：Appium 元素定位

**任务**：练习 Android 元素定位。

```python
# Android 常见定位
driver.find_element("id", "com.app:id/login_btn")
driver.find_element("accessibility id", "Login")
driver.find_element("xpath", "//android.widget.EditText[@resource-id='username']")
driver.find_element("class name", "android.widget.Button")
```

**验收**：能定位 Android 元素。

### T5-16：Playwright Mobile

**任务**：用 Playwright 模拟移动端。

```python
from playwright.sync_api import devices

iphone = devices["iPhone 12"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(**iphone)
    page = context.new_page()
    page.goto("https://example.com")
    page.screenshot(path="mobile.png")
```

**验收**：能模拟移动端视口。

### T5-17：Selenium 基础

**任务**：

```bash
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://example.com")
print(driver.title)
driver.quit()
```

**验收**：理解 Selenium 与 Playwright 的差异。

### T5-18：Selenium vs Playwright

**任务**：用两个工具分别写一个登录测试，对比。

| 维度 | Selenium | Playwright |
|---|---|---|
| 安装 | 需要 driver | 自带浏览器 |
| 等待 | 显式等待 | 自动等待 |
| 多标签 | 手动管理 | context.pages |
| 报告 | 自己集成 | 内置 trace |
| 速度 | 慢 | 快 |

**验收**：能说出选型理由。

### T5-19：测试稳定性

**任务**：
- 用 `pytest-rerunfailures` 重试
- 用 fixture 隔离测试
- 避免全局状态

```python
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_flaky():
    ...
```

**验收**：理解 flaky 的处理方式。

### T5-20：并行执行

**任务**：

```bash
pip install pytest-xdist
pytest -n 4
```

**注意**：并行测试需要浏览器实例隔离。

**验收**：能并行运行测试。

### T5-21：浏览器兼容

**任务**：

```python
@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser_factory(request):
    with sync_playwright() as p:
        browser = getattr(p, request.param).launch()
        yield browser
        browser.close()
```

**验收**：能在三个浏览器跑同一测试。

---

## 七、4 个项目

### 项目 A：登录页测试（第 1 周）

**任务**：为 [Demo 登录页](https://playwright.dev/python/docs/intro) 写测试。

**要求**：
- 正常登录
- 密码错误
- 空用户名
- 空密码
- 超长输入
- 特殊字符
- 用 PO 组织
- 输出 Allure 报告

### 项目 B：端到端流程（第 2 周）

**任务**：在 [Sauce Demo](https://www.saucedemo.com/) 上完成端到端流程。

```
登录 → 浏览商品 → 加入购物车 → 结算 → 完成订单 → 登出
```

**要求**：
- 用 PO 组织
- 用 fixture 管理登录态
- 用 Allure 报告
- 至少 5 个测试

### 项目 C：Appium 登录测试（第 3 周）

**任务**：用 Appium 测试一个 Android App 的登录。

**前置**：
- Android 模拟器或真机
- Appium Server 运行中
- 一个测试 App（可用自己的 demo app）

**要求**：
- 启动 App
- 定位登录按钮
- 输入账号密码
- 验证登录结果
- 处理弹窗、权限

### 项目 D：完整 Web 自动化框架（第 4 周）

**任务**：设计一个完整的 Web 自动化框架。

**目录结构**：

```
web_tests/
├── pytest.ini
├── requirements.txt
├── README.md
├── conftest.py
├── config/
│   ├── settings.yaml         # 环境配置
│   └── test_data.yaml        # 测试数据
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_product.py
│   ├── test_cart.py
│   └── test_checkout.py
├── utils/
│   ├── logger.py
│   └── helpers.py
└── reports/
    └── allure/
```

**要求**：
- PO 模式
- 数据驱动（YAML）
- fixture 管理浏览器、上下文、登录态
- Allure 报告
- 支持 headless 模式
- 支持多浏览器
- 至少 20 个测试
- README 文档

**验收标准**：
- 框架结构清晰
- 测试可重复运行
- 报告完整
- 能跨浏览器运行

---

## 八、常见陷阱

| 陷阱 | 说明 | 解决 |
|---|---|---|
| 硬编码等待 | `time.sleep(2)` | 用自动等待或显式等待 |
| 选择器脆弱 | `.btn-primary` 改了就挂 | 用 `data-testid` 或 `role` |
| 测试顺序依赖 | 测试 A 登录影响测试 B | 每个测试独立登录或 fixture |
| 浏览器未关闭 | 资源泄漏 | 用 fixture yield 关闭 |
| 弹窗未处理 | 阻塞流程 | 注册 dialog handler |
| iframe 未切换 | 找不到元素 | `page.frame_locator()` |
| 测试数据污染 | 数据残留 | 用 Mock 或测试账号 |
| 多浏览器差异 | Safari 不兼容 | 用 Playwright 抽象 |

---

## 九、阶段验收

- [ ] 我能用 Playwright 写 Web 自动化
- [ ] 我能用 PO 模式组织代码
- [ ] 我理解等待策略，能避免 flaky
- [ ] 我能输出 Allure 报告
- [ ] 我了解 Appium 移动端测试
- [ ] 我了解 Selenium 的基本用法
- [ ] 我完成了一个端到端流程测试

> 全部打勾 → 进入 [06_性能测试与监控.md](./06_性能测试与监控.md)。

---

## 十、打卡表

| 训练 | 完成日期 | 备注 |
|---|---|---|
| T5-1 HTML/DOM |  |  |
| T5-2 Playwright 安装 |  |  |
| T5-3 元素定位 |  |  |
| T5-4 操作 |  |  |
| T5-5 等待策略 |  |  |
| T5-6 断言 |  |  |
| T5-7 Page Object |  |  |
| T5-8 多标签与弹窗 |  |  |
| T5-9 文件上传/截图/PDF |  |  |
| T5-10 请求拦截与 Mock |  |  |
| T5-11 fixture |  |  |
| T5-12 Allure 报告 |  |  |
| T5-13 Appium 概念 |  |  |
| T5-14 Appium 基础 |  |  |
| T5-15 Appium 元素定位 |  |  |
| T5-16 Playwright Mobile |  |  |
| T5-17 Selenium 基础 |  |  |
| T5-18 Selenium vs Playwright |  |  |
| T5-19 测试稳定性 |  |  |
| T5-20 并行执行 |  |  |
| T5-21 浏览器兼容 |  |  |
| 项目 A 登录页测试 |  |  |
| 项目 B 端到端流程 |  |  |
| 项目 C Appium 登录 |  |  |
| 项目 D 完整框架 |  |  |
