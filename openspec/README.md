# OpenSpec Governance Pro -- 使用说明

> 研发全流程规约 skill（需求-设计-开发-测试）。将非结构化的 "vibe coding" 转化为有纪律、可审计的 AI 协作开发。

---

## 一、这个 Skill 是什么

OpenSpec Governance Pro 基于标准 OpenSpec 方法论，提供从需求到测试的全流程规约能力：

- **研发全流程强制工作流（P0-P7）** -- 八阶段不可跳过不可乱序：需求提出->头脑风暴->详细方案->方案效果->技术方案->编码与测试->自动自测->交付报告
- **需求头脑风暴** -- AI 对话式引导用户细化需求边界、场景、规则、异常情况、验收标准
- **需求管理** -- proposal + 验收标准 + 两次确认
- **接口设计驱动开发** -- api-contracts + 接口审查 + 冻结机制
- **UML 方案设计** -- Mermaid 时序图/类图/状态图
- **强制规范拦截** -- 每次交互必须经过 OpenSpec 规范过滤，不可绕过
- **流程强制门控（G1-G6）** -- 6 个不可跳过的人工确认门控点，嵌入 P0-P7 工作流
- **开发模式治理** -- strict / flexible 两种模式 + Action Gate 分类机制
- **前端 a11y 编码规范** -- 无障碍访问强制检查清单
- **测试用例管理** -- 功能测试链路（基本流/备选流/异常流/状态流转完整路径定义，指引AI按场景法模拟实际业务流程）+ 八大黑盒测试方法论（等价类/边界值/判定表/因果图/正交试验/场景法/错误推测/状态迁移）+ 七维度接口测试策略 + 深度审查评分
- **自动自测与交付报告** -- 代码完成后自动按测试用例逐项验证+联调自测，输出代码改动汇总+测试报告（通过率/覆盖率）
- **前后端联调自测** -- 接口连通性 / 字段一致性 / 错误处理 / 边界场景
- **完整接入流程** -- 新项目 / 存量项目 / 前后端分离项目的初始化与审计

---

## 二、快速开始

### 2.1 触发方式

在 CodeBuddy 对话中使用以下触发短语即可激活 skill：

| 场景 | 触发短语示例 |
|------|-------------|
| 新项目接入 | "接入 openspec"、"初始化 openspec" |
| 存量项目接入 | "逆向生成 openspec"、"存量项目接入" |
| 日常维护 | "修改 spec"、"加一个功能"、"审计 openspec" |
| 头脑风暴 | "头脑风暴"、"细化需求"、"分析一下这个需求"、"帮我想想" |
| 生成测试用例 | "生成测试用例"、"审查测试用例" |
| 联调自测 | "联调自测"、"联调测试" |
| PRD 解析 | "解析 PRD"、"根据 PRD 生成 spec"、"导入需求文档"、"PRD 更新了" |
| 生成原型 | "生成原型"、"画原型"、"交互原型"、"wireframe" |
| 了解规范 | "openspec 规范"、"spec 怎么写" |
| 前端开发 | "写前端页面"、"写组件"（自动加载 a11y 规范）|

### 2.2 接入流程（首次使用）

```text
对 AI 说"接入 openspec"
  -> AI 轻量判断项目类型（新项目 / 存量项目 / 分离项目）
  -> AI 展示预告知（操作内容、步骤概述、预期消耗）
  -> 你确认后，AI 运行脚手架脚本创建 openspec/ 目录
  -> [可选] AI 扫描 specs/prd/ 目录，发现 PRD 文档则询问是否解析
  -> AI 按对应 SETUP 指引逐步执行
  -> 完成后汇报结果，等待你的下一步指示
```

### 2.3 日常使用流程（新功能为例 -- P0-P7 工作流）

