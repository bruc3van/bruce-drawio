English | [中文](README.md)

# Draw.io Diagram Generator Skill

Cross-platform draw.io (diagrams.net) diagram generation skill for AI coding agents — Claude Code, codex, zcode, workbuddy, OpenClaw and others. The agent directly generates drawio XML, validates it, and exports via CLI — falling back to a one-click app.diagrams.net link when the desktop app is not available.

The skill is plain Markdown plus two dependency-free scripts, so it is not tied to any particular agent runtime.

## Installation

Send the following prompt to your AI coding agent:

```
Help me install this skill: https://github.com/bruc3van/bruce-drawio
```

The agent will clone the repository and configure the skill automatically.

If your agent has no automatic install, clone it into that agent's skills directory yourself:

| Agent                                      | Skills directory    |
| ------------------------------------------ | ------------------- |
| Claude Code                                | `~/.claude/skills/` |
| codex / zcode / workbuddy / OpenClaw, etc. | `~/.agents/skills/` |

```bash
# Claude Code
git clone https://github.com/bruc3van/bruce-drawio ~/.claude/skills/bruce-drawio

# every other agent
git clone https://github.com/bruc3van/bruce-drawio ~/.agents/skills/bruce-drawio
```

On Windows, replace `~` with `$HOME` (PowerShell) or `%USERPROFILE%` (cmd). There is no build step — the skill works as soon as it is cloned.

## Supported Diagram Types

| Type             | Description                                    | Trigger                        |
| ---------------- | ---------------------------------------------- | ------------------------------ |
| Flowchart        | Business process, approval flows, algorithms   | "draw a flowchart"             |
| Architecture     | System architecture, microservices, deployment | "draw an architecture diagram" |
| UML Sequence     | Interaction timelines between components       | "draw a sequence diagram"      |
| UML Class        | Class relationships, inheritance               | "draw a class diagram"         |
| ER Diagram       | Database design, entity relationships          | "draw an ER diagram"           |
| Mindmap          | Brainstorming, knowledge organization          | "draw a mindmap"               |
| Network Topology | Network architecture, device connectivity      | "draw a network topology"      |

## Platform Support

