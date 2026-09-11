---
title: Responsibility and Exceptions
---

Residency and classification only work if it's clear **who does what**. {{< param product_short >}}
writes that down in a **Responsibility Matrix (RACI)**, and it defines what happens when a
workload genuinely can't meet a control — the **Security Exception Process**.

## The RACI split

**RACI** — Responsible, Accountable, Consulted, Informed — is how {{< param product_short >}}
splits governance duties between the **platform** and the **tenant**. Read the sample matrix:

```editor:open-file
file: ~/exercises/raci.md
```

Pull out the rows the **tenant** owns:

```terminal:execute
command: grep -i 'tenant' raci.md
```

```examiner:execute-test
name: verify-raci-tenant-rows
title: The RACI fixture lists tenant-owned rows
args:
- raci.md
timeout: 10
```

The split has a clear shape:

- The **platform** is Responsible/Accountable for the things a tenant *can't* control — the
  regional infrastructure and the residency guarantee, the node region labels, and cluster-wide
  security controls (Kyverno, scanning gates).
- The **tenant** is Responsible/Accountable for the things only it knows — **classifying** the
  data its workloads handle, **tagging and placing** those workloads accordingly, **requesting
  exceptions**, and **accepting the Terms & Conditions** for its namespaces.

In one line: the platform guarantees *where* data can live and enforces the controls; the tenant
classifies, tags, places, and requests. That's why the previous page had you *read* placement
rather than change node labels — labelling nodes is the platform's row, not yours.

## The Security Exception Process

Sometimes a workload legitimately can't satisfy a control — an image can't clear the scan gate
in time, or a component needs a region that its classification wouldn't normally allow. On
{{< param product_short >}} that is **not** a config toggle you flip yourself. It is a governed
**Security Exception**: a **[ITSM request]({{< param dcs_docs_base_url >}}/support/itsm-requests)**
that is reviewed, **time-boxed**, and **approved** before the workload proceeds — and it expires,
so it must be renewed or closed. The exception is recorded, not silent.

## Terms & Conditions

Underpinning all of it are the {{< param product_short >}} **Terms & Conditions** — the
agreement covering access, data and storage handling, and image/registry use. Accepting the
T&Cs for a tenant's namespaces is a **tenant** responsibility (it's a row in the matrix), and it
is what binds a team to the classification and residency rules in the first place.

{{< note >}}
The RACI, the exception process, and the T&Cs are {{< param product_short >}}-specific
governance — see the
[{{< param product_short >}} governance & compliance docs]({{< param dcs_docs_base_url >}}/governance/overview).
The exception thread connects back to the scan-gate exceptions you met earlier in the Security
track: same governed ITSM path, different control.
{{< /note >}}
