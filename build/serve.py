"""
The dev server for this project. One port, always. Port 8000.

Why this exists
---------------
`python3 -m http.server` sends **no cache headers at all**, so browsers hold
`scripts.js` and `styles.css` hard and a refresh keeps showing the old file.
The project worked around that by serving on a fresh port every single time,
which meant the URL moved constantly and open tabs, bookmarks and half-typed
addresses all went stale. Ahmed asked for one stable address, which is the
right call — the port bumping was treating the symptom.

This serves the same directory with `Cache-Control: no-store` on every
response, so the browser is told, correctly, never to keep any of it. A plain
refresh then always shows the current build and the address never changes.

That makes the old "USE A FRESH PORT" rule obsolete. Use this instead.

Behaviour worth knowing
-----------------------
- Binds 127.0.0.1 only. Nothing here should be reachable from the network.
- `SO_REUSEADDR`, so restarting immediately after a Ctrl-C does not trip over
  the socket's TIME_WAIT and send you hunting for another port.
- If the port is already serving THIS project it says so and exits 0 — running
  it twice is harmless and idempotent.
- If the port is taken by something else it fails loudly rather than quietly
  picking a different one. Silently moving is exactly the behaviour this
  script exists to stop.
- Serves from `static-export/` regardless of the directory it is invoked from,
  so "what is this server rooted at?" stops being a question.

Usage
-----
    python3 build/serve.py              # foreground, Ctrl-C to stop
    python3 build/serve.py --port 8100  # only if 8000 is genuinely unavailable
"""
import argparse
import contextlib
import functools
import http.server
import os
import socket
import socketserver
import sys
import urllib.request

PORT = 8000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = os.path.join(ROOT, "static-export")

# A response this server always sends, so a running instance can be recognised
# as ours rather than as some unrelated thing squatting on the port.
BANNER = "jaad-static-dev"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # The entire point of this file. `no-store` is stronger than
        # `no-cache`: no-cache permits storing and revalidating, no-store
        # forbids keeping a copy at all, which is what makes a plain refresh
        # reliable for CSS and JS.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Dev-Server", BANNER)
        super().end_headers()

    def log_message(self, fmt, *args):
        # Default logging prints a line per asset; a page here pulls ~40.
        # Errors still matter, so keep 4xx/5xx and drop the rest.
        status = str(args[1]) if len(args) > 1 else ""
        if status.startswith(("4", "5")):
            super().log_message(fmt, *args)


class Server(socketserver.ThreadingTCPServer):
    # Threaded: a single-threaded server deadlocks the moment a page requests
    # a second asset while the first is still being written, which with 40-odd
    # assets per page is immediate.
    daemon_threads = True
    allow_reuse_address = True


def already_ours(port):
    """True when the port is serving THIS project already."""
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/", method="HEAD")
        with urllib.request.urlopen(req, timeout=2) as r:
            return r.headers.get("X-Dev-Server") == BANNER
    except Exception:                                  # noqa: BLE001
        return False


def port_is_free(port):
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=PORT)
    args = ap.parse_args(argv)
    port = args.port

    if not os.path.isdir(EXPORT):
        sys.exit(f"static-export not found at {EXPORT}")

    if not port_is_free(port):
        if already_ours(port):
            print(f"already serving this project on http://localhost:{port} — reusing it")
            return 0
        sys.exit(
            f"port {port} is in use by something that is not this server.\n"
            f"Stop it (lsof -ti tcp:{port} | xargs kill) or pass --port. "
            f"Refusing to pick a different port silently."
        )

    handler = functools.partial(Handler, directory=EXPORT)
    with Server(("127.0.0.1", port), handler) as httpd:
        print(f"serving {EXPORT}")
        print(f"  -> http://localhost:{port}   (no-store; a plain refresh is enough)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
