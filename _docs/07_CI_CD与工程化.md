# 07 · CI/CD 与工程化

> **阶段时长**：3 周
> **前置**：完成阶段 03、04
> **核心目标**：把测试接入 CI/CD，让测试在 PR 上自动运行。

---

## 一、为什么工程化是测试开发的分水岭

测试执行 → 测试工程师
测试开发 → 会用代码写测试
测试开发专家 → **能搭 CI/CD、能容器化、能平台化**

工程化能力决定你的天花板。

---

## 二、学习目标

- [ ] 熟练使用 Git（分支、提交、PR、冲突解决）
- [ ] 理解 Git 工作流（feature branch、PR review）
- [ ] 用 GitHub Actions 配置 CI
- [ ] 让 pytest 在 PR 上自动运行
- [ ] 用 Docker 容器化测试环境
- [ ] 集成 Allure 报告
- [ ] 配置测试失败通知
- [ ] 了解 Jenkins（兼容企业环境）

---

## 三、周计划

### 第 1 周：Git + GitHub Actions 基础

| 天 | 主题 | 训练 |
|---|---|---|
| D1 | Git 基础（clone、commit、push、log） | T7-1 |
| D2 | Git 分支（branch、merge、rebase） | T7-2 |
| D3 | GitHub PR 流程、代码审查 | T7-3 |
| D4 | 解决冲突 | T7-4 |
| D5 | GitHub Actions 概念、语法 | T7-5 |
| D6 | 第一个 Actions 工作流 | T7-6 |
| D7 | 复盘 + 小项目：配置 PR 自动跑测试 | 项目 A |

### 第 2 周：CI 进阶 + Docker

| 天 | 主题 | 训练 |
|---|---|---|
| D8 | Actions 进阶（缓存、矩阵、并发） | T7-7 |
| D9 | Docker 基础（镜像、容器、Dockerfile） | T7-8 |
| D10 | Docker Compose（多容器） | T7-11 |
| D12 | Allure 报告集成到 CI | T7-13 |
| D13 | 测试失败通知（Slack、钉钉、邮件） | T7-14 |
| D14 | 复盘 + 小项目：Docker 化测试 | 项目 B |

### 第 3 周：Jenkins + 综合

| 天 | 主题 | 训练 |
|---|---|---|
| D15 | Jenkins 概念、安装 | T7-15 |
| D16 | Jenkins Pipeline（Jenkinsfile） | T7-16 |
| D17 | 对比 GitHub Actions vs Jenkins | T7-17 |
| D18 | 测试环境管理 | T7-18 |
| D19 | 密钥管理（GitHub Secrets、Vault） | T7-19 |
| D20 | **大项目**：完整 CI/CD 流水线 | 项目 C |
| D21 | 答辩与复盘 | 验收 |
| D22 | 缓冲 | — |

---

## 四、关键知识点

### 4.1 Git 工作流

```
main (生产)
  │
  ├── feature/login     ← 开发分支
  │     └── PR ──▶ code review ──▶ merge to main
  │
  ├── hotfix/bug-123    ← 紧急修复
  │     └── PR ──▶ merge to main + release
  │
  └── release/v1.2.0    ← 发布分支
```

**关键命令**：

```bash
git checkout -b feature/login    # 创建分支
git add .                         # 暂存
git commit -m "feat: add login"  # 提交
git push -u origin feature/login # 推送
git pull --rebase                 # 同步
git merge main                    # 合并
git rebase main                   # 变基
git cherry-pick <commit>          # 摘取提交
```

### 4.2 GitHub Actions

```yaml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest --cov=.
```

### 4.3 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]
```

### 4.4 Docker Compose

```yaml
version: "3.8"
services:
  test:
    build: .
    volumes:
      - .:/app
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"
```

### 4.5 Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/xxx/yyy.git'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --cov=. --cov-fail-under=80'
            }
        }
    }
}
```

---

## 五、训练任务

### T7-1：Git 基础

**任务**：
```bash
# 1. 初始化仓库
git init my-project
cd my-project

# 2. 编辑文件
echo "Hello" > README.md

# 3. 查看状态
git status

# 4. 添加 + 提交
git add README.md
git commit -m "Initial commit"

# 5. 查看历史
git log --oneline

# 6. 推送到远程
git remote add origin https://github.com/xxx/my-project.git
git push -u origin main
```

**验收**：能完成基本操作。

### T7-2：Git 分支

**任务**：

```bash
# 创建分支
git checkout -b feature/login

# 提交
git commit -m "Add login feature"

# 合并
git checkout main
git merge feature/login

# 删除分支
git branch -d feature/login

# 变基
git checkout feature/login
git rebase main
```

**验收**：能解释 merge 与 rebase 的区别。

### T7-3：PR 流程

**任务**：
1. 创建 feature 分支
2. 提交代码
3. 推送
4. 在 GitHub 创建 PR
5. 写 PR 描述（标题、说明、测试说明）
6. 请求 review
7. 根据反馈修改
8. merge 到 main

**验收**：完成一次 PR 流程。

### T7-4：解决冲突

**任务**：故意制造冲突并解决。

