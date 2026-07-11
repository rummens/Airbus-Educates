---
title: The Tenant Model
---

Before you can reason about *access*, you need the vocabulary for *who owns what* on
{{< param product_short >}}. That's the tenancy model, and it has exactly two levels — no more.

## Tenant → Namespaces

{{< param product_short >}} uses a **two-level** [tenancy model]({{< param dcs_docs_base_url >}}/tenancy/tenants-and-namespaces):

- A **Tenant** is the team or organisation. It is the *org-level* unit — the thing DCS uses for **recharging** (who pays) and **accountability** (who owns the workloads). A tenant is not something you `oc get`; it exists at the platform/billing level.
- A tenant owns one or more **Namespaces** — the actual working areas where your Pods, Deployments and Services live. These are the DEV and PROD namespaces you met earlier.

That's the whole model. A tenant, and the namespaces underneath it.

{{< warning >}}
**"Project" is not a third level.** On OpenShift, a *project* is simply another word for a
*namespace* — the same object, with a little extra metadata. When you see "project" in the
console or in `oc` output, read it as "namespace". There is **no** Namespace → Project → Tenant
hierarchy on {{< param product_short >}}; that's a common misconception. Two levels: Tenant, then
Namespaces.
{{< /warning >}}

## How a team becomes a tenant

A team doesn't create its own tenant with a command — onboarding is a platform process. The
team is registered as a tenant (for recharging and accountability), granted one or more
namespaces, and its members are given access through **SSO**: you log in with your normal
corporate identity and the platform maps you to your tenant's namespaces. That's why you never
typed a password to reach this session — your SSO identity is already known.

## Isolation on a shared cluster

Most tenants run on the **shared cluster**, so many tenants' namespaces sit side by side on the
same nodes. Two mechanisms keep them apart:

- **[RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)** confines *what you can do and where* — your access is scoped to your tenant's namespaces (you'll prove this on the next page).
- **Network Policies** confine *what can talk to what* — the default posture is restrictive, so one tenant's Pods can't freely reach another's. (Network Policies are covered in the networking lab; here we just note they're the second half of isolation.)

## Who am I, and where am I?

Start by confirming the identity SSO gave you:

```terminal:execute
command: oc whoami
```

You'll see your username — the identity everything else in this workshop is evaluated against:

```
user1
```

```examiner:execute-test
name: verify-whoami
title: Verify you have an authenticated identity
timeout: 10
```

Now confirm which namespace you're working in. `oc project` reports your **current** namespace
(remember: "project" = namespace); the `-q` flag prints just the name, nothing else:

```terminal:execute
command: oc project -q
```

```
lab-a05-access-tenancy-w01-s001
```

This is your tenant's namespace for this session — the one place the next pages' permission and
quota checks apply.

```examiner:execute-test
name: verify-project
title: Verify a current namespace is set
timeout: 10
```

{{< note >}}
Your session namespace name is generated per session, so yours will differ from the example
above. What matters is that `oc whoami` and `oc project -q` both return a value — that's your
identity and your scope, the two inputs to every access decision that follows.
{{< /note >}}
