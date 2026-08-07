[English](README_EN.md) | 中文

# Draw.io 图表生成技能

跨平台的 draw.io (diagrams.net) 图表生成技能，适用于 Claude Code、codex、zcode、workbuddy、OpenClaw 等各类 AI 编程 Agent。Agent 直接生成 drawio XML，校验后通过 CLI 导出图片；没有桌面版时自动降级为 draw.io 官网打开链接。

技能本身是纯 Markdown + 两个零依赖脚本，不绑定任何特定 Agent 的运行时。

## 安装

向你的 AI 编程 Agent 发送以下提示词：

```
帮我安装这个skill：https://github.com/bruc3van/bruce-drawio
```

Agent 会自动克隆仓库并完成配置。

如果你的 Agent 不支持自动安装，手动克隆到对应的 skills 目录即可：

| Agent                                   | skills 目录         |
| --------------------------------------- | ------------------- |
| Claude Code                             | `~/.claude/skills/` |
| codex / zcode / workbuddy / OpenClaw 等 | `~/.agents/skills/` |

```bash
# Claude Code
git clone https://github.com/bruc3van/bruce-drawio ~/.claude/skills/bruce-drawio

# 其他 Agent
git clone https://github.com/bruc3van/bruce-drawio ~/.agents/skills/bruce-drawio
```

Windows 上把 `~` 换成 `$HOME`（PowerShell）或 `%USERPROFILE%`（cmd）。技能没有构建步骤，克隆完就能用。

## 支持的图表类型

| 类型       | 说明                         | 触发词示例         |
| ---------- | ---------------------------- | ------------------ |
| 流程图     | 业务流程、审批流程、算法逻辑 | "画一个流程图"     |
| 架构图     | 系统架构、微服务、部署架构   | "画一个架构图"     |
| UML 时序图 | 组件之间的交互时序           | "画一个时序图"     |
| UML 类图   | 类关系、继承结构             | "画一个类图"       |
| ER 图      | 数据库设计、实体关系         | "画一个 ER 图"     |
| 思维导图   | 头脑风暴、知识梳理           | "画一个思维导图"   |
| 网络拓扑图 | 网络架构、设备连接           | "画一个网络拓扑图" |

## 平台支持

