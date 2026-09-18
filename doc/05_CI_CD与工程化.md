# 05 · CI/CD 与工程化

> **阶段时长**：3 周（预计 Day 92~104）
> **前置**：阶段 04（接口自动化）验收通过
> **核心目标**：Git 分支策略、GitHub Actions 跑测试、Docker 容器化、Allure 报告集成
> **状态**：⏳ 待开始（到达此阶段时完善详细计划）

---

## 一、阶段概述

工程化是测试开发的"基础设施"。本阶段让测试在 CI 中自动运行，让团队从"手动跑测试"变成"推代码自动跑"。

---

## 二、核心能力目标

- [ ] 掌握 Git 分支策略（Git Flow / Trunk Based）
- [ ] 用 GitHub Actions 自动跑测试
- [ ] 用 Docker 容器化测试环境
- [ ] 在 CI 中集成 Allure 报告
- [ ] 推 PR 后自动触发测试，失败自动通知

---

## 三、训练任务（概览）

| 训练 | 主题 | 核心知识点 |
|------|------|-----------|
| T5-1 | Git 分支策略 | Git Flow、Trunk Based、PR 流程 |
| T5-2 | GitHub Actions 基础 | workflow、job、step、触发条件 |
| T5-3 | CI 跑测试 | pytest 集成、矩阵构建、缓存 |
| T5-4 | Docker 容器化 | Dockerfile、docker-compose |
| T5-5 | Allure 报告集成 | CI 中生成并上传报告 |
| T5-6 | 通知集成 | 微信/钉钉/Slack 通知 |

---

## 四、阶段验收

| 维度 | 要求 | 验证方式 |
|------|------|----------|
| CI 能力 | 推 PR 后自动触发测试 | GitHub Actions workflow |
| Docker 能力 | 测试环境容器化 | Dockerfile + compose |
| 通知能力 | 失败自动通知 | 通知配置 |

> 到达此阶段时，将本文件展开为详细版。