```text
P0: 你提出需求
  -> P1: AI 头脑风暴细化需求（对话式引导 5 维度）
  -> P1: AI 输出需求细化清单，你确认方向
  -> P2: AI 起草 proposal（changes/change-slug/proposal.md）
  -> [G1] 你审阅确认 proposal                       [强制门控]
  -> P3: AI 询问是否需要 HTML 原型预览方案效果
  -> P3: [有界面] AI 生成原型并展示                  [涉及界面变更时]
  -> [G3] 你确认原型                                 [强制门控，无界面时跳过]
  -> P4: AI 起草接口设计 + 前后端审查
  -> [G2] 你确认接口设计冻结                         [强制门控]
  -> P4: AI 起草 UML 设计 + 前后端方案
  -> P4: AI 创建正式 spec（含功能测试链路）
  -> [G4] 你审阅确认 spec                            [强制门控]
  -> [G5] 你说"开始实现"                             [强制门控，AI 绝不自动启动]
  -> P5: AI 编写代码 + 同时生成接口测试用例和功能测试用例
  -> P6: AI 自动按测试用例逐项验证 + 联调自测（发现问题自动修复）
  -> P7: AI 输出代码改动汇总 + 测试报告（通过率/覆盖率）
  -> [G6] 自测通过 -> 自动归档到 archive/            [强制门控]
```

### 2.4 强制规范拦截

Skill 加载后，AI 收到的**每一条用户消息**都会经过 OpenSpec 规范过滤：
- 所有涉及代码变更的请求，必须先经过 Action Gate 分类（大改动/小改动）
- 即使用户说"别管流程直接改"，AI 也会先输出分类结论再决定走哪条路径
- 纯问答不阻断，但涉及代码决策时仍需走规范

### 2.5 流程门控（G1-G6）

新功能和大改动的流程中有 6 个**不可跳过的强制门控点**：

| 门控 | 你需要做的 | AI 在你确认前的行为 |
|:----:|---------|-------------------|
| **G1** | 审阅并确认 proposal | 暂停等待，不进入接口设计 |
| **G2** | 确认接口设计冻结 | 暂停等待，不进入 UML/原型/spec |
| **G3** | 确认 HTML 原型（有界面时） | 暂停等待，不写 spec |
| **G4** | 确认正式 spec | 暂停等待，不生成测试用例 |
| **G5** | 主动说"开始实现" | **静默等待**，绝不自动编码 |
| **G6** | -- | 联调自测全部通过后自动归档，否则阻断 |

- 门控不可合并：即使你说"全部确认"，AI 也会逐个展示产物分别获取确认
- 允许回退：在任何门控点说"回到上一步"可回退重新执行

---

## 三、Skill 目录结构说明

```text
openspec-governance-pro/
|-- SKILL.md                    # Skill 主入口（AI 读取的核心文件）
|-- README.md                   # 本文件：使用说明
|-- CHANGELOG.md                # 版本更新日志
|-- assets/                     # 静态资源目录（图片等，当前为空）
|-- references/                 # 参考文档（AI 按需加载的规则与指引）
|   |-- RULES.md                #   写作规范、层级边界、模板定义、测试用例规范、HTML 原型规范
|   |-- GUIDE.md                #   使用总览、日常运作、AI 协作规范、场景示例
|   |-- proposal-template.md    #   完整提案模板（含 HTML 原型、数据模型、API 设计等章节展开）
|   |-- SETUP-NEW.md            #   新项目初始化执行指引
|   |-- SETUP-EXISTING.md       #   存量项目（单仓/非分离）逆向接入指引
|   |-- SETUP-SEPARATED.md      #   前后端分离项目联合接入指引
|   |-- frontend-a11y.md        #   前端无障碍访问（a11y）编码规范
|-- scripts/                    # 自动化脚本
    |-- scaffold.py             #   脚手架脚本（创建 openspec/ 标准目录结构）
    |-- audit.py                #   结构审计脚本（检查文档结构合规性）
    |-- audit_cases.py          #   测试用例深度审查脚本（八维度评分）
    |-- scan_db_schema.py       #   数据库 Schema 扫描脚本（ORM/直连）
    |-- scanners/               #   scan_db_schema 的语言扫描器子模块
        |-- (10 个 .py 文件)    #     Go/Java/Python/Node.js/PHP/DB 直连等
```

