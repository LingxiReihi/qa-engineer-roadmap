# 03 · pytest 核心与进阶

> **阶段时长**：4 周（预计 Day 36~63）
> **前置**：阶段 01（Python 基础）验收通过
> **核心目标**：掌握 fixture/parametrize/conftest/hook/Mock/标记/插件/报告
> **状态**：⏳ 待开始（到达此阶段时完善详细计划）

---

## 一、阶段概述

pytest 是测试开发的核心工具。本阶段从"会用 assert"到"能写框架级测试套件"。

---

## 二、核心能力目标

- [ ] 用 fixture 管理测试前置/后置（含 scope 和 yield）
- [ ] 用 parametrize 写数据驱动测试
- [ ] 用 conftest.py 组织多模块测试套件
- [ ] 用 Mock 替换外部依赖（网络/文件/数据库）
- [ ] 配置测试覆盖率门禁（coverage > 80% 阻断 CI）
- [ ] 用 Allure 输出含图表的测试报告

---

## 三、训练任务（概览）

| 训练 | 主题 | 核心知识点 |
|------|------|-----------|
| T3-1 | fixture 基础 | setup/teardown、scope、yield |
| T3-2 | parametrize | 参数化数据、间接参数化 |
| T3-3 | conftest.py | 跨模块复用、fixture 继承 |
| T3-4 | Mock | unittest.mock、patch、MagicMock |
| T3-5 | 覆盖率与门禁 | coverage、fail_under |
| T3-6 | Allure 报告 | 报告生成、步骤、附件 |
| T3-7 | 标记与跳过 | mark、skip、xfail、pytest.ini |
| T3-8 | Hook 与插件 | conftest 钩子、自定义插件 |
| T3-9 | 进阶实战 | 完整测试套件 + CI 集成 |

---

## 四、阶段验收

| 维度 | 要求 | 验证方式 |
|------|------|----------|
| fixture 能力 | 能设计 fixture 管理测试环境 | 多模块测试套件 |
| Mock 能力 | 能 Mock 外部依赖 | 脱离外部环境的测试 |
| 覆盖率能力 | 能配置覆盖率门禁 | CI 中 coverage 阻断 |
| 报告能力 | 能输出 Allure 报告 | 含图表的测试报告 |

> 到达此阶段时，将本文件展开为详细版。
