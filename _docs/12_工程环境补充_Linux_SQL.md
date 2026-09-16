# 12 · 工程环境补充：Linux 与 SQL

> **本文件补齐原路径的两个明显缺口**：Linux 命令与 SQL 基础。
> **定位**：阶段 02（测试理论）和阶段 04（接口自动化）的**并行补充**，可与主线穿插学习。
> **建议时长**：10~14 天，穿插在阶段 02~04 之间。

---

## 一、为什么要补这两个

| 能力 | 测试开发场景 | 原路径覆盖 | 本文档覆盖 |
|---|---|---|---|
| Linux 命令 | 日志分析、环境排查、部署 | ❌ 完全没讲 | ✅ 阶段 07 简略提到 |
| 日志分析 | grep/awk 找错误、过滤异常 | ❌ 没讲 | ✅ 详细 |
| 性能观察 | top/free/iostat 定位瓶颈 | ❌ 没讲 | ✅ 详细 |
| SQL 基础 | 测试数据准备、数据库验证 | ❌ 完全没讲 | ✅ 详细 |
| Git 进阶 | 分支、PR、rebase、冲突 | 阶段 05 集中讲 | ✅ 前置基础 |

**测试开发日常**：60% 时间在与日志、数据库、命令行打交道。不会 Linux 和 SQL 就做不到自动化排查。

---

## 二、Linux 基础命令（速查）

### 2.1 文件系统

```bash
pwd                        # 当前目录
ls -la                     # 列出所有文件（含隐藏）
cd /path/to/dir            # 切换目录
mkdir -p a/b/c             # 递归创建目录
cp src dst                 # 复制
mv src dst                 # 移动/重命名
rm -rf dir/                # 删除（危险！）
cat file                   # 查看文件内容
less file                  # 分页查看
head -n 20 file            # 前 20 行
tail -n 20 file            # 后 20 行
tail -f file               # 实时追踪（日志必备）
wc -l file                 # 统计行数
```

### 2.2 权限与属主

```bash
chmod +x script.sh         # 加执行权限
chmod 755 script.sh        # rwxr-xr-x
chown user:group file      # 改属主
ls -l file                 # 查看权限
```

### 2.3 进程与作业

```bash
ps -ef                     # 列出所有进程
ps -ef | grep python       # 找特定进程
top                        # 实时进程监控
htop                       # 彩色版 top（更好用）
kill <pid>                 # 终止进程
kill -9 <pid>              # 强制终止
Ctrl+C                     # 终止前台进程
Ctrl+Z                     # 挂起到后台
bg / fg                    # 后台/前台切换
jobs                       # 查看作业
```

### 2.4 网络

```bash
ping example.com           # 测试连通性
curl http://example.com    # 抓接口
curl -X POST -d '...' URL  # 发 POST
curl -H "Authorization: Bearer xxx" URL
wget http://example.com/file   # 下载文件
netstat -tulpn             # 查看端口（旧）
ss -tulpn                  # 查看端口（新，推荐）
traceroute example.com     # 路由追踪
nslookup example.com       # DNS 查询
```

### 2.5 包管理

```bash
# Ubuntu/Debian
apt update
apt install -y curl vim git

# CentOS/RHEL
yum install -y curl vim git

# Python 包
pip install pytest requests
pip list
pip show pytest
pip freeze > requirements.txt
```

### 2.6 用户与 SSH

```bash
whoami                     # 当前用户
id                         # 用户 ID
su - otheruser             # 切换用户
sudo command               # 提权执行
ssh user@host              # 远程登录
scp file user@host:/path   # 远程复制
```

---

## 三、Linux 日志分析（测试开发核心技能）

### 3.1 日志文件位置

```
/var/log/syslog            # 系统日志（Ubuntu）
/var/log/messages          # 系统日志（CentOS）
/var/log/auth.log          # 认证日志
/var/log/nginx/*.log       # Nginx 日志
/var/log/mysql/*.log       # MySQL 日志
/var/log/app/xxx.log       # 应用日志（自定）
```

### 3.2 grep 过滤（最常用）

```bash
# 基础过滤
grep "ERROR" app.log

# 忽略大小写
grep -i "error" app.log

# 多模式（OR）
grep -E "ERROR|WARN|CRITICAL" app.log

# 排除
grep -v "DEBUG" app.log

# 上下文（前后 3 行）
grep -C 3 "ERROR" app.log

# 只匹配整行
grep -w "ERROR" app.log

# 统计行数
grep -c "ERROR" app.log

# 只看文件名
grep -l "ERROR" *.log
```