```bash
# 分支 A
git checkout -b feature/a
echo "A" > file.txt
git commit -am "A"

# 分支 B
git checkout main
echo "B" > file.txt
git commit -am "B"

# 合并冲突
git checkout feature/a
git merge main  # 冲突
```

**解决**：
- 打开 file.txt，看到 `<<<<<<<` 标记
- 选择保留哪部分
- 删除标记
- `git add file.txt`
- `git commit -m "Resolve conflict"`

**验收**：能解决冲突。

### T7-5：GitHub Actions 概念

**任务**：
- 理解 Actions 的组成（workflow、job、step）
- 理解触发器（push、pull_request、schedule）
- 理解 runner（ubuntu、windows、macos、self-hosted）

**参考**：[GitHub Actions 文档](https://docs.github.com/en/actions)

**验收**：能解释 Actions 的基本结构。

### T7-6：第一个 Actions 工作流

**任务**：在 `.github/workflows/ci.yml` 创建：

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -v
```

**验收**：push 后能看到 CI 运行。

### T7-7：Actions 进阶

**任务 A**：缓存 pip 包

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    cache: "pip"
```

**任务 B**：测试矩阵（多 Python 版本）

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11"]
```

**任务 C**：并发控制

```yaml
concurrency:
  group: ${{ github.ref }}
  cancel-in-progress: true
```

**任务 D**：调度任务（每天凌晨跑）

```yaml
on:
  schedule:
    - cron: "0 0 * * *"
```

**验收**：能写出进阶工作流。

### T7-8：Docker 基础

**任务**：
```bash
docker --version
docker run hello-world
docker images
docker ps
```

**写 Dockerfile**：

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest"]
```

**构建 + 运行**：

```bash
docker build -t my-tests .
docker run --rm my-tests
```

**验收**：能在容器中跑测试。

### T7-11：Docker Compose

**任务**：写 `docker-compose.yml`：

```yaml
version: "3.8"
services:
  test:
    build: .
    volumes:
      - .:/app
    depends_on:
      - mysql
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: test_db
    ports:
      - "3306:3306"
```

**运行**：

```bash
docker compose up --build
```

**验收**：能启动多个容器。

### T7-13：Allure 报告集成到 CI

**任务**：

```yaml
- name: Run tests with Allure
  run: pytest --alluredir=allure-results

- name: Upload Allure report
  uses: actions/upload-artifact@v4
  with:
    name: allure-results
    path: allure-results/
```

**生成 HTML 报告**（用 `allure` CLI 或 Docker）：

```yaml
- name: Generate Allure report
  uses: actions/download-artifact@v4
  with:
    name: allure-results
    path: allure-results

- name: Build Allure report
  uses: simple-elf/allure-report-action@master
  with:
    results: ./allure-results
```

**验收**：CI 能上传 Allure 报告。

### T7-14：测试失败通知

**任务**：用 GitHub Actions + Slack Webhook。

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Test failed in ${{ github.repository }} - ${{ github.sha }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

**验收**：测试失败时收到通知。

### T7-15：Jenkins 概念

**任务**：
- 阅读 [Jenkins 文档](https://www.jenkins.io/doc/)
- 理解 Jenkins 的组成（Job、Pipeline、Plugin）
- 理解 Jenkins 与 GitHub Actions 的区别

**验收**：能解释 Jenkins 的用途。

### T7-16：Jenkins Pipeline

**任务**：写 `Jenkinsfile`：

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/xxx/yyy.git'
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '. .venv/bin/activate && pytest --cov=. --cov-fail-under=80'
            }
        }

        stage('Report') {
            steps {
                sh 'pytest --alluredir=allure-results'
            }
            post {
                always {
                    allure results: 'allure-results'
                }
            }
        }
    }

    post {
        failure {
            slackSend channel: '#qa',
                      message: "Test failed in ${env.JOB_NAME} - ${env.BUILD_URL}"
        }
    }
}
```

**验收**：能在 Jenkins 上跑测试。

### T7-17：Actions vs Jenkins

**任务**：对比表。

| 维度 | GitHub Actions | Jenkins |
|---|---|---|
| 部署 | SaaS / self-hosted | 自托管 |
| 配置 | YAML | Groovy / DSL |
| 生态 | 官方 + Marketplace | 大量 Plugin |
| 成本 | GitHub 额度 | 免费 |
| 维护 | GitHub 负责 | 自己维护 |
| 学习曲线 | 低 | 中 |

**验收**：能说出选型理由。

### T7-18：测试环境管理

**任务**：
- 用环境变量区分环境（dev、test、staging、prod）
- 用 `.env` 文件管理配置
- 用 GitHub Secrets 管理密钥

```yaml
# pytest.ini
[pytest]
env =
    ENV=test
    DATABASE_URL=postgresql://test:test@localhost/test_db
