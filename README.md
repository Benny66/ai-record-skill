# Conversation Recorder — AI 协作开发经验引擎

将碎片化的 AI 对话转化为可积累、可检索、可复用的开发经验。

## 三层知识架构

```
第一层：对话原始记录（每轮自动）
     ↓ 生成日报时回顾式提炼
第二层：日报 + 经验卡片（每日沉淀）
     ↓ 生成周报/月报时蒸馏
第三层：经验手册（长期精华，去重合并）
```

## 功能特性

### 自动对话记录
- 每轮对话自动追加到 `conversation-logs/YYYY-MM-DD.md`
- 用户输入**原封不动**保留，AI 反馈以**关键要点列表**总结
- 每轮自动识别 5 种使用场景分类
- 支持记录不完整对话（用户终止、AI 异常中断）

### 场景分类

| 分类 | 说明 |
|------|------|
| `快速代码生成与复用` | 生成新代码、脚手架、模板、批量生成 |
| `代码纠错与实时调试排障` | bug 修复、报错排查、异常分析 |
| `代码优化与规范整改` | 性能优化、重构、规范检查、安全修复 |
| `学习赋能与技术落地` | 概念讲解、方案选型、技术调研 |
| `辅助文档与注释产出` | 文档生成、注释、README、报告 |

### 经验卡片（日报内）
生成日报时 AI **回顾式提炼**当日经验，4 大类 12 种经验类型：

| 大类 | 类型 |
|------|------|
| 提示词与对话策略 | 提示词技巧、Token优化、上下文管理、迭代策略 |
| 代码开发经验 | 踩坑记录、技术决策、开发最佳实践 |
| AI 风险认知 | 幻觉识别、认知偏差、安全防范 |
| 工具与流程 | 工具技巧、流程优化 |

### 经验手册
长期积累的精华知识库（`conversation-logs/experience-handbook.md`），支持：
- 从日报经验卡片自动蒸馏
- 去重合并、星级升降、淘汰归档
- 关键词搜索、统计概览

### 报告体系

| 报告 | 触发词 | 内容 |
|------|--------|------|
| 日报 | `生成日报`、`今日总结` | 场景分布 + 对话摘要 + 关键产出 + 经验卡片 |
| 周报 | `生成周报`、`本周总结` | 趋势分析 + 经验精选 + AI使用效率分析 |
| 月报 | `生成月报`、`本月总结` | 月度趋势 + Top10经验 + 改进计划 |

### 经验推荐
对话过程中如命中经验手册中的高星级条目，在回复末尾自动提示。

## 项目结构

```
record-spec/
├── .codebuddy/
│   └── skills/
│       └── conversation-recorder/
│           ├── SKILL.md                   # Skill 核心指令文件
│           └── scripts/
│               ├── report.py              # 报告数据生成（日报/周报/月报）
│               ├── experience.py          # 经验手册管理（搜索/统计/去重）
│               └── stats.py              # 跨天统计分析
├── conversation-logs/
│   ├── 2026-04-28.md                      # 按天的对话记录
│   ├── experience-handbook.md             # 经验手册（长期积累）
│   └── reports/
│       ├── 2026-04-28-report.md           # 日报（含经验卡片）
│       ├── 2026-W18-weekly.md             # 周报
│       └── 2026-04-monthly.md             # 月报
├── openspec/                              # OpenSpec 规范文档
├── .gitignore
└── README.md
```

## 使用方式

### 方式一：项目级 Skill（推荐）

1. 用 CodeBuddy 打开本项目
2. Skill 自动加载，每轮对话自动静默记录
3. 需要日报时输入"生成日报"

### 方式二：安装到其他项目

将 `.codebuddy/skills/conversation-recorder/` 复制到目标项目的 `.codebuddy/skills/` 下。

### 方式三：用户级 Skill（全局生效）

将 `conversation-recorder/` 复制到：
- **Windows**: `%USERPROFILE%\.codebuddy\skills\conversation-recorder\`
- **macOS/Linux**: `~/.codebuddy/skills/conversation-recorder/`

### 方式四：通过 CodeBuddy Rule 自动加载（最省心）

CodeBuddy 设置 → Rules → 添加：
```
每一次对话都需要使用 conversation-recorder skill记录
```

搭配方式二或三，实现"安装一次 + 规则一次 = 永久自动记录"。

## 触发词速查

| 功能 | 触发词 |
|------|--------|
| 日报 | `生成日报`、`今日总结`、`daily report`、`对话日报`、`生成今日日报` |
| 周报 | `生成周报`、`weekly report`、`本周总结` |
| 月报 | `生成月报`、`monthly report`、`本月总结` |
| 更新经验 | `更新经验手册`、`整理经验`、`沉淀经验` |
| 查看经验 | `查看经验`、`经验手册`、`有什么经验` |
| 搜索经验 | `搜索经验 {关键词}` |

## 脚本工具

```bash
# 日报数据
python .codebuddy/skills/conversation-recorder/scripts/report.py . --type daily

# 周报数据
python .codebuddy/skills/conversation-recorder/scripts/report.py . --type weekly

# 经验搜索
python .codebuddy/skills/conversation-recorder/scripts/experience.py . search --keyword "token"

# 经验统计
python .codebuddy/skills/conversation-recorder/scripts/experience.py . stats

# 跨天统计
python .codebuddy/skills/conversation-recorder/scripts/stats.py . --from 2026-04-21 --to 2026-04-28
```

## 许可

内部项目
