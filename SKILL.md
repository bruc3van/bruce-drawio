---
name: bruce-drawio
description: |
  **Use this skill** when the user wants to create any diagram: flowchart, architecture, UML (sequence/class), ER, mindmap, network topology, or any visual diagram.

  Trigger words: "draw", "diagram", "flowchart", "architecture", "UML", "sequence diagram", "mindmap", "ER diagram", "network topology", "visualize", "draw.io", "drawio".

  Workflow: understand requirements -> generate drawio XML directly -> validate -> CLI export PNG/SVG/PDF, falling back to an app.diagrams.net browser link when draw.io desktop is unavailable.
---

# Draw.io Diagram Generator

## Workflow

Each numbered step below has a matching `## Step N` section. Follow them in order.

```
1. Understand requirements   -> determine diagram type, elements, relationships
2. Generate XML directly     -> write drawio XML; read the matching reference section first
3. Apply layout rules        -> coordinates, spacing, sizes, cell order
4. Save + validate (DO NOT SKIP) -> write the .drawio file, run the validator, fix every error
5. CLI export (optional)     -> call draw.io desktop CLI to export an image (skip if not installed)
6. Browser link (conditional) -> only when the export failed, or the user asks for it
7. Deliver to user           -> image + .drawio file path, kept short
```

Steps 5 and 6 are two routes to the same goal, not two deliverables to stack up. Export is
the default. The browser link is the fallback that needs nothing installed — it guarantees
the user can always see the diagram, so it is never a dead end, but it is also a detached
copy of the file (Step 6d) and should not be pushed on a user who already has an image.

## Step 1: Understand Requirements

Determine:
- **Diagram type**: flowchart / architecture / uml-sequence / uml-class / er / mindmap / network
- **Key elements**: nodes, components, participants, entities
- **Relationships**: connections, dependencies, flow direction
- **Output format**: PNG (default) / SVG / PDF
- **Language**: match the user's language for labels

## Step 2: Generate XML

**You MUST write the XML directly.** Do not call any script to generate it.

### Read the matching reference first

| Diagram type | Read before writing |
|--------------|--------------------|
| Architecture | `references/best-practices.md` → *Architecture Diagram Templates*, then `references/examples.md` → *Example 2* |
| Flowchart | `references/examples.md` → *Example 1* |
| Mindmap | `references/examples.md` → *Example 3* |
| ER | `references/examples.md` → *Example 4* |
| UML sequence/class, network, anything else | `references/best-practices.md` → *General Rules*, then write from your own knowledge |

`references/examples.md` holds complete, validated diagrams — copying the structure of the
closest example is faster and more reliable than composing one from scratch. Read only the
sections you need, not the whole file.

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

### Text Content Rules

- For multi-line labels, encode line breaks as `&#xa;` inside `value`, for example `value="API&#xa;Gateway"`
- Do not write literal `\n` inside `value`; draw.io will render it as backslash + n text
- Keep `html=1` on nodes, but still use `&#xa;` as the default line-break form for predictable output

### Edge Template

```xml
<mxCell id="edge-1" value=""
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        edge="1" parent="1" source="node-1" target="node-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Cell Order Is Z-Order (CRITICAL)

draw.io paints cells **in document order**: whatever comes later in `<root>` is drawn on top.
Emit cells back-to-front:

```
1. Background plate      (the big gray rectangle, if any)
2. Layer containers      (semi-transparent blocks)
3. Sub-group containers
4. Leaf nodes / labels
5. Edges
```

Writing the background rectangle after the nodes hides the entire diagram behind a gray
block — this is the single most destructive ordering mistake, and it renders as a blank
image with no error anywhere.

### Parent and Coordinate System

A cell's `x`/`y` are **relative to its parent**. That gives you two valid approaches, and
mixing them is what produces diagrams where everything is shifted off-screen:

| Approach | When | `parent` | Coordinates |
|----------|------|----------|-------------|
| **Flat + absolute** (default) | Everything except ER/UML tables, including the Layered Block Style — visual nesting comes from the numbers, not the tree | always `"1"` | absolute canvas coordinates |
| **True nesting** | Only when the shape genuinely owns its children: `swimlane` tables (ER, UML class), `childLayout=stackLayout` rows | the container's ID | relative to the container's top-left, so a child at `y="30"` sits 30px below the container's top |

**Default to flat + absolute.** The Layered Block Style puts every leaf node at `parent="1"`
with absolute coordinates even though it looks nested — see `references/examples.md` Example 2.
Only ER/UML table rows use true nesting, where a row's `x` is omitted and `y` is its offset
inside the swimlane — see Example 4.

## Step 3: Layout Rules (CRITICAL for beautiful output)

### General Principles

1. **Grid alignment**: anchor top-level blocks (background plate, layer containers, sidebars,
   the primary column/row of a flowchart) to multiples of 10. Positions *derived* from the
   centering formulas below may land off the grid — that is fine and expected. The hard rule
   is that **every coordinate must be a whole number**; never emit fractional values.
2. **Generous spacing**: minimum 80px gap between node edges (not centers)
3. **Center alignment**: nodes in the same column share the same x; nodes in the same row share the same y
4. **Consistent sizing**: same-type nodes use identical width and height
5. **Page margins**: keep at least 60px from the canvas edge (pageWidth/pageHeight)
6. **Use `whiteSpace=wrap;html=1;`** on all nodes so long text wraps instead of overflowing
7. **Balanced gutters**: outer padding around a row/column should visually match the internal gaps; avoid one oversized blank side
8. **Symmetry first**: centered groups should have roughly equal left/right and top/bottom whitespace
9. **Dense fill**: containers, sub-groups, and sidebars should fit content plus consistent padding; do not leave large dead zones just because the canvas is large

### Layout by Diagram Type

| Type | Direction | Primary axis | Spacing (between edges) | Alignment |
|------|-----------|-------------|------------------------|-----------|
| Flowchart | Top-to-bottom | Y increases | 100px vertical | Center x |
| Architecture | Layered block (preferred) | Y increases | 20px between layers | Left label + container rows |
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
start_x = round((pageWidth - total_width) / 2)
item[i].x = start_x + i * (node_width + gap)
```

