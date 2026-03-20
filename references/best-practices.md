# Draw.io XML Best Practices & Templates

## General Rules

### ID Management
- Use meaningful IDs: `start`, `process-1`, `decision-stock`, `edge-payment`
- All IDs must be globally unique within the file
- Recommended format: `{type}-{name}` or `{type}-{number}`
- IDs `0` and `1` are reserved for root mxCells

### Style Essentials
- Always include `whiteSpace=wrap;html=1;` so text wraps properly
- Always set `fontSize=14;` or larger for readability
- Use `fontStyle=1` for bold headers, `fontStyle=0` for normal text
- Use `strokeWidth=2;` for important borders
- Edges should use `edgeStyle=orthogonalEdgeStyle;rounded=1;` for clean right-angle routing
- Add `exitX`, `exitY`, `entryX`, `entryY` on edges for precise anchor points

### Edge Anchor Points Reference

Anchor point values (0 to 1) for `exitX/exitY/entryX/entryY`:

| Position | X | Y |
|----------|---|---|
| Top center | 0.5 | 0 |
| Bottom center | 0.5 | 1 |
| Left center | 0 | 0.5 |
| Right center | 1 | 0.5 |
| Top-left | 0 | 0 |
| Top-right | 1 | 0 |
| Bottom-left | 0 | 1 |
| Bottom-right | 1 | 1 |

### Color Palette

| Purpose | Fill | Stroke | Usage |
|---------|------|--------|-------|
| Start/End/Success | #d5e8d4 | #82b366 | Green - start, end, success states |
| Process/Service | #dae8fc | #6c8ebf | Blue - processing steps, services, DB |
| Decision/Warning | #fff2cc | #d6b656 | Yellow - decisions, cache, warnings |
| Error/Client | #f8cecc | #b85450 | Red - errors, exceptions, external |
| Subprocess/Storage | #e1d5e7 | #9673a6 | Purple - sub-processes, storage |
| Neutral/Default | #f5f5f5 | #666666 | Gray - backgrounds, lifelines |
| Highlight/Primary | #1ba1e2 | #006EAF | Accent blue - highlights, key items |
| Dark header | #333333 | #333333 | Dark - container headers, titles |

## Flowchart Templates

### Start / End Node (green rounded)
```xml
<mxCell id="start" value="Start"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;fontStyle=1;arcSize=50;"
        vertex="1" parent="1">
  <mxGeometry x="320" y="40" width="160" height="60" as="geometry" />
</mxCell>
```

### Process Step (blue rectangle)
```xml
<mxCell id="process-1" value="Process Step"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="320" y="160" width="160" height="60" as="geometry" />
</mxCell>
```

### Decision Node (yellow diamond)
```xml
<mxCell id="decision-1" value="Condition?"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="320" y="280" width="160" height="80" as="geometry" />
</mxCell>
```

### Error / Exception (red)
```xml
<mxCell id="error-1" value="Error"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="560" y="290" width="160" height="60" as="geometry" />
</mxCell>
```

### Standard Edge
```xml
<mxCell id="edge-1" value=""
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
               exitX=0.5;exitY=1;exitDx=0;exitDy=0;
               entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        edge="1" parent="1" source="start" target="process-1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Labeled Branch Edge (from decision)
```xml
<mxCell id="edge-yes" value="Yes"
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
               exitX=0.5;exitY=1;exitDx=0;exitDy=0;
               entryX=0.5;entryY=0;entryDx=0;entryDy=0;
               fontSize=12;fontStyle=1;"
        edge="1" parent="1" source="decision-1" target="process-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<mxCell id="edge-no" value="No"
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
               exitX=1;exitY=0.5;exitDx=0;exitDy=0;
               entryX=0;entryY=0.5;entryDx=0;entryDy=0;
               fontSize=12;fontStyle=1;"
        edge="1" parent="1" source="decision-1" target="error-1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Flowchart Layout Strategy

```
     [Start]          x=320, y=40
        |
     [Process]        x=320, y=160   (gap = 160-40-60 = 60px min)
        |
     [Decision]       x=320, y=280
      /      \
   [Yes]    [No]      Yes: x=320, y=420   No: x=560, y=290
     |
   [End]              x=320, y=540
```

- Main flow: vertical, all nodes center-aligned at same x
- Branches: alternate path goes RIGHT from decision (exitX=1)
- Rejoin: bring alternate path back to main column with waypoints if needed
- Vertical gap between nodes: at least 60px (edge of node to edge of next)

