# Local workshop testing on CRC (portal-less)


# TODO Rewrite

Test OpenShift-targeted workshops on local CRC (Apple Silicon) **without the
training portal**.

## Scripts (deploy + smoke)

Two helpers automate the flow below (stdlib Python only; default `--context crc-admin`):

```bash
# deploy a workshop from git (portal-less; drops the custom base image so it
# runs on the stock base-environment). --vcluster / --delete / --keep-image.
./deploy_workshop.py lab-a02-kubernetes-essentials

# list every deployed session (name, phase, URL):
./deploy_workshop.py --list

# deploy ALL workshops under a parent folder at once (also works with --delete):
./deploy_workshop.py dcs-academy/workshops
./deploy_workshop.py dcs-academy/workshops --delete

# run the workshop's smoke test (setup steps + every examiner check) in the
# live session pod. --oc-shim aliases oc->kubectl so oc-based workshops run on
# the stock base image before dcs-workshop-base (with real oc) exists.
./smoke_test.py lab-a02-kubernetes-essentials --oc-shim
```

Smoke plans live in `smoke-plans/<workshop>.json` (ordered `run` setup steps +
`check` examiner-test steps). Full green needs the workshops' images
(`dcs-workshop-base`, `hello-dcs`) in a reachable registry — until then,
checks that need a running app pod fail as expected.

### Run a whole track/module in one go

`run_track.sh` points at a folder, discovers every workshop under it, runs
`smoke_test.py` for each **one at a time** (CRC is small — parallel runs starve
the node), and prints a pass/fail summary. It also **pauses ArgoCD auto-sync**
on the app that manages the Workshop CRs for the duration and **always restores
it on exit** (even Ctrl-C) — the portal-less deploy rewrites those shared CRs, so
selfHeal must be off while testing.

```bash
./run_track.sh workshops-monorepo/tracks/core-track                 # a whole track
./run_track.sh workshops-monorepo/tracks/core-track/lab-a03-expose-app  # one lab
./run_track.sh --dry-run workshops-monorepo/tracks/core-track       # list what would run, touch nothing
```

Labs with no smoke-plan (or a plan with no checks, e.g. a content-tour lab) are
skipped and listed. Env overrides: `CTX` (oc context), `ARGO_APP`/`ARGO_NS`,
`SMOKE_ARGS` (default `--no-links`). Note a track folder currently also contains
the old-design labs — point at individual lab dirs for a subset.

## TLS: editor/console tab shows "temporarily down"

The dashboard, editor and console are each on a **separate hostname**
(`<session>`, `editor-<session>`, `console-<session>`), all served with CRC's
**self-signed** wildcard cert (`*.apps-crc.testing`, issued by the cluster's
`ingress-operator` CA). Accepting the cert for the dashboard host does **not**
cover the editor/console hosts, and an iframe (the editor/console tabs) can't
prompt for a cert exception — so those tabs fail with "temporarily down" even
though the backends are healthy (`curl -k` returns 200/302).

Two fixes:

- **Quick (per host):** open the editor and console URLs (printed by
  `deploy_workshop.py`) directly in a browser tab, click through the warning
  (Advanced → proceed), then reload the dashboard — the tabs now load.
- **One-time (best):** trust the CRC ingress CA so every `*.apps-crc.testing`
  host is accepted with no prompts:

  ```bash
  # export the router CA and add it to the login keychain as trusted
  oc --context crc-admin -n openshift-ingress-operator get secret router-ca \
    -o jsonpath='{.data.tls\.crt}' | base64 -d > /tmp/crc-router-ca.crt
  # (macOS) trust it — you will be prompted for your password:
  sudo security add-trusted-cert -d -r trustRoot \
    -k /Library/Keychains/System.keychain /tmp/crc-router-ca.crt
  ```

  Restart the browser afterwards. (Modifying the system trust store is your
  call — run it yourself; the deploy script never touches it.)

## Why portal-less

The `educates-training-portal` image SIGILLs (`Illegal instruction`, exit 132)
on CRC's Apple-Silicon guest CPU — its Python stack uses instructions the
vfkit/QEMU guest doesn't expose. Everything else runs fine natively on arm64:

- `session-manager` / `secrets-manager` (Go) — fine.
- `educates-base-environment` (the workshop **session/dashboard** pod) — fine.
- loft-sh vcluster — fine.

So only the portal (a catalog/session broker UI) is broken. `session-manager`
reconciles `WorkshopSession` CRs directly, so you can create sessions yourself
and skip the portal entirely. You lose the catalog page — nothing else.

