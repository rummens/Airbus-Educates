---
title: Tenant to Namespaces, in Depth
---

Core A06 gave you two words: **Tenant** and **Namespace**. Here's the model behind them, in
full, because everything else in this lab builds on getting it exactly right.

## Two levels, not three

{{< param product_short >}} uses a **two-level** model. A [**Tenant**]({{< param dcs_docs_base_url >}}/concepts/tenancy-and-access)
is your team or organisation — the org-level unit used for recharging and accountability —
and it owns one or more [**Namespaces**](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
(DEV or PROD type). That's it. There is **no separate "project" layer**: on OpenShift,
"project" is simply another word for a namespace, not a third level sitting between Tenant
and Namespace. If you've heard someone describe Namespace → Project → Tenant as three
distinct layers, that's wrong — correct it to Tenant → Namespaces.

{{< note >}}
If you've worked with VMs: think of a Tenant as the department that owns a block of
resource-pool quota, and a Namespace as one resource pool carved out of it. The department
(Tenant) is the accountable unit; the resource pool (Namespace) is where workloads actually
run.
{{< /note >}}

## What actually enforces isolation

On a shared cluster, many tenants' namespaces sit side by side. Two mechanisms keep them
apart:

- **RBAC** — decides *who* can act on *what*, inside which namespace. This is this lab's
  focus, starting on the next page.
- **Network Policies** — decide which workloads may talk to each other over the network.
  These are covered where they're relevant to networking; on DCS today they're an
  observe-only concept for tenants (self-service authoring is on the roadmap).

So when someone asks "why can't I see another team's pods?", the answer is RBAC: your
access is scoped to your tenant's namespaces, and nothing grants you a rule elsewhere.

## See your own project and its labels

Your session namespace is already the active project — you don't need to log in or switch to
it. Confirm which one you're in:

```terminal:execute
command: oc project
```

```examiner:execute-test
name: verify-project-reported
title: Verify the current project is reported
timeout: 10
```

You should see something like `Using project "<your-namespace>" on server "https://...".` —
that namespace is your workspace for the rest of this lab.

Now read the labels the platform attached to it, which is how {{< param product_short >}}
records which Tenant a namespace belongs to and what type it is:

```terminal:execute
command: oc get namespace $(oc project -q) -o jsonpath='{.metadata.labels}'
```

Here, `oc project -q` prints **just** the current project's name with no extra text (the
`-q` flag means "quiet" — no headers, no decoration, only the value), and `$(...)` runs that
command first and substitutes its output into the outer command. `-o jsonpath='{...}'`
extracts one specific field from the full object instead of dumping the whole thing — here,
the `metadata.labels` map.

```examiner:execute-test
name: verify-namespace-labels
title: Verify the namespace's labels are readable
timeout: 10
```

You'll see a small JSON object of labels — at minimum the built-in
`kubernetes.io/metadata.name` label, matching your namespace's own name. On a live DCS
namespace this is also where tenant and lifecycle-type labels live.

Tenancy and namespace types are DCS-specific concepts — see
[Tenancy & Access]({{< param dcs_docs_base_url >}}/concepts/tenancy-and-access) for the full
model, including DEV vs PROD lifecycle and how a namespace is provisioned.

Now: you know *which* namespace is yours. Next page starts from the sharper question —
within it, what exactly are you allowed to do?
