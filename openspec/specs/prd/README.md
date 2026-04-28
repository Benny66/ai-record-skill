# PRD 需求文档投放区

> 将产品需求文档（PRD）放入此目录，AI 会自动识别并生成对应的需求规格说明。

## 使用方式

1. 将 PRD 文档放入本目录（支持 `.md`、`.txt`、`.pdf`、`.docx` 等格式）
2. 对 AI 说"解析 PRD"或"根据 PRD 生成 spec"
3. AI 会自动扫描本目录，识别 PRD 文档并解析
4. 解析后生成对应的功能 spec 到 `specs/<feature-name>/spec.md`

## 支持的文档格式

| 格式 | 说明 |
|------|------|
| `.md` / `.markdown` | Markdown 格式，AI 可直接读取 |
| `.txt` | 纯文本格式，AI 可直接读取 |
| `.pdf` | PDF 格式，AI 借助工具解析 |
| `.docx` | Word 文档，AI 借助工具解析 |
| `.html` | HTML 格式，AI 可直接读取 |

## PRD 文档命名建议

建议按功能模块命名，便于 AI 识别和映射：

```text
specs/prd/
├── README.md                    # 本文件
├── user-auth.md                 # 用户认证模块 PRD
├── order-management.md          # 订单管理模块 PRD
├── payment-flow.pdf             # 支付流程 PRD
└── complete-prd.docx            # 完整 PRD（包含多个功能模块）
```

## 自动识别规则

- AI 在接入模式和日常模式中，都会检查此目录是否有 PRD 文档
- 如果检测到 PRD 文档，AI 会主动提示用户是否需要基于 PRD 生成 spec
- 同一份 PRD 可能覆盖多个功能模块，AI 会按功能拆分生成多个 spec
- PRD 中的需求与代码冲突时：新项目以 PRD 为准，存量项目以代码为准并标注差异

## 处理后的文档

PRD 被解析并生成 spec 后，原始 PRD 文档**保留在此目录不删除**，作为需求溯源的参考。
AI 会在生成的 spec 中标注来源：`> 来源 PRD: specs/prd/xxx.md`
