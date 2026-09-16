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
