---
title: Summary
---

You can now get yourself onto **{{< param product_name >}}** from nothing: pick the right
portal, request a Tenant, request the namespaces you need, and know what every field on
those forms is for.

## What You Did

- Found **your** myITSM portal — one per location, a Tenant requested in its own location
  and **not movable** afterwards.
- Walked the **New tenant** request: owner, name, members, siglum, purpose, default
  namespace name, location, billing, export control.
- Walked the **New namespace** request: general options, then **basic** vs **DevSpace** vs
  **customized (expert)**, features, DEV/PROD usage, operators, capacity tiers and the
  resource quotas.
- Learned why the forms are long: onboarding is **automated on the DCS side**, and ITSM is
  the input form for that automation until the self-service frontend exists.
- Sorted everyday tasks into **self-service `oc`** vs **ITSM request**.

## Check Your Understanding

1. You work in the German national environment and need a Tenant. Which portal?

{{< note >}}
**Answer:** The **German** myITSM. A Tenant is requested per location, in that location's
own portal, and cannot be moved later.
{{< /note >}}

2. You have just been given a Tenant. Do you need a second request to get a namespace?

{{< note >}}
**Answer:** Not for the first one — a Tenant comes with a **default namespace**. Every
*further* namespace is a "New namespace for existing tenant" request.
{{< /note >}}

3. You need a namespace but have no idea what CPU and memory numbers to put in.

{{< note >}}
**Answer:** Choose **basic standard namespace** — pre-configured and standard-sized. Raise
the limits later with a *Modify namespace* request. (In expert mode the advice is the
same: keep the defaults.)
{{< /note >}}

4. Is **scaling a Deployment** a request?

{{< note >}}
**Answer:** No — scaling is self-service via `oc`, within the quota and rights you already
have. Only *raising* that quota is a request.
{{< /note >}}

5. Why does the form ask for so much detail?

{{< note >}}
**Answer:** Because {{< param product_short >}} onboarding is **automated** and the fields
feed that automation directly — the missing piece is the self-service frontend, not the
provisioning.
{{< /note >}}

## Next Steps

That completes the Core track. The **Console track** does the same work in the OpenShift
web console, and the **Developer track** goes into the mechanisms: **B05** (RBAC and
tenancy in full) and **B06** (how DEV and PROD differ by policy).
