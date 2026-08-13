---
title: The Gate
---

A report on its own is just information. {{< param product_short >}} turns it into
enforcement with a **scan gate**: a policy that blocks using an image whose findings exceed
a threshold. Read a report that trips it, then see exactly where the gate sits.

## A report that fails

Open the flagged report — same schema as the clean one, different image
(`samples/hello-dcs:flagged`):

```editor:open-file
file: ~/exercises/scan-report-flagged.json
```

Count the Critical findings — the severity a block-on-High-and-above gate cares about
most:

```terminal:execute
command: |-
  jq '[.vulnerabilities[] | select(.severity == "Critical")] | length' scan-report-flagged.json
```

You should get `2` — both in `openssl` — plus several High findings on top, well over any
sensible threshold.

```examiner:execute-test
name: verify-flagged-criticals
title: The flagged report has Critical findings
args:
- scan-report-flagged.json
timeout: 10
```

That count is *why* the gate trips. The gate doesn't read intentions — it reads the
severity counts on the artifact and applies the threshold.

## Where the gate sits: the pull path

A scan gate isn't a linter you run in CI and forget about — it sits **in the pull path**,
between a node asking Harbor for an image and Harbor handing it over. Open the manifest
that would try to use the flagged image:

```editor:open-file
file: ~/exercises/deploy-flagged.yaml
```

Trace what happens if this were applied on a gated cluster:

1. The scheduler places the Pod; the node asks Harbor to pull `samples/hello-dcs:flagged`.
2. Harbor checks the artifact's scan result against the gate threshold.
3. The findings exceed it, so Harbor **refuses the pull** — the layers are never served.
4. The kubelet can't start the container, and the Pod sticks in **`ImagePullBackOff`**.

The image is quarantined at the source. It doesn't matter how many manifests reference it —
if the gate blocks the artifact, nothing on the platform can pull it.

{{< warning >}}
**Observe, don't apply.** This workshop's environment has no live scanner wired to Harbor,
so applying `deploy-flagged.yaml` here would not reproduce the block — the tag is a
narrative prop, not a real quarantined artifact. On a gated {{< param product_short >}}
cluster, the `ImagePullBackOff` above is exactly what you'd see. Read the report (which
*is* real) and reason about the gate, rather than faking a failure.
{{< /warning >}}

## Threshold policy

A gate is a **threshold plus a scope**:

- **Block at High-and-above** — an image with any High or Critical finding is refused.
- **Warn on Medium** — surfaced in the report and the UI, but not blocking on its own.
- **Per-project override** — a project can tighten the threshold (e.g. block on Medium too)
  where its risk profile demands it. Loosening below the platform floor is governed, not
  self-service.

{{< note >}}
The gate itself — its default threshold and how the block is enforced in the pull path — is
a {{< param product_short >}}-specific control. See the
[{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/services/registry).
{{< /note >}}

Two Criticals, blocked at the gate. Next, get it unstuck.
