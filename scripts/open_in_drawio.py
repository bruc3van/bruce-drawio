#!/usr/bin/env python3
"""Turn a .drawio file into an app.diagrams.net URL that opens it directly in the browser.

The diagram XML is URL-encoded, raw-deflated and base64'd, then appended to
https://app.diagrams.net/ as a `#R<data>` fragment. draw.io decodes that fragment
client-side, so nothing is uploaded to a server and no account is needed.

Usage:
    python open_in_drawio.py diagram.drawio              # print the URL
    python open_in_drawio.py diagram.drawio --open       # print it and launch the browser
    python open_in_drawio.py diagram.drawio --html a.html  # write a click-to-open launcher
    cat diagram.drawio | python open_in_drawio.py -      # read from stdin

Exit codes: 0 ok, 1 usage/IO error.
"""

import argparse
import base64
import html
import os
import sys
import tempfile
import webbrowser
import zlib
from urllib.parse import quote

BASE_URL = "https://app.diagrams.net/"

# ShellExecute (Windows) and some desktop handlers truncate very long URLs.
# Above this length we hand the browser a local launcher page instead.
DIRECT_URL_LIMIT = 1800


def encode_diagram(xml: str) -> str:
    """Return the `#R` payload: base64(deflateRaw(encodeURIComponent(xml)))."""
    # Matches JS encodeURIComponent: unreserved set is A-Za-z0-9 and -_.~!*'()
    encoded = quote(xml, safe="!*'()")
    deflater = zlib.compressobj(9, zlib.DEFLATED, -15)
    compressed = deflater.compress(encoded.encode("utf-8")) + deflater.flush()
    return base64.b64encode(compressed).decode("ascii")


def build_url(xml: str, title: str = "") -> str:
    payload = encode_diagram(xml)
    query = "?title=" + quote(title, safe="!*'()") if title else ""
    return f"{BASE_URL}{query}#R{payload}"


def write_launcher(url: str, path: str, title: str) -> str:
    """Write a tiny HTML page that redirects to `url`, and return its path."""
    safe_url = html.escape(url, quote=True)
    safe_title = html.escape(title or "diagram", quote=True)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Open {safe_title} in draw.io</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 4rem auto; max-width: 40rem;
         line-height: 1.6; color: #222; }}
  a.btn {{ display: inline-block; padding: .7rem 1.4rem; background: #f08705;
          color: #fff; border-radius: 6px; text-decoration: none; font-weight: 600; }}
</style>
</head>
<body>
  <h1>Opening {safe_title} in draw.io&hellip;</h1>
  <p>If nothing happens, click the button below.</p>
  <p><a class="btn" id="go" href="{safe_url}">Open in draw.io</a></p>
  <script>location.replace(document.getElementById('go').href);</script>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an app.diagrams.net link for a .drawio file."
    )
    parser.add_argument("file", help="path to the .drawio file, or - for stdin")
    parser.add_argument("--open", action="store_true", dest="open_browser",
                        help="launch the default browser on the generated link")
    parser.add_argument("--html", metavar="PATH",
                        help="write a click-to-open launcher page to PATH")
    parser.add_argument("--title", default="",
                        help="file name shown in draw.io (defaults to the input file name)")
    args = parser.parse_args(argv)

    if args.file == "-":
        # Read bytes, not sys.stdin: the console encoding is not UTF-8 on Windows.
        xml = sys.stdin.buffer.read().decode("utf-8")
        title = args.title
    else:
        if not os.path.isfile(args.file):
            print(f"error: file not found: {args.file}", file=sys.stderr)
            return 1
        with open(args.file, "r", encoding="utf-8") as fh:
            xml = fh.read()
        title = args.title or os.path.basename(args.file)

    xml = xml.strip()
    if not xml:
        print("error: diagram is empty", file=sys.stderr)
        return 1
    if "<mxfile" not in xml and "<mxGraphModel" not in xml:
        print("error: not a draw.io diagram (no <mxfile> or <mxGraphModel> found)",
              file=sys.stderr)
        return 1

    url = build_url(xml, title)

    launcher = args.html
    if launcher:
        write_launcher(url, launcher, title)
    elif args.open_browser and len(url) > DIRECT_URL_LIMIT:
        # Long fragment: go through a local page so the OS URL handler can't truncate it.
        fd, launcher = tempfile.mkstemp(prefix="open-in-drawio-", suffix=".html")
        os.close(fd)
        write_launcher(url, launcher, title)

    print(url)
    if launcher:
        print(f"launcher: {launcher}", file=sys.stderr)

    if args.open_browser:
        target = url
        if launcher:
            target = "file:///" + os.path.abspath(launcher).replace("\\", "/")
        if not webbrowser.open(target):
            print("error: could not launch a browser; open the link above manually",
                  file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