> The portal images ARE multi-arch (amd64 + arm64); the arm64 variant just
> can't execute under CRC's restricted guest CPU. Same image runs fine under
> Docker Desktop / kind (fuller CPU passthrough), and on any amd64 OpenShift.

## Prerequisites

- CRC running; platform (`dcs-academy-platform`) + `kapp-controller` synced.
- The `Workshop` CR you want exists: `oc get workshops.training.educates.dev`.

## 1. Point the platform at the CRC domain (one-time, cluster-only override)

The installed platform defaults to the x86 cluster
(`apps.test.ocp.globomantics.com` + `globomantics-ingress-cert`). Sessions need
`apps-crc.testing` + a cert that exists on CRC (`router-certs-default`).

This override lives **only on the cluster** (not git). ArgoCD `selfHeal` would
revert it, so we disable auto-sync on root + platform first. Re-enabling sync
(or pushing the same change to git) reverts to the globomantics domain.

```bash
CTX=crc-admin

# stop ArgoCD reverting the override
oc --context $CTX -n openshift-gitops patch application educates-root \
  --type=merge -p '{"spec":{"syncPolicy":{"automated":null}}}'
oc --context $CTX -n openshift-gitops patch application dcs-academy-platform \
  --type=merge -p '{"spec":{"syncPolicy":{"automated":null}}}'

# inject CRC domain + cert (the repo's documented per-cluster override knob)
oc --context $CTX -n openshift-gitops patch application dcs-academy-platform \
  --type=merge -p '{"spec":{"source":{"helm":{"valuesObject":{"educates":{"ingressDomain":"apps-crc.testing","ingress":{"tlsCertificateRef":{"name":"router-certs-default"}}}}}}}}'

# re-render installer config, then force the kapp installer to re-run
oc --context $CTX -n openshift-gitops annotate application dcs-academy-platform \
  argocd.argoproj.io/refresh=hard --overwrite
oc --context $CTX -n dcs-educates-installer patch app installer.educates.dev \
  --type=merge -p '{"spec":{"syncPeriod":"720h0m0s"}}'   # spec change = kick

# verify: session-manager picks up a new educates-config-ver-N with the domain
oc --context $CTX -n educates get deploy session-manager \
  -o jsonpath='{.spec.template.spec.volumes[?(@.name=="config")].secret.secretName}{"\n"}'
oc --context $CTX -n educates get secret <that-secret> -o jsonpath='{.data.educates-operator-config\.yaml}' \
  | base64 -d | grep -m1 'domain:'      # -> domain: apps-crc.testing
```

## 2. Create the environment + session

```bash
oc --context crc-admin apply -f workshop-environment.yaml
oc --context crc-admin apply -f workshop-session.yaml

oc --context crc-admin get workshopsession lab-k8s-fundamentals-w01 \
  -o jsonpath='{.status.educates.phase} {.status.educates.url}{"\n"}'
```

## 3. Access

- **URL:** `https://lab-k8s-fundamentals-01.apps-crc.testing`  (`<env>-<id>.<domain>`)
- **Login:** `educates` / `educates`  (basic auth; the session username/password)
- Accept the CRC self-signed cert.

`dig`/`host` report NXDOMAIN — they skip CRC's `/etc/resolver/testing`. Browsers
and curl (getaddrinfo) resolve it fine:
`curl -sk -u educates:educates https://lab-k8s-fundamentals-01.apps-crc.testing/`.

Pods land in the **environment** namespace + a per-session vcluster namespace:

```bash
oc --context crc-admin -n lab-k8s-fundamentals get pods            # dashboard
oc --context crc-admin -n lab-k8s-fundamentals-01-vc get pods      # vcluster
oc --context crc-admin -n lab-k8s-fundamentals logs deploy/lab-k8s-fundamentals-01 -f
```

## 4. Teardown

```bash
oc --context crc-admin delete workshopsession lab-k8s-fundamentals-w01
oc --context crc-admin delete workshopenvironment lab-k8s-fundamentals
```

## 5. Restore GitOps (reverts to globomantics domain)

