#!/usr/bin/env python3
"""DCS Academy sample app: a tiny, dependency-free HTTP server on :8080.

Customisation (all via env vars, so `oc set env` visibly changes the response):
  GREETING  the headline message           (default: "Hello from the Digital Container Service")
  MODE      CLI | UI                        (default: CLI)
              CLI = plain text, for the `curl` steps in A02.
              UI  = styled HTML for a browser, and it prints the app's OWN
                    externally-reachable URL (from the incoming request) into
                    the page — so a learner exposing it via a Route sees the
                    live DCS Route host.
  PORT      listen port                     (default: 8080)
  VERSION   shown in the response           (default: 1.0)

Endpoints:
  /         the greeting (CLI text or UI html, per MODE)
  /healthz  liveness/readiness probe target
  /metrics  Prometheus text format, so the app can be scraped by a ServiceMonitor
            in the Operate & Observe track. Hand-rolled on purpose: the exposition
            format is a few lines of text, and pulling in prometheus_client would
            break "no third-party packages" for one counter.

Runs non-root, no third-party packages (UBI9 python base), multiarch.
"""
import html
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

GREETING = os.environ.get("GREETING", "Hello from the Digital Container Service")
MODE = os.environ.get("MODE", "CLI").strip().upper()
PORT = int(os.environ.get("PORT", "8080"))
VERSION = os.environ.get("VERSION", "1.0")
POD = socket.gethostname()
STARTED = time.monotonic()

# Request counters, by path label. ThreadingHTTPServer serves each request on its
# own thread, so the increment needs a lock to be honest under load — and the
# Autoscaling lab drives exactly that.
_counts = {"/": 0, "/healthz": 0, "/metrics": 0, "other": 0}
_counts_lock = threading.Lock()


def _count(path):
    key = path if path in _counts else "other"
    with _counts_lock:
        _counts[key] += 1


def render_metrics():
    """Prometheus exposition format: HELP, TYPE, then samples.

    Kept deliberately small — one counter and two gauges — so a learner can read
    the whole output and match every line to something they did.
    """
    with _counts_lock:
        counts = dict(_counts)
    lines = [
        "# HELP hello_dcs_requests_total Requests served, by path.",
        "# TYPE hello_dcs_requests_total counter",
    ]
    for path, n in sorted(counts.items()):
        lines.append(f'hello_dcs_requests_total{{path="{path}"}} {n}')
    lines += [
        "# HELP hello_dcs_uptime_seconds Seconds since this instance started.",
        "# TYPE hello_dcs_uptime_seconds gauge",
        f"hello_dcs_uptime_seconds {time.monotonic() - STARTED:.1f}",
        "# HELP hello_dcs_up Always 1; useful as a trivially matchable series.",
        "# TYPE hello_dcs_up gauge",
        f'hello_dcs_up{{pod="{POD}",version="{VERSION}"}} 1',
    ]
    return "\n".join(lines) + "\n"


def self_url(headers):
    """Reconstruct the URL the client actually used to reach us.

    Behind an OpenShift Route the router sets Host + X-Forwarded-Proto, so this
    is the real external Route URL; hit directly (curl a Service/Pod) it's the
    in-cluster address. Either way it's honest about how the request arrived.
    """
    host = headers.get("X-Forwarded-Host") or headers.get("Host") or f"localhost:{PORT}"
    proto = headers.get("X-Forwarded-Proto", "http")
    return f"{proto}://{host}"


def render_cli(url):
    return (
        f"{GREETING}\n"
        f"---\n"
        f"mode:    CLI\n"
        f"version: {VERSION}\n"
        f"pod:     {POD}\n"
        f"url:     {url}\n"
    )


def render_ui(url):
    g = html.escape(GREETING)
    u = html.escape(url)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hello DCS</title>
<style>
 body{{font-family:system-ui,sans-serif;background:#0f1720;color:#e8eef5;margin:0;
   display:flex;min-height:100vh;align-items:center;justify-content:center}}
 .card{{background:#17222e;border:1px solid #2b3b4a;border-radius:12px;
   padding:2.5rem 3rem;max-width:640px}}
 h1{{margin:0 0 .5rem;color:#7fd8a0}}
 .u{{font-family:monospace;background:#0f1720;border:1px solid #2b3b4a;
   border-radius:6px;padding:.4rem .6rem;display:inline-block;word-break:break-all}}
 dl{{display:grid;grid-template-columns:auto 1fr;gap:.3rem 1rem;margin-top:1.5rem;
   font-size:.9rem;color:#9fb0c0}}
 dt{{color:#6b7d8d}}
</style></head>
<body><div class="card">
 <h1>{g}</h1>
 <p>You reached this DCS Academy sample app at its own address:</p>
 <p class="u">{u}</p>
 <dl>
   <dt>mode</dt><dd>UI</dd>
   <dt>version</dt><dd>{html.escape(VERSION)}</dd>
   <dt>pod</dt><dd>{html.escape(POD)}</dd>
 </dl>
</div></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    server_version = "hello-dcs/" + VERSION

    def do_GET(self):
        _count(self.path)
        if self.path == "/healthz":
            self._send(200, "text/plain; charset=utf-8", "ok\n")
            return
        if self.path == "/metrics":
            # text/plain version=0.0.4 is what Prometheus expects to find here.
            self._send(200, "text/plain; version=0.0.4; charset=utf-8", render_metrics())
            return
        url = self_url(self.headers)
        if MODE == "UI":
            self._send(200, "text/html; charset=utf-8", render_ui(url))
        else:
            self._send(200, "text/plain; charset=utf-8", render_cli(url))

    def _send(self, code, ctype, body):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # Log to stdout so `oc logs` shows request activity (the A03 logging step).
        # Skip /healthz: it's the liveness/readiness probe target, hit every few
        # seconds, and would otherwise drown the real request lines learners read.
        if getattr(self, "path", "") in ("/healthz", "/metrics"):
            return
        print("[hello-dcs] " + (fmt % args), flush=True)


def main():
    print(f"[hello-dcs] starting v{VERSION} mode={MODE} on :{PORT} (greeting={GREETING!r})",
          flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


def _selftest():
    # ponytail: one runnable check for the mode-branching logic.
    hdrs = {"Host": "app-x.apps.example.dcs", "X-Forwarded-Proto": "https"}
    url = self_url(hdrs)
    assert url == "https://app-x.apps.example.dcs", url
    cli = render_cli(url)
    assert cli.startswith(GREETING) and "mode:    CLI" in cli and url in cli, cli
    ui = render_ui(url)
    assert "<!doctype html>" in ui and url in ui and "UI" in ui, ui
    # Host header missing -> falls back, never crashes.
    assert self_url({}) == f"http://localhost:{PORT}"
    # /metrics is valid exposition format, and counts what it is asked for.
    _count("/")
    _count("/")
    _count("/nope")
    m = render_metrics()
    assert 'hello_dcs_requests_total{path="/"} 2' in m, m
    assert 'hello_dcs_requests_total{path="other"} 1' in m, m
    assert "# TYPE hello_dcs_requests_total counter" in m, m
    assert "hello_dcs_up{" in m and m.endswith("\n"), m
    for line in m.splitlines():                 # no blank or malformed lines
        assert line.startswith("#") or " " in line, line
    print("selftest OK")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        _selftest()
    else:
        main()