## Architecture Diagram Templates (Layered Block Style)

**This is the preferred style for architecture diagrams.** It uses a structured block layout
with no connecting arrows, organized into horizontal layers with a left label column and an
optional right-side cross-cutting concerns sidebar.

### Visual Structure

```
+------------------------------------------------------------------+
| [Background: gray #f5f5f5, no stroke]                            |
|                                                                   |
| [Layer    | [Layer Container (blue, opacity=60)         ] [Side  ]|
|  Label    |   [SubGroup A header]    [SubGroup B header] | panel ]|
|  (blue,   |     [item] [item]          [item] [item]    | (red, ]|
|  bold)]   |     [item] [item]          [item] [item]    | dashed|
|           |                                              | opac  ]|
| [Layer    | [Layer Container (blue, opacity=60)         ] | 30)  ]|
|  Label]   |   [SubGroup C]           [SubGroup D]       |       ]|
|           |     [item] [item]          [item] [item]    |       ]|
+------------------------------------------------------------------+
```

### Key Design Principles

1. **Background rectangle** - Gray `#f5f5f5` with `strokeColor=none` covering entire diagram area
2. **Left label column** - Bold blue cells (width=100) naming each layer (e.g., "Scene Layer", "Application Layer")
3. **Layer containers** - Blue `#dae8fc` with `opacity=60`, sits to the right of the label column
4. **Sub-groups within layers** - Blue `#dae8fc` containers with `verticalAlign=top;spacingTop=8;` for header text
5. **Leaf items** - White `#ffffff` with gray border `#999999`, compact size (90-140px wide, 35-60px tall)
6. **Cross-cutting sidebar (optional)** - Vertical panel on the right (e.g., red `#f8cecc` with `opacity=30;dashed=1;`) for cross-cutting concerns like security, monitoring
7. **No edges/arrows** - Pure block diagram; hierarchy is expressed through spatial nesting
8. **Compact packing** - Items tightly arranged in grid within sub-groups, minimal wasted space

### Layout Constants

```
MARGIN = 40                    // outer margin from canvas edge
LABEL_X = MARGIN + 20         // layer label x (60)
LABEL_W = 100                  // layer label width
CONTAINER_X = LABEL_X + LABEL_W + 20   // layer container x (180)
CONTAINER_W = 790              // layer container width
SIDEBAR_X = CONTAINER_X + CONTAINER_W + 20  // sidebar x (990)
SIDEBAR_W = 110                // sidebar width
LAYER_GAP = 20                 // vertical gap between layers
SUBGROUP_PAD = 20              // padding inside layer container to sub-groups
ITEM_GAP_H = 10               // horizontal gap between leaf items
ITEM_GAP_V = 10               // vertical gap between leaf item rows
ITEM_H = 35                   // standard leaf item height
PAGE_W = SIDEBAR_X + SIDEBAR_W + MARGIN   // total page width (~1160)
```

### Background Rectangle
```xml
<mxCell id="background" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="1080" height="700" as="geometry" />
</mxCell>
```

### Layer Label (left column)
```xml
<mxCell id="layer-scenario" value="Scene Layer"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
               fontSize=18;fontStyle=1;verticalAlign=middle;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="60" y="60" width="100" height="110" as="geometry" />
</mxCell>
```

Note: layer label height matches its container height.

### Layer Container (semi-transparent)
```xml
<mxCell id="scenario-container" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;opacity=60;"
        vertex="1" parent="1">
  <mxGeometry x="180" y="60" width="790" height="110" as="geometry" />
</mxCell>
```

### Leaf Item (white with gray border)
```xml
<mxCell id="scenario-office" value="Smart Office"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="85" width="140" height="60" as="geometry" />
</mxCell>
```

### Sub-Group Container (within a layer)
```xml
<mxCell id="app-open" value="Open Applications"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
               fontSize=16;verticalAlign=top;align=center;spacingTop=8;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="210" width="330" height="130" as="geometry" />
</mxCell>
```

Items inside the sub-group:
```xml
<mxCell id="app-workspace" value="Workspace"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="212" y="250" width="95" height="35" as="geometry" />
</mxCell>
<mxCell id="app-management" value="Management"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="317" y="250" width="95" height="35" as="geometry" />
</mxCell>
```

