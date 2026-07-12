# HANDOVER — dcs-academy-portal bring-up & CRC troubleshooting

Running log for bringing the **custom DCS Academy portal** up on the local
**CRC (Apple-Silicon / OpenShift Local, arm64)** cluster, and the fixes made along
the way. Target production is **x86 OpenShift** — most CRC pain here is arm64/VM
specific and does **not** apply there. Read alongside auto-memory
`crc-arm64-educates-portal-sigill`, `dcs-academy-custom-portal`,
`educates-oauth-gating-openshift`.

## Architecture (after the chart merge)

One chart — `dcs-academy-portal/chart` — owns the whole academy:
- Workshop CRs (`70-workshops.yaml`) + TrainingPortal (`71-trainingportal.yaml`,
  name **`dcst-dcs-backend`**) — both cluster-scoped.
- oauth gate: `60-oauth-proxy.yaml`, `61-oauth-sealed-secret.yaml`,
  `62-oauth-route-vap.yaml` (host-reservation VAP).
- Custom Flask UI (`20-deployment.yaml`/`21-service.yaml`), CNPG feedback
  (`30-cnpg-cluster.yaml`), Tracks (`10-tracks.yaml`), RBAC, ServiceMonitor.
- `40-networkpolicy.yaml` — locks the Educates backend Service to this app +
  session namespaces.
- `63-crc-armcap-job.yaml` — CRC-only PostSync workaround (see below).

The old `dcs-academy-workshops` chart was merged in and deleted. ArgoCD apps:
`02-educates-platform` (wave 1) → `04-academy-portal` (wave 2). Per-cluster values
come from `argocd/envs/platform-crc.yaml` via `$values`.

Request flow: browser → Route `oauth-proxy` (reencrypt, academy host) → oauth-proxy
(SSO gate) → **upstream = the Flask app** → app reverse-proxies Educates session
paths to the backend `training-portal` REST in `dcst-dcs-backend-ui`.

## Deploy status (2026-07-12)

| Thing | State |
|---|---|
| Merge into one chart, workshops chart deleted | ✅ on `main` |
| Custom portal pod runs on CRC | ✅ (needs `OPENSSL_armcap=0`, see below) |
| `academy.apps-crc.testing` reachable | ✅ after `/etc/hosts` entry (see gotchas) |
| oauth-proxy SSO gate + VAP | ✅ 302→OpenShift OAuth, redirect_uri correct |
| TrainingPortal provisioning | ✅ CR `Running`, robot creds present |
| Educates backend pod (`training-portal`) runs on CRC | ⚠️ only with the PostSync Job (below) |
| **Admin button (#1)** | ⚠️ **code fixed + on `main`, NOT deployed — needs image rebuild** |
| End-to-end session start on CRC | ❓ **not yet verified** — next task |

## The CRC SIGILL saga (arm64 only)

`cryptography`'s bundled OpenSSL runs an aarch64 capability probe (reads ID
registers / probe instructions) that Apple `Virtualization.framework` does not
emulate → **SIGILL, exit 132**. Hits any Python process importing `cryptography`.

Fix everywhere: **`OPENSSL_armcap=0`** (skips the probe → software crypto; no-op on
x86). Verified: unset → 132; `=0` → clean boot.

Two pods need it:
1. **Custom portal pod** — declarative: `values.openssl.armcap` (empty default),
   rendered as an env in `20-deployment.yaml`. Set to `"0"` in `platform-crc.yaml`.
2. **Educates backend `training-portal` pod** — operator-owned Deployment in
   `dcst-dcs-backend-ui`, NOT in our chart. Handled by `values.crcWorkaround.enabled`
   → PostSync hook Job `63-crc-armcap-job.yaml` that runs
   `oc set env deployment/training-portal -n dcst-dcs-backend-ui OPENSSL_armcap=0`
   after each sync. Enabled in `platform-crc.yaml`. Idempotent; re-applies if the
   TrainingPortal recreates the backend. **x86: leave both OFF.**

## Fixes landed this session

- **k8sclient `portal_status()`**: cluster-scoped read (`get_cluster_custom_object`)
  — TrainingPortal CRD is Cluster-scoped. (committed)
- **Admin SSAR (`user_can_admin`)**: was building the client via
  `Configuration.get_default_copy()`, which carries the in-cluster
  `refresh_api_key_hook` that re-injects the SA token → SSAR ran as the SA (no
  `delete`) → admin hidden for everyone. Now builds a **fresh Configuration**
  (host/CA only) with the user token. Verified in-cluster: kubeadmin → allowed=True.
  **NEEDS IMAGE REBUILD to deploy.**
- **TrainingPortal provisioning**: removed a stray `01-backend-namespace.yaml` that
  pre-created the Educates-owned `-ui` namespace (Educates then failed "namespace
  already exists"); moved `40-networkpolicy.yaml` to sync-wave 6 (after the TP at 5)
  so Educates owns/creates the namespace first. (committed)
- `OPENSSL_armcap` + `crcWorkaround` options (this handover's subject).

## Open TODOs (next session)

1. **Rebuild + push the portal image** so the admin-SSAR fix ships:
   `cd images && ./build.sh` (arm64 default; needs `docker` + ghcr push creds), then
   `oc rollout restart deploy/dcs-academy-portal -n dcs-academy-portal`. Confirm the
   admin button shows for kubeadmin.
2. **Verify a session start end-to-end** on CRC (browser SSO → launch a workshop →
   session host resolves + dashboard). Needs the academy host AND each session host
   in `/etc/hosts` (see gotchas). Watch `WorkshopSession.status.educates.phase`.
3. Confirm the PostSync Job actually fires on a fresh sync (it was applied manually
   this session via `oc set env`; the Job path is new and unverified end-to-end).
4. Decide durability of the backend workaround (Job re-runs only on sync; a bare TP
   recreate without a sync leaves the backend crashlooping until next sync).

## Gotchas / commands

- **CRC DNS**: custom routes on `*.apps-crc.testing` are NOT wildcard-resolved; only
  hosts in `/etc/hosts` work. Add each:
  `echo "127.0.0.1 academy.apps-crc.testing" | sudo tee -a /etc/hosts`
  (session hosts `<lab>-<id>.apps-crc.testing` + `console-`/`editor-` variants too).
- Workshop + TrainingPortal CRDs are **Cluster-scoped** — namespace is irrelevant to
  them; read cluster-scoped.
- The `-ui` namespace (`dcst-dcs-backend-ui`) is **Educates-owned** — never create it
  (chart or `oc`); Educates fails if it pre-exists.
- Backend pod crash check:
  `oc get pod -n dcst-dcs-backend-ui -l deployment=training-portal`
  `oc logs <pod> -n dcst-dcs-backend-ui --previous | tail` (look for "Illegal instruction").
- TrainingPortal health:
  `oc get trainingportal dcst-dcs-backend -o jsonpath='{.status.educates}'`
- Portal image is `:dev` (pullPolicy Always) — `oc rollout restart` re-pulls.
