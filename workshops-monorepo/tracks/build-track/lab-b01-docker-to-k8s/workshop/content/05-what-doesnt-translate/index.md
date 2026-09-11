---
title: What Doesn't Translate
---

Three compose lines mapped cleanly onto a Deployment, a Service and a ConfigMap.

Four lines did **not** make it into any manifest you applied — because
{{< param product_short >}} refuses them. That is the point of this page: the mapping is the
easy half, the constraints are the half that changes how you build.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/rejected
```

Look at what is left over in the compose file:

```editor:open-file
file: ~/exercises/docker-compose.yml
```

![Four compose lines and the DCS control that rejects each](rejected-lines.svg)

## `image: docker.io/rummens/hello-dcs:latest`

Two separate problems live on this one line.

**Not from Harbor.** {{< param product_short >}} is **air-gapped** — `docker.io` is
unreachable from inside the platform. Every image must already be mirrored into
[Harbor]({{< param dcs_docs_base_url >}}/services/container-registry), which is why page 02
pulled from `{{< param dcs_registry >}}`. An image that is not mirrored yet is requested,
not pulled ad hoc.

**The floating tag.** A [tag](https://kubernetes.io/docs/concepts/containers/images/#image-names)
like `latest` means the same manifest can quietly start a *different* image tomorrow. That
is impossible to reproduce, and impossible to scan as a known artifact.
{{< param product_short >}} wants a pinned version, or better a digest — `hello-dcs:1.0` is
exactly that.

## `user: root`

Docker containers run as root unless told otherwise. {{< param product_short >}} enforces a
**restricted** [Security Context Constraint](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html):

- no container may run as **UID 0**;
- every container must tolerate an **arbitrary non-zero UID** assigned at deploy time.

`hello-dcs` already runs as UID 1001 for that reason. Nothing to fix here — it is a property
of the **image** you choose, not a field you set in the workload.

## `privileged: true`

A [privileged container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
gets root-equivalent access to the node: every device, every kernel capability.

The restricted SCC blocks it outright. A workload that genuinely needs one capability gets
that one capability granted explicitly — never a blanket escape hatch.

## `volumes: - /var/run/docker.sock:/var/run/docker.sock`

This is a **host bind mount**, reaching into the node's own filesystem — here the Docker
socket itself, which would hand the container control of every other container on that node.

Kubernetes has no "the host's files" concept for an ordinary workload. Storage is a
namespace-scoped [Volume](https://kubernetes.io/docs/concepts/storage/volumes/), backed by a
[PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) the
platform provisions. The restricted SCC rejects `hostPath` for the same reason it rejects
`privileged`.

## See the constraint for yourself

The SCC is not a document — it is enforced by the cluster. Ask what your own workload is
allowed to do:

```terminal:execute
command: oc get pod -l app=hello-dcs -o jsonpath='{.items[0].metadata.annotations.openshift\.io/scc}{"\n"}'
```

That prints the SCC the running Pod was admitted under. `restricted-v2` is the one described
above.

```examiner:execute-test
name: verify-scc-restricted
title: Verify the running Pod was admitted under a restricted SCC
timeout: 10
retries: 3
delay: 2
```

Four lines, four controls, one lesson: a naive lift-and-shift assumes a single trusted host.
A secured, air-gapped, multi-tenant platform cannot give you one.
