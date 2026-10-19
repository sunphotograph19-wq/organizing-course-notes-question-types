# 大学课程笔记整理（侧重题型版）

一个把大学课程 PPT、PDF 和习题整理为中文 Obsidian 复习笔记的 Agent Skill。重点不是复述课件，而是帮助读者**识别题型、选择方法、完整求解、避免常见错误**。

Skill 标识：`organizing-course-notes-question-types`。

## 输出规则

- 每章一个文件夹，每节一个独立 Markdown 文件：左侧文件列表直接选节。
- 节内保留真实 Markdown 标题：右侧 Obsidian 内置大纲直接跳到概念、重点题型或具体题型。
- H1 为章名，H2 为节名；每节固定且仅有两个 H3：“一、概念”和“二、重点题型”；各题型为 H4。
- 每个题型包含：题型特征、解题方法、核心公式、典型例题、易错点。
- 优先使用课件原例题，保留来源与完整解题过程，不编造条件或页码。
- 首次出现的必要术语就近解释；公式写明条件，重点有材料依据。
- 支持 LaTeX、原生 Callout、Wikilinks 和本地附件，不依赖第三方插件。
- 对概率论额外检查端点、支持集、参数化、独立性、近似条件及变量变换分支。
- 用户要求双端导入时，按真实仓库位置复制并校验，不更改其他课程及插件配置。

## 仓库内容

```text
organizing-course-notes-question-types/
├── SKILL.md
├── README.md
├── templates/
│   ├── Obsidian-分节笔记模板.md
│   └── Obsidian-章节导航模板.md
└── scripts/
    └── validate_notes.py
```

两个模板与脚本是 Skill 的资源，安装和移动时保留整个目录，不能只复制 `SKILL.md`。

## 安装到 Amp

在已安装 Amp CLI 的电脑上运行：

```sh
amp skill add --global sunphotograph19-wq/organizing-course-notes-question-types
```

这会安装到当前电脑的个人全局 Skill 目录，不局限于当前项目。其他电脑需单独安装；若需账号级跨设备使用，应按 Amp 的个人 User Skills 仓库流程导入并推送。不要把本机全局安装称为已经发布到账号级个人仓库。

安装后在 Amp 刷新 Skills 或开启新会话。也可以将整个目录放进某项目的 `.agents/skills/organizing-course-notes-question-types/`，只供该项目使用。

## 如何调用

把课程资料放入工作目录，然后提出：

> 使用 `organizing-course-notes-question-types`（侧重题型版）整理这些概率论 PPT 和习题。每章建文件夹，每节单独成文；节内只设“概念”和“重点题型”两个固定部分。解释新术语，按题型写清识别方法、解题步骤、公式条件、原题完整解答和易错点。根据我提供的同课程学习安排强调重点，保留大纲标题，导入指定的 Obsidian 仓库。

未提供学习安排时，Skill 不应假装掌握考试范围。未连接平板或未完成复制时，也不应声称已完成双端同步。

## 结构检查

需要 Python 3.9 或更新版本，无第三方依赖：

```sh
python scripts/validate_notes.py "你的课程笔记目录"
```

脚本识别类似 `2.1 节名.md` 的分节文件，检查标题层级、五项字段、模板占位符和公式定界符，失败时返回非零退出码。导航与资料索引不是分节文件，不受固定两部分规则限制。

**脚本不验证数学正确性、原始资料覆盖、链接可达、公式渲染或同步结果。** 这些仍须按 Skill 工作流独立检查。内容无法可靠读取时应说明缺口，不以结构通过代替整理完成。

## 隐私与范围

仓库只保存 Skill、空白模板和结构校验脚本，不包含课程 PPT、完整课程笔记、学生信息、设备路径、API Key 或插件配置。本 Skill 不会自动上传资料或修改设备；具体文件操作仍由 Agent 按用户授权执行。
