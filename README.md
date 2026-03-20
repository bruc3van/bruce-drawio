# Draw.io Diagram Generator Skill

Cross-platform draw.io (diagrams.net) diagram generation skill for Claude Code. LLM directly generates drawio XML, self-reviews it, then exports via CLI.

## Supported Diagram Types

| Type | Description | Trigger |
|------|-------------|---------|
| Flowchart | Business process, approval flows, algorithms | "draw a flowchart" |
| Architecture | System architecture, microservices, deployment | "draw an architecture diagram" |
| UML Sequence | Interaction timelines between components | "draw a sequence diagram" |
| UML Class | Class relationships, inheritance | "draw a class diagram" |
| ER Diagram | Database design, entity relationships | "draw an ER diagram" |
| Mindmap | Brainstorming, knowledge organization | "draw a mindmap" |
| Network Topology | Network architecture, device connectivity | "draw a network topology" |

## Platform Support

| Platform | draw.io Install | Package Manager |
|----------|----------------|-----------------|
| macOS | `brew install --cask drawio` | Homebrew |
| Windows | `winget install JGraph.Draw` | winget / Chocolatey |
| Linux | `snap install drawio` | snap / manual |

All platforms also support manual download from [draw.io releases](https://github.com/jgraph/drawio-desktop/releases).

## How It Works

1. User describes the diagram they want
2. LLM determines diagram type and elements
3. LLM generates complete drawio XML directly
4. Self-review checklist verifies correctness and layout
5. Saves `.drawio` file
6. CLI exports to PNG/SVG/PDF
7. Delivers image and editable source file

Text rule: when a label needs a forced line break, write it as `&#xa;` in the XML `value` attribute. Do not use literal `\n`.
Layout rule: keep sibling boxes evenly aligned, gutters balanced, and containers densely filled. If a sidebar or group has obvious dead space, resize the frame or redistribute item spacing before export.

## Export Formats

| Format | Flag | Use Case |
|--------|------|----------|
| PNG | `-f png` | Default, universal |
| SVG | `-f svg` | Scalable vector |
| PDF | `-f pdf` | Print / document |

Use `--scale 2` for high-DPI PNG output.

## Project Structure

```
drawio-skill/
  SKILL.md                      # Main skill document (workflow + rules)
  skill.json                    # Skill metadata
  references/
    best-practices.md           # XML templates, styles, layout rules
    examples.md                 # Complete working XML examples
  assets/
    example-architecture.json   # Architecture diagram data
    example-mindmap.json        # Mindmap diagram data
  evals/
    evals.json                  # Test cases
```

## Dependency Check

No separate script needed. The LLM follows instructions in SKILL.md Step 5 to detect draw.io via shell commands (`which drawio`, checking default paths). If not found, it guides the user to install.
