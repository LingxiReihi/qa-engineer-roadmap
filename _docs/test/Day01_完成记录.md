# Day 01 完成记录（2026-09-16）

## 学习内容

- **变量与别名**：变量是"标签"不是"盒子"；`b = a` 不复制，改 b 连带改 a
- **基本类型**：int / float / str / bool（动态类型，类型跟着值走）
- **4 种容器对比**：list（有序·可变）、tuple（有序·不可变）、dict（键值对·键唯一）、set（无序·去重）
- **推导式**：列表 / 字典 / 集合推导式，一行从旧容器造新容器
- **类型注解**：`def add(a: int) -> int`，运行时不生效，供人和工具阅读

## 提交物（`01-python/day01/`）

| 文件 | 内容 |
|---|---|
| `containers.py` | count_words / unique_sorted / merge_dicts + assert 自检 |
| `t1_1_comprehensions.py` | T1-1 三道推导式 |
| `demo1_types.py` | 别名与类型演示（课堂示例） |
| `demo2_comp.py` | 推导式演示（课堂示例） |

## Code Review 记录

| 轮次 | 评分 | 问题 |
|---|---|---|
| 首提 | C | ① set 去重后未排序，测试**碰巧**通过 ② `merge_dicts` 的 `a.update(b)` 污染原字典 ③ T1-1 第 1 题漏"偶数"条件，断言预期被实现带着走 |
| 修正后 | **B+（通过）** | 三处全部修复；另补 `count_words(" ")` 边界用例 |

## 核心收获（测试思维第一课）

1. **断言预期来自需求，不是来自实现** —— 测试全绿 ≠ 需求满足
2. 断言三步心法：算结果 → 写预期 → `assert 实际 == 预期`
3. 用例顺序：正常 → 边界 → 异常
4. assert 消息写"预期是什么"，而不是"我失败了"

## 术语积累（5 条）

断言 / 类型注解 / 容器 / 推导式 / 别名

## 打卡

- [x] T1-1 容器与推导式（2026-09-16，B+）

## 相关 commit

```
ffd1e62 day(01): variables, containers and comprehensions
739ea29 fix：修复count_words，unique_sorted，以及t1_1
f97d8c0 docs: record day01 review (B+) in README and T1-1 tracking
```

## 下一步

Day 2：控制流（if/for/while）+ 列表推导式，实战 T1-2 猜数字游戏（`guess_number(target, max_attempts=5)`，非法输入不崩溃）
