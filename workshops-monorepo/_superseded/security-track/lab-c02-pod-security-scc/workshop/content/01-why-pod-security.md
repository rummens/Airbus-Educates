---
title: Why Pod Security
---

Before you deploy anything, it's worth understanding *why* {{< param product_short >}} refuses to
run a Pod as root — because that single rule shapes how you build and ship every workload.

## Two gates at admission

When you `oc apply` a Pod, it doesn't go straight to a node. It first passes through **admission**,
where two mechanisms decide whether the Pod is allowed to run at all:

- **[Security Context Constraints (SCC)](https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html)**
  — OpenShift's own control. An SCC defines what a Pod is permitted to do: which UIDs it may run as,
  whether it can be privileged, which Linux capabilities it may hold. Your service account is bound
  to a set of SCCs; the Pod is admitted under the *most restrictive* one that still allows it.
- **[Pod Security Standards (PSA)](https://kubernetes.io/docs/concepts/security/pod-security-standards/)**
  — the upstream Kubernetes standard, enforced at the namespace level in three levels:
  **privileged** (no restrictions), **baseline** (blocks the worst), and **restricted** (locked down).

On {{< param product_short >}} your session namespace enforces the **restricted** PSA level and
admits Pods under the **restricted-v2** SCC. Both gates agree: no root, no privilege, minimal
capabilities. A Pod that asks for more is rejected before it ever reaches a node.

{{< note >}}
SCC and the Pod Security Standards are **standard OpenShift / Kubernetes** constructs — follow the
links above for the authoritative reference. What's {{< param product_short >}}-specific is the
**governance** that decides these defaults, covered at the end of this lab.
{{< /note >}}

## What "restricted" actually requires

For a Pod to pass the restricted bar, its `securityContext` must satisfy four controls:

- **`runAsNonRoot: true`** — the container must run as a non-root user. It may **not** run as UID 0.
- **`allowPrivilegeEscalation: false`** — the process cannot gain more privileges than it started
  with (no `setuid` climb to root).
- **`capabilities.drop: [ALL]`** — drop every Linux capability; add back only the few a workload
  truly needs (ideally none).
- **`seccompProfile.type: RuntimeDefault`** — apply the runtime's default seccomp filter, which
  blocks dangerous syscalls.

And, of course, **`privileged: true` is forbidden** — a privileged container effectively has full
access to the host, which is the opposite of everything above.

## The arbitrary-UID requirement

Here's the part that trips up images brought from elsewhere. Under restricted-v2, OpenShift doesn't
let you *pick* your UID — it **assigns** one from a per-namespace range, and it's a large, arbitrary
number (e.g. `1000740000`), different in every namespace. Your image has to cope with running as a
user it has never seen.

In practice that means an image must **not** assume a fixed UID, and least of all root:

- Don't hardcode `USER 0` (root) in the Containerfile.
- Make files and directories the process writes to **group-writable** and owned by the root *group*
  (GID 0), because the arbitrary UID always runs in group 0.
- Don't listen on privileged ports (< 1024) — a non-root process can't bind them.

An image that hardcodes root works fine on your laptop and then fails the instant it lands on
{{< param product_short >}}. Building for the arbitrary UID up front is the whole game.

{{< note >}}
Think of the platform like a shared secure building: you don't get your own master key (root), and
you don't get to choose your desk (fixed UID). You're handed a visitor badge with a number that
changes each visit, and your work has to function with just that. An image that only works "as the
owner with the master key" won't get through the door.
{{< /note >}}

## Where this comes from: the responsibility split

Why can't you just turn the policy off for your own namespace? Because the secure floor isn't yours
to lower. Under {{< param product_short >}}'s **governance** model, responsibilities are split: the
**platform** sets and enforces the security baseline for every tenant, and the **tenant** is
responsible for building images and workloads that comply with it. Raising the policy above the
floor (for a workload that genuinely needs more) is a **governed exception**, not a checkbox — more
on that once you've felt the floor for yourself.

{{< note >}}
The platform/tenant responsibility split, data classification, and the security-exception process
are {{< param product_short >}} **governance** concepts. See the
[{{< param product_short >}} governance overview]({{< param dcs_docs_base_url >}}/governance/overview).
{{< /note >}}

Enough theory. On the next page you'll deploy a Pod that plays by the rules and watch it sail
through admission.