### Cross-Cutting Sidebar (optional, e.g., Security)
```xml
<!-- Sidebar frame (semi-transparent, dashed) -->
<mxCell id="security-frame" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;
               fontSize=16;verticalAlign=middle;align=center;opacity=30;dashed=1;"
        vertex="1" parent="1">
  <mxGeometry x="990" y="60" width="110" height="660" as="geometry" />
</mxCell>

<!-- Sidebar title -->
<mxCell id="security-title" value="Security"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;
               whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#b85450"
        vertex="1" parent="1">
  <mxGeometry x="1015" y="70" width="60" height="30" as="geometry" />
</mxCell>

<!-- Sidebar items (stacked vertically, evenly distributed) -->
<mxCell id="security-permission" value="Permissions"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b85450;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="1000" y="110" width="90" height="135" as="geometry" />
</mxCell>
<mxCell id="security-protection" value="Protection"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b85450;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="1000" y="265" width="90" height="135" as="geometry" />
</mxCell>
```

### Layered Block Layout Calculation

For a diagram with N layers:
```
// Layer positions
layer[0].y = MARGIN + 20                           // first layer y (60)
layer[i].y = layer[i-1].y + layer[i-1].height + LAYER_GAP

// Background covers everything
background.width = SIDEBAR_X + SIDEBAR_W - MARGIN  // 1080
background.height = layer[N-1].y + layer[N-1].height - MARGIN + 20

// Each layer: label + container at same y, same height
label[i].x = LABEL_X                               // 60
label[i].width = LABEL_W                            // 100
label[i].height = layer[i].height
container[i].x = CONTAINER_X                        // 180
container[i].width = CONTAINER_W                    // 790
container[i].height = layer[i].height

// Sub-groups inside container: split container width
// For 2 sub-groups side by side:
subgroup[0].x = container.x + 20
subgroup[0].width = (container.width - 60) / 2      // ~365
subgroup[1].x = subgroup[0].x + subgroup[0].width + 20
subgroup[1].width = subgroup[0].width

// Items inside sub-group: grid layout
// header takes ~40px from top (spacingTop=8 + fontSize=16)
item_start_y = subgroup.y + 40
item[row][col].x = subgroup.x + 12 + col * (item_width + ITEM_GAP_H)
item[row][col].y = item_start_y + row * (ITEM_H + ITEM_GAP_V)

// Sidebar spans full height alongside all layers
sidebar.y = layer[0].y
sidebar.height = layer[N-1].y + layer[N-1].height - layer[0].y
```

### Architecture Diagram with Arrows (Alternative Style)

For simpler diagrams that need to show data flow, use the connected-box style instead:

```
Layer 0 (y=60):    [Client]
Layer 1 (y=200):   [Gateway]
Layer 2 (y=340):   [Service A]  [Service B]  [Service C]
Layer 3 (y=480):   [DB A]       [DB B]       [Cache]
```

With edges connecting them (use `edgeStyle=orthogonalEdgeStyle`).
For N components in a layer:
```
gap = 80
total_width = N * component_width + (N - 1) * gap
start_x = (pageWidth - total_width) / 2
component[i].x = start_x + i * (component_width + gap)
```

## UML Sequence Diagram Templates

### Participant: Actor
```xml
<mxCell id="actor-user" value="User"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;
               fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="40" height="60" as="geometry" />
</mxCell>
```

### Participant: Object (rectangle)
```xml
<mxCell id="obj-frontend" value="Frontend"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="260" y="40" width="120" height="50" as="geometry" />
</mxCell>
```

### Lifeline (dashed vertical line)
```xml
<mxCell id="lifeline-frontend" value=""
        style="html=1;points=[];perimeter=orthogonalPerimeter;outlineConnect=0;
               strokeColor=#999999;strokeWidth=1;dashed=1;"
        vertex="1" parent="1">
  <mxGeometry x="319" y="90" width="1" height="500" as="geometry" />
</mxCell>
```

Note: lifeline x = participant center x (participant.x + participant.width / 2).

### Activation Bar
```xml
<mxCell id="act-frontend-1" value=""
        style="html=1;points=[];perimeter=orthogonalPerimeter;outlineConnect=0;
               fillColor=#f5f5f5;strokeColor=#666666;strokeWidth=1;"
        vertex="1" parent="1">
  <mxGeometry x="314" y="130" width="12" height="60" as="geometry" />
</mxCell>
```

Note: activation x = lifeline.x - 6 (half of activation width).

