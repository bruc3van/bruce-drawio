---
name: drawio
description: |
  **Use this skill** when the user wants to create any diagram: flowchart, architecture, UML (sequence/class), ER, mindmap, network topology, or any visual diagram.

  Trigger words: "draw", "diagram", "flowchart", "architecture", "UML", "sequence diagram", "mindmap", "ER diagram", "network topology", "visualize", "draw.io", "drawio".

  Workflow: understand requirements -> generate drawio XML directly -> self-review -> CLI export PNG/SVG/PDF.
---

# Draw.io Diagram Generator

## Workflow

```
1. Understand requirements  -> determine diagram type, elements, relationships
2. Generate XML directly    -> LLM writes drawio XML (refer to references/best-practices.md)
3. Self-review checklist    -> verify structure, layout, connections
4. Save .drawio file        -> write to user's working directory
5. CLI export               -> call draw.io desktop CLI to export image
6. Deliver to user          -> show image + provide editable .drawio file
```

## Step 1: Understand Requirements

Determine:
- **Diagram type**: flowchart / architecture / uml-sequence / uml-class / er / mindmap / network
- **Key elements**: nodes, components, participants, entities
- **Relationships**: connections, dependencies, flow direction
- **Output format**: PNG (default) / SVG / PDF
- **Language**: match the user's language for labels

## Step 2: Generate XML

**You MUST write the XML directly.** Do not call any script to generate it.

### Base XML Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="drawio-skill" version="21.0.0" type="device">
  <diagram name="DiagramName" id="diagram-1">
    <mxGraphModel dx="1422" dy="762"
                   grid="1" gridSize="10"
                   guides="1" tooltips="1" connect="1"
                   arrows="1" fold="1"
                   page="1" pageScale="1"
                   pageWidth="1600" pageHeight="1200"
                   math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- nodes and edges here -->

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Node Template

```xml
<mxCell id="node-1" value="Label"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
</mxCell>
```

### Edge Template