Round the result to a whole number. Do not then "fix" it to a multiple of 10 by nudging
individual items — that breaks the equal-gap invariant, which matters far more than the grid.

For vertical centering in a column, apply the same logic to Y axis.

For rows inside a fixed-width container, also check fill density:

```
inner_width = container_width - 2 * side_pad
gap = (inner_width - N * item_width) / (N - 1)
```

If `gap` is much larger than the item width, or side padding is much larger than `gap`, adjust one of:
- increase item width moderately
- increase item count per row only if still readable
- reduce container width
- split into multiple balanced rows

For incomplete last rows, center the remaining items instead of left-aligning them and leaving a large blank tail.

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

Pick one size per role and keep it identical for every node of that role in the diagram. A
start node that is 20px wider than the process nodes below it reads as a mistake, not as
emphasis — use color and `fontStyle=1` to emphasize instead.

## Step 4: Save and Validate (DO NOT SKIP)

Write the `.drawio` file to the user's working directory, then run the validator on it.

### 4a. Run the validator

```bash
python scripts/validate_drawio.py diagram.drawio
```

Use `python3` if `python` is missing. It exits non-zero when it finds errors.

**Fix every ERROR and re-run until it exits clean.** Do not export or deliver a file that
still reports errors — each one is a diagram that renders wrong or not at all. The validator
catches what re-reading your own XML reliably misses:

| Reported as | Checks |
|-------------|--------|
| ERROR | malformed XML, duplicate IDs, missing root cells, dangling `parent`/`source`/`target`, missing `as="geometry"`, literal `\n` in a label, partially overlapping nodes |
| WARN | missing `whiteSpace=wrap` / `html=1`, `fontSize` under 12, fractional coordinates, content past `pageWidth`/`pageHeight` |

Treat WARNs as defects too unless you have a specific reason — a "content extends past
pageWidth" warning means part of the diagram falls outside the page.

Note what the validator **cannot** see: it reports partial overlaps only, since full
containment is how the Layered Block Style expresses nesting. It says nothing about whether
the layout is balanced or the diagram is readable. That is 4b.

### 4b. Review what the validator cannot check

Re-read your XML and confirm:

- [ ] Cells are in back-to-front order: background → containers → sub-groups → leaves → edges
- [ ] Sibling items in the same row/column use equal sizes and equal gaps unless there is a clear reason not to
- [ ] Left/right and top/bottom padding inside each container are visually balanced; no obvious one-sided blank area
- [ ] Containers, sub-groups, and sidebars are sized to content plus padding; if a blank region is larger than a normal item gap or roughly a full item row, tighten the layout
- [ ] Incomplete last rows are centered, not stuck to one side with a large empty remainder
- [ ] Decision branches (Yes/No) leave in clearly different directions
- [ ] Edges use `edgeStyle=orthogonalEdgeStyle` for clean routing (except mindmaps, which use `curved=1`)
- [ ] Decision nodes use `rhombus`; database nodes use `shape=cylinder3`
- [ ] Labels are in the user's language and read naturally

## Step 5: CLI Export (Optional, Cross-Platform)

This step needs the draw.io **desktop app**, and it is the preferred route: it renders an
image the user can see immediately, and the `.drawio` it reads is the same file the desktop
app edits in place. If the app is not installed, do not stop and do not block on an install —
go to Step 6, which needs nothing but a browser.

