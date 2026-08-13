---
title: Data Classification and Residency
---

Before you can talk about *where* data is allowed to live, you need a way to say *how
sensitive* it is. That's what **data classification** does — and on {{< param product_short >}}
the classification of the data decides which **regions** may hold it.

## Data classification

{{< param product_short >}} assigns every piece of data a **classification** — a sensitivity
level, from broadly shareable to highly restricted. The classification is the input to almost
every governance decision: which storage class you may use, which region the data may sit in,
and which controls a workload must satisfy.

Open the sample classification matrix and read it:

```editor:open-file
file: ~/exercises/data-classification-matrix.md
```

```terminal:execute
command: grep -c '|' data-classification-matrix.md
```

That prints how many table lines the matrix has — a quick confirmation the fixture is present
and readable. Each data row is one classification level, its typical example data, and the
region(s) it is allowed to reside in.

```examiner:execute-test
name: verify-matrix-present
title: The classification matrix fixture is readable
args:
- data-classification-matrix.md
timeout: 10
```

{{< note >}}
The classification scheme is a {{< param product_short >}}-specific governance concept — the
levels, and which region each maps to, are defined by the platform, not by Kubernetes. See the
[{{< param product_short >}} governance & compliance docs]({{< param dcs_docs_base_url >}}/governance/overview).
{{< /note >}}

## Multi-national residency

{{< param product_short >}} runs across a **multi-national European** footprint — for example
`eu-de` (Germany) and `eu-es` (Spain). **Data residency** is the guarantee that data of a given
classification **stays inside its permitted region(s)**. Read down the matrix's *Allowed
region(s)* column: the more sensitive the classification, the fewer regions it may live in —
`CONFIDENTIAL` and `RESTRICTED` data is pinned to `eu-de` in this sample, while `PUBLIC` data
may sit anywhere in the footprint.

What makes that guarantee credible is the platform's shape. {{< param product_short >}} is
**on-prem and air-gapped**: there is no public network path, no external registry, no
third-party cloud region for data to leak into. So residency isn't only a policy you trust — it
is enforced by the fact that the data physically has nowhere else to go. Classification decides
*where data may live*; the air-gapped, regional platform is *what keeps it there*.

Next, you'll see how a workload says which region it belongs in.