The draw.io desktop app is only needed for image export and is optional — without it you can still view and edit every diagram through [Open in the Browser](#open-in-the-browser).

| Platform | Install Command                | Package Manager     |
| -------- | ------------------------------ | ------------------- |
| macOS    | `brew install --cask drawio` | Homebrew            |
| Windows  | `winget install JGraph.Draw` | winget / Chocolatey |
| Linux    | `snap install drawio`        | snap / manual       |

All platforms also support manual download from [draw.io releases](https://github.com/jgraph/drawio-desktop/releases).

On headless Linux (containers, CI) the export needs `xvfb-run -a` and `--no-sandbox`; the agent handles this automatically.

## How It Works

1. User describes the diagram they want
2. Agent determines diagram type and elements
3. Agent generates complete drawio XML, following the closest reference example
4. Layout rules are applied (coordinates, spacing, sizes, cell order)
5. Saves the `.drawio` file and runs the validator until it exits clean
6. CLI exports to PNG/SVG/PDF (skipped when the desktop app is not installed)
7. Builds an app.diagrams.net link when one is needed
8. Delivers the image and the source file path

## XML Validation

After saving, the agent runs `scripts/validate_drawio.py` to catch mechanically what re-reading the XML by eye reliably misses:

```bash
python scripts/validate_drawio.py diagram.drawio
```

| Level | Checks                                                                                                                              |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------- |
| ERROR | malformed XML, duplicate IDs, missing root cells, dangling `parent`/`source`/`target`, missing `as="geometry"`, literal `\n` in a label, partially overlapping nodes |
| WARN  | missing `whiteSpace=wrap` / `html=1`, `fontSize` under 12, fractional coordinates, content past `pageWidth`/`pageHeight`       |

Exit code is 1 when errors are found. Overlap detection reports **partial** overlaps only — full containment is how the Layered Block Style expresses nesting, not a bug.

## Open in the Browser

The agent can hand back a `https://app.diagrams.net/?title=xxx#R...` link. Clicking it opens that exact diagram in the official web editor for further editing or export — **no desktop install, no account, no sign-in**.

How it works: the diagram XML goes through `encodeURIComponent → deflate raw → base64` and rides in the URL's `#R` fragment. Fragments are never sent to the server; draw.io decodes it locally in the browser, so **the diagram content is not uploaded anywhere**.

### When you get a link

The link is a **fallback and an on-request extra**, not an attachment on every diagram:

| Situation                        | Behaviour                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------- |
| Export succeeded                 | No link by default — just a closing line offering one                        |
| No desktop app / export failed   | The link becomes the primary delivery. This is the point of it: the diagram is viewable in any environment |
| You ask for it                   | Generated right away ("open it", "I want to tweak this", "share this")       |

### ⚠️ The link is a copy, not a handle on the local file

The `#R` link carries a **copy** of the diagram inside the URL. draw.io opens it as a new file with no connection to the one on disk, so **edits made in the browser do not sync back to the local `.drawio`**.

Two ways to close the loop:

- In draw.io, **File → Save as → Device** and overwrite the local `.drawio`
- Or just tell the agent what to change, and let it edit the local file and re-export

With the desktop app installed, opening the local file directly (`draw.io diagram.drawio`) is the better route for continued editing — edits save in place, no fork. Opening the local file from the website via **File → Open From → Device** avoids the fork too.

### Script usage

The link is produced by the scripts under `scripts/` — use whichever runtime you have:

```bash
python scripts/open_in_drawio.py diagram.drawio          # print the link
python scripts/open_in_drawio.py diagram.drawio --open   # print it and launch the browser
node   scripts/open_in_drawio.js diagram.drawio          # equivalent, for Node-only environments
```

| Flag           | Purpose                                                     |
| -------------- | ----------------------------------------------------------- |
| *(none)*       | Print the link only (default)                               |
| `--open`     | Also open it in the default browser                         |
| `--html PATH`  | Write a local click-to-open launcher page                   |
| `--title NAME` | File name shown in draw.io; defaults to the input file name |

**Large diagrams**: the whole diagram is encoded into the URL, so a busy diagram yields a very long link (over ~2000 characters) that terminals and OS URL handlers may truncate. With `--open` the script automatically routes through a local launcher page instead, so nothing gets cut off; you can also generate that page yourself with `--html`.

**Fallback**: with neither Python nor Node available, open [app.diagrams.net](https://app.diagrams.net), pick **File → Open From → Device**, or just drag the `.drawio` file onto the page.

## Export Formats

| Format | Flag       | Use Case           |
| ------ | ---------- | ------------------ |
| PNG    | `-f png` | Default, universal |
| SVG    | `-f svg` | Scalable vector    |
| PDF    | `-f pdf` | Print / document   |

PNG defaults to `--scale 2 --border 20` (high-DPI plus padding). Add `--crop` when the canvas is much larger than the drawing and the export comes out with wide empty margins. `--scale` does nothing useful for SVG and PDF.

After exporting, the agent confirms the output file exists and is non-empty — draw.io desktop is a GUI application that frequently returns 0 from the command line without having written anything, so the exit code cannot be trusted. A failed export is reported as such, and delivery falls back to the browser link.

## Project Structure

```
bruce-drawio/
  SKILL.md                      # Main skill document (workflow + rules)
  skill.json                    # Skill metadata
  references/
    best-practices.md           # XML templates, styles, layout rules, common mistakes
    examples.md                 # 4 complete examples (flowchart/architecture/mindmap/ER) + palette
  scripts/
    validate_drawio.py          # Mechanical .drawio checks (ids, refs, geometry, overlap)
    open_in_drawio.py           # Build the app.diagrams.net one-click link (Python)
    open_in_drawio.js           # Same CLI, for Node-only environments
  evals/
    evals.json                  # Test cases
```

## Architecture Diagram Style

Architecture diagrams use a **layered block layout** style by default:

- Gray background plate
- Left label column for each layer (e.g., "Scene Layer", "Application Layer")
- Blue semi-transparent layer containers with sub-groups
- White leaf nodes with gray borders
- Optional right-side cross-cutting sidebar (e.g., security, monitoring)
- Pure block diagram with no arrows; hierarchy expressed through spatial nesting

## Dependency Check

The draw.io desktop app is an **optional** dependency, used only for PNG/SVG/PDF export. The agent follows SKILL.md Step 5 to detect it using the syntax of whichever shell it is in: `Get-Command` / `Test-Path $env:LOCALAPPDATA\Programs\draw.io\draw.io.exe` on PowerShell, `which drawio` plus the default install paths on bash. If it is missing the workflow does not stall and does not nag about installing — it falls through to the browser link and mentions the install only as an optional extra.

Validation and link building need only Python 3 or Node; every script is standard library only, with no `pip install` / `npm install`.

## Usage Examples

After installation, simply describe the diagram you want in natural language:

- "Draw an e-commerce order flowchart"
- "Draw a microservice architecture diagram"
- "Draw a user registration sequence diagram"
- "Draw a blog system ER diagram"
- "Draw an AI Agent mindmap"
