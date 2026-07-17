---
title: Remediation and ITSM
---

A blocked image isn't the end — it's a task. And plenty of the registry's day-to-day
isn't something you fix yourself at all; it goes through a ticket. Both belong on the same
page: what you can act on directly, and what you request.

## Two ways to remediate

Both routes end the same way — a re-scanned artifact with the findings gone:

- **Pick a patched tag.** If the fix already exists upstream, a finding's `FixedVersion`
  (page 4) tells you which package version clears it — often a newer tag already bundles
  those patched packages. Switch your manifest to that tag and let Harbor re-scan it. No
  rebuild needed.
- **Rebuild on a patched base.** If no ready-made clean tag exists, rebuild on an updated
  base image — each finding's `FixedVersion` is your shopping list of package versions —
  and push the result. This is exactly the loop B02 taught: a `BuildConfig` producing a new
  image and pushing it to Harbor; only the trigger changes, from "the source changed" to
  "the base image needs patching."

Either way you finish with an artifact whose report shows the Criticals and Highs gone. In
this workshop, the clean, remediated artifact is the one you already trust:
`samples/hello-dcs:1.0`.

## Confirm the remediated image passes

First, prove the clean image is real and pullable — inspect it again, exactly as on page 2:

```terminal:execute
command: skopeo inspect docker://{{< param dcs_registry >}}/samples/hello-dcs:1.0
```

```examiner:execute-test
name: verify-clean-image
title: The remediated image is present and inspectable
args:
- "{{< param dcs_registry >}}/samples/hello-dcs:1.0"
timeout: 15
```

Now prove it would *pass the gate* — its report must carry zero Criticals:

```terminal:execute
command: |-
  jq '.summary.severityCount.Critical // 0' scan-report.json
```

The `// 0` returns `0` whether the key is literally zero or absent entirely — either way,
nothing Critical, so a block-on-High-and-above gate lets it through.

```examiner:execute-test
name: verify-no-criticals
title: The remediated image's report has zero Criticals
args:
- scan-report.json
timeout: 10
```

That's the full loop: the flagged image was blocked (page 5, two Criticals); the
remediated image passes (zero Criticals, digest present). Swap the reference, re-scan,
ship.

## When you can't fix it: the Security Exception Process

Sometimes remediation isn't available — a finding with an **empty `FixedVersion`** (you saw
one on page 4) has no upstream patch yet, or a fix exists but can't ship before a deadline.
You don't quietly lower the gate. You request a **Security Exception**: a time-boxed,
approved waiver for a *specific* image and a *specific* finding, raised as an
[ITSM]({{< param dcs_docs_base_url >}}/support/itsm-requests) request and reviewed under
the platform's governance rules — so the image can be used while the fix is pursued,
without weakening the gate for anyone else.

## The rest of the registry runs on ITSM too

Two more things you'll hit as a developer never happen ad hoc on {{< param product_short >}}
— they're requested, not self-service:

- **Mirroring an external image.** Bringing something new in from an Allowed External
  Registry (or copying between DCS Harbor projects) is a **mirror request** — an ITSM
  ticket, External→Harbor or Harbor→Harbor. The image doesn't appear because someone ran a
  pull; it appears because a request was approved and the platform team mirrored it.
- **Quota increases.** Your project's storage and image-count quota has a default; if your
  team is pushing more or bigger images than it allows, you request a **quota increase**,
  also via ITSM — not a self-service dial you turn yourself.

{{< note >}}
Mirroring, quota, and security exceptions are all facets of the same idea: on
{{< param product_short >}}, changes to the registry's shape and policy go through a
tracked **service-management workflow**, not direct admin access. See the
[{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/services/registry)
and the [ITSM request process]({{< param dcs_docs_base_url >}}/support/itsm-requests).
{{< /note >}}

Fix if you can, waive only if you must, and request rather than assume for anything that
changes what the registry holds or how much of it you're allowed.
