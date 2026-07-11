---
title: The DCS Ownership Model
---

This is the page to remember. The operator automates a lot — but on
{{< param product_short >}} that does **not** mean the platform runs your database for you.

## Operators, not "as a Service"

{{< param product_short >}} offers services like PostgreSQL, GitLab, and Argo CD as
**OpenShift Operators**, not as a managed/aaS product. The responsibility splits like this:

| Concern | Owned by |
|---|---|
| Installing & upgrading the **operator** | **Platform (DCS)** |
| CRD versions, operator patching | **Platform (DCS)** |
| The **instance** you create (the CR) | **You (the tenant)** |
| Instance sizing, config, storage | **You** |
| **Backups**, restore drills | **You** |
| Upgrading the CR / database version | **You** |
| Monitoring & incident response for the app | **You** |

Contrast with a managed DBaaS or SaaS, where the provider owns day-2 — backups, failover,
upgrades. Here the operator gives you strong *automation*, but **you are the operator's
customer and the instance's owner**. If `demo-db` needs a backup policy, that's your job to
configure; the platform keeps the CloudNativePG operator healthy, not your specific
database.

This maps to the {{< param product_short >}}
**[Responsibility Matrix (RACI)]({{< param dcs_docs_base_url >}}/concepts/operators)** — it
spells out, per service, exactly which side owns which task. Read it before you take a
service into production so there are no surprises about who does backups at 2am.

{{< note >}}
Why does {{< param product_short >}} do it this way? Operators give tenants real
self-service and control on an air-gapped platform without the platform team having to run
every tenant's database. The trade is ownership: more control, more responsibility.
{{< /note >}}

The Operators track (GitLab, Argo CD, CloudNativePG) applies this exact model service by
service — each workshop ends by mapping the service to who-owns-what.