### 3.3 awk 处理（结构化日志必备）

```bash
# 分隔符是空格
awk '{print $1, $5}' access.log       # 打印第 1、5 列

# 统计每种 URL 的访问次数
awk '{print $7}' access.log | sort | uniq -c | sort -rn

# 找出状态码 500 的请求
awk '$9 == 500' access.log

# 找出响应时间 > 1 秒的请求
awk '$NF+0 > 1.0' access.log

# 按字段排序
awk '{print $5, $1}' access.log | sort -n

# 条件判断
awk 'NR > 100' access.log             # 跳过前 100 行
```

### 3.4 组合实战（高频场景）

```bash
# 场景 1：找出最近 1000 行里的所有 ERROR
tail -n 1000 app.log | grep "ERROR"

# 场景 2：找出某个用户 ID 的所有请求
grep "user_id=12345" access.log

# 场景 3：统计每个 IP 的访问次数（Top 10）
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 场景 4：找出 5xx 错误的时间分布
awk '$9 ~ /^5/' access.log | awk '{print $4}' | sort | uniq -c

# 场景 5：实时追踪 ERROR
tail -f app.log | grep --line-buffered "ERROR"

# 场景 6：找出慢请求（响应时间 > 500ms）
awk '$NF+0 > 0.5' access.log | head -20

# 场景 7：统计每分钟请求量
awk '{print substr($4, 14, 5)}' access.log | sort | uniq -c

# 场景 8：找超时（请求耗时 0 但状态 499 或 504）
awk '$9 == 499 || $9 == 504' access.log
```

### 3.5 日志分析训练

**训练 T12-L1**：给你一份 access.log，完成：
- [ ] 找出所有 500 错误的请求
- [ ] 统计每个 URL 的访问次数，输出 Top 5
- [ ] 找出响应时间最长的 10 个请求
- [ ] 找出某个 IP 的所有请求
- [ ] 统计每秒请求量

**训练 T12-L2**：给你一份 app.log，完成：
- [ ] 找出所有 ERROR 行
- [ ] 找出 ERROR 前后的上下文（前后 5 行）
- [ ] 统计每种错误类型的数量
- [ ] 找出某个 user_id 的所有日志

---

## 四、Linux 性能观察（配合阶段 07）

```bash
# CPU
top                          # 实时
htop                         # 彩色版
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -10  # Top 10 进程

# 内存
free -h                      # 人类可读格式
vmstat 1                     # 每秒刷新
cat /proc/meminfo            # 详细

# 磁盘
df -h                        # 磁盘使用
du -sh *                     # 目录大小
iostat -x 1                  # 磁盘 IO
iotop                        # 实时 IO

# 网络
ss -tulpn                    # 端口与连接
ss -s                        # 连接统计
iftop                        # 实时带宽
```

**瓶颈定位思路**：

| 现象 | 检查 | 命令 |
|---|---|---|
| CPU 高 | 哪个进程占 CPU | `top` / `htop` |
| 内存高 | 哪个进程占内存 | `ps -eo pid,rss,cmd --sort=-rss` |
| 磁盘慢 | IO 等待 | `iostat -x 1` |
| 网络慢 | 连接数、丢包 | `ss -s` / `netstat -s` |
| 数据库慢 | 慢查询 | 应用慢日志 |

---

## 五、SQL 基础（测试数据准备与验证）

### 5.1 基本概念

```
数据库（Database）
  └── 表（Table）
        ├── 行（Row / Record）
        └── 列（Column / Field）
              ├── 主键（Primary Key）
              ├── 外键（Foreign Key）
              ├── 索引（Index）
              └── 约束（Constraint）
```

### 5.2 DDL：建表与改表

```sql
-- 建表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 改表
ALTER TABLE users ADD COLUMN status TINYINT DEFAULT 1;
ALTER TABLE users DROP COLUMN status;
ALTER TABLE users MODIFY COLUMN username VARCHAR(100);

-- 加索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);

-- 删表
DROP TABLE users;
```

### 5.3 DML：增删改查

