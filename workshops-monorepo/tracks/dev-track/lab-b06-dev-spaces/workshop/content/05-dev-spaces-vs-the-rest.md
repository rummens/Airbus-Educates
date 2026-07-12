---
title: Dev Spaces vs the Rest
---

You've now used three different "editors/environments" across this academy. They look similar
but do very different jobs — knowing which is which saves a lot of confusion.

| | What it is | When you use it |
|---|---|---|
| **Educates editor** | The VS Code panel in *this workshop* | Following a lab. It exists only for the session and disappears with it. |
| **Dev Spaces** | Your real, in-cluster tenant IDE | Day-to-day development *on* {{< param product_short >}} — reproducible, policy-compliant, air-gapped. |
| **`oc apply`** | Deploying a built image | Shipping a finished change to a namespace (B01). |

The trap is thinking the **workshop editor** is a real development environment. It isn't — it's
a teaching tool. **Dev Spaces** is what a tenant developer actually uses to build software on
the platform; `oc apply` is how the built result gets deployed.

## Check Your Understanding

A teammate says "I'll just develop in the Educates editor from the workshop." What's wrong with
that, and what should they use instead?

{{< note >}}
**Answer:** The Educates editor is per-workshop and ephemeral — it's for learning, not real
work. For actual development on {{< param product_short >}} they should use **Dev Spaces**,
which is a persistent, reproducible, policy-compliant in-cluster IDE.
{{< /note >}}
