---
title: "DEV vs PROD Namespaces"
---

On **{{< param product_name >}}** a DEV namespace and a PROD namespace are not separated by a
naming convention. They differ in **policy posture**.

PROD enforces rules DEV does not, and only PROD may publish a
[**Route**](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html).

This session gives you **one of each**. You will apply the same manifests to both and read the
two different answers.

{{< note >}}
**💡 First time in one of these labs?** See the
[DCS Academy help page]({{< param ingress_protocol >}}://academy.{{< param ingress_domain >}}/help)
for the terminal, editor and clickable actions.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Say what actually distinguishes a DEV namespace from a PROD one on {{< param product_short >}}.
- Predict which manifests a PROD namespace will refuse, and why.
- Read an **admission** rejection and identify the policy and rule that produced it.
- Explain why only a PROD-type namespace may publish a Route.
- Describe **promotion** — and why it is a fresh apply to PROD, not an edit in place.

## Prerequisites

- The Core lab **Terms — Namespaces & Tenancy** — the vocabulary.
- **Health & Resources** — requests and limits, which PROD is about to insist on.
- Helpful: **RBAC & Tenancy**, the previous lab in this track.

{{< note >}}
**📌 Note:** this session has **three** namespaces: your usual session namespace, plus
`$DEV_NS` and `$PROD_NS` created for this lab. The variables are already set in your terminal.
{{< /note >}}

## Your Environment

A browser-based session with a split **terminal** and an **editor**. All commands run with
`oc`, and each one names the namespace it targets with `-n`.

The policy enforcing the PROD posture is a real admission policy on this cluster, scoped to
your two namespaces. The rejections you get are genuine — nothing is simulated.

## Time and Difficulty

- **Estimated time:** 25 minutes
- **Difficulty:** Intermediate

## Further Reading

- [Admission controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) — where a rejection like this comes from.
- [Route configuration](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html) — the object PROD may publish and DEV may not.
- [{{< param product_short >}} namespace types]({{< param dcs_docs_base_url >}}/concepts/namespace-types) — the platform's own description of the split.
