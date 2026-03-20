# Draw.io Skill v3.0 Changelog

## v3.0 Changes (from v2.0)

### Cross-Platform Support
- **check_dependency.py** rewritten to detect and install draw.io on Windows (winget/choco), macOS (brew), and Linux (snap)
- **SKILL.md** includes platform-specific CLI export commands with bash detection snippet
- **README.md** documents all three platforms

### Layout & Visual Quality
- Added **anti-overlap rules** with bounding box verification checklist
- Added **coordinate calculation formulas** for centering N items in a row/column
- Added **standard size table** for all element types
- All nodes now require `whiteSpace=wrap;html=1;` to prevent text overflow
- All edges require `edgeStyle=orthogonalEdgeStyle;rounded=1;` for clean routing
- Added **edge anchor points** (exitX/exitY/entryX/entryY) guidance
- Added `--scale 2` recommendation for crisp PNG export

### Missing Diagram Types Added
- **Mindmap**: center node, branch nodes, leaf nodes, curved edges, radial layout, color-per-branch scheme
- **Network Topology**: modem, router, switch, NAS, end devices, wired vs wireless edge styles, hierarchical layout
- **UML Class Diagram**: 3-section HTML boxes, inheritance arrows, association arrows
- **Groups/Containers**: dashed containers for grouping related components

### Complete XML Examples
- **examples.md** completely rewritten with 4 full, copy-paste-ready XML examples:
  1. Order flowchart with decision branches
  2. Microservice architecture with layers
  3. AI Agent mindmap with 4 colored branches
  4. Blog system ER diagram with swimlane tables

### Removed
- Dead `generate_diagram.py` script references
- macOS-only assumptions throughout
- Old JSON-based diagram definition format from examples

### Test Coverage
- 8 eval cases (was 6): added UML Class Diagram and Cross-platform Export tests
- All eval expected_output descriptions updated to match v3 quality standards

## Directory Structure

```
drawio-skill/
  SKILL.md                      # Core workflow, layout rules, cross-platform CLI
  skill.json                    # Metadata (v3.0.0)
  README.md                     # User-facing documentation
  OPTIMIZATION_REPORT.md        # This file
  scripts/
    check_dependency.py         # Cross-platform dependency detection + install
  references/
    best-practices.md           # XML templates, styles, colors, layout strategies
    examples.md                 # 4 complete working XML examples
  assets/
    example-architecture.json   # Sample architecture data
    example-mindmap.json        # Sample mindmap data
  evals/
    evals.json                  # 8 test cases
```