### Synchronous Message (solid arrow)
```xml
<mxCell id="msg-1" value="request()"
        style="html=1;verticalAlign=bottom;endArrow=block;rounded=0;
               strokeWidth=1;strokeColor=#333333;fontSize=12;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="120" y="140" as="sourcePoint" />
    <mxPoint x="314" y="140" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

### Return Message (dashed arrow)
```xml
<mxCell id="ret-1" value="response"
        style="html=1;verticalAlign=bottom;endArrow=open;dashed=1;rounded=0;
               strokeWidth=1;strokeColor=#333333;fontSize=12;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="314" y="180" as="sourcePoint" />
    <mxPoint x="120" y="180" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

### Sequence Diagram Layout

- Participants spaced 200px apart horizontally
- Messages: each message pair (request + response) takes 50-60px vertical space
- Lifeline height = total messages * 50 + padding
- Activation bars start at first incoming message, end at last outgoing response

```
Participant spacing:  200px
Message vertical gap: 50px
Activation width:     12px
Lifeline starts at:   participant bottom (y + height)
```

## ER Diagram Templates

### Entity Table (using swimlane)
```xml
<mxCell id="tbl-users" value="users"
        style="shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;
               fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;
               fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="220" height="150" as="geometry" />
</mxCell>
```

### Entity using simpler swimlane style
```xml
<mxCell id="tbl-users" value="users"
        style="swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;
               resizeParent=1;resizeParentMax=0;collapsible=0;marginBottom=0;
               fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;html=1;whiteSpace=wrap;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="220" height="150" as="geometry" />
</mxCell>

<!-- PK field -->
<mxCell id="tbl-users-id" value="PK  id: INT"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;
               spacingLeft=4;spacingRight=4;overflow=hidden;
               points=[[0,0.5],[1,0.5]];portConstraint=eastwest;
               fontStyle=1;fontSize=12;html=1;whiteSpace=wrap;"
        vertex="1" parent="tbl-users">
  <mxGeometry y="30" width="220" height="30" as="geometry" />
</mxCell>

<!-- Divider line -->
<mxCell id="tbl-users-div" value=""
        style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;
               spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;
               labelPosition=left;points=[];portConstraint=eastwest;strokeColor=#6c8ebf;"
        vertex="1" parent="tbl-users">
  <mxGeometry y="60" width="220" height="8" as="geometry" />
</mxCell>

<!-- Regular field -->
<mxCell id="tbl-users-name" value="username: VARCHAR(50)"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;
               spacingLeft=4;spacingRight=4;overflow=hidden;
               points=[[0,0.5],[1,0.5]];portConstraint=eastwest;
               fontSize=12;html=1;whiteSpace=wrap;"
        vertex="1" parent="tbl-users">
  <mxGeometry y="68" width="220" height="30" as="geometry" />
</mxCell>

<!-- FK field -->
<mxCell id="tbl-users-email" value="email: VARCHAR(100)"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;
               spacingLeft=4;spacingRight=4;overflow=hidden;
               points=[[0,0.5],[1,0.5]];portConstraint=eastwest;
               fontSize=12;html=1;whiteSpace=wrap;"
        vertex="1" parent="tbl-users">
  <mxGeometry y="98" width="220" height="30" as="geometry" />
</mxCell>
```

**Important for ER tables:**
- Child cells use `parent="tbl-users"` (the table ID), NOT `parent="1"`
- Child y is relative to the parent (starts at 0 inside the container)
- `startSize=30` reserves 30px for the header
- Fields start at y=30, each 30px tall
- Divider at y=60 (after PK fields), height=8
- Table height = startSize + (field_count * 30) + divider_height

### ER Relationship Edge
```xml
<!-- One-to-Many -->
<mxCell id="rel-user-article" value=""
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
               endArrow=ERmany;endFill=0;startArrow=ERmandOne;startFill=0;
               strokeColor=#666666;fontSize=12;"
        edge="1" parent="1" source="tbl-users" target="tbl-articles">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Relationship Arrow Types

| Type | Start Arrow | End Arrow | Notation |
|------|------------|-----------|----------|
| 1:1 mandatory | ERmandOne | ERmandOne | \|--\| |
| 1:N mandatory | ERmandOne | ERmany | \|--< |
| 1:1 optional | ERone | ERone | o\|--\|o |
| 1:N optional | ERone | ERmany | o\|--< |
| M:N | ERmany | ERmany | >--< |

### ER Layout Strategy

Place tables in a grid pattern:
```
[Table A]     [Table B]     [Table C]
  x=100         x=400         x=700
  y=100         y=100         y=100

