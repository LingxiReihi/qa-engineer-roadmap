# Day 5：用户输入校验器（validator 包）

> **日期**：2026-09-19 ｜ 训练 T1-5 ｜ Review：⬜ 未开始
> **对应文件**：`01-python/day05/validator/`（实战包，待完成）、`01-python/day05/test_validator.py`（验收入口）
> **数据库**：topic #17 Python 函数与模块化 → in_progress（mastery 0.832，证据 5/5）
> **前情**：Day 4 T1-4 calc 包评 A，4 类错误（哨兵值 / 死断言 / 边界缺失 / 覆盖空洞）全部结案

---

## 一、今日目标

- [ ] 分清 **TypeError 与 ValueError 的分工**：传错类型 vs 类型对但值不合法
- [ ] 掌握校验函数的三层结构：**类型校验 → 格式校验 → 语义校验**
- [ ] 理解**为什么「校验报告」可以返回列表，而「运算结果」不能返回哨兵值**
- [ ] 把 Day 4 的 `expect_typeerror` 模式迁移到 ValueError 场景
- [ ] 验收：T1-5 的 `validator/` 包全部断言通过，且**至少改坏一个函数验证测试会失败**

---

## 二、理论要点

### 2.1 校验的三层

```text
① 类型校验   isinstance(x, str)      传错类型   → TypeError
② 格式校验   去空格、剥前缀、长度     格式不对   → ValueError
③ 语义校验   范围、区间、规则组合     值不合法   → ValueError
```

- 顺序不能颠倒：先确认类型，再解析格式，最后判断语义。类型不对时调用 `len()` 之类会冒出意料之外的报错。
- Day 4 的 `clamp` 校验 `low > high` 属于第 ③ 层，所以抛 **ValueError** 而不是 TypeError——参数类型都是 int，只是语义上不成立。

### 2.2 TypeError vs ValueError 的分工

| 场景 | 异常 | 例子 |
|------|------|------|
| 传了非预期类型 | `TypeError` | `normalize_phone(13812345678)` |
| 类型对，但值不合法 | `ValueError` | `normalize_phone("23812345678")` |
| 类型对，但参数组合矛盾 | `ValueError` | `clamp(5, low=20, high=10)` |

> 判断口诀：**「这参数压根不是我要的东西」→ TypeError；「是我要的东西，但它不对」→ ValueError。**

### 2.3 为什么「校验报告」可以返回列表，而「运算结果」不能返回哨兵值

Day 4 里 `add("a", "b")` 返回 `0` 是错的，`validate_password("abc")` 返回 `["需要大写字母", ...]` 却是对的。区别不在「返回什么类型」，而在：

| | 哨兵值（错） | 校验报告（对） |
|---|---|---|
| 调用方预期 | 期望一个数字，拿到 0 会当成合法结果 | 期望一个报告，拿到列表就是正常结果 |
| 错误是否被伪装 | 调用方的 bug 被伪装成合法返回值 | 没有伪装，报告本身就是答案 |
| 调用方是否必须防御 | 必须写 `if result is not None` | 不需要 |

> 核心：**哨兵值的罪在于把「调用方的错误」伪装成「合法结果」。** 如果返回值本身就是合法的，那就不叫哨兵值。

### 2.4 错误信息要「可操作」

```python
# ❌ 不可操作：只说错了
raise ValueError("手机号不合法")

# ✅ 可操作：说清收到什么、期望什么
raise ValueError(
    f"normalize_phone() 期望 11 位且以 1 开头的手机号，"
    f"实际收到 {raw!r}（去空格剥前缀后为 {digits!r}，共 {len(digits)} 位）"
)
```

---

## 三、练习：textutil 包（热身）

### 3.1 目标

建 `textutil/` 包，实现 `word_count`，包外写断言。

### 3.2 规格

```python
def word_count(text: str) -> int:
    """统计中英混合文本的词数：英文按空格分隔，中文按字符计。"""
```

| 输入 | 预期 | 说明 |
|------|------|------|
| `"hello 世界 abc"` | `4` | hello / 世 / 界 / abc |
| `"hello"` | `1` | 纯英文单词 |
| `"世界"` | `2` | 纯中文按字符 |
| `""` | `0` | 空串 |
| `"  多个   空格  "` | `2` | 多空格不产生空词 |

- 非 str 输入 → `TypeError`
- 全部通过后打印 `print("textutil 包全部通过")`

---

## 四、训练任务 T1-5：validator 包

### 4.1 目标结构

```text
01-python/day05/
├── validator/
│   ├── __init__.py      # 对外导出
│   ├── phone.py         # normalize_phone, mask_phone
│   └── password.py      # validate_password, parse_score
└── test_validator.py    # 包外测试脚本（验收入口）
```

### 4.2 `phone.py`

#### `normalize_phone(raw: str) -> str`

行为：
1. 去掉空格、横线 `-`、括号 `()`
2. 剥离国际前缀 `+86` / `0086`
3. 剥离裸 `86` 前缀**仅当剥离后是 11 位且以 1 开头**时（否则 `86` 可能是号码本身的一部分）
4. 结果必须是 **11 位且以 1 开头**

| 输入 | 预期 |
|------|------|
| `"13812345678"` | `"13812345678"` |
| `"138 1234 5678"` | `"13812345678"` |
| `"+8613812345678"` | `"13812345678"` |
| `"0086-138-1234-5678"` | `"13812345678"` |
| `"8613812345678"` | `"13812345678"` |
| `"23812345678"` | `ValueError`（不以 1 开头） |
| `"12345"` | `ValueError`（位数不足） |
| `""` | `ValueError` |

> ⚠️ **必测幂等性**：`normalize_phone(normalize_phone(x)) == normalize_phone(x)`。
> 归一化函数跑两次应该得到同一个结果——这是「归一化」的定义。写一条断言验证它。

