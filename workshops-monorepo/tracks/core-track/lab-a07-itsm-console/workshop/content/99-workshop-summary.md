---
title: Summary
---

You now know the second half of getting things done on **{{< param product_name >}}**: not
just what you can do yourself, but what you **request** — and where.

## What You Did

- Drew the line between **self-service `oc`** actions and **ITSM requests**.
- Sorted a set of tasks into the right bucket.
- Toured the **ITSM console** and walked a quota-increase request end to end.
- Learned the **request → approval → provisioning** loop.

## Check Your Understanding

1. Name **two** actions that need an ITSM ticket.

{{< note >}}
**Answer:** Any two of: quota increase, image mirroring, new Harbor repo/catalog, S3
bucket, security exception.
{{< /note >}}

2. Is **scaling a Deployment** a ticket?

{{< note >}}
**Answer:** No — scaling is self-service via `oc`, within your existing quota and rights.
{{< /note >}}

3. What are the **three stages** of a request?

{{< note >}}
**Answer:** Request → approval → provisioning.
{{< /note >}}

## Next Steps

**A08** tours the *other* console — the OpenShift web console — mapped to the `oc`
commands you already know. And across the Developer and Security tracks you'll lean on ITSM
for mirroring, catalogs, and exceptions.
