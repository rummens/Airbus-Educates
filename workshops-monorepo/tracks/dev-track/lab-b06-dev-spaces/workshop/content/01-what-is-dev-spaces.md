---
title: What Is Dev Spaces?
---

[OpenShift Dev Spaces](https://docs.openshift.com/dev-spaces/latest/) is an in-cluster,
browser-based development environment — the productised, supported build of the upstream
[Eclipse Che](https://www.eclipse.org/che/) project. Instead of setting up a toolchain on
your laptop, you open a full IDE (editor, terminal, build tools) that runs as Pods **in the
cluster**, next to where your app runs.

## Why it fits an air-gapped platform

On {{< param product_name >}} that in-cluster model is a feature, not a compromise:

- **Consistent** — everyone gets the same environment from the same **devfile**; no "works on
  my machine."
- **Policy-compliant** — the IDE runs under the same namespaces, quotas, SCCs and RBAC as your
  workloads. Nothing leaves the platform.
- **Air-gapped** — every workspace image comes from **Harbor**. There's no reaching out to a
  public devfile registry or image host, because there's no internet to reach.

## Who installs it

Dev Spaces is delivered as an **OpenShift operator** — and, exactly like the operators you met
in A09, the **platform team installs and owns the operator**, while **you (the tenant) consume
the service**: you open workspaces, you don't run the Dev Spaces control plane. It's a
{{< param product_short >}} service, described at
[{{< param dcs_docs_base_url >}}/services/dev-spaces]({{< param dcs_docs_base_url >}}/services/dev-spaces).

## Check Your Understanding

Dev Spaces runs your IDE **in the cluster**. Name one concrete benefit of that on an
air-gapped platform like {{< param product_short >}}.

{{< note >}}
**Answer (any one):** the environment is reproducible from a devfile; it runs under the same
policy/quota/RBAC as your apps; and all images come from Harbor, so no internet access is
needed — impossible to satisfy with a laptop toolchain on an air-gapped network.
{{< /note >}}