draw.io 桌面版仅用于导出图片，属于可选项；不安装也能通过[在浏览器打开](#在浏览器打开)查看和编辑图表。

| 平台    | 安装命令                       | 包管理器            |
| ------- | ------------------------------ | ------------------- |
| macOS   | `brew install --cask drawio` | Homebrew            |
| Windows | `winget install JGraph.Draw` | winget / Chocolatey |
| Linux   | `snap install drawio`        | snap / 手动安装     |

所有平台也支持从 [draw.io releases](https://github.com/jgraph/drawio-desktop/releases) 手动下载安装。

Linux 无头环境（容器、CI）下导出需要 `xvfb-run -a` 并加 `--no-sandbox`，Agent 会自动处理。

## 工作流程

1. 用户描述想要的图表
2. Agent 判断图表类型和关键元素
3. Agent 参照对应示例直接生成完整的 drawio XML
4. 应用布局规则（坐标、间距、尺寸、单元格顺序）
5. 保存 `.drawio` 并跑校验脚本，错误清零
6. 通过 CLI 导出为 PNG/SVG/PDF（未安装桌面版则跳过）
7. 需要时生成 draw.io 官网打开链接
8. 交付图片和源文件路径

## XML 校验

保存后 Agent 会跑一遍 `scripts/validate_drawio.py`，把靠肉眼复读必然会漏的问题机械地查出来：

```bash
python scripts/validate_drawio.py diagram.drawio
```

| 级别  | 检查项                                                                                              |
| ----- | --------------------------------------------------------------------------------------------------- |
| ERROR | XML 不良构、ID 重复、缺根节点、`parent`/`source`/`target` 指向不存在的节点、缺 `as="geometry"`、`value` 里的字面 `\n`、节点部分重叠 |
| WARN  | 缺 `whiteSpace=wrap`/`html=1`、`fontSize` 小于 12、小数坐标、内容超出 `pageWidth`/`pageHeight`   |

有 ERROR 时退出码为 1。重叠检测只报**部分重叠**——完全包含是分层块状风格表达嵌套的方式，不算问题。

## 在浏览器打开

Agent 可以给出一条 `https://app.diagrams.net/?title=xxx#R...` 链接，点开就是这张图，能继续编辑或导出——**不需要安装桌面版，也不需要注册登录**。

原理：图表 XML 经过 `encodeURIComponent → deflate raw → base64` 后放进 URL 的 `#R` 片段。片段部分不会发送给服务器，由 draw.io 前端在浏览器本地解码，因此**图表内容不会上传到任何服务器**。

### 什么时候会给链接

这条链接是**兜底和按需**，不是每张图都附赠：

| 情况                | 行为                                                   |
| ------------------- | ------------------------------------------------------ |
| 导出成功            | 不主动给，只在结尾提一句「需要在线打开就说一声」       |
| 没装桌面版/导出失败 | 链接作为主交付——这也是它存在的意义：任何环境都能看到图 |
| 你开口要            | 立刻生成（"打开看看"、"我想改一下"、"发给同事"）       |

### ⚠️ 链接是副本，不是本地文件的入口

`#R` 链接把整张图**复制**进了 URL，draw.io 打开的是一个和磁盘文件毫无关联的新文件。**在浏览器里的修改不会同步回本地 `.drawio`。**

改完有两条路：

- 在 draw.io 里 **File → Save as → Device** 下载，覆盖本地的 `.drawio`
- 或者直接告诉 Agent 要改什么，让它改本地文件再重新导出

如果装了桌面版，想继续编辑更推荐直接打开本地文件（`draw.io diagram.drawio`），改动原地保存，没有分叉问题。从官网用 **File → Open From → Device** 打开本地文件也同样没有这个问题。

### 脚本用法

链接由 `scripts/` 下的脚本生成，Python / Node 二选一即可：

```bash
python scripts/open_in_drawio.py diagram.drawio          # 仅打印链接
python scripts/open_in_drawio.py diagram.drawio --open   # 打印并直接打开浏览器
node   scripts/open_in_drawio.js diagram.drawio          # 没有 Python 时的等价实现
```

| 参数           | 说明                                                     |
| -------------- | -------------------------------------------------------- |
| 无参数         | 只打印链接（默认行为）                                   |
| `--open`     | 同时用默认浏览器打开                                     |
| `--html PATH`  | 生成一个点击即跳转的本地 HTML 启动页                     |
| `--title NAME` | 指定在 draw.io 中显示的文件名，默认取输入文件名          |

**超长图表**：整张图都编码在 URL 里，节点很多时链接会非常长（超过约 2000 字符），可能被终端或系统的 URL 处理器截断。使用 `--open` 时脚本会自动改走本地 HTML 启动页，不会被截断；也可以用 `--html` 手动生成启动页。

**兜底方案**：如果环境里既没有 Python 也没有 Node，打开 [app.diagrams.net](https://app.diagrams.net)，选择 **File → Open From → Device**，或者直接把 `.drawio` 文件拖进页面。

## 导出格式

| 格式 | 参数       | 适用场景           |
| ---- | ---------- | ------------------ |
| PNG  | `-f png` | 默认格式，通用性强 |
| SVG  | `-f svg` | 可缩放矢量图       |
| PDF  | `-f pdf` | 打印 / 嵌入文档    |

PNG 默认带 `--scale 2 --border 20`（高清 + 留白）。画布远大于图形、导出后四周空白过多时，加 `--crop` 裁到内容。SVG / PDF 不需要 `--scale`。

导出后 Agent 会确认输出文件确实存在且非空——draw.io 桌面版是 GUI 程序，从命令行调用时经常立刻返回 0 但并没有写出文件，退出码不可信。导出失败会如实告知，并改用浏览器链接交付。

## 项目结构

```
bruce-drawio/
  SKILL.md                      # 主技能文档（工作流程 + 规则）
  skill.json                    # 技能元数据
  references/
    best-practices.md           # XML 模板、样式、布局规则、常见错误
    examples.md                 # 4 个完整可用的示例（流程图/架构图/思维导图/ER）+ 配色表
  scripts/
    validate_drawio.py          # .drawio 机械校验（ID、引用、几何、重叠）
    open_in_drawio.py           # 生成 draw.io 官网一键打开链接（Python）
    open_in_drawio.js           # 同上（Node 版，无 Python 时使用）
  evals/
    evals.json                  # 测试用例
```

## 架构图风格

架构图默认采用**分层块状布局**风格：

- 灰色背景底板
- 左侧标签列标注每一层（如"场景层"、"应用层"）
- 蓝色半透明层容器，内含子分组
- 白色叶子节点，灰色边框
- 可选的右侧跨层侧边栏（如安全、监控等横切关注点）
- 纯块状图，不使用箭头连线，通过空间嵌套表达层次关系

## 依赖检测

draw.io 桌面版是**可选**依赖，只用于导出 PNG/SVG/PDF。Agent 按照 SKILL.md 中的步骤自动检测，并且会用当前 shell 的语法：PowerShell 下用 `Get-Command` / `Test-Path $env:LOCALAPPDATA\Programs\draw.io\draw.io.exe`，bash 下用 `which drawio` 加默认安装路径。未安装时不会卡住流程，也不会追着让你装，而是直接走浏览器打开链接这条路，安装方式只作为可选项提一句。

校验和生成打开链接只依赖 Python 3 或 Node 之一（全部使用标准库，无需 `pip install` / `npm install`）。

## 使用示例

安装完成后，用自然语言描述你想要的图表即可，例如：

- "画一个电商下单流程图"
- "画一个微服务架构图"
- "画一个用户注册的时序图"
- "画一个博客系统的 ER 图"
- "画一个 AI Agent 的思维导图"
