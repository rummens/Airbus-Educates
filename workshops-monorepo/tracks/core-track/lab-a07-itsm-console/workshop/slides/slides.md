<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# The ITSM Console — Self-Service on DCS

Some actions on DCS you do yourself with `oc`. Others are requests that go through the platform team via an ITSM ticket. This lab draws that line and shows where requests happen.

**In this lab:** tell self-service from requests · sort a set of tasks · tour the ITSM console · follow the request → approval → provisioning loop.

Digital Container Service · DCS Academy

---

<!-- id: self-service -->
## Self-Service vs Requests

The general rule: anything inside your namespace you do yourself; anything that changes your entitlements or the shared platform you request.

- **Self-service with `oc`:** deploy, scale, restart · configure with ConfigMaps and Secrets · expose with a Service and Route · claim storage with a PVC.
- **Request with an ITSM ticket:** quota increase · image mirroring into Harbor · new repos or catalogs · S3 bucket · security exception.
- Self-service actions live within the rights and quota you already have.
- Requests touch entitlements, the shared registry, or governance — so they go through approval.

---

<!-- id: map-tasks -->
## Map the Tasks

Sort each task into the right bucket, then check the answers.

- **Self-service via `oc`:** scale a Deployment · create a ConfigMap · expose an app with a Route (in a PROD namespace).
- **Raise an ITSM ticket:** increase quota · mirror an external image · request an S3 bucket · add a Harbor catalog/repo · request a security exception.
- The rule: if it changes what is inside your namespace using rights you already have, it is `oc`.
- If it changes your entitlements or the shared platform, it is a ticket.
- Example: needing 2 more CPU cores than your quota allows is a ticket (a quota increase); deploying the load test afterwards is self-service.

---

<!-- id: console-tour -->
## The ITSM Console Tour

Requests happen in the **ITSM console**. This tour follows one request end to end: a quota increase.

- **1. Request catalog** — grouped by type (quota, registry, storage, security); each is a form.
- **2. Quota-increase form** — state the namespace, the resource, the new amount, and a justification, then submit.
- **3. Approval** — the request goes to an approver; this is the gate self-service does not have.
- **4. Provisioning** — once approved, the platform applies the change; you see the new limit with `oc describe quota`.
- Every request follows the same loop: **request → approval → provisioning**.

---

<!-- id: close -->
## What's Next

You can now tell self-service from requests, and you know where and how requests are made.

- **Self-service `oc`** stays inside your namespace, rights, and quota.
- **ITSM requests** cover quota, mirroring, catalogs, S3, and security exceptions.
- Every request is **request → approval → provisioning**.

**A08** tours the OpenShift web console, mapped to the `oc` commands you already know.
