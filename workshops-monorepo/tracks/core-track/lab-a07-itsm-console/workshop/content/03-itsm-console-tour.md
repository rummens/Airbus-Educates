---
title: The ITSM Console Tour
---

Requests happen in the **ITSM console**. Because {{< param product_short >}} sessions are
air-gapped, the console usually can't be opened from inside this lab — so this is a
guided, annotated tour. We'll walk one real request end to end: a **quota increase**.

{{< warning >}}
**Rough draft.** The screenshots below are placeholders to be captured from the live ITSM
console. If the in-session embedding spike succeeds, this page becomes a live dashboard
tab instead.
{{< /warning >}}

## 1. Find the request catalog

_(screenshot: ITSM console home — the request catalog listing available request types.)_

The catalog groups requests by type — quota, registry, storage, security. You pick the
one you need; each is a form.

## 2. Open a quota-increase request

_(screenshot: the quota-increase form — namespace, resource, current vs requested amount, justification.)_

You state **which namespace**, **which resource** (CPU / memory / storage), the **new
amount**, and a **justification**. Submit.

## 3. Approval

_(screenshot: the request in "pending approval", showing the approver and status.)_

The request goes to an approver — this is the gate that self-service doesn't have. You can
track status here.

## 4. Provisioning and result

_(screenshot: the request "completed", and the namespace showing the new quota.)_

Once approved, the platform **provisions** the change automatically, and it shows up on
your namespace — you'd see the higher limit with `oc describe quota`.

## The loop

Every request follows the same three stages: **request → approval → provisioning**. That
approval step is the whole reason these actions aren't self-service. More in the
[{{< param product_short >}} requests guide]({{< param dcs_docs_base_url >}}/getting-started/requests).
