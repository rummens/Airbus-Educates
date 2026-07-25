---
title: Map the Tasks
---

Now check what you just learned. In this page you sort a set of tasks into self-service
or ticket.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/map-tasks
```

Open the worksheet and decide, for each task, whether it is self-service or a ticket:

```editor:open-file
file: ~/exercises/self-service-vs-ticket.md
```

Decide each one before you reveal the answers.

## Answers

{{< note >}}
**Self-service via `oc`:** scale a Deployment · create a ConfigMap · expose an app with a
Route (in a PROD namespace).

**Raise an ITSM ticket:** increase your namespace quota · mirror an external image to
Harbor · request an S3 bucket · add a new Harbor catalog/repo · request a security
exception.
{{< /note >}}

The rule: if it changes **what's inside your namespace** using rights you already have,
it's `oc`. If it changes **your entitlements or the shared platform**, it's a ticket.

## Quick check

You need 2 more CPU cores than your namespace allows for a load test. Self-service or
ticket?

{{< note >}}
**Answer:** **Ticket** — a quota increase changes your entitlement, so it needs approval.
Deploying the load test itself (once you have the quota) is self-service.
{{< /note >}}