```

**验收**：能管理多环境。

### T7-19：密钥管理

**任务**：
- 在 GitHub 仓库设置里添加 Secrets
- 在 Actions 里引用 `${{ secrets.API_KEY }}`
- 不要提交 `.env` 文件到 Git

```yaml
- name: Test with secret
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: echo "Using $API_KEY"
```

**验收**：能安全使用密钥。

---

## 六、3 个项目

### 项目 A：PR 自动跑测试（第 1 周）

**任务**：配置 GitHub Actions，让每次 PR 都自动跑测试。

**要求**：
- push 到 main 触发
- PR 触发
- 多 Python 版本矩阵（3.9、3.10、3.11）
- 测试覆盖率门禁 80%
- 失败时显示错误信息

**交付物**：
- `.github/workflows/ci.yml`
- 运行截图

### 项目 B：Docker 化测试（第 2 周）

**任务**：用 Docker 容器化测试环境。

**要求**：
- Dockerfile（Python + 依赖）
- docker-compose.yml（含 MySQL）
- 测试在容器中运行
- 数据初始化脚本
- 报告集成

**交付物**：
- Dockerfile
- docker-compose.yml
- 初始化脚本
- README

### 项目 C：完整 CI/CD 流水线（第 3 周）

**任务**：设计一个完整的 CI/CD 流水线。

**目录结构**：

```
project/
├── .github/
│   └── workflows/
│       ├── ci.yml              # PR 跑测试
│       ├── nightly.yml         # 夜间跑全量
│       └── release.yml         # 发布时跑 E2E
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── README.md
├── src/
│   └── my_module.py
├── tests/
│   ├── unit/
│   ├── api/
│   └── e2e/
└── scripts/
    ├── init_db.sh
    └── run_tests.sh
```

**要求**：
- 多阶段工作流（unit、api、e2e）
- 多环境（dev、test、staging）
- 报告集成（Allure）
- 失败通知
- 密钥管理
- 覆盖率门禁
- README 文档

**验收标准**：
- PR 自动跑测试
- 报告可访问
- 失败有通知
- 环境隔离

---

## 七、CI 工作流模板

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"
  COV_THRESHOLD: "80"

jobs:
  unit-test:
    name: Unit Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest tests/unit --cov=src --cov-fail-under=${{ env.COV_THRESHOLD }}

  api-test:
    name: API Test
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
        options: >
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest tests/api --alluredir=allure-results

  e2e-test:
    name: E2E Test
    runs-on: ubuntu-latest
    needs: [unit-test, api-test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: playwright install --with-deps
      - run: pytest tests/e2e --alluredir=allure-results

  upload-report:
    name: Upload Report
    runs-on: ubuntu-latest
    needs: [unit-test, api-test, e2e-test]
    if: always()
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: allure-results
      - uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: allure-results/
          retention-days: 7

  notify:
    name: Notify
    runs-on: ubuntu-latest
    needs: [unit-test, api-test, e2e-test]
    if: always()
    steps:
      - name: Notify on failure
        if: ${{ failure() }}
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "❌ Test failed in ${{ github.repository }} - ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 八、常见陷阱

| 陷阱 | 说明 | 解决 |
|---|---|---|
| CI 太慢 | 每次 PR 跑 30 分钟 | 分阶段跑、并行、缓存 |
| 测试顺序依赖 | CI 失败本地通过 | 测试隔离，每个测试独立 |
| 密钥泄露 | 提交到 Git | 用 Secrets，不要提交 .env |
| 环境不一致 | 本地通过 CI 失败 | 容器化、版本锁定 |
| 报告丢失 | CI 跑完没报告 | 用 artifact 上传 |
| 失败无通知 | 没人知道测试失败 | 配置 Slack/邮件 |
| 覆盖率门禁 | 没人遵守 | 强制门禁，PR 不通过不能合并 |

---

## 九、阶段验收

- [ ] 我能用 Git 完成日常开发流程
- [ ] 我能用 GitHub Actions 配置 CI
- [ ] 我能用 Docker 容器化测试
- [ ] 我能集成 Allure 报告
- [ ] 我能配置测试失败通知
- [ ] 我了解 Jenkins Pipeline
- [ ] 我完成了一个完整的 CI/CD 流水线

> 全部打勾 → 进入 [08_测试开发进阶与项目实战.md](./08_测试开发进阶与项目实战.md)。

---

## 十、打卡表

| 训练 | 完成日期 | 备注 |
|---|---|---|
| T7-1 Git 基础 |  |  |
| T7-2 Git 分支 |  |  |
| T7-3 PR 流程 |  |  |
| T7-4 解决冲突 |  |  |
| T7-5 Actions 概念 |  |  |
| T7-6 第一个工作流 |  |  |
| T7-7 Actions 进阶 |  |  |
| T7-8 Docker 基础 |  |  |
| T7-11 Docker Compose |  |  |
| T7-13 Allure 集成 |  |  |
| T7-14 失败通知 |  |  |
| T7-15 Jenkins 概念 |  |  |
| T7-16 Jenkins Pipeline |  |  |
| T7-17 Actions vs Jenkins |  |  |
| T7-18 环境管理 |  |  |
| T7-19 密钥管理 |  |  |
| 项目 A PR 自动测试 |  |  |
| 项目 B Docker 化测试 |  |  |
| 项目 C 完整流水线 |  |  |
