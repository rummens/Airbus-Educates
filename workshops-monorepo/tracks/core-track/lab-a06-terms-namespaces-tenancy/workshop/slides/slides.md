<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Terms — Namespaces & Tenancy

Names the place your apps have been running in — the **Namespace** — then shows isolation for real by running the same app in two namespaces at once.

**In this lab:** define a Namespace · see isolation directly · reasons to split into namespaces · the Tenant → Namespaces model · DEV vs PROD namespace types.

Digital Container Service · DCS Academy

---

<!-- id: namespace -->
## What is a Namespace?

A **Namespace** groups and isolates a set of workloads (Deployments, Pods, Services, ConfigMaps). Objects in one namespace do not see or collide with objects in another.

- On DCS the namespace is the **unit of consumption** — you request namespaces, not servers.
- Your **active namespace** is the one your `oc` context points at by default.
- Everything you create lands in the active namespace unless `-n` says otherwise.

```
oc project
oc get deployments,pods,services
```

- `oc project` prints the active namespace.
- The comma-separated list asks for three kinds at once.

---

<!-- id: isolation -->
## Isolation in action

Deploy the **same** manifest into two namespaces (`app-a`, `app-b`) and watch them stay independent. The `-n <namespace>` flag is the only thing that changes where a command runs.

- The manifest has **no `namespace:` field** — `-n` decides the target.
- Both namespaces get a Deployment named `hello` with **no clash**.
- Scaling `app-a` to zero leaves `app-b` untouched — actions do not leak.

```
envsubst < app.yaml | oc apply -n "$(oc project -q)-app-a" -f -
envsubst < app.yaml | oc apply -n "$(oc project -q)-app-b" -f -
oc scale deploy/hello --replicas=0 -n "$(oc project -q)-app-a"
```

- Result: `app-a` shows `0/0`, `app-b` still `1/1`.

---

<!-- id: why-split -->
## Why split into namespaces?

Four common reasons to run more than one namespace — each one something you saw in the demo.

- **Separate instances** — DEV / QA / PROD copies of one app, each in its own namespace.
- **Blast-radius isolation** — a mistake in one namespace cannot reach another.
- **Independent quotas and RBAC** — each namespace has its own budget and access rules.
- **Naming freedom** — two teams can both name an app `hello` without coordinating.

No command on this page — it is a reason to remember, not a step to run.

---

<!-- id: tenancy -->
## Tenants & namespace types

Every Namespace belongs to a **Tenant** — the org-level unit that is accountable and recharged. The model has two levels only: **Tenant → Namespaces**. There is no "project" layer.

- **DEV** namespaces: looser, for fast iteration, no policy enforcement.
- **PROD** namespaces: stricter, enforce **Kyverno** policy, and can expose apps.
- Labels on a namespace record its Tenant and its type.

![A Tenant owns one or more Namespaces of type DEV or PROD; PROD enforces Kyverno](tenancy-model.svg)

```
oc get namespace "$(oc project -q)" -o jsonpath='{.metadata.labels}'
```

---

<!-- id: next -->
## What's next

You now have the vocabulary and have seen isolation for real.

- The **deep access model** is Developer **B05** (RBAC, Tenancy & Namespaces in full).
- **DEV vs PROD by policy** — how PROD is enforced with Kyverno — is Developer **B06**.
- Leave feedback in the **Feedback** tab before you finish.
