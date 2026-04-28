# OpenSpec Changes 目录

此目录用于存放**新功能或大改动**的变更提案，不用于存放正式规格。

## 标准结构

```text
changes/
└── feature-name/
    ├── proposal.md          # 变更说明：为什么做、做什么、UML 设计
    ├── specs/               # 验收场景或规格草案
    ├── design.md            # 技术方案（按需）
    ├── tasks.md             # 实现任务清单（按需）
    └── integration-test.md  # 前后端联调自测记录（必须）
```

## 使用规则

- **新功能 / 大改动**：先在 `changes/` 下起 proposal，再确认后同步到 `specs/`
- **proposal 模板**：proposal 必须包含背景与动机、目标、方案概述、影响范围、验收标准等必备章节，详见 RULES.md 5.4 节
- **接口设计先行**：proposal 确认后，先完成接口设计（写入 `design/api-contracts.md`），经前后端双方审查确认后才进入 spec 编写
- **UML 设计**：proposal 中应包含 UML 设计（Mermaid 语法），至少一个时序图描述核心交互流程
- **联调自测**：代码编写完成后必须执行前后端联调自测，结果记录在 `integration-test.md` 中
- **小修改**：可以直接更新对应 `spec.md`
- **轻量状态**：建议在 `proposal.md` 顶部标注 `状态：draft / approved / cancelled`；实现完成后通过移入 `openspec/archive/` 表达已完成
- **归档**：联调自测通过且正式规格落地后，将对应提案移入 `openspec/archive/`

## 不确定时怎么办

如果你不确定某个需求该走 `proposal` 还是直接改 `spec`，或者不确定何时归档，请让 AI 查阅 skill 中的 GUIDE.md。
