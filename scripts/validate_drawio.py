#!/usr/bin/env python3
"""Mechanically validate a .drawio file before exporting or delivering it.

Catches the rendering bugs a human re-read reliably misses: malformed XML,
duplicate IDs, dangling edge endpoints, missing as="geometry", literal \\n in
labels, partially overlapping nodes, content spilling off the page.

Usage:
    python validate_drawio.py diagram.drawio
    python validate_drawio.py diagram.drawio --quiet   # only print problems

Exit codes: 0 clean (warnings allowed), 1 errors found, 2 file/parse failure.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

BACKSLASH_N = chr(92) + "n"

# Shapes that legitimately hold other cells inside their bounding box, so a
# containment relationship with them is nesting rather than a collision.
CONTAINER_HINTS = ("swimlane", "group", "childLayout=", "container=1")


def parse_style(style: str) -> dict:
    """Split a draw.io style string into a key -> value dict."""
    out = {}
    for part in (style or "").split(";"):
        part = part.strip()
        if not part:
            continue
        key, sep, value = part.partition("=")
        out[key.strip()] = value.strip() if sep else ""
    return out


def geometry_of(cell):
    geo = cell.find("mxGeometry")
    if geo is None:
        return None
    try:
        return {
            "x": float(geo.get("x", 0)),
            "y": float(geo.get("y", 0)),
            "w": float(geo.get("width", 0)),
            "h": float(geo.get("height", 0)),
            "as": geo.get("as"),
            "raw": geo,
        }
    except ValueError:
        return None


def boxes_overlap(a, b) -> bool:
    """True only for a partial overlap - full containment is nesting, not a bug."""
    if a["w"] <= 0 or a["h"] <= 0 or b["w"] <= 0 or b["h"] <= 0:
        return False
    ax2, ay2 = a["x"] + a["w"], a["y"] + a["h"]
    bx2, by2 = b["x"] + b["w"], b["y"] + b["h"]
    if ax2 <= b["x"] or bx2 <= a["x"] or ay2 <= b["y"] or by2 <= a["y"]:
        return False  # disjoint
    a_in_b = a["x"] >= b["x"] and a["y"] >= b["y"] and ax2 <= bx2 and ay2 <= by2
    b_in_a = b["x"] >= a["x"] and b["y"] >= a["y"] and bx2 <= ax2 and by2 <= ay2
    return not (a_in_b or b_in_a)


def looks_like_container(cell) -> bool:
    style = cell.get("style", "") or ""
    return any(hint in style for hint in CONTAINER_HINTS)


def validate(path: str):
    errors, warnings = [], []

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML is not well-formed: {exc}"], []
    except OSError as exc:
        return [f"cannot read file: {exc}"], []

    root_el = tree.getroot()
    if root_el.tag != "mxfile":
        errors.append(f"root element is <{root_el.tag}>, expected <mxfile>")

    diagrams = root_el.findall("diagram")
    if not diagrams:
        errors.append("no <diagram> element found")
        return errors, warnings

    seen_ids = defaultdict(list)

    for d_index, diagram in enumerate(diagrams):
        name = diagram.get("name") or f"#{d_index}"
        model = diagram.find("mxGraphModel")
        if model is None:
            errors.append(f"[{name}] <diagram> has no <mxGraphModel> "
                          "(compressed diagrams are not supported - write plain XML)")
            continue
        root = model.find("root")
        if root is None:
            errors.append(f"[{name}] <mxGraphModel> has no <root>")
            continue

        cells = root.findall("mxCell")
        by_id = {}
        for cell in cells:
            cid = cell.get("id")
            if cid is None:
                errors.append(f"[{name}] an mxCell has no id attribute")
                continue
            seen_ids[cid].append(name)
            by_id[cid] = cell

        for cid, where in seen_ids.items():
            if len(where) > 1:
                errors.append(f"duplicate id {cid!r} (used {len(where)} times)")
        seen_ids.clear()

        for reserved in ("0", "1"):
            if reserved not in by_id:
                errors.append(f"[{name}] missing reserved root cell id=\"{reserved}\"")

        page_w = float(model.get("pageWidth", 0) or 0)
        page_h = float(model.get("pageHeight", 0) or 0)
        max_x = max_y = 0.0

        siblings = defaultdict(list)

        for cell in cells:
            cid = cell.get("id")
            if cid in (None, "0"):
                continue

            parent = cell.get("parent")
            if parent is None:
                errors.append(f"[{name}] cell {cid!r} has no parent attribute")
            elif parent not in by_id:
                errors.append(f"[{name}] cell {cid!r} has parent {parent!r}, which does not exist")

            is_vertex = cell.get("vertex") == "1"
            is_edge = cell.get("edge") == "1"

            if is_edge:
                for end in ("source", "target"):
                    ref = cell.get(end)
                    if ref is not None and ref not in by_id:
                        errors.append(f"[{name}] edge {cid!r} has {end}={ref!r}, "
                                      "which is not an existing cell")

            geo = geometry_of(cell)
            if (is_vertex or is_edge) and geo is None:
                if cell.find("mxGeometry") is None:
                    errors.append(f"[{name}] cell {cid!r} has no <mxGeometry>")
                else:
                    errors.append(f"[{name}] cell {cid!r} has a non-numeric <mxGeometry>")
            elif geo is not None and geo["as"] != "geometry":
                errors.append(f"[{name}] cell {cid!r}: <mxGeometry> is missing as=\"geometry\"")

            value = cell.get("value") or ""
            if BACKSLASH_N in value:
                errors.append(f"[{name}] cell {cid!r} has a literal {BACKSLASH_N} in value - "
                              "use &#xa; for a real line break")

            if is_vertex:
                style = parse_style(cell.get("style", ""))
                if "text" not in style and "line" not in style:
                    if style.get("whiteSpace") != "wrap":
                        warnings.append(f"[{name}] cell {cid!r} is missing whiteSpace=wrap "
                                        "- long labels will overflow")
                    if style.get("html") != "1":
                        warnings.append(f"[{name}] cell {cid!r} is missing html=1")
                font = style.get("fontSize")
                if font:
                    try:
                        if float(font) < 12:
                            warnings.append(f"[{name}] cell {cid!r} uses fontSize={font} "
                                            "- minimum 12, prefer 14")
                    except ValueError:
                        pass

                if geo is not None:
                    for axis in ("x", "y", "w", "h"):
                        if geo[axis] != int(geo[axis]):
                            warnings.append(f"[{name}] cell {cid!r} has a fractional "
                                            f"{axis}={geo[axis]} - round to an integer")
                    if parent in ("1", None):
                        max_x = max(max_x, geo["x"] + geo["w"])
                        max_y = max(max_y, geo["y"] + geo["h"])
                    if not looks_like_container(cell):
                        siblings[parent].append((cid, geo))

        for parent, items in siblings.items():
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    (id_a, box_a), (id_b, box_b) = items[i], items[j]
                    if boxes_overlap(box_a, box_b):
                        errors.append(
                            f"[{name}] cells {id_a!r} and {id_b!r} partially overlap "
                            f"({box_a['x']:g},{box_a['y']:g},{box_a['w']:g}x{box_a['h']:g} vs "
                            f"{box_b['x']:g},{box_b['y']:g},{box_b['w']:g}x{box_b['h']:g})"
                        )

        if page_w and max_x > page_w:
            warnings.append(f"[{name}] content extends to x={max_x:g} but pageWidth={page_w:g} "
                            "- increase pageWidth")
        if page_h and max_y > page_h:
            warnings.append(f"[{name}] content extends to y={max_y:g} but pageHeight={page_h:g} "
                            "- increase pageHeight")

    return errors, warnings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate a .drawio file.")
    parser.add_argument("file", help="path to the .drawio file")
    parser.add_argument("--quiet", action="store_true",
                        help="print nothing when the file is clean")
    args = parser.parse_args(argv)

    errors, warnings = validate(args.file)

    for msg in errors:
        print(f"ERROR: {msg}")
    for msg in warnings:
        print(f"WARN:  {msg}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) - fix the errors "
              "in the XML before exporting.")
        return 1
    if not args.quiet:
        if warnings:
            print(f"\nOK with {len(warnings)} warning(s).")
        else:
            print("OK - no problems found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