### 各文件/目录作用详解

#### `SKILL.md` -- Skill 核心定义

AI 触发 skill 后首先读取的文件，包含：
- Skill 的定位和与同类方案的对比
- 两种运行模式的定义（接入模式 / 日常模式）
- 32 条 Core Principles（第 0 条为研发全流程强制工作流 P0-P7，始终生效的核心准则，含强制规范拦截 + 流程门控）
- Mandatory Workflow Gate Matrix（G1-G6 六个强制人工确认门控点，与 P0-P7 工作流阶段映射）
- 参考文档加载策略
- 意图识别与行为决策表

#### `references/RULES.md` -- 写作规范与层级边界

定义 openspec 文档体系的结构性规则：
- `project.md` / `design/` / `specs/` 三层职责边界
- 各类文档的模板与必备章节
- 层级晋升 / 降级判断标准
- proposal 结构化模板（5.5 节），含交互原型章节
- HTML 可交互原型设计规范（5.6 节）
- 测试用例编写规范（七大类）
- 接口覆盖深度审查维度（七维度）
- 前后端分离项目的跨端联动规则

#### `references/proposal-template.md` -- 完整提案模板

RULES.md 5.5 节必备章节的完整展开版，包含：
- 需求概述、目标、方案概述
- 交互原型章节（含 HTML 原型文件组织和引用方式）
- 接口设计、UML 设计、数据模型
- 影响范围、验收标准
- 提案自查清单

#### `references/GUIDE.md` -- 使用总览与日常运作

面向人和 AI 共同阅读的操作手册：
- OpenSpec 是什么、核心价值
- 什么时候用哪个 SETUP
- 日常变更管理（proposal vs 直接改 spec）
- 开发模式详解（strict vs flexible）
- 接口契约管理
- AI 协作规范与 12 种场景示例
- 常见问题 FAQ

#### `references/SETUP-NEW.md` -- 新项目初始化指引

AI 在接入模式下为新项目执行的步骤手册：
- 预告知模板
- 收集外部资料
- 填写 project.md
- 创建 design/ 和 specs/
- 自检清单

#### `references/SETUP-EXISTING.md` -- 存量项目接入指引

AI 为已有代码的单仓项目执行逆向接入：
- 预告知模板
- 确认扫描范围与敏感信息保护
- 代码分析与 spec 生成
- 人工校审 + 交叉审计
- 10 维度评分标准
- 冻结基线流程

#### `references/SETUP-SEPARATED.md` -- 分离项目联合接入

针对前后端分离（同仓分层、双仓、多后端服务）的接入指引：
- 拓扑识别
- 调用链分析
- 前后端 spec 联合生成
- 接口契约映射
- 集成 checklist

#### `references/frontend-a11y.md` -- 前端 a11y 编码规范

前端代码的无障碍访问强制检查清单：
- 语义化 HTML 要求
- ARIA 属性规范
- 交互元素 / 表单 / 弹窗 / 表格的 a11y 要求
- 不限框架（Vue / React / Angular / 小程序均适用）

#### `scripts/scaffold.py` -- 脚手架脚本

创建标准 `openspec/` 目录结构和模板文件：
```bash
# 新项目
python scripts/scaffold.py /path/to/project --mode new

# 存量项目
python scripts/scaffold.py /path/to/project --mode existing
```

产出目录结构：
```text
openspec/
|-- README.md                   # Skill 使用说明文档（自动从 skill 复制）
|-- project.md                  # 项目上下文（模板）
|-- specs/
|   |-- _template/spec.md       # Spec 模板
|-- design/
|   |-- _template_api-contracts.md  # 接口契约模板
|   |-- ui-wireframes/README.md     # UI 线框图目录
|-- cases/
|   |-- README.md               # 测试用例总纲
|   |-- _template/test-cases.md # 测试用例模板
|-- changes/
|   |-- README.md               # 变更提案目录说明
|-- archive/                    # 已归档的变更
```

