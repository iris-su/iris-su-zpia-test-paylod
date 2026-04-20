"""
XPIA Test Harness - Local HTTP Server

Serves HTML payloads from the ./payloads/ directory.
Payloads auto-refresh on every request (no restart needed).

Usage:
    python server.py                  # default port 8080
    python server.py --port 9090      # custom port

Browse http://localhost:8080 for payload index.
"""

import http.server
import os
import argparse
from pathlib import Path

PAYLOADS_DIR = Path(__file__).parent / "payloads"


class XPIAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PAYLOADS_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_index()
        else:
            super().do_GET()

    def send_index(self):
        """Auto-generated index listing all payload files."""
        files = sorted(PAYLOADS_DIR.glob("*.html"))
        rows = ""
        for f in files:
            name = f.stem
            # Read first line of file as description (strip HTML tags)
            first_line = ""
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    for line in fh:
                        stripped = line.strip()
                        if stripped.startswith("<!-- ") and stripped.endswith(" -->"):
                            first_line = stripped[5:-4]
                            break
            except Exception:
                pass
            desc = first_line or "No description"
            url = f"http://localhost:{self.server.server_port}/{f.name}"
            rows += f"""
            <tr>
                <td><a href="/{f.name}">{name}</a></td>
                <td>{desc}</td>
                <td><code>{url}</code></td>
                <td><button onclick="navigator.clipboard.writeText('{url}')">Copy URL</button></td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html><head><title>XPIA Test Harness</title>
<style>
    body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    code {{ background: #eee; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }}
    button {{ cursor: pointer; padding: 4px 8px; }}
    h1 {{ color: #333; }}
    .hint {{ color: #666; font-size: 0.9em; margin-bottom: 1.5rem; }}
</style></head><body>
<h1>XPIA Test Payloads</h1>
<p class="hint">Add/edit .html files in <code>payloads/</code> &mdash; changes appear instantly on refresh. 
Use the first HTML comment <code>&lt;!-- description --&gt;</code> as a description.</p>
<table>
    <tr><th>Payload</th><th>Description</th><th>URL</th><th></th></tr>
    {rows}
</table>
<p><strong>{len(files)}</strong> payload(s) found.</p>
</body></html>"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def end_headers(self):
        # Disable caching so edits show up immediately
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description="XPIA Test Harness Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on (default: 8080)")
    args = parser.parse_args()

    os.makedirs(PAYLOADS_DIR, exist_ok=True)

    server = http.server.HTTPServer(("localhost", args.port), XPIAHandler)
    print(f"\n  XPIA Test Harness running at http://localhost:{args.port}")
    print(f"  Serving payloads from: {PAYLOADS_DIR.resolve()}")
    print(f"  Edit/add .html files in payloads/ — changes appear instantly.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