```sql
-- 插入
INSERT INTO users (username, email, password_hash) VALUES ('alice', 'a@x.com', 'hash1');
INSERT INTO users (username, email, password_hash) VALUES ('bob', 'b@x.com', 'hash2'), ('carol', 'c@x.com', 'hash3');

-- 更新
UPDATE users SET status = 0 WHERE id = 1;
UPDATE users SET email = 'new@x.com' WHERE username = 'alice';

-- 删除
DELETE FROM users WHERE id = 1;
DELETE FROM users WHERE username = 'bob';

-- 查询
SELECT * FROM users;
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE username = 'alice' AND status = 1;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
```

### 5.4 条件与函数

```sql
-- 比较
WHERE age > 18
WHERE age BETWEEN 18 AND 60
WHERE username LIKE '%alice%'        -- 模糊匹配
WHERE username IN ('alice', 'bob')
WHERE email NOT LIKE '%test%'

-- 空值
WHERE status IS NULL
WHERE status IS NOT NULL

-- 聚合
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT email) FROM users;
SELECT SUM(amount) FROM orders;
SELECT AVG(price) FROM products;
SELECT MAX(created_at) FROM users;

-- GROUP BY
SELECT status, COUNT(*) FROM users GROUP BY status;
SELECT DATE(created_at), COUNT(*) FROM users GROUP BY DATE(created_at);

-- HAVING
SELECT status, COUNT(*) AS cnt FROM users GROUP BY status HAVING cnt > 10;
```

### 5.5 JOIN：多表查询

```sql
-- 内连接
SELECT u.username, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接
SELECT u.username, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 右连接
SELECT u.username, o.total
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- 多表
SELECT u.username, o.total, p.product_name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### 5.6 事务与并发

```sql
-- 显式事务
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;                          -- 提交
-- 或 ROLLBACK;                   -- 回滚

-- 测试中的事务（用完回滚，不污染数据）
BEGIN;
-- 执行测试操作
ROLLBACK;
```

### 5.7 测试场景速查

| 场景 | SQL |
|---|---|
| 验证插入成功 | `SELECT COUNT(*) FROM users WHERE email='test@x.com';` |
| 验证删除成功 | `SELECT * FROM users WHERE id=1;`（应返回空） |
| 验证更新成功 | `SELECT status FROM users WHERE id=1;` |
| 准备测试数据 | `INSERT INTO ... VALUES ...;` |
| 清理测试数据 | `DELETE FROM users WHERE email LIKE '%test@x.com';` |
| 验证事务回滚 | `BEGIN; UPDATE ...; ROLLBACK; SELECT ...;` |
| 验证唯一约束 | `INSERT ...;`（应失败） |
| 验证外键约束 | `DELETE FROM users WHERE id=1;`（有订单时失败） |
| 验证分页 | `SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;` |
| 验证排序 | `SELECT * FROM users ORDER BY created_at DESC;` |

---

## 六、SQL 训练

**训练 T12-S1：用户表 CRUD**

```sql
-- 建表
CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), email VARCHAR(100) UNIQUE, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);

-- 插入 5 个用户
-- 查询：所有用户、按 id 查、按 email 查、按名字模糊查
-- 更新：改名字、改 email
-- 删除：按 id 删、按 email 删
-- 统计：用户总数、2024 年创建的用户数
```

**训练 T12-S2：订单表 JOIN**

```sql
-- 三张表：users、orders、order_items
-- 查询：每个用户的订单总数
-- 查询：每个用户的订单总金额
-- 查询：订单数 Top 10 的用户
-- 查询：没有下过单的用户（左连接 + IS NULL）
-- 查询：某个订单包含的所有商品
```

**训练 T12-S3：测试数据准备**

```sql
-- 准备 100 个测试用户
-- 准备 500 个测试订单
-- 清理所有测试数据（按 email LIKE '%test@' 过滤）
-- 用事务包起来，测试完回滚
```

---

## 七、Git 进阶（前置基础，阶段 05 深入）

### 7.1 基础命令

```bash
git init                     # 初始化仓库
git status                   # 查看状态
git add .                    # 暂存所有变更
git add <file>               # 暂存单个文件
git commit -m "message"      # 提交
git log --oneline            # 查看历史（简短）
git log --graph --oneline    # 图形化历史
git diff                     # 查看未暂存差异
git diff --cached            # 查看已暂存差异
```

### 7.2 分支

```bash
git branch                   # 列出分支
git branch feature/login     # 创建分支
git checkout feature/login   # 切换分支
git checkout -b feature/login  # 创建并切换
git merge feature/login      # 合并分支
git branch -d feature/login  # 删除分支
```

### 7.3 PR 流程（GitHub）

```
1. 本地创建分支
   git checkout -b day/01

