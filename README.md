# Conversation Recorder Skill

自动记录用户与 AI 大模型的每轮对话内容，生成结构化日志和日报，便于向领导汇报 AI 辅助工作情况。

## 功能特性

### 自动对话记录

- 每轮对话自动追加到 `conversation-logs/YYYY-MM-DD.md`
- 用户输入**原封不动**保留（blockquote 格式）
- AI 反馈以**关键要点列表**形式总结（2-5 个要点）
- 支持记录不完整对话（用户手动终止、AI 异常中断）

### 场景分类

每轮对话自动识别核心使用场景：

| 分类 | 说明 |
|------|------|
| `快速代码生成与复用` | 生成新代码、脚手架、模板、批量生成 |
| `代码纠错与实时调试排障` | bug 修复、报错排查、异常分析 |
| `代码优化与规范整改` | 性能优化、重构、规范检查、安全修复 |
| `学习赋能与技术落地` | 概念讲解、方案选型、技术调研 |
| `辅助文档与注释产出` | 文档生成、注释、README、报告 |

### 日报生成

触发词：`生成日报` / `今日总结` / `daily report` / `对话日报` / `生成今日日报`

日报包含：
- 概览（日期、对话总数、涉及项目）
- 场景分布统计表
- 对话摘要表（含场景分类列）
- 关键产出汇总
- 经验与改进建议

## 项目结构

```
record-spec/
├── .codebuddy/
│   └── skills/
│       └── conversation-recorder/
│           └── SKILL.md               # Skill 核心指令文件
├── conversation-logs/
│   ├── 2026-04-21.md                  # 按天的对话记录
│   └── reports/
│       └── 2026-04-21-report.md       # 按天的日报
├── openspec/                          # OpenSpec 规范文档
│   ├── project.md
│   ├── changes/
│   ├── design/
│   ├── specs/
│   └── cases/
├── .gitignore
└── README.md
```

## 使用方式

### 方式一：项目级 Skill（推荐）

Skill 文件位于 `.codebuddy/skills/conversation-recorder/SKILL.md`，属于项目级 Skill：

1. 用 CodeBuddy 打开本项目（或包含 `.codebuddy/skills/conversation-recorder/` 目录的任何项目）
2. Skill 自动加载，无需手动操作
3. 每轮对话结束后自动静默记录到 `conversation-logs/` 目录
4. 需要日报时，在对话中输入触发词即可

### 方式二：安装到其他项目

如果想在**其他项目**中也使用此 Skill：

1. 将 `.codebuddy/skills/conversation-recorder/` 整个目录复制到目标项目的 `.codebuddy/skills/` 下
2. 用 CodeBuddy 打开目标项目，Skill 自动生效

### 方式三：安装为用户级 Skill（全局生效）

1. 将 `conversation-recorder/` 目录复制到用户级 Skill 目录：
   - **Windows**: `%USERPROFILE%\.codebuddy\skills\conversation-recorder\`
   - **macOS/Linux**: `~/.codebuddy/skills/conversation-recorder/`
2. 之后在任何项目中打开 CodeBuddy 对话，Skill 都会自动生效

### 方式四：通过 CodeBuddy Rule 自动加载（最省心）

在 CodeBuddy 的 **用户规则（User Rules）** 中添加一条规则，让每次新对话自动加载此 Skill：

1. 打开 CodeBuddy 设置 → **Rules**
2. 添加一条规则：
   ```
   每一次对话都需要使用 conversation-recorder skill记录
   ```
3. 保存后，每次新建对话时 AI 会自动加载 `conversation-recorder` Skill，无需手动输入 `@command://conversation-recorder`

> **适用场景**：搭配方式二或方式三安装 Skill 后，再配置 Rule，实现"安装一次 + 规则一次 = 永久自动记录"。

### 触发词速查

| 功能 | 触发词 |
|------|--------|
| 生成日报 | `生成日报`、`今日总结`、`daily report`、`对话日报`、`生成今日日报` |

> 自动记录无需触发词，Skill 加载后每轮对话自动执行

## 不完整对话记录

支持以下非正常结束场景的记录：

| 场景 | 标记 | 说明 |
|------|------|------|
| 用户手动终止 | `⚠️ 用户终止` | 用户点击"停止生成"后补记 |
| AI 异常中断 | `⚠️ 异常中断` | 网络/超时/token 限制等原因中断后补记 |
| 终止后重新提问 | 先记终止，再记新对话 | 两条记录各自独立编号 |

## 许可

内部项目