[Table D]     [Table E]
  x=100         x=400
  y=350         y=350
```

Gap between columns: at least 180px (table width + 80px).
Gap between rows: at least 100px from bottom of tallest table in row.

## Mindmap Templates

### Center Node
```xml
<mxCell id="center" value="Central Topic"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;
               fontSize=18;fontStyle=1;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="410" y="260" width="180" height="80" as="geometry" />
</mxCell>
```

### Branch Node (Level 1)
```xml
<mxCell id="branch-1" value="Branch 1"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
               fontSize=14;fontStyle=1;arcSize=50;"
        vertex="1" parent="1">
  <mxGeometry x="660" y="120" width="140" height="50" as="geometry" />
</mxCell>
```

### Leaf Node (Level 2)
```xml
<mxCell id="leaf-1-1" value="Leaf Item"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;
               fontSize=12;arcSize=50;"
        vertex="1" parent="1">
  <mxGeometry x="860" y="80" width="120" height="40" as="geometry" />
</mxCell>
```

### Mindmap Edge (curved, no arrows)
```xml
<mxCell id="edge-center-b1" value=""
        style="rounded=1;curved=1;html=1;endArrow=none;
               strokeWidth=2;strokeColor=#6c8ebf;"
        edge="1" parent="1" source="center" target="branch-1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Mindmap Layout Strategy

Use radial layout from center. For 4 branches, place them in 4 quadrants:

```
                    [Branch 1]
                   /  |leaf1| |leaf2|
                  /
[Branch 4] --- [CENTER] --- [Branch 2]
  |leaf|          \           |leaf|
                   \
                    [Branch 3]
                     |leaf|
```

**Coordinate calculation for N branches evenly around center:**

```
center_x = pageWidth / 2 - center_width / 2     (e.g., 410 for 1000px page)
center_y = pageHeight / 2 - center_height / 2    (e.g., 260 for 600px page)

For branch i (0-indexed), angle = i * (360 / N) degrees:
  branch_x = center_cx + cos(angle) * radius_1 - branch_width / 2
  branch_y = center_cy + sin(angle) * radius_1 - branch_height / 2

For leaf j of branch i:
  leaf_x = branch_cx + cos(angle) * radius_2 - leaf_width / 2
  leaf_y = branch_cy + (j - mid) * (leaf_height + 10)
```

**Practical 4-branch placement (pageWidth=1000, pageHeight=600):**

| Element | x | y |
|---------|---|---|
| Center | 410 | 260 |
| Branch Right | 660 | 270 |
| Branch Left | 80 | 270 |
| Branch Top | 430 | 60 |
| Branch Bottom | 430 | 440 |

Leaves fan out from their branch, spaced 50px vertically.

**Color scheme per branch** (use different colors for visual distinction):

| Branch | Fill | Stroke |
|--------|------|--------|
| Branch 1 | #dae8fc | #6c8ebf |
| Branch 2 | #d5e8d4 | #82b366 |
| Branch 3 | #fff2cc | #d6b656 |
| Branch 4 | #e1d5e7 | #9673a6 |
| Branch 5 | #f8cecc | #b85450 |

## Network Topology Templates

### Router
```xml
<mxCell id="router" value="Router"
        style="shape=mxgraph.cisco.routers.router;whiteSpace=wrap;html=1;
               fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;fontStyle=1;
               verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" parent="1">
  <mxGeometry x="400" y="160" width="60" height="50" as="geometry" />
</mxCell>
```

### Alternative: Use simple rounded rectangles with icons in label
```xml
<mxCell id="router" value="&lt;b&gt;Router&lt;/b&gt;&lt;br&gt;192.168.1.1"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
               fontSize=12;verticalAlign=middle;spacingTop=0;spacingBottom=0;"
        vertex="1" parent="1">
  <mxGeometry x="370" y="160" width="140" height="60" as="geometry" />
</mxCell>
```

### Switch
```xml
<mxCell id="switch" value="&lt;b&gt;Switch&lt;/b&gt;"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;
               fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="370" y="300" width="140" height="60" as="geometry" />
</mxCell>
```

### Modem / ONT
```xml
<mxCell id="modem" value="&lt;b&gt;Modem / ONT&lt;/b&gt;"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;
               fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="370" y="40" width="140" height="60" as="geometry" />
</mxCell>
```