```bash
oc --context crc-admin -n openshift-gitops patch application dcs-academy-platform \
  --type=json -p '[{"op":"remove","path":"/spec/source/helm/valuesObject"}]'
oc --context crc-admin -n openshift-gitops patch application dcs-academy-platform \
  --type=merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
oc --context crc-admin -n openshift-gitops patch application educates-root \
  --type=merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

---

# Reuse for ANY workshop (generic)

The steps above are the `lab-k8s-fundamentals` worked example. For a new
workshop the flow is identical — three CRs, all reconciled by `session-manager`.
Do the platform domain override (section 1) **once**; it applies to every
session. Then:

```bash
CTX=crc-admin
WS=my-workshop     # Workshop CR name
ID=01              # session id  ->  URL host is <WS>-<ID>.apps-crc.testing

# 1. Ensure a Workshop CR exists. Either it's already in the catalog:
oc --context $CTX get workshops.training.educates.dev
#    ...or define a new one from the template:
cp workshop-definition.template.yaml workshop-definition.yaml   # edit name/source
oc --context $CTX apply -f workshop-definition.yaml

# 2. Environment (one per workshop):
oc --context $CTX apply -f - <<EOF
apiVersion: training.educates.dev/v1beta1
kind: WorkshopEnvironment
metadata: { name: $WS }
spec: { workshop: { name: $WS } }
EOF

# 3. Session (one per attendee/run; bump ID for more):
oc --context $CTX apply -f - <<EOF
apiVersion: training.educates.dev/v1beta1
kind: WorkshopSession
metadata: { name: $WS-w$ID }
spec:
  environment: { name: $WS }
  session: { id: "$ID", username: educates, password: educates }
EOF

# 4. Get the URL (wait for phase Running):
oc --context $CTX get workshopsession $WS-w$ID \
  -o jsonpath='{.status.educates.phase} {.status.educates.url}{"\n"}'
```

Access: `https://<WS>-<ID>.apps-crc.testing`, basic-auth `educates`/`educates`.
Dashboard pod runs in the **environment** namespace (`$WS`); vcluster (if enabled)
in `<WS>-<ID>-vc`.

## How exposing works

`session-manager` creates the edge-TLS routes automatically — you don't create
Ingress/Route by hand:

- **Dashboard** → `<WS>-<ID>.apps-crc.testing` (main URL).
- **Built-in apps** (editor/console) → their own `…-<app>` / `<app>-…` hosts,
  created when `session.applications.<app>.enabled: true`.
- **Your own web apps** → declare `session.ingresses[]` in the Workshop CR
  (see template). Each becomes `<WS>-<ID>-<name>.apps-crc.testing`. The kyverno
  `require-ingress-session-name` policy **rejects** any session Ingress whose
  host doesn't embed the session name — so always expose via `session.ingresses`,
  never a raw Ingress with an arbitrary host.

All hosts are `*.apps-crc.testing` → resolve on the CRC host only (browser/curl,
not `dig`). `INGRESS_PROTOCOL=https`, so routes edge-terminate with
`router-certs-default`.

## Teardown (any workshop)

```bash
oc --context crc-admin delete workshopsession $WS-w$ID
oc --context crc-admin delete workshopenvironment $WS   # removes all its sessions
```

## Routes show "Application is not available" (pods stuck Init:0/1)

If freshly deployed sessions never come up and their dashboard/editor Routes show
the OpenShift **"Application is not available"** page, check the session pod:

```bash
oc --context crc-admin -n <workshop> get pods         # stuck at 0/1 Init:0/1 ?
oc --context crc-admin -n <workshop> get events | grep FailedCreatePodSandBox
```

If events show `Multus ... error waiting for pod: Unauthorized`, it's **not** the
workshop — CRC's Multus CNI auth token has gone stale (typically after long
cluster uptime). Existing pods keep running; only *new* pods fail to get a network
sandbox, so their Route has no backend. Quick in-cluster fix:

```bash
oc --context crc-admin -n openshift-multus rollout restart daemonset/multus \
  deployment/multus-admission-controller
oc --context crc-admin -n openshift-multus rollout status daemonset/multus
# then recreate the stuck session pods so they get networking:
oc --context crc-admin -n <workshop> delete pod --all
```

Durable fix (regenerates certs + restarts the network stack): `crc stop && crc start`
(host command — run it yourself).

## Gotchas

- **Only the portal is broken on CRC arm64** (SIGILL). Everything a session needs
  — dashboard (`base-environment`), vcluster, session-manager — runs natively.
  Never reintroduce the `training-portal` pod on CRC.
- vcluster needs `budget: large` + the `educates-privileged-scc` RoleBinding on
  the `-vc` namespace (in the template). Without it coredns CrashLoops.
- New session but old URL still 404s? Check `phase` is `Running` and the route
  exists: `oc --context crc-admin get route -n $WS | grep $WS-$ID`.

