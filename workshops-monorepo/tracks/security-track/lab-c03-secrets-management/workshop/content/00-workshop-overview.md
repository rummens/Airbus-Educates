---
title: Workshop Overview
---

Welcome. In this workshop, part of **{{< param product_name >}}**, you'll deal with the thing
that quietly ends up in the wrong place more than any other: a **credential**. An API token, a
database password, a signing key — the moment one is written in plaintext where it shouldn't
be, it has leaked, whether or not anyone has noticed yet.

You'll take a deployment that leaks a token three different ways, move that token into a
Kubernetes **Secret**, wire the workload to it **by reference**, and then prove the leak is
gone. Along the way you'll meet the single most common misconception about Secrets head-on —
and see exactly why it's wrong.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

Handling credentials correctly isn't just good hygiene on {{< param product_short >}} — it's a
governance obligation. The {{< param product_short >}} **Terms & Conditions** and data-handling
policy make secret and data protection the tenant's responsibility, part of the platform's
**Governance & compliance** framework.

{{< note >}}
**Governance & compliance** is a {{< param product_short >}}-specific concept: a Responsibility
Matrix, a data-classification scheme, a security-exception process, and Terms & Conditions
covering access, data, and registry policy. See the
[{{< param product_short >}} governance documentation]({{< param dcs_docs_base_url >}}/governance/overview).
The Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) object
itself is standard, and links to its upstream docs.
{{< /note >}}

## What You'll Learn

By the end you will be able to:

- Identify the three common secret-leak paths: **baked into the image**, **printed to logs**,
  and **inline in a manifest / env dump**.
- Explain that a Kubernetes **Secret** is **base64-encoded, not encrypted**, and that its
  protection comes from **RBAC** plus platform **etcd encryption at rest** — not from the
  encoding.
- Move a plaintext credential into a Secret and consume it via `secretKeyRef` rather than a
  literal value.
- Verify a secret is not exposed — not in an env dump, not as a literal in the rendered
  workload.
- Describe the stronger options {{< param product_short >}} offers (sealed / external secrets)
  at a concept level.

## Prerequisites

- **Module A** — especially **lab-a02-kubernetes-essentials**: you should be comfortable
  applying a manifest, setting env on a Deployment, and reading logs with `oc`.
- Familiarity with [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
  and [environment variables in a container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/).

No prior experience with Secrets is assumed — we introduce them here.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} session namespace. All work is `oc` against local manifests in
`~/exercises` — no admin rights, no cluster-wide changes.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Secrets (Kubernetes)](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Distribute credentials securely using Secrets](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)
- [Encrypting confidential data at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
