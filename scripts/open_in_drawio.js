#!/usr/bin/env node
/**
 * Node fallback for open_in_drawio.py — same CLI, same output.
 *
 * Turns a .drawio file into an app.diagrams.net URL: the XML is URL-encoded,
 * raw-deflated and base64'd into a `#R<data>` fragment that draw.io decodes
 * client-side, so nothing is uploaded and no account is needed.
 *
 *   node open_in_drawio.js diagram.drawio
 *   node open_in_drawio.js diagram.drawio --open
 *   node open_in_drawio.js diagram.drawio --html launcher.html
 *   node open_in_drawio.js -            # read from stdin
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const zlib = require('zlib');
const { spawn } = require('child_process');

const BASE_URL = 'https://app.diagrams.net/';
// ShellExecute (Windows) and some desktop handlers truncate very long URLs.
const DIRECT_URL_LIMIT = 1800;

function parseArgs(argv) {
    const opts = { file: null, open: false, html: null, title: '' };
    for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--open') opts.open = true;
        else if (arg === '--html') opts.html = argv[++i];
        else if (arg === '--title') opts.title = argv[++i] || '';
        else if (arg === '-h' || arg === '--help') opts.help = true;
        else if (!opts.file) opts.file = arg;
    }
    return opts;
}

function buildUrl(xml, title) {
    const compressed = zlib.deflateRawSync(Buffer.from(encodeURIComponent(xml), 'utf8'), { level: 9 });
    const query = title ? '?title=' + encodeURIComponent(title) : '';
    return `${BASE_URL}${query}#R${compressed.toString('base64')}`;
}

function escapeHtml(str) {
    return str.replace(/[&<>"']/g, (c) => (
        { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
}

function writeLauncher(url, filePath, title) {
    const safeUrl = escapeHtml(url);
    const safeTitle = escapeHtml(title || 'diagram');
    const page = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Open ${safeTitle} in draw.io</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 4rem auto; max-width: 40rem;
         line-height: 1.6; color: #222; }
  a.btn { display: inline-block; padding: .7rem 1.4rem; background: #f08705;
          color: #fff; border-radius: 6px; text-decoration: none; font-weight: 600; }
</style>
</head>
<body>
  <h1>Opening ${safeTitle} in draw.io&hellip;</h1>
  <p>If nothing happens, click the button below.</p>
  <p><a class="btn" id="go" href="${safeUrl}">Open in draw.io</a></p>
  <script>location.replace(document.getElementById('go').href);</script>
</body>
</html>
`;
    fs.writeFileSync(filePath, page, 'utf8');
    return filePath;
}

function openInBrowser(target) {
    const platform = process.platform;
    if (platform === 'win32') {
        // `start` is a cmd builtin; the empty "" is the window title placeholder.
        spawn('cmd', ['/c', 'start', '""', target], { detached: true, stdio: 'ignore' }).unref();
    } else if (platform === 'darwin') {
        spawn('open', [target], { detached: true, stdio: 'ignore' }).unref();
    } else {
        spawn('xdg-open', [target], { detached: true, stdio: 'ignore' }).unref();
    }
}

function run(xml, opts) {
    xml = xml.trim();
    if (!xml) {
        console.error('error: diagram is empty');
        process.exit(1);
    }
    if (!xml.includes('<mxfile') && !xml.includes('<mxGraphModel')) {
        console.error('error: not a draw.io diagram (no <mxfile> or <mxGraphModel> found)');
        process.exit(1);
    }

    const title = opts.title || (opts.file === '-' ? '' : path.basename(opts.file));
    const url = buildUrl(xml, title);

    let launcher = opts.html || null;
    if (launcher) {
        writeLauncher(url, launcher, title);
    } else if (opts.open && url.length > DIRECT_URL_LIMIT) {
        launcher = path.join(os.tmpdir(), `open-in-drawio-${Date.now()}.html`);
        writeLauncher(url, launcher, title);
    }

    console.log(url);
    if (launcher) console.error(`launcher: ${launcher}`);

    if (opts.open) {
        openInBrowser(launcher ? 'file:///' + path.resolve(launcher).replace(/\\/g, '/') : url);
    }
}

function main() {
    const opts = parseArgs(process.argv.slice(2));
    if (opts.help || !opts.file) {
        console.error('usage: node open_in_drawio.js <file.drawio|-> [--open] [--html PATH] [--title NAME]');
        process.exit(opts.help ? 0 : 1);
    }

    if (opts.file === '-') {
        const chunks = [];
        process.stdin.on('data', (c) => chunks.push(c));
        process.stdin.on('end', () => run(Buffer.concat(chunks).toString('utf8'), opts));
    } else {
        if (!fs.existsSync(opts.file)) {
            console.error(`error: file not found: ${opts.file}`);
            process.exit(1);
        }
        run(fs.readFileSync(opts.file, 'utf8'), opts);
    }
}

main();