```xml
<mxCell id="edge-1" value=""
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        edge="1" parent="1" source="node-1" target="node-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Step 3: Layout Rules (CRITICAL for beautiful output)

### General Principles

1. **Grid alignment**: all x, y coordinates must be multiples of 10 (snap to grid)
2. **Generous spacing**: minimum 80px gap between node edges (not centers)
3. **Center alignment**: nodes in the same column share the same x; nodes in the same row share the same y
4. **Consistent sizing**: same-type nodes use identical width and height
5. **Page margins**: keep at least 60px from the canvas edge (pageWidth/pageHeight)
6. **Use `whiteSpace=wrap;html=1;`** on all nodes so long text wraps instead of overflowing

### Layout by Diagram Type

| Type | Direction | Primary axis | Spacing (between edges) | Alignment |
|------|-----------|-------------|------------------------|-----------|
| Flowchart | Top-to-bottom | Y increases | 100px vertical | Center x |
| Architecture | Top-to-bottom layers | Y increases | 120px vertical, 80px horizontal | Center each layer |
| UML Sequence | Left-to-right participants | X increases | 200px horizontal | Top-aligned |
| UML Class | Grid / top-to-bottom | Y increases | 100px vertical, 80px horizontal | Left-aligned columns |
| ER Diagram | Spread / grid | Both axes | 120px both | Grid-aligned |
| Mindmap | Center-outward radial | Both axes | 150px from center per level | Radial symmetric |
| Network | Hierarchical layers | Y increases | 100px vertical, 120px horizontal | Center each layer |

### Anti-Overlap Checklist

Before finalizing coordinates, verify:
- No two nodes' bounding boxes overlap (check x, y, width, height)
- Edge labels don't overlap with nodes
- Decision branches (Yes/No) go in clearly different directions
- For flowcharts with branches: main path goes down, alternate path goes right (or left)
- For wide diagrams: increase `pageWidth` in mxGraphModel; for tall ones increase `pageHeight`

### Calculating Coordinates

Use this formula to center N items horizontally in a row:

```
total_width = N * node_width + (N - 1) * gap
start_x = (pageWidth - total_width) / 2
item[i].x = start_x + i * (node_width + gap)
```

For vertical centering in a column, apply the same logic to Y axis.

### Standard Sizes

| Element | Width | Height |
|---------|-------|--------|
| Standard node | 160 | 60 |
| Decision (rhombus) | 160 | 80 |
| Database (cylinder) | 140 | 80 |
| Actor (UML) | 40 | 60 |
| Start/End (rounded) | 160 | 60 |
| Mindmap center | 180 | 80 |
| Mindmap branch | 140 | 50 |
| Mindmap leaf | 120 | 40 |
| ER table header | 200 | varies |
| Group/container | auto | auto |

## Step 4: Self-Review Checklist

After generating XML, verify every item:

- [ ] All `id` values are unique across the entire file
- [ ] Every `mxCell` with `vertex="1"` has `parent="1"`
- [ ] Every edge's `source` and `target` reference existing node IDs
- [ ] No two nodes overlap (compare x, y, width, height bounding boxes)
- [ ] Coordinates are multiples of 10
- [ ] All nodes include `whiteSpace=wrap;html=1;` in style
- [ ] `fontSize=14` or larger for readability
- [ ] Edges use `edgeStyle=orthogonalEdgeStyle` for clean routing (except mindmaps which use curved)
- [ ] Decision nodes use `rhombus` shape
- [ ] Database nodes use `shape=cylinder3` or `shape=cylinder`
- [ ] XML is well-formed: all tags closed, all attribute values quoted
- [ ] `mxGeometry` always has `as="geometry"` attribute
- [ ] Page dimensions (pageWidth, pageHeight) are large enough for all content

## Step 5: CLI Export (Cross-Platform)

### Detect draw.io installation

```bash
python3 scripts/check_dependency.py
```

### Export commands by platform

**macOS:**
```bash
/Applications/draw.io.app/Contents/MacOS/draw.io \
  -x -f png --scale 2 \
  -o output.png diagram.drawio
```

**Windows (bash shell):**
```bash
"/c/Program Files/draw.io/draw.io.exe" \
  -x -f png --scale 2 \
  -o output.png diagram.drawio
```

**Windows (if bash path fails, use cmd-style):**
```bash
"C:/Program Files/draw.io/draw.io.exe" \
  -x -f png --scale 2 \
  -o output.png diagram.drawio
```

**Linux:**
```bash
drawio -x -f png --scale 2 \
  -o output.png diagram.drawio
```

### Export flags

| Flag | Purpose |
|------|---------|
| `-x` | Export mode (no GUI) |
| `-f png/svg/pdf` | Output format |
| `-o path` | Output file path |
| `--scale 2` | 2x resolution for crisp PNG |
| `--border 20` | Add border padding (px) |
| `--width 1600` | Constrain output width |
| `-p 0` | Export specific page (0-indexed) |
| `--crop` | Crop to diagram content |

### Platform detection in bash

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  DRAWIO="/Applications/draw.io.app/Contents/MacOS/draw.io"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  DRAWIO="/c/Program Files/draw.io/draw.io.exe"
  if [ ! -f "$DRAWIO" ]; then
    DRAWIO="$LOCALAPPDATA/Programs/draw.io/draw.io.exe"
  fi
else
  DRAWIO="drawio"
fi
```

## Step 6: Deliver to User

After export:
- Show the exported image
- Tell the user the .drawio file location (can be edited at https://app.diagrams.net)
- Mention the export format used

## File Naming

- Lowercase + hyphens: `ecommerce-order-flow.drawio`
- No Chinese characters, spaces, or special characters in filenames
- Output image uses same base name: `ecommerce-order-flow.png`

## Reference

For detailed XML templates, color codes, and per-diagram-type examples, read `references/best-practices.md`.