### End Device (PC, Phone, etc.)
```xml
<mxCell id="device-pc" value="&lt;b&gt;PC&lt;/b&gt;"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;
               fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="440" width="120" height="50" as="geometry" />
</mxCell>
```

### NAS / Server
```xml
<mxCell id="nas" value="&lt;b&gt;NAS&lt;/b&gt;"
        style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;
               fontSize=12;fontStyle=1;boundedLbl=1;backgroundOutline=1;size=10;
               verticalLabelPosition=middle;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="550" y="430" width="100" height="70" as="geometry" />
</mxCell>
```

### Network Edge (solid line, no arrows)
```xml
<mxCell id="edge-modem-router" value=""
        style="rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
               endArrow=none;strokeWidth=2;strokeColor=#333333;"
        edge="1" parent="1" source="modem" target="router">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Wireless Edge (dashed)
```xml
<mxCell id="edge-wifi-phone" value="WiFi"
        style="rounded=1;orthogonalLoop=1;jettySize=auto;html=1;
               endArrow=none;dashed=1;strokeWidth=2;strokeColor=#6c8ebf;fontSize=11;"
        edge="1" parent="1" source="router" target="device-phone">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Network Topology Layout

Hierarchical layers, top-to-bottom:

```
Layer 0 (Internet):    [Modem/ONT]
Layer 1 (Core):        [Router]
Layer 2 (Distribution):[Switch]
Layer 3 (Access):      [PC] [TV] [Phone] [NAS]
```

- Each layer centered horizontally
- Wired connections: solid lines
- Wireless: dashed lines
- Layer gap: 120px vertical

## UML Class Diagram Templates

### Class Box
```xml
<mxCell id="class-user" value="&lt;p style='margin:0px;margin-top:4px;text-align:center;'&gt;&lt;b&gt;User&lt;/b&gt;&lt;/p&gt;&lt;hr size='1'/&gt;&lt;p style='margin:0px;margin-left:4px;'&gt;- id: int&lt;br/&gt;- name: string&lt;br/&gt;- email: string&lt;/p&gt;&lt;hr size='1'/&gt;&lt;p style='margin:0px;margin-left:4px;'&gt;+ login(): bool&lt;br/&gt;+ register(): void&lt;/p&gt;"
        style="verticalAlign=top;align=left;overflow=fill;html=1;whiteSpace=wrap;
               fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="160" as="geometry" />
</mxCell>
```

### Inheritance Arrow (empty triangle)
```xml
<mxCell id="edge-inherit" value=""
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;
               endArrow=block;endFill=0;strokeWidth=1;"
        edge="1" parent="1" source="class-admin" target="class-user">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Association Arrow
```xml
<mxCell id="edge-assoc" value="1..*"
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;
               endArrow=open;endFill=0;strokeWidth=1;fontSize=12;"
        edge="1" parent="1" source="class-user" target="class-order">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Groups / Containers

Use containers to group related components (e.g., "Backend Services"):

```xml
<mxCell id="group-backend" value="Backend Services"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;
               strokeColor=#999999;dashed=1;strokeWidth=2;
               fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=10;
               container=1;collapsible=0;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="200" width="540" height="200" as="geometry" />
</mxCell>

<!-- Child nodes use parent="group-backend" and relative coordinates -->
<mxCell id="svc-1" value="Service A"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
        vertex="1" parent="group-backend">
  <mxGeometry x="30" y="50" width="160" height="60" as="geometry" />
</mxCell>
```

## Common Mistakes to Avoid

1. **Duplicate IDs** - every mxCell must have a unique id
2. **Wrong parent** - standalone nodes use `parent="1"`, ER fields use `parent="table-id"`, group children use `parent="group-id"`
3. **Missing `as="geometry"`** - every mxGeometry must have this attribute
4. **Overlapping nodes** - always calculate and verify bounding boxes
5. **Missing `whiteSpace=wrap;html=1;`** - text will overflow without this
6. **Edges referencing non-existent IDs** - double-check source/target
7. **Coordinates not grid-aligned** - use multiples of 10
8. **Too small font** - minimum fontSize=12, prefer 14
9. **No edge style** - without `edgeStyle=orthogonalEdgeStyle`, edges route randomly
10. **Page too small** - if content exceeds 1200x900, increase pageWidth/pageHeight
