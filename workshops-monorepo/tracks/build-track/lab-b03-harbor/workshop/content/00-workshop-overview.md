---
title: "Harbor: Projects, Push & Scan"
---

Every lab so far treated the registry as a string in a manifest. It is more than that: on
**{{< param product_name >}}** the registry is where the platform decides **what may run at
all**.

This lab opens it up — the tools, the rules, and the arithmetic behind the gate.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Inspect an image **without pulling it**, and say why its digest matters more than its tag.
- Copy an image between registries with [`skopeo`](https://github.com/containers/skopeo) — no Docker daemon.
- Name the {{< param product_short >}} **catalogs**, and what each is for.
- State the **DEV/PROD project rules**, including the CVE threshold PROD pulls under.
- Read a vulnerability report and decide whether an image would pass the gate.
- Describe the only two ways an image reaches a PROD project.

## Prerequisites

- **Build Your Image on DCS** — you have produced an image and watched it pushed.
- **From Docker to Kubernetes** — why there is no Docker daemon here.

{{< note >}}
**📌 Note:** there is no `docker` and no `podman` in this session, and there will not be one on
{{< param product_short >}} either. `skopeo` talks to registries directly over their API, which
is why it is the tool you are given.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**. All commands run with `oc`
and `skopeo`.

The scan reports you read are **fixtures**: this training cluster has no scanner-backed
registry attached. The structure, the fields and the gate arithmetic are real — only the
scanner running live is missing, and the lab says so where it matters.

## Time and Difficulty

- **Estimated time:** 30 minutes
- **Difficulty:** Intermediate

## Further Reading

- [skopeo](https://github.com/containers/skopeo) — inspect and copy images without a daemon.
- [Harbor documentation](https://goharbor.io/docs/) — projects, robot accounts and scanning.
- [{{< param product_short >}} registry]({{< param dcs_docs_base_url >}}/services/container-registry) — the platform's own rules.