### 5a. Detect draw.io

**Use the syntax of the shell you actually have.** On Windows the default shell is usually
PowerShell, where `which` and `ls "/c/..."` do not exist and the check fails for the wrong
reason. Stop at the first command that succeeds.

**Windows (PowerShell):**
```powershell
(Get-Command draw.io, drawio -ErrorAction SilentlyContinue | Select-Object -First 1).Source
# then the default install locations
"$env:ProgramFiles\draw.io\draw.io.exe", "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" |
  Where-Object { Test-Path $_ } | Select-Object -First 1
```

**macOS / Linux (bash):**
```bash
which drawio 2>/dev/null || which draw.io 2>/dev/null
```

If PATH lookup fails, check the platform default paths:

```bash
# macOS
ls /Applications/draw.io.app/Contents/MacOS/draw.io 2>/dev/null
# Linux
ls /usr/bin/drawio 2>/dev/null || ls /snap/bin/drawio 2>/dev/null
```

**Windows (bash/MSYS2)**, if that is what you are running in:
```bash
ls "/c/Program Files/draw.io/draw.io.exe" 2>/dev/null || \
ls "$LOCALAPPDATA/Programs/draw.io/draw.io.exe" 2>/dev/null
```

### 5b. If not found, fall back to the browser

**Do not stall the task on an install.** Go to Step 6 and deliver the diagram through
app.diagrams.net, then mention the desktop app as an optional extra for offline editing
and image export:

| Platform | Install Command |
|----------|----------------|
| macOS | `brew install --cask drawio` |
| Windows | `winget install JGraph.Draw` |
| Linux | `snap install drawio` |
| All | Download from https://github.com/jgraph/drawio-desktop/releases |

Do NOT auto-install without user confirmation.

### 5c. Export

Use the detected path (stored as `$DRAWIO`) to export:

```bash
"$DRAWIO" -x -f png --scale 2 --border 20 -o output.png diagram.drawio
```

On a headless Linux box the Electron app needs a display and a sandbox opt-out:

```bash
xvfb-run -a "$DRAWIO" -x -f png --scale 2 --border 20 --no-sandbox -o output.png diagram.drawio
```

### 5d. Verify the output file exists

**Do not trust the exit code.** draw.io desktop is a GUI application; when launched from a
shell it often returns 0 immediately, before (or without) writing anything. Always confirm
the file landed and is non-empty:

```bash
ls -l output.png          # bash
```
```powershell
Get-Item output.png | Select-Object Length   # PowerShell
```

If the file is missing or 0 bytes, treat the export as failed: say so, and deliver via the
Step 6 browser link instead. Never report an export you did not verify.

### 5e. If the user wants to keep editing

When the desktop app is present, the best way to hand off an editable diagram is the local
file itself — `"$DRAWIO" diagram.drawio` opens it and saves edits back to the same path. Only
reach for the Step 6 link when the desktop app is unavailable or the user explicitly wants
the browser.

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

Default to `--scale 2 --border 20` for PNG. Reach for `--crop` when the diagram is much
smaller than the `pageWidth`/`pageHeight` you set and the export comes out with wide empty
margins; drop `--scale` for SVG and PDF, where it does nothing useful.

## Step 6: Open in draw.io Online (Conditional)

An app.diagrams.net link opens the finished diagram in the official web editor with no
install and no account. It is the fallback that guarantees delivery when Step 5 could not
produce an image — but it is **not** something to attach to every diagram.

### 6a. Decide whether to build a link

| Situation | What to do |
|-----------|-----------|
| Step 5 exported successfully | **Do not build a link.** The user already has an image plus a `.drawio` their desktop app opens natively. Close with one short line: "需要在线打开/编辑的链接就说一声。" |
| Step 5 was skipped or failed | **Build the link** — it is now the only way the user can see the diagram |
| The user asks for it | Build it. Triggers: "打开看看", "我想改一下", "在浏览器里打开", "发给同事", "share this", "open it" |

Why not always: the link is a **snapshot copy**, not a reference to the file (see 6d). Handing
one out unprompted invites the user to edit a fork of a diagram they already have locally.

The link format is `https://app.diagrams.net/?title=<name>#R<data>`, where `<data>` is
`base64(deflateRaw(encodeURIComponent(xml)))`. draw.io decodes the `#R` fragment in the
browser — the diagram never leaves the user's machine, and no account or upload is needed.

### 6b. Build the link

