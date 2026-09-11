---
title: Where Your Workload Runs
---

A classification says *where data may live*; a workload has to actually say *which region it
belongs in*. That intent lives in the workload's **spec** — as a data-classification annotation
and a region `nodeSelector`. Let's read one.

## A classified workload

Open the sample manifest:

```editor:open-file
file: ~/exercises/workload-classified.yaml
```

Two lines carry the governance intent:

- an **annotation** — `data.dcs/classification: CONFIDENTIAL` — records the classification of
  the data this workload handles (drawn from the matrix on the previous page);
- a **`nodeSelector`** — `topology.kubernetes.io/region: eu-de` — pins the Pod to nodes in the
  region that classification is allowed to reside in.

Print just those two pieces:

```terminal:execute
command: yq '.spec.template.metadata.annotations, .spec.template.spec.nodeSelector' workload-classified.yaml
```

You should see the classification annotation and the region selector. Both live in the Pod
template, so they travel with every replica the Deployment creates.

```examiner:execute-test
name: verify-placement-expressed
title: The manifest expresses classification and region placement
args:
- workload-classified.yaml
timeout: 10
```

The [`nodeSelector`](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
and the region [label](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
are standard Kubernetes mechanics — nothing {{< param product_short >}}-specific about *how*
they work. What is {{< param product_short >}}-specific is the *meaning*: `eu-de` is a real
governed region, and matching a workload to it is how residency intent is expressed in the spec.
Placement here is **declared**, not enforced — the scheduler and platform policy do the
enforcing.

## How the platform advertises regions

For a region `nodeSelector` to mean anything, the cluster's nodes must be **labelled** with the
region they're in. See what regions this cluster advertises:

```terminal:execute
command: oc get nodes -o jsonpath='{range .items[*]}{.metadata.labels.topology\.kubernetes\.io/region}{"\n"}{end}' | sort -u
```

On a {{< param product_short >}} cluster this lists the governed regions (e.g. `eu-de`,
`eu-es`). The scheduler compares a Pod's `nodeSelector` against these labels and places the Pod
only on matching nodes — which is how a manifest's region intent becomes real placement.

```examiner:execute-test
name: verify-node-topology
title: The cluster returns node topology (region labels tolerated if absent)
timeout: 15
```

{{< note >}}
On a **test cluster** the output above may be empty — the nodes simply carry no region label.
That's expected here and the check tolerates it: the point is that {{< param product_short >}}
nodes *do* carry `topology.kubernetes.io/region`, and the scheduler honours it. Residency is a
**platform guarantee** — the tenant expresses intent in the spec, it does not edit node labels
or the regions themselves.
{{< /note >}}
