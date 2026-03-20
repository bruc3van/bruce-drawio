# Draw.io Complete XML Examples

These are ready-to-use, tested XML examples demonstrating proper structure, layout, and styling.

## Example 1: Simple Flowchart (Order Process)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="drawio-skill" version="21.0.0" type="device">
  <diagram name="Order Flow" id="order-flow">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1"
                   connect="1" arrows="1" fold="1" page="1" pageScale="1"
                   pageWidth="1000" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Start -->
        <mxCell id="start" value="User Places Order"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;fontStyle=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="340" y="40" width="180" height="60" as="geometry" />
        </mxCell>

        <!-- Process: Create Order -->
        <mxCell id="process-create" value="Create Order Record"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="350" y="160" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- Decision: Stock Check -->
        <mxCell id="decision-stock" value="In Stock?"
                style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="350" y="280" width="160" height="80" as="geometry" />
        </mxCell>

        <!-- Process: Payment -->
        <mxCell id="process-pay" value="Process Payment"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="350" y="420" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- Error: Out of Stock -->
        <mxCell id="error-stock" value="Notify: Out of Stock"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="600" y="290" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- Process: Ship -->
        <mxCell id="process-ship" value="Ship Order"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="350" y="540" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- End -->
        <mxCell id="end" value="Order Complete"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;fontStyle=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="350" y="660" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="start" target="process-create">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="process-create" target="decision-stock">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" value="Yes"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=12;fontStyle=1;"
                edge="1" parent="1" source="decision-stock" target="process-pay">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" value="No"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontSize=12;fontStyle=1;"
                edge="1" parent="1" source="decision-stock" target="error-stock">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e5" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="process-pay" target="process-ship">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="process-ship" target="end">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Example 2: Microservice Architecture

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="drawio-skill" version="21.0.0" type="device">
  <diagram name="Architecture" id="arch-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1"
                   connect="1" arrows="1" fold="1" page="1" pageScale="1"
                   pageWidth="1200" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Layer 0: Client -->
        <mxCell id="client" value="&lt;b&gt;Web / Mobile Client&lt;/b&gt;"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="440" y="40" width="180" height="60" as="geometry" />
        </mxCell>

        <!-- Layer 1: Gateway -->
        <mxCell id="gateway" value="&lt;b&gt;API Gateway (Nginx)&lt;/b&gt;"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="440" y="170" width="180" height="60" as="geometry" />
        </mxCell>

        <!-- Layer 2: Services -->
        <mxCell id="svc-user" value="&lt;b&gt;User Service&lt;/b&gt;"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="160" y="320" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="svc-order" value="&lt;b&gt;Order Service&lt;/b&gt;"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="440" y="320" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="svc-pay" value="&lt;b&gt;Payment Service&lt;/b&gt;"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="720" y="320" width="160" height="60" as="geometry" />
        </mxCell>

        <!-- Layer 3: Data -->
        <mxCell id="db-user" value="&lt;b&gt;MySQL&lt;/b&gt;&lt;br&gt;Users"
                style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;boundedLbl=1;backgroundOutline=1;size=10;"
                vertex="1" parent="1">
          <mxGeometry x="170" y="470" width="140" height="80" as="geometry" />
        </mxCell>
        <mxCell id="db-order" value="&lt;b&gt;MySQL&lt;/b&gt;&lt;br&gt;Orders"
                style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;boundedLbl=1;backgroundOutline=1;size=10;"
                vertex="1" parent="1">
          <mxGeometry x="450" y="470" width="140" height="80" as="geometry" />
        </mxCell>
        <mxCell id="cache" value="&lt;b&gt;Redis&lt;/b&gt;&lt;br&gt;Cache"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;fontStyle=1;"
                vertex="1" parent="1">
          <mxGeometry x="730" y="480" width="140" height="60" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="e-client-gw" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="client" target="gateway">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-gw-user" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;exitX=0.25;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="gateway" target="svc-user">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-gw-order" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="gateway" target="svc-order">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-gw-pay" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;exitX=0.75;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="gateway" target="svc-pay">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-user-db" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="svc-user" target="db-user">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-order-db" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="svc-order" target="db-order">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-order-cache" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="svc-order" target="cache">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e-order-pay" value="call"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontSize=11;"
                edge="1" parent="1" source="svc-order" target="svc-pay">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Example 3: Mindmap (AI Agent)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="drawio-skill" version="21.0.0" type="device">
  <diagram name="AI Agent Mindmap" id="mindmap-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1"
                   connect="1" arrows="1" fold="1" page="1" pageScale="1"
                   pageWidth="1400" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Center -->
        <mxCell id="center" value="AI Agent"
                style="ellipse;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontSize=20;fontStyle=1;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="580" y="360" width="180" height="80" as="geometry" />
        </mxCell>

        <!-- Branch 1: Capabilities (right) -->
        <mxCell id="b1" value="Core Capabilities"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="880" y="200" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell id="b1-l1" value="Perception"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="1100" y="150" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b1-l2" value="Reasoning"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="1100" y="200" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b1-l3" value="Action"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="1100" y="250" width="120" height="40" as="geometry" />
        </mxCell>

        <!-- Branch 2: Applications (bottom-right) -->
        <mxCell id="b2" value="Applications"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;fontStyle=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="880" y="500" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell id="b2-l1" value="Customer Service"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="1100" y="460" width="130" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b2-l2" value="Programming"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="1100" y="510" width="130" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b2-l3" value="Research"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="1100" y="560" width="130" height="40" as="geometry" />
        </mxCell>

        <!-- Branch 3: Tech Stack (left) -->
        <mxCell id="b3" value="Tech Stack"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;fontStyle=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="280" y="200" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell id="b3-l1" value="LLM"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="150" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b3-l2" value="RAG"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="200" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b3-l3" value="Tool Calling"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="250" width="120" height="40" as="geometry" />
        </mxCell>

        <!-- Branch 4: Challenges (bottom-left) -->
        <mxCell id="b4" value="Challenges"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=14;fontStyle=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="280" y="500" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell id="b4-l1" value="Hallucination"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="460" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b4-l2" value="Safety"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="510" width="120" height="40" as="geometry" />
        </mxCell>
        <mxCell id="b4-l3" value="Cost"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="560" width="120" height="40" as="geometry" />
        </mxCell>

        <!-- Curved edges from center to branches -->
        <mxCell id="ec1" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=3;strokeColor=#6c8ebf;"
                edge="1" parent="1" source="center" target="b1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="ec2" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=3;strokeColor=#82b366;"
                edge="1" parent="1" source="center" target="b2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="ec3" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=3;strokeColor=#d6b656;"
                edge="1" parent="1" source="center" target="b3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="ec4" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=3;strokeColor=#9673a6;"
                edge="1" parent="1" source="center" target="b4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Branch to leaf edges -->
        <mxCell id="el1-1" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#6c8ebf;"
                edge="1" parent="1" source="b1" target="b1-l1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el1-2" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#6c8ebf;"
                edge="1" parent="1" source="b1" target="b1-l2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el1-3" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#6c8ebf;"
                edge="1" parent="1" source="b1" target="b1-l3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el2-1" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#82b366;"
                edge="1" parent="1" source="b2" target="b2-l1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el2-2" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#82b366;"
                edge="1" parent="1" source="b2" target="b2-l2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el2-3" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#82b366;"
                edge="1" parent="1" source="b2" target="b2-l3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el3-1" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#d6b656;"
                edge="1" parent="1" source="b3" target="b3-l1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el3-2" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#d6b656;"
                edge="1" parent="1" source="b3" target="b3-l2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el3-3" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#d6b656;"
                edge="1" parent="1" source="b3" target="b3-l3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el4-1" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#9673a6;"
                edge="1" parent="1" source="b4" target="b4-l1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el4-2" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#9673a6;"
                edge="1" parent="1" source="b4" target="b4-l2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="el4-3" style="rounded=1;curved=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#9673a6;"
                edge="1" parent="1" source="b4" target="b4-l3"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Example 4: ER Diagram (Blog System)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="drawio-skill" version="21.0.0" type="device">
  <diagram name="Blog ER" id="er-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1"
                   connect="1" arrows="1" fold="1" page="1" pageScale="1"
                   pageWidth="1200" pageHeight="700" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Users table -->
        <mxCell id="tbl-users" value="users"
                style="swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;collapsible=0;marginBottom=0;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;html=1;whiteSpace=wrap;"
                vertex="1" parent="1">
          <mxGeometry x="100" y="120" width="220" height="188" as="geometry" />
        </mxCell>
        <mxCell id="tbl-users-id" value="PK  id: INT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=1;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-users">
          <mxGeometry y="30" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-users-div" value=""
                style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest;strokeColor=#6c8ebf;"
                vertex="1" parent="tbl-users">
          <mxGeometry y="60" width="220" height="8" as="geometry" />
        </mxCell>
        <mxCell id="tbl-users-name" value="username: VARCHAR(50)"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-users">
          <mxGeometry y="68" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-users-email" value="email: VARCHAR(100)"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-users">
          <mxGeometry y="98" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-users-created" value="created_at: DATETIME"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-users">
          <mxGeometry y="128" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-users-pwd" value="password_hash: VARCHAR(255)"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-users">
          <mxGeometry y="158" width="220" height="30" as="geometry" />
        </mxCell>

        <!-- Articles table -->
        <mxCell id="tbl-articles" value="articles"
                style="swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;collapsible=0;marginBottom=0;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;html=1;whiteSpace=wrap;"
                vertex="1" parent="1">
          <mxGeometry x="460" y="120" width="220" height="188" as="geometry" />
        </mxCell>
        <mxCell id="tbl-articles-id" value="PK  id: INT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=1;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-articles">
          <mxGeometry y="30" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-articles-div" value=""
                style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest;strokeColor=#82b366;"
                vertex="1" parent="tbl-articles">
          <mxGeometry y="60" width="220" height="8" as="geometry" />
        </mxCell>
        <mxCell id="tbl-articles-title" value="title: VARCHAR(200)"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-articles">
          <mxGeometry y="68" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-articles-content" value="content: TEXT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-articles">
          <mxGeometry y="98" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-articles-author" value="FK  author_id: INT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=2;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-articles">
          <mxGeometry y="128" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-articles-created" value="created_at: DATETIME"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-articles">
          <mxGeometry y="158" width="220" height="30" as="geometry" />
        </mxCell>

        <!-- Comments table -->
        <mxCell id="tbl-comments" value="comments"
                style="swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;collapsible=0;marginBottom=0;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;html=1;whiteSpace=wrap;"
                vertex="1" parent="1">
          <mxGeometry x="820" y="120" width="220" height="188" as="geometry" />
        </mxCell>
        <mxCell id="tbl-comments-id" value="PK  id: INT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=1;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-comments">
          <mxGeometry y="30" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-comments-div" value=""
                style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest;strokeColor=#d6b656;"
                vertex="1" parent="tbl-comments">
          <mxGeometry y="60" width="220" height="8" as="geometry" />
        </mxCell>
        <mxCell id="tbl-comments-content" value="content: TEXT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-comments">
          <mxGeometry y="68" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-comments-article" value="FK  article_id: INT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=2;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-comments">
          <mxGeometry y="98" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-comments-user" value="FK  user_id: INT"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=2;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-comments">
          <mxGeometry y="128" width="220" height="30" as="geometry" />
        </mxCell>
        <mxCell id="tbl-comments-created" value="created_at: DATETIME"
                style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;html=1;whiteSpace=wrap;"
                vertex="1" parent="tbl-comments">
          <mxGeometry y="158" width="220" height="30" as="geometry" />
        </mxCell>

        <!-- Relationships -->
        <mxCell id="rel-user-article" value="1:N"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;endFill=0;startArrow=ERmandOne;startFill=0;strokeColor=#666666;fontSize=12;"
                edge="1" parent="1" source="tbl-users" target="tbl-articles">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="rel-article-comment" value="1:N"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;endFill=0;startArrow=ERmandOne;startFill=0;strokeColor=#666666;fontSize=12;"
                edge="1" parent="1" source="tbl-articles" target="tbl-comments">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="rel-user-comment" value="1:N"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;endFill=0;startArrow=ERmandOne;startFill=0;strokeColor=#666666;fontSize=12;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;"
                edge="1" parent="1" source="tbl-users" target="tbl-comments">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="210" y="400" />
              <mxPoint x="930" y="400" />
            </Array>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Color Palette Reference

| Purpose | Fill | Stroke |
|---------|------|--------|
| Start/End/Success (green) | #d5e8d4 | #82b366 |
| Process/Service (blue) | #dae8fc | #6c8ebf |
| Decision/Warning (yellow) | #fff2cc | #d6b656 |
| Error/Client (red) | #f8cecc | #b85450 |
| Subprocess/Storage (purple) | #e1d5e7 | #9673a6 |
| Neutral/Default (gray) | #f5f5f5 | #666666 |
| Accent/Center (dark blue) | #1ba1e2 | #006EAF |