Run the bundled script on the saved file (paths are relative to this skill's directory):

```bash
python scripts/open_in_drawio.py diagram.drawio
```

If `python` is missing or is a stub, use `python3`, then fall back to Node:

```bash
node scripts/open_in_drawio.js diagram.drawio
```

Both print the URL on stdout and share the same flags:

| Flag | Purpose |
|------|---------|
| *(none)* | Print the URL only — the default; use this and let the user click |
| `--open` | Also launch the default browser on that URL |
| `--html PATH` | Write a click-to-open launcher page instead of relying on the terminal |
| `--title NAME` | File name shown in draw.io (defaults to the input file name) |

**Only pass `--open` when the user asked to open it** ("打开看看", "open it in the browser").
Launching a browser unprompted is intrusive. Default to printing the link.

### 6c. Long diagrams

The whole diagram travels inside the URL, so big diagrams produce very long links. A link
over ~2000 characters can be mangled by terminals and by the OS URL handler:

- With `--open`, the script handles this automatically — it writes a temporary launcher page
  and opens that instead, so nothing is truncated.
- Without `--open`, if the URL exceeds ~2000 characters, write a launcher next to the diagram
  with `--html diagram-open.html` and tell the user to open that file, **or** fall back to 6e.

### 6d. Warn that browser edits do not sync back (REQUIRED)

The `#R` link carries a **copy** of the diagram. draw.io opens it as a new, unsaved file with
no connection to the `.drawio` on disk. Anything the user changes in the browser lives only
in that browser tab — the local file silently becomes the older version.

Whenever you hand over a link, say so in one line and give the two ways forward:

> 浏览器里的修改不会同步回本地文件。改完请用 **File → Save as → Device** 下载并覆盖
> `diagram.drawio`；或者直接告诉我要改什么，我改本地文件再重新导出。

Never present the link as "the editable version" of the local file. It is a detached copy.

### 6e. Manual fallback

If the script cannot run at all (no Python, no Node), tell the user to:

1. Open https://app.diagrams.net
2. Choose **File → Open From → Device** (or just drag the `.drawio` file onto the page)
3. Select the generated `.drawio` file

This route has no fork problem — draw.io keeps working against the file the user picked.

## Step 7: Deliver to User

Keep it short. The diagram is the deliverable; everything else is one line each.

**When the export succeeded:**

1. The exported image
2. The `.drawio` file path, and the format exported
3. One closing line offering the browser link — do not paste a link that was not asked for

**When the export was skipped or failed:**

1. The `.drawio` file path
2. The app.diagrams.net link, as the primary way to view the diagram
3. The fork warning from 6d
4. One line on why there is no image (desktop app missing / export produced no file), with
   the install commands only if the user seems to want them

Do not pad the delivery with a recap of the diagram's contents — the user can see it.

## File Naming

- Lowercase + hyphens: `ecommerce-order-flow.drawio`
- No Chinese characters, spaces, or special characters in filenames
- Output image uses same base name: `ecommerce-order-flow.png`

## Architecture Diagram: Layered Block Style

For architecture diagrams, use the **Layered Block Style** — see `references/best-practices.md` for full templates and layout constants. This is the preferred style: structured block layout with no arrows, horizontal layers, left label column, and optional cross-cutting sidebar.

## Modifying Existing Diagrams

When the user is not satisfied with the result and asks for modifications:
1. **Read the existing .drawio file** first to understand current structure
2. **Edit based on the existing XML** — do not regenerate from scratch
3. Apply the user's requested changes while preserving the overall layout and style
4. Re-run steps 4 → 7

**Check first whether the local file is stale.** If you previously handed the user an
app.diagrams.net link, they may have edited that copy in the browser — those changes never
reach the local `.drawio` (Step 6d). If the user describes the current diagram in a way that
does not match the file you just read, say so and ask them to save their browser version over
the local file before you continue. Do not silently rebuild from the stale version.

If you do hand over a new link, always regenerate it — the old one still encodes the
previous version of the diagram.

## Reference

`references/best-practices.md`:
- **General Rules** — ID management, cell order, parent/coordinate system, style essentials, common mistakes
- **Architecture Diagram Templates (Layered Block Style)** — the preferred architecture style with full XML templates and layout constants

`references/examples.md` — four complete, validated diagrams to copy the structure of:
- Example 1: flowchart · Example 2: layered block architecture · Example 3: mindmap · Example 4: ER
- Also holds the **Color Palette Reference** — use these fill/stroke pairs instead of inventing colors

`scripts/`:
- `validate_drawio.py` — mechanical checks on a `.drawio` file (Step 4). Run it every time.
- `open_in_drawio.py` / `open_in_drawio.js` — build the app.diagrams.net `#R` link for a
  `.drawio` file (Step 6). Identical CLIs; use whichever runtime is available.

For diagram types without an example (UML sequence/class, network topology, etc.), read the
"General Rules" section and generate the XML from your own knowledge.