2. 写代码 + 提交
   git add . && git commit -m "day(01): ..."

3. 推送分支
   git push -u origin day/01

4. 在 GitHub 网页创建 PR
   - 标题：Day 1 作业提交
   - 描述：包含今日目标、代码、运行结果、测试场景、问题

5. AI Review
   - 通过：合并到 main
   - 不通过：修改后重新 push，PR 自动更新

6. 合并
   - Squash and merge（推荐，保持 main 历史整洁）
   - 或 Merge commit / Rebase and merge
```

### 7.4 解决冲突

```bash
git checkout main && git pull
git checkout feature/login && git merge main
# 出现冲突：
# 1. 打开冲突文件，看到 <<<<<<< / ======= / >>>>>>>
# 2. 选择保留哪部分，删除标记
# 3. git add <file>
# 4. git commit -m "resolve conflict"
```

### 7.5 常用补救

```bash
git checkout -- <file>       # 撤销工作区修改
git reset HEAD <file>        # 撤销暂存
git reset --soft HEAD~1      # 撤销最近一次 commit（保留修改）
git revert <commit>          # 反向 commit（推荐用于已 push 的）
git reflog                   # 查看所有操作历史（救命用）
```

---

## 八、阶段衔接

| 本文档章节 | 对应主线阶段 | 用途 |
|---|---|---|
| 2.1~2.6 Linux 基础 | 阶段 01（工程环境） | 命令速查 |
| 3.1~3.5 日志分析 | 阶段 02（测试理论）+ 阶段 07（性能） | 日志实战 |
| 4 性能观察 | 阶段 07（性能测试） | 瓶颈定位 |
| 5.1~5.7 SQL 基础 | 阶段 04（接口自动化） | 测试数据 + 数据库验证 |
| 6 SQL 训练 | 阶段 04~05 项目 | 项目练手 |
| 7.1~7.5 Git 进阶 | 阶段 05（CI/CD） | 前置基础 |

---

## 九、阶段验收

- [ ] 我能用 grep/awk 分析日志，找出 ERROR、统计 Top N
- [ ] 我能用 top/free/iostat/ss 观察系统性能
- [ ] 我能用 SQL 做 CRUD、JOIN、聚合、事务
- [ ] 我能用 SQL 准备测试数据 + 验证测试效果
- [ ] 我能用 Git 完成分支、PR、冲突解决、回退
- [ ] 我完成了 3 个 SQL 训练 + 2 个日志训练

> 全部打勾 → 工程基础补齐，主线学习更扎实。

---

## 十、常见陷阱

| 陷阱 | 说明 | 解决 |
|---|---|---|
| `rm -rf` 误删 | 不可恢复 | 加 `.` 确认、用 `-i` 交互 |
| `sudo` 乱用 | 权限混乱 | 只在需要时用 |
| 日志太大 grep 慢 | 卡住 | 用 `tail -n 1000` 先缩小范围 |
| SQL `SELECT *` | 性能差、字段不确定 | 明确列名 |
| SQL 不带 `WHERE` 更新/删除 | 删全表 | 永远加 `WHERE`，先 `SELECT` 验证 |
| SQL 不写事务 | 数据污染 | `BEGIN` ... `ROLLBACK` |
| Git `git push --force` | 覆盖历史 | 仅在 rebase 后，且确认 |
| Git commit message 乱写 | 历史难读 | 用规范格式 |

---

## 十一、本文件的承诺

读完这一份，你应该明白：

1. **Linux 是测试开发的日常** —— 日志、性能、环境排查都用它
2. **日志分析是核心技能** —— grep + awk 能解决 80% 的问题
3. **SQL 是测试数据的基础** —— 准备、验证、清理都离不开
4. **Git 进阶要前置** —— PR 流程从 Day 1 就开始用
5. **训练可立即上手** —— 3 个 SQL + 2 个日志训练

> 「不会 Linux 和 SQL 的测试开发，只能做点点点。」
