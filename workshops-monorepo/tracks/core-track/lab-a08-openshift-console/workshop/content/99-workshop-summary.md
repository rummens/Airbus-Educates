---
title: Summary
---

You've now seen both sides of **{{< param product_name >}}**: the `oc` command line you
worked in all through Core, and the web console that mirrors it.

## What You Did

- Toured the console's **perspectives** and found your app in **Workloads**/Topology.
- Located your **Services/Routes** (Networking) and **PVC** (Storage) in the console.
- Found your **ConfigMaps/Secrets** (Config), with Secrets masked.
- Mapped every view to its **`oc` twin** and learned when to reach for which.

## Check Your Understanding

1. Which console **perspective** gives you the visual Topology view?

{{< note >}}
**Answer:** The **Developer** perspective. (Administrator is resource-centric.)
{{< /note >}}

2. What `oc` command matches the console's **Routes** view?

{{< note >}}
**Answer:** `oc get route` (and `oc describe route` / `-o jsonpath='{.spec.host}'` for the
external host).
{{< /note >}}

3. Give **one** case where the CLI beats the console.

{{< note >}}
**Answer:** Any of: scripting/automation, repeatable changes, bulk operations, fast
air-gapped work — anything you'll do more than once.
{{< /note >}}

## Next Steps

That's **Core** complete: you know what {{< param product_short >}} is, you've deployed,
configured, fixed, exposed and persisted an app, learned the terms, and toured both
consoles. Pick a track next — **Developer** for the build-and-integrate mechanisms behind
everything you just did, or **Security** for governance and compliance.