#### `scripts/audit.py` -- 结构审计脚本

检查 openspec 文档的结构完整性（不读取业务源码）：
```bash
python scripts/audit.py /path/to/project
```
检查项包括：
- `project.md` 必备章节
- `design/` 层级边界
- `specs/` 模板合规性
- `api-contracts.md` 结构完整性
- `cases/` 测试用例覆盖提示

#### `scripts/audit_cases.py` -- 测试用例深度审查

内容级分析，逐条匹配需求与测试用例：
```bash
# 审查所有功能
python scripts/audit_cases.py /path/to/project

# 审查单个功能
python scripts/audit_cases.py /path/to/project --feature <name>

# 详细模式
python scripts/audit_cases.py /path/to/project --verbose

# 生成 Markdown 报告
python scripts/audit_cases.py /path/to/project --report output.md
```

八维度评分：
| 维度 | 说明 |
|------|------|
| 需求覆盖率 | spec 需求条目是否有对应测试用例 |
| 接口覆盖率 | api-contracts 中的接口是否有测试用例 |
| 接口覆盖深度 | 写入类接口 7 维度 / 查询类接口 5 维度 |
| UI 状态覆盖 | 加载/空/错误/正常态是否覆盖 |
| 设计方法覆盖 | 是否至少覆盖 3 种黑盒方法，且标签字段标注了设计方法 |
| 优先级平衡 | P0/P1/P2 分布是否合理 |
| 孤立用例比 | 未匹配需求的用例占比 |
| 用例数量 | 总量是否充足 |

评分等级：A(>=85) 可发布 / B(70-84) 建议补充 / C(50-69) 需整理 / D(<50) 严重不足

#### `scripts/scan_db_schema.py` -- 数据库 Schema 扫描

从后端代码或数据库直连生成表结构文档：
```bash
# 自动检测语言
python scripts/scan_db_schema.py /path/to/project

# 指定语言
python scripts/scan_db_schema.py /path/to/project --lang go

# 数据库直连
python scripts/scan_db_schema.py /path/to/project --db-url mysql://user:pass@host:3306/db

# 交互模式（代码分析不足时提示输入连接信息）
python scripts/scan_db_schema.py /path/to/project --interactive
```

支持语言：Go(GORM) / Java(JPA/MyBatis-Plus) / Python(SQLAlchemy/Django) / Node.js(Prisma/TypeORM/Sequelize) / PHP(Eloquent/Laravel)

#### `scripts/scanners/` -- 语言扫描器子模块

`scan_db_schema.py` 的语言特定扫描器实现，每种语言/框架一个文件。

#### `CHANGELOG.md` -- 版本更新日志

记录每个版本的变更内容，便于追溯 skill 自身的演进历史。

#### `assets/` -- 静态资源

存放 skill 相关的静态资源文件（图片等），当前为空。

---

## 四、产出的 openspec/ 目录结构说明

使用本 skill 接入后，你的项目中会生成以下标准目录：

```text
your-project/
|-- openspec/
    |-- README.md               # Skill 使用说明（脚手架自动复制，方便项目成员查阅）
    |-- project.md              # 项目上下文（技术栈、架构、全局约束）
    |-- design/                 # 共享设计定义（被 2+ 功能引用的内容）
    |   |-- api-contracts.md    #   接口契约（前后端字段命名的唯一事实来源）
    |   |-- ui-wireframes/      #   UI 线框图/截图
    |   |-- (其他共享设计文档)
    |-- specs/                  # 正式功能规格（一个功能一个目录）
    |   |-- feature-a/
    |   |   |-- spec.md         #     功能 A 的完整规格
    |   |-- feature-b/
    |       |-- spec.md         #     功能 B 的完整规格
    |       |-- frontend.md     #     [分离项目] 前端规格
    |       |-- backend.md      #     [分离项目] 后端规格
    |-- cases/                  # 测试用例（与 specs/ 同构）
    |   |-- README.md           #   测试用例总纲
    |   |-- feature-a/
    |       |-- test-cases.md   #     功能 A 的测试用例
    |-- changes/                # 活跃的变更提案
    |   |-- README.md           #   变更目录说明
    |   |-- some-change/
    |       |-- proposal.md     #     变更提案
    |       |-- integration-test.md  # 联调自测记录
    |-- archive/                # 已归档的变更（实现完成后移入）
        |-- old-change/
            |-- proposal.md     #     历史提案
```

