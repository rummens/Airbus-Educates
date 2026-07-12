---
title: Summary
---

You've now seen the other half of life on **{{< param product_name >}}** — not just deploying
to it, but **developing on it**.

## What You Did

- Explained **Dev Spaces**: an in-cluster, browser IDE (Eclipse Che upstream), operator-installed
  by the platform and consumed by you — a good fit for an air-gapped platform.
- Read a **devfile** and confirmed its workspace image comes from **Harbor** (`${DCS_REGISTRY}`).
- Launched (or toured) a workspace and ran the sample app **inside the cluster**.
- Drew the line between the **Educates editor**, **Dev Spaces**, and **`oc apply`**.

## Check Your Understanding

1. Who installs Dev Spaces on {{< param product_short >}}, and who uses it?

{{< note >}}
**Answer:** The **platform team** installs and owns the Dev Spaces **operator** (like every
operator in A09); **tenants** consume the service by opening workspaces.
{{< /note >}}

2. Why must the devfile's workspace image come from Harbor?

{{< note >}}
**Answer:** {{< param product_short >}} is air-gapped — no public registries. Every image,
including the developer/UDI image, is mirrored into Harbor and pulled via the registry variable.
{{< /note >}}

3. What's the difference between the **inner** loop (Dev Spaces) and the **outer** loop (`oc apply`)?

{{< note >}}
**Answer:** The inner loop is fast source iteration inside a workspace; the outer loop builds
an image and deploys it to a namespace. You use Dev Spaces to develop, then B01's flow to ship.
{{< /note >}}

## Next Steps

That's the end of the **Developer track**. A natural next step is the **Operators / Platform
Services** module — for example provisioning your tenant's **GitLab** and cloning straight from
it into a Dev Spaces workspace, or owning a **PostgreSQL** instance for a stateful app. You now
have the full developer arc on {{< param product_short >}}: deploy, configure, scale, debug,
persist, and develop.
