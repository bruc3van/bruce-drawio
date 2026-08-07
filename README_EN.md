English | [中文](README.md)

# Draw.io Diagram Generator Skill

Cross-platform draw.io (diagrams.net) diagram generation skill for AI coding agents (Claude Code, OpenClaw, etc.). The agent directly generates drawio XML, self-reviews it, exports via CLI, and hands back a one-click link that opens the diagram on app.diagrams.net.

## Installation

Send the following prompt to your AI coding agent:

```
Help me install this skill: https://github.com/bruc3van/bruce-drawio
```

The agent will clone the repository and configure the skill automatically.

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

## How It Works

1. User describes the diagram they want
2. Agent determines diagram type and elements
3. Agent generates complete drawio XML, following the closest reference example
4. Layout rules are applied (coordinates, spacing, sizes, cell order)
5. Saves the `.drawio` file and runs the validator until it exits clean
6. CLI exports to PNG/SVG/PDF (skipped when the desktop app is not installed)
7. Builds a one-click app.diagrams.net link
8. Delivers the image, the editable source file and the browser link

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

After every diagram, the agent hands back a `https://app.diagrams.net/?title=xxx#R...` link. Clicking it opens that exact diagram in the official web editor for further editing or export — **no desktop install, no account, no sign-in**.

How it works: the diagram XML goes through `encodeURIComponent → deflate raw → base64` and rides in the URL's `#R` fragment. Fragments are never sent to the server; draw.io decodes it locally in the browser, so **the diagram content is not uploaded anywhere**.

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

Use `--scale 2` for high-DPI PNG output.

## Project Structure

```
bruce-drawio/
  SKILL.md                      # Main skill document (workflow + rules)
  skill.json                    # Skill metadata
  references/
    best-practices.md           # XML templates, styles, layout rules
    examples.md                 # Complete working XML examples
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

The draw.io desktop app is an **optional** dependency, used only for PNG/SVG/PDF export. The agent follows SKILL.md Step 5 to detect it via shell commands (`which drawio`, checking default paths). If it is missing the workflow does not stall — it falls through to the browser link and mentions the optional install.

Building that link needs only Python 3 or Node; both scripts use standard library only, with no `pip install` / `npm install`.

## Usage Examples

After installation, simply describe the diagram you want in natural language:

- "Draw an e-commerce order flowchart"
- "Draw a microservice architecture diagram"
- "Draw a user registration sequence diagram"
- "Draw a blog system ER diagram"
- "Draw an AI Agent mindmap"