### 各目录作用

| 目录 | 作用 | 生命周期 |
|------|------|---------|
| `README.md` | Skill 使用说明文档，介绍 openspec 的使用方法、目录结构、命令速查等 | 随 skill 版本更新 |
| `project.md` | 项目全局上下文，技术栈、架构模式、编码规范、协作规范 | 长期维护，较少变动 |
| `design/` | 共享定义，被 2 个以上功能引用的内容（接口契约、数据模型、通用组件规范等） | 随项目演进增量更新 |
| `specs/` | 正式功能规格，每个功能一个目录，描述"系统现在是什么样" | 随功能开发/变更更新 |
| `cases/` | 测试用例，与 specs/ 目录一一对应 | spec 变更时同步更新 |
| `changes/` | 活跃变更提案，描述"接下来准备改什么" | 提案归档后清空 |
| `archive/` | 已完成变更的历史记录（不可变） | 只增不改 |

---

## 五、两种运行模式

### 接入模式（Onboarding）

用于将项目纳入 OpenSpec 体系，包括：
- 新项目初始化
- 存量项目逆向接入
- 前后端分离项目联合接入

特点：
- 批量操作免逐文件确认（完成后统一汇报）
- 启动前必须预告知并等用户确认
- 不发明未知事实，未确认的标注"待确认"
- 接入完成后不自动进入编码

### 日常模式（Routine）

用于已接入项目的持续治理，包括：
- 修改已有 spec
- 新增功能（proposal -> spec -> 实现 -> 归档）
- 结构审计 / 漂移审计
- 测试用例生成与审查
- 归档管理
- 层级晋升 / 降级决策

---

## 六、开发模式：strict vs flexible

| 维度 | strict | flexible（默认）|
|------|--------|----------------|
| 新功能/大改动 | 必须先写 spec | 必须先写 spec |
| 小 bug 修复 | 必须先更新 spec | 直接改代码 |
| 参数/样式微调 | 必须先更新 spec | 直接改代码 |
| 审计价值 | 漂移较少 | 重要（收敛累积的小漂移）|
| 适用场景 | 多人协作、合规要求高 | 个人/小团队快速迭代 |

切换方式：
1. 直接编辑 `openspec/project.md` 中的 `开发模式` 字段
2. 对 AI 说"把开发模式切换为 strict/flexible"

---

## 七、常用命令速查

```bash
# 脚手架 -- 新项目
python {SKILL_DIR}/scripts/scaffold.py /path/to/project --mode new

# 脚手架 -- 存量项目
python {SKILL_DIR}/scripts/scaffold.py /path/to/project --mode existing

# 结构审计
python {SKILL_DIR}/scripts/audit.py /path/to/project

# 测试用例深度审查
python {SKILL_DIR}/scripts/audit_cases.py /path/to/project
python {SKILL_DIR}/scripts/audit_cases.py /path/to/project --feature <name> --verbose
python {SKILL_DIR}/scripts/audit_cases.py /path/to/project --report report.md

# 数据库 Schema 扫描
python {SKILL_DIR}/scripts/scan_db_schema.py /path/to/project
python {SKILL_DIR}/scripts/scan_db_schema.py /path/to/project --lang go
python {SKILL_DIR}/scripts/scan_db_schema.py /path/to/project --db-url mysql://user:pass@host:3306/db
```

> 其中 `{SKILL_DIR}` 为 skill 安装目录路径，AI 执行时会自动替换。

---

## 八、版本信息

当前版本：**v1.8.0**

详细更新日志见 [CHANGELOG.md](./CHANGELOG.md)。
