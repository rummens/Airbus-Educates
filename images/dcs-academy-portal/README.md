# dcs-academy-portal (image)

Custom DCS Academy training portal — one Flask image that is **UI +
backend-for-frontend + reverse-proxy**. It replaces the Educates landing/catalog
UI at the `academy` host and reverse-proxies the Educates session paths so the
session runtime keeps working. Design/plan: `../../dcs-academy-portal/PLAN.md`.

**Runtime base = Red Hat Hardened Image** `registry.access.redhat.com/hi/python`
(distroless: no shell, no pip, nonroot uid 65532, Python 3.14). Multi-stage
build: a `python:3.14` builder installs deps into `/opt/deps`, the hardened
runtime copies them and runs `python3 -m gunicorn` (PYTHONPATH=/opt/deps). Deps
must have cp314 wheels — keep `psycopg[binary]` ≥ 3.2.10.

## Layout
```
portal/
  config.py      env + theme (→ CSS variables)
  k8sclient.py   SA reads: Workshop/Track/TrainingPortal/WorkshopSession + pods; SSAR (user token)
  educates.py    Educates REST client (robot token from TrainingPortal.status) — session lifecycle
  proxy.py       reverse-proxy allowlist for the Educates session paths (the crux)
  feedback.py    absorbed feedback-collector — CNPG (psycopg) / sqlite behind DATABASE_URL
  metrics.py     Prometheus (/metrics): live gauges + request/latency/error counters
  app.py         Flask routes + provisioning status feed
  templates/ static/  Jinja + vanilla JS, vendored Poppins + inline SVG icons (no CDN)
```

## Run locally (no cluster)
```bash
PORTAL_DEMO=1 python3 -m gunicorn -b 127.0.0.1:8099 portal.app:app   # bundled sample catalog
python3 test_portal.py                                               # asserts, prints OK
```
`PORTAL_DEMO=1` serves a sample catalog so the UI renders with no cluster.
Without it the app uses the in-cluster SA (or your kubeconfig) for real CRs.

## Run locally against a real cluster (fast iterate, e.g. CRC from outside)
```bash
# one-time: Track CRD + a few Track CRs + label workshops into tracks
oc --context crc-admin apply -f ../../dcs-academy-portal/chart/crds/track.yaml
# (create Track CRs; label workshops: academy.dcs/track,order + annotate summary/difficulty/duration)

KUBE_CONTEXT=crc-admin PORTAL_SESSION_TLS_VERIFY=false FEEDBACK_DB=/tmp/portal.db \
  python3 -m gunicorn -b 127.0.0.1:8099 portal.app:app
```
`KUBE_CONTEXT` picks a kubeconfig context without touching your global
current-context. Catalog, provisioning status feed (real session pods),
metrics, feedback (sqlite) and the SSAR admin gate all work this way. Test the
admin gate: `curl -H "X-Forwarded-Access-Token: $(oc --context crc-admin whoami -t)" .../admin`.
Only **/launch** (Educates REST session request) needs the portal pod running —
broken on CRC arm64 (SIGILL), so verify that path on the x86 cluster.

## Build
```bash
cd ../ && ./build.sh          # arm64 (CRC);  MULTIARCH=1 ./build.sh for amd64+arm64
```
Dev pushes to `ghcr.io/rummens/dcs-academy-portal:dev` — **make the package
public** in GitHub after the first push (like the other images). Mirror to
Harbor for prod (air-gap).

## Two things to verify against a live authenticated session
1. **Proxy allowlist** (`proxy.py:ALLOW_PREFIXES`) — start a real session behind
   the oauth-proxy and confirm the minimal set of `academy/…` paths the session
   gateway hits. Under-proxy breaks sessions; over-proxy re-exposes the Educates
   UI. (Not reproducible on CRC — portal is SIGILL there; verify on the x86 cluster.)
2. **Workshop fields** — confirmed on the live CRD: `spec.title`/`spec.description`
   are populated; `difficulty`/`duration`/summary/track/order come from
   `academy.dcs/*` labels+annotations (real Workshop CRs don't set spec.difficulty).
