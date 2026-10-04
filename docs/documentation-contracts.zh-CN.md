# 文档完整性契约

[English](documentation-contracts.md) | 简体中文

`documentation/` 是可选的工程信息完整性分类，与
[规范模型](specification-model.zh-CN.md)中的语言、框架等层并列。
它落实 [ESP-0014](../proposals/0014_documentation-integrity-contracts.md) 的方向，
不新增写作 Skill、渲染器或审批流程。

## 两份规范，各自按需选择

| 规范 | 负责内容 | 选择与依赖 |
| --- | --- | --- |
| [Technical Documentation](../specification/documentation/technical-documentation.md) | 状态、证据、命令效果、术语归属、现状与历史 | 显式选择；依赖 `core/semantic-naming` |
| [Derived Explanations](../specification/documentation/derived-explanations.md) | 派生内容的权限、来源、关键信息的等价获取 | 显式选择；依赖 Technical Documentation |

普通技术文档可以只选择第一份。选择派生解释规范会补齐声明的依赖，目录嵌套不构成
隐式继承。两份规范初始版本都是 `0.1.0`、Development，自动执行级别均为 Advisory。
现有规范不因此升级、弱化或改变。版本、范围和摘要以 [Catalog](../catalog.json) 为准。

Google-informed 的组织方法和 STE-inspired 的表达建议继续留在消费者的写作指导里。
项目仍拥有自己的语言、目录、标题、术语和发布权限。文风建议不能修改源事实，也不能
静默豁免已经采用的规范义务。不声称 Google、ASD 或 W3C 背书，也不宣称完整标准合规。

## 路径只是候选，任务意图决定适用性

通用文档规范覆盖 Markdown、MDX、reStructuredText、AsciiDoc 和直接编写的 HTML。
派生解释规范使用较宽的 `**/*`，以便发现生成器源码和媒体配套文件；无关业务代码、
纯装饰修改不因此受约束。文件匹配不等于自动安装，更不等于全文激活。

二进制媒体不会被当作规范原文解析。仓库外的临时 HTML 或视频也不会自动获得路径门禁
覆盖，需要通过消费者已有任务机制明确审阅生成器和输出。本次不改变 Router 协议或
Explore 模式。

## 检查工程含义，而不是制造新的形式门禁

每条要求都有独立 ID、激活说明、精确上下文依赖、验证方式和证据说明。复用现有 PR、
评审和测试记录；不要求另一套审批、固定来源元数据格式、英文句长检查或历史文档改写。

摘要校验能确认字节，不能证明事实或授权。示例题目不是已经执行的模型评估。视频源码包
不是已经渲染、加字幕且完成可访问性检查的视频。缺少工具或证据时保留缺口，不编造通过。

[评审场景](../tests/fixtures/documentation-contract/review-cases.json)包含八组正反案例。
仓库测试检查结构和错误元数据的拒绝行为；独立消费者 CI 使用固定 RF 提交检查实际选择、
依赖和 capsule。两者都不证明任意文档的语义正确性或可访问性。

## 发布与采用分开

本次集成记入 Unreleased。Catalog schema 保持 1；新 Catalog 版本在独立发布 PR 中按
[发布流程](../RELEASING.md)确定。本次不创建或移动 tag。工作树尚保留旧 Catalog 版本号，
不意味着同名旧发布 tag 含有新增规范。

新的固定版本发布后，维护者再通过消费者的 preview/apply 明确选择可选 ID。RF 默认
版本升级需要另一个消费者变更；既有 lock、本地项目、历史决定和已分享视图不会自动更新。

## 贡献边界

沿用 [贡献流程](../CONTRIBUTING.md)和正式模板。共同语义引用上游契约，不再复制。
语气、英文词表、目录结构和渲染器实现不属于这个分类。跨语言不意味着必须归入 Core。
新增类别、schema 字段或提升自动执行级别，需要单独评审与证据。
