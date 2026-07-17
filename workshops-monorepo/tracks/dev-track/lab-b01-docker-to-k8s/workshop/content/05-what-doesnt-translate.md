---
title: What Doesn't Translate
---

Three lines mapped cleanly onto a Deployment, a Service and a ConfigMap. Four lines in the
original compose file did **not** make it into any manifest you applied — because DCS
rejects them outright. That's not an oversight in this lab; it's the point. Open the
compose file again and look at what's left over:

```editor:open-file
file: ~/exercises/docker-compose.yml
```

## `image: docker.io/rummens/hello-dcs:latest`

Two separate problems live on this one line.

**Not from Harbor.** {{< param product_short >}} is air-gapped — `docker.io` is
unreachable from inside the platform. Every image must already be mirrored into
[Harbor]({{< param dcs_docs_base_url >}}/registry/overview), the platform's own registry,
which is why page 02 pulled from `{{< param dcs_registry >}}` instead. An external image
that isn't mirrored yet is requested through an
[ITSM ticket]({{< param dcs_docs_base_url >}}/support/itsm-requests), not pulled ad hoc.

**The `latest` tag.** [Image tags](https://kubernetes.io/docs/concepts/containers/images/#image-names)
that float (`latest`, or no tag at all) mean the same manifest can silently start a
different image tomorrow — impossible to reproduce, and impossible to scan a specific,
known artifact for vulnerabilities. DCS requires a pinned version (or better, a digest);
`hello-dcs:1.0` is exactly that.

## `user: root`

Docker containers default to root unless told otherwise. Educates sessions on
{{< param product_short >}} enforce a **restricted**
[Security Context Constraint](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html) —
no container may run as UID 0, and every container must tolerate an arbitrary, non-zero
UID assigned by OpenShift at deploy time. `hello-dcs`'s own image already runs as UID 1001
for exactly this reason (see its `USER 1001` line) — nothing to fix here, it's a property
of the image you choose, not something you set in the workload manifest.

## `privileged: true`

A [privileged container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
gets root-equivalent access to the host — every device, every kernel capability. The
restricted SCC blocks it outright: no workload gets more than the minimal capability set it
needs. If an app genuinely needs a specific capability, that's an explicit, narrow grant —
never a blanket `privileged` escape hatch.

## `volumes: - /var/run/docker.sock:/var/run/docker.sock`

A **host bind mount** reaches straight into the underlying node's filesystem — here, the
Docker socket itself, which would let the container control every other container on the
host. Kubernetes has no concept of "the host's files" for an ordinary workload; storage is
a namespace-scoped [Volume](https://kubernetes.io/docs/concepts/storage/volumes/), backed
by a [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
the platform provisions — never a raw path on a node. The
restricted SCC rejects `hostPath` volumes for the same reason it rejects `privileged`.

## Check Your Understanding

1. Which line is rejected because of the platform's air-gapped registry policy, and which
   because of a floating tag — even though they're the same line?

{{< note >}}
**Answer:** `image: docker.io/rummens/hello-dcs:latest`. `docker.io` is an external
registry (air-gapped, Harbor-only), and `:latest` is a floating tag (DCS requires a pinned
version). Two separate constraints happen to land on one line.
{{< /note >}}

2. `user: root` and `privileged: true` are both rejected by the same platform control —
   which one?

{{< note >}}
**Answer:** the **restricted Security Context Constraint** enforced on every Educates
session — it blocks running as UID 0 and blocks privileged containers.
{{< /note >}}

3. Why can't `volumes: - /var/run/docker.sock:/var/run/docker.sock` become a Kubernetes
   Volume the way `environment:` became a ConfigMap?

{{< note >}}
**Answer:** it's a **host bind mount**, reaching into the node's own filesystem — there is
no equivalent workload-facing concept in Kubernetes for that. A Volume is always
namespace-scoped and provisioned by the platform (e.g. a PersistentVolumeClaim), never a
raw path on a node.
{{< /note >}}

Four lines, four DCS controls, one lesson: the mapping in this lab isn't only about
*translating* syntax — it's also about which parts of a Docker workflow simply have no
home on a secured, air-gapped, multi-tenant platform.
