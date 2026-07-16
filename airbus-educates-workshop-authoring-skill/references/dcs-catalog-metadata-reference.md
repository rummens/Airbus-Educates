# DCS Academy Catalog Metadata Reference

How a workshop plugs into the **DCS Academy catalog**. This is DCS-specific and
sits on top of the standard Educates `workshop.yaml` — the custom portal reads
extra metadata that plain Educates ignores. Get this wrong and the workshop
deploys fine but **never appears in the portal**.

## Where a workshop lives (catalog repo layout)

Workshops live in the **dcs-academy** repo (the catalog), grouped into tracks:

```
dcs-academy/                          <- catalog repo; the workshops Helm chart is at its root
  tracks/
    core-track/                       <- a TRACK folder (folder name is free)
      track.yaml                      <- track metadata (see below)
      lab-a01-what-is-dcs/            <- one workshop
        resources/
          workshop.yaml               <- the Educates Workshop CR
        workshop/  exercises/  README.md
      lab-a02-.../
    advanced-track/
      track.yaml
      lab-b01-.../
```

The chart discovers everything by globbing the tree — `tracks/*/track.yaml` and
`tracks/*/*/resources/workshop.yaml`. **There is no central catalog list to
edit.** Add a workshop = add its folder + push. The `workshop.yaml` is emitted
**verbatim**, so it must carry all catalog metadata itself (below).

## track.yaml

One per track folder → one `Track` CR. The `id` is **explicit** (not the folder
name), so folders can be renamed freely.

```yaml
id: core                          # REQUIRED — the track id (workshops join via this)
title: "Core — DCS Foundations"   # REQUIRED — shown as the section heading
description: "Get oriented on DCS: containers, images, namespaces, oc."   # optional
order: 10                         # optional (default 100; low = first)
icon: code                        # optional (default "layers"); FA-style name
```

## Workshop catalog metadata (on `metadata`, NOT `spec`)

The portal reads these off the Workshop CR's **`metadata`** — the Educates
`spec.labels`/`spec.title` are separate and mostly ignored for catalog placement.

### Required labels (`metadata.labels`)

```yaml
metadata:
  name: lab-a01-what-is-dcs
  labels:
    academy.dcs/track: core        # MUST equal a track's `id` (else the lab is hidden)
    academy.dcs/order: "10"        # sort within the track — STRING, low = first
    dcs.airbus.com/lifecycle: dev  # dev | prod — see "Lifecycle label" below
```

> A workshop whose `academy.dcs/track` matches no Track is **not rendered** — the
> portal only shows labs in a declared track.

### Lifecycle label (`dcs.airbus.com/lifecycle`) — dev vs prod

Every workshop MUST carry `metadata.labels."dcs.airbus.com/lifecycle"`. The value
follows one rule:

- **`prod`** — the workshop **exposes something** — i.e. it creates (or has the
  learner create) a **`Route` or `Ingress`** to reach a service from outside the
  cluster.
- **`dev`** — everything else (no externally-exposed Route/Ingress).

```yaml
metadata:
  labels:
    dcs.airbus.com/lifecycle: prod   # this lab creates a Route/Ingress
```

**Why it matters — it propagates to the session namespace.** The platform copies
this label from the Workshop CR onto **every session namespace** Educates creates
for the lab (via a Kyverno policy keyed on `training.educates.dev/workshop.name`).
The cluster's dev/prod policy set then keys off the namespace label — a `prod`
namespace gets the stricter enforcement (Kyverno/PROD policies) that a namespace
hosting a Route requires, a `dev` namespace does not. Get the label wrong and a
lab that exposes a Route lands in a `dev` namespace where the exposure policy
isn't applied (or a plain lab is needlessly forced into `prod` enforcement).

This matches the DCS model: **a Route needs a PROD namespace**, and PROD
namespaces enforce Kyverno while DEV ones don't. When in doubt (no Route/Ingress),
use `dev`. Set it to `prod` the moment the lab teaches or performs external
exposure.

> Note: Educates' own session-proxy ingresses (`spec.session.ingresses`, the
> `app-$(session_hostname)` form) are platform-managed and are **not** what this
> label is about — it tracks whether the *workshop content* stands up a real
> `Route`/`Ingress` object in the session namespace.

### Recommended annotations (`metadata.annotations`)

```yaml
  annotations:
    # GitOps: apply the CR before the Educates Workshop CRD is dry-run-checked.
    # Keep this wave BELOW the TrainingPortal's (100) so the workshop exists first.
    argocd.argoproj.io/sync-wave: "5"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
```

### Optional display annotations (all have fallbacks)

| Annotation | Falls back to |
|---|---|
| `academy.dcs/display-name` | `spec.title` |
| `academy.dcs/summary` | first sentence of `spec.description` |
| `academy.dcs/duration` | `spec.duration` |
| `academy.dcs/difficulty` | `spec.difficulty` |
| `academy.dcs/author` | `spec.vendor` |
| `academy.dcs/icon` | the track's section icon |
| `academy.dcs/details` | — (long-form markdown for the tile detail view) |
| `academy.dcs/expires`, `academy.dcs/orphaned` | the workshops chart's default session lifetimes |

Because `duration`/`difficulty`/`title`/`description` fall back to `spec`, **do
not duplicate them** into annotations — set them in `spec` as usual and only add
an annotation to override.

`spec.labels` (the Educates array-of-`{name,value}`) stay for Educates' own
search; keep descriptive ones (e.g. `module`) but the **track grouping lives in
`metadata.labels.academy.dcs/track`**, not `spec.labels`.

## vcluster — always explicit

Under the verbatim model there is **no global vcluster default**. Every workshop
**states its stance explicitly** under `spec.session.applications`:

```yaml
      vcluster:
        enabled: false      # native OpenShift session namespace (the common case)
```

Set `enabled: true` **only** when the learner needs a throwaway cluster with
cluster-admin (creating real namespaces, cluster-scoped objects, applying
cluster policies). Operator/SCC/UID topics must stay **native** (`false`).

A vcluster lab (`enabled: true`) **also requires** two things or CoreDNS
crashloops on OpenShift (Educates pins the `-vc` namespace to the baseline SCC,
which rejects `NET_BIND_SERVICE`):

```yaml
  session:
    namespaces:
      budget: large         # vcluster runs a control plane + CoreDNS — needs headroom
    objects:
    - apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: educates-vcluster-scc
        namespace: $(vcluster_namespace)
      roleRef:
        apiGroup: rbac.authorization.k8s.io
        kind: ClusterRole
        name: educates-privileged-scc
      subjects:
      - apiGroup: rbac.authorization.k8s.io
        kind: Group
        name: system:serviceaccounts:$(vcluster_namespace)
    applications:
      vcluster:
        enabled: true
```

> vcluster is the one application where we DO write `enabled: false` explicitly
> (house standard: record the vcluster-vs-namespace decision). Other unused
> applications are still simply omitted.

## Deployment model (context)

Two charts, two repos:

| Chart / repo | Owns |
|---|---|
| `dcs-academy-portal` (dcs-helm-charts) | portal app, oauth gate, CNPG/feedback, **Track CRD** |
| `dcs-academy-workshops` (dcs-academy, this catalog) | **Track CRs, Workshop CRs, TrainingPortal** |

The TrainingPortal enumerates every workshop (Educates requires explicit names —
no label selector), carries `sync-wave: "100"`, and must settle after the portal
app. Authors don't touch it — it's generated from the globbed workshop list.
Keep `academy.dcs/track` ids in sync with the `track.yaml` files and you're done.
