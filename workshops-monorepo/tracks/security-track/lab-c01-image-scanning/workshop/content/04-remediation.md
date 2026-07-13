---
title: Remediation
---

A blocked image isn't the end — it's a task. Remediation means getting a version of the image
that passes the gate, then proving it. And when you *can't* fix it in time, there's a governed
way through.

## Two ways to remediate

Both routes end the same way — a re-scanned artifact with the findings gone:

- **Pick a patched tag.** If the fix already exists upstream, the finding's `FixedVersion`
  tells you which package version clears it. Often a newer image tag already bundles those
  patched packages — switch your manifest to that tag and re-scan. No rebuild needed.
- **Rebuild on a patched base.** If no ready-made clean tag exists, rebuild the image on an
  updated base (the `FixedVersion` of each finding is your shopping list of package versions),
  push it, and let Harbor scan the result. This is CI's job, not a live in-session step — same
  as pushing in A04.

Either way you finish with an artifact whose report shows the Criticals and Highs gone. In
this workshop the clean, remediated artifact is the one you already trust:
`samples/hello-dcs:1.0`.

## Confirm the remediated image passes

First, prove the clean image is real and pullable — inspect it in Harbor (this reads live over
your read-only robot account, exactly like A04):

```terminal:execute
command: skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0
```

You should see the image JSON, including its **`Digest`** — the immutable identity of the
artifact the gate would evaluate.

```examiner:execute-test
name: verify-clean-image
title: The remediated image is present and inspectable
args:
- $DCS_REGISTRY/samples/hello-dcs:1.0
timeout: 30
retries: 3
delay: 3
```

Now prove it would *pass the gate* — its report must carry zero Criticals. Read the count
straight from the clean report:

```terminal:execute
command: |-
  jq '.summary.severityCount.Critical // 0' scan-report.json
```

The `// 0` gives `0` whether the count is literally zero or the key is absent — either way,
nothing Critical, so the gate lets it through.

```examiner:execute-test
name: verify-no-criticals
title: The remediated image's report has zero Criticals
args:
- scan-report.json
timeout: 10
```

That's the full loop: the flagged image was blocked (page 3, two Criticals); the remediated
image passes (zero Criticals, digest present). Swap the reference, re-scan, ship.

## When you can't fix it: the Security Exception Process

Sometimes remediation isn't available yet — a finding with an **empty `FixedVersion`** (you
saw one on page 2) has no upstream patch, or a fix exists but can't ship before a deadline. You
don't quietly lower the gate. You request a **Security Exception**.

A **Security Exception** is a time-boxed, approved waiver: a documented, risk-accepted
allowance for a *specific* image and *specific* finding, granted for a limited window, so the
image can be used while the fix is pursued — without weakening the gate for everything else.
It's raised as an **ITSM request** and reviewed under the platform's governance rules.

{{< note >}}
The Security Exception Process is part of {{< param product_short >}} **governance** — the
Responsibility Matrix, data-classification, and exception rules that decide who may accept
what risk. See the
[{{< param product_short >}} governance documentation]({{< param dcs_docs_base_url >}}/governance/overview)
and the [ITSM request process]({{< param dcs_docs_base_url >}}/support/itsm-requests).
{{< /note >}}

The order matters: **fix if you can, waive only if you must** — and a waiver is a tracked,
expiring exception, never a permanent hole in the gate.
