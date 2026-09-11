---
title: Summary
---

You looked at {{< param product_short >}} through the **governance and compliance** lens — how
data is classified, how the multi-national European platform guarantees it stays in-region, how
a workload expresses that intent, and who owns each step.

## What You Did

- Read the {{< param product_short >}} **Data Classification** matrix and the multi-national
  **residency** guarantee that pins each classification to permitted region(s) — made credible
  by the **on-prem, air-gapped** platform.
- Inspected how **placement** is expressed in a workload spec: a `data.dcs/classification`
  annotation plus a `topology.kubernetes.io/region` **`nodeSelector`** — and saw how the
  platform advertises regions via node labels.
- Read the **Responsibility Matrix (RACI)** to tell **platform** duties (residency, infra,
  controls) from **tenant** duties (classify, tag, place, request).
- Learned the **Security Exception Process** and **Terms & Conditions** — exceptions are
  governed, time-boxed **ITSM requests**, not config toggles.
- Walked the tenant **compliance loop**: classify → tag → place → request an exception via ITSM
  if needed → renew/close.

## Check Your Understanding

1. What does {{< param product_short >}} **data classification** determine, and what is the
   **residency** guarantee?

{{< note >}}
**Answer:** Classification is the sensitivity level assigned to a workload's data. Residency is
the guarantee that data of a given classification stays inside its permitted European region(s)
— higher classifications are pinned to fewer regions. The on-prem, air-gapped platform is what
keeps it there: there's no external path for the data to leave.
{{< /note >}}

2. How is a workload's **placement** expressed, and **who enforces** it?

{{< note >}}
**Answer:** In the Pod spec — a `data.dcs/classification` annotation plus a
`topology.kubernetes.io/region` `nodeSelector` (standard labels/selectors). The tenant only
*expresses* the intent; the **scheduler and platform policy enforce** it against the region
labels the platform puts on nodes. The tenant does not edit node labels or the regions.
{{< /note >}}

3. What is the **Security Exception Process** for, and **who owns** it?

{{< note >}}
**Answer:** It's the governed path for a workload that genuinely can't meet a control (e.g. scan
gate or region rule). Per the RACI, the **tenant** raises it as a **time-boxed, approved ITSM
request** (and renews/closes it); the **platform** reviews and approves. It's recorded, not a
silent config change.
{{< /note >}}

## Challenge

Do it yourself, unguided: **confirm the sample workload declares both its data classification
and its region placement.** Inspect `workload-classified.yaml` and check it carries a
`data.dcs/classification` annotation and a `topology.kubernetes.io/region` `nodeSelector`. Run
the check when ready.

```examiner:execute-test
name: verify-placement-expressed
title: Challenge — the workload expresses classification and region
args:
- workload-classified.yaml
timeout: 10
```

{{< note >}}
**Hint:** `yq '.spec.template.metadata.annotations, .spec.template.spec.nodeSelector' workload-classified.yaml`
— you should see the classification annotation and the region selector.
{{< /note >}}

## Next Steps

This closes the **Security & Compliance** track: the earlier labels harden the image, runtime,
and supply chain; this one places what you run inside the **EU governance and residency** frame.
From here, the Architect track picks up the platform-wide responsibility split in more depth.