#### `mask_phone(phone: str) -> str`

行为：先 `normalize_phone`，再脱敏成 `138****5678`（保留前 3 后 4，中间 4 位掩码）。

| 输入 | 预期 |
|------|------|
| `"13812345678"` | `"138****5678"` |
| `"138 1234 5678"` | `"138****5678"` |
| `"abc"` | `ValueError` |

> 思考：`mask_phone` 为什么不返回掩码失败时的空串？（回到 §2.3）

### 4.3 `password.py`

#### `validate_password(pwd: str) -> list[str]`

行为：返回**未满足**的规则名列表；全部满足返回空列表。**不要 raise**（见 §2.3）。

规则（4 条）：
- `长度 ≥ 8`
- `包含大写字母`
- `包含数字`
- `包含符号（非字母数字）`

| 输入 | 预期 |
|------|------|
| `"Abc12345!"` | `[]` |
| `"abcdefgh"` | `["需要大写字母", "需要数字", "需要符号"]` |
| `"A1"` | 4 条全缺 |
| `"abcdefgh1!"` | `[]`（刚好 10 位，含四类） |
| `"A"` | 3 条缺（长度、小写、数字…自行核对） |

> 每条规则的消息文本**自己定义**，但要在 docstring 里列出，保证实现和文档一致。
> 非 str 输入 → `TypeError`。

#### `parse_score(raw: str) -> int`

行为：解析百分制分数，支持三种写法：`"95"` / `"95分"` / `"95/100"`。结果必须在 **[0, 100] 闭区间**。

| 输入 | 预期 |
|------|------|
| `"95"` | `95` |
| `"95分"` | `95` |
| `"95/100"` | `95` |
| `"0"` | `0`（下界合法） |
| `"100"` | `100`（上界合法） |
| `"101"` | `ValueError` |
| `"-1"` | `ValueError` |
| `"95/90"` | `ValueError`（分母不是 100） |

> ⚠️ **闭区间边界**：`0` 和 `100` 都合法。Day 3 的 rate 区间坑是「排除默认值 1.0」，这里是同一类错误的反面——**别忘了端点是合法的**。

### 4.4 `__init__.py`

```python
from .phone import normalize_phone, mask_phone
from .password import validate_password, parse_score
```

- 全部导出即可（Day 4 的「故意不导出」实验已完成，本轮不再重复）。

### 4.5 `test_validator.py` —— 包外测试脚本

**要求**：
1. 全部断言通过、exit 0；运行方式：在 `01-python/day05/` 目录下执行 `python test_validator.py`
2. **迁移 Day 4 的助手函数模式**，新增 `expect_valueerror`（不要复制 `expect_typeerror` 五遍）
3. 每个函数 ≥ 5 条断言：正常 / 边界 / 格式变体 / 非法值 / 类型错误
4. `normalize_phone` 必须有**幂等性**断言
5. `validate_password` 必须断言**返回值的精确列表**（顺序和文案都要对）
6. 全部通过后打印 `print("validator 包全部通过")`

参考（迁移自 Day 4）：

```python
def expect_error(fn, exc, *args, label):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError(f"{label}：预期抛出 {exc.__name__}，实际未抛出")


expect_error(normalize_phone, ValueError, "23812345678", label="normalize_phone用例7")
```

### 4.6 验收清单

- [ ] `from validator import normalize_phone, mask_phone, validate_password, parse_score` 全部可用
- [ ] 每个函数 ≥ 5 条断言，覆盖正常 / 边界 / 格式变体 / 非法值 / 类型错误
- [ ] `normalize_phone` 有幂等性断言
- [ ] `validate_password` 有精确列表断言（含空列表）
- [ ] `parse_score` 断言 `0` 和 `100` 两个端点都合法
- [ ] TypeError 与 ValueError 的分工正确，错误信息含实际收到的值
- [ ] 全部断言通过、exit 0、打印 `validator 包全部通过`
- [ ] **负向验证**：故意改坏一个函数，确认测试真的失败（把这一轮的验证结果写进本文档第五节）
- [ ] docstring 写 `:raises TypeError:` / `:raises ValueError:`

---

## 五、当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| textutil 包（热身） | ⬜ 未开始 | word_count |
| validator/phone.py | ⬜ 未开始 | normalize_phone + mask_phone |
| validator/password.py | ⬜ 未开始 | validate_password + parse_score |
| validator/__init__.py | ⬜ 未开始 | 4 个函数全部导出 |
| test_validator.py | ⬜ 未开始 | 含 expect_error 迁移 |
| 幂等性断言 | ⬜ 待完成 | normalize_phone 跑两次结果一致 |
| 负向验证 | ⬜ 待完成 | 改坏一个函数，测试必须失败 |

---

## 六、下一步

1. 热身：实现 `textutil/word_count`，包外写 6 条断言
2. 实现 `validator/phone.py`：`normalize_phone`（含前缀剥离与幂等）+ `mask_phone`
3. 实现 `validator/password.py`：`validate_password`（返回未满足规则列表）+ `parse_score`（闭区间 [0,100]）
4. 配置 `validator/__init__.py`：4 个函数全部导出
5. 编写 `test_validator.py`：迁移 `expect_error` 模式，每函数 ≥5 条断言
6. 做负向验证：改坏一个函数，贴出失败输出
7. 提交作业，等待 Code Review

---

## 七、打卡

| 项目 | 状态 | 日期 | Review |
|------|------|------|--------|
| textutil 热身包 | ⬜ | — | — |
| T1-5 validator 包 | ⬜ | — | — |
| 负向验证 | ⬜ | — | — |
| 数据库更新 | ⬜ | — | topic #17 in_progress (0.832) |
