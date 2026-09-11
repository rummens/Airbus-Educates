# Operators on DCS

**Every platform service you are offered arrives the same way: as an operator.**

An operator is a controller that watches for objects of a kind it understands and makes
reality match them — the same reconcile loop a Deployment uses, applied to something bigger
than a Pod.

You read the **CustomResourceDefinition** that taught this cluster a new kind, create a
**Custom Resource** of that kind — a PostgreSQL cluster, in a few lines — and watch the
operator build the StatefulSet, the storage and the Services underneath it.

Then the part that matters here: the **ownership split**. The platform owns the operator and
its lifecycle. You own the instance it manages — its data, its configuration, its backups,
its day-2.

> **💡 Tip:** the manifest you write has no image, no StatefulSet and no volumes in it.
> Counting what you did *not* have to write is the point of the lab.

- **Track:** Operate & Observe
- **Audience:** Advanced
- **Duration:** ~25 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** **Stateful Workloads** helps (the operator builds one for you), and **RBAC & Tenancy** for who-may-do-what.

## By the end of this lab you'll be able to

- Explain the operator pattern: controller, reconcile loop, desired state.
- Tell a **CRD** from a **CR**, and find both on a cluster.
- Create an instance of an operator-provided service and watch it be built.
- State the DCS ownership model, and what it means when something breaks.

## What you'll do

1. **Find** the kinds an operator added to this cluster.
2. **Read** a CRD, and the instance type it defines.
3. **Create** a database with a few lines of YAML.
4. **Watch** the operator build everything you did not write.
5. **Place** the boundary: platform owns the operator, you own the instance.
