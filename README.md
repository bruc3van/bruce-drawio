[English](README_EN.md) | 中文

# Draw.io 图表生成技能

跨平台的 draw.io (diagrams.net) 图表生成技能，适用于 AI 编程 Agent（Claude Code、OpenClaw 等）。Agent 直接生成 drawio XML，经过自检后通过 CLI 导出图片。

## 安装

向你的 AI 编程 Agent 发送以下提示词：

```
帮我安装这个skill：https://github.com/bruc3van/bruce-drawio
```

Agent 会自动克隆仓库并完成配置。

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

draw.io 桌面版仅用于导出图片，属于可选项；不安装也能通过下面的[一键在浏览器打开](#一键在浏览器打开)查看和编辑图表。

| 平台    | 安装命令                       | 包管理器            |
| ------- | ------------------------------ | ------------------- |
| macOS   | `brew install --cask drawio` | Homebrew            |
| Windows | `winget install JGraph.Draw` | winget / Chocolatey |
| Linux   | `snap install drawio`        | snap / 手动安装     |

所有平台也支持从 [draw.io releases](https://github.com/jgraph/drawio-desktop/releases) 手动下载安装。

## 工作流程

1. 用户描述想要的图表
2. Agent 判断图表类型和关键元素
3. Agent 参照对应示例直接生成完整的 drawio XML
4. 应用布局规则（坐标、间距、尺寸、单元格顺序）
5. 保存 `.drawio` 并跑校验脚本，错误清零
6. 通过 CLI 导出为 PNG/SVG/PDF（未安装桌面版则跳过）
7. 生成 draw.io 官网一键打开链接
8. 向用户展示图片、源文件路径和在线打开链接

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

## 一键在浏览器打开

每次生成图表后，Agent 都会给出一条 `https://app.diagrams.net/?title=xxx#R...` 链接，点击即可在 draw.io 官网直接打开该图，继续编辑或导出——**不需要安装桌面版，也不需要注册登录**。

原理：图表 XML 经过 `encodeURIComponent → deflate raw → base64` 后放进 URL 的 `#R` 片段。片段部分不会发送给服务器，由 draw.io 前端在浏览器本地解码，因此**图表内容不会上传到任何服务器**。

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

使用 `--scale 2` 可导出高清 PNG。

## 项目结构

```
bruce-drawio/
  SKILL.md                      # 主技能文档（工作流程 + 规则）
  skill.json                    # 技能元数据
  references/
    best-practices.md           # XML 模板、样式、布局规则
    examples.md                 # 完整的可用 XML 示例
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

draw.io 桌面版是**可选**依赖，只用于导出 PNG/SVG/PDF。Agent 按照 SKILL.md 中的步骤通过 shell 命令（`which drawio`、检查默认安装路径）自动检测；未安装时不会卡住流程，而是直接走浏览器打开链接这条路，并顺带提示可选的安装方式。

生成打开链接只依赖 Python 3 或 Node 之一（两者都用标准库，无需 `pip install` / `npm install`）。

## 使用示例

安装完成后，用自然语言描述你想要的图表即可，例如：

- "画一个电商下单流程图"
- "画一个微服务架构图"
- "画一个用户注册的时序图"
- "画一个博客系统的 ER 图"
- "画一个 AI Agent 的思维导图"
