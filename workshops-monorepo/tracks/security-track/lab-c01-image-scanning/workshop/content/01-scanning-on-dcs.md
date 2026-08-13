---
title: Scanning on DCS
---

Before you read a report, it helps to know what a scanner actually looks for — because
"scanning" is really **two** different jobs, and {{< param product_short >}} runs both.

## Two kinds of scan

**Vulnerability scanning** asks: *does this image contain software with known security
flaws?* A scanner such as [Trivy](https://trivy.dev/) reads the packages baked into each
image layer — the OS packages, language libraries, binaries — and matches them against public
vulnerability databases. Each match is a **CVE** (a [Common Vulnerabilities and
Exposures](https://www.cve.org/) identifier, e.g. `CVE-2022-0778`) with a **severity**
(Critical / High / Medium / Low) and, usually, the version that fixes it. This is the scan
you'll read on the next page.

**Compliance scanning** asks a different question: *is this image built and configured the way
policy requires?* Not "is there a known bug" but "does it break the rules" — for example, does
it run as root, is it missing a required label, does it use a forbidden base image. The
findings aren't CVEs; they're policy violations.

Analogy: vulnerability scanning is the safety recall list for the parts in your car;
compliance scanning is the roadworthiness inspection. A car can have zero recalled parts and
still fail inspection for a broken light — and vice versa. {{< param product_short >}} cares
about both.

## Scan scope: per-image, per-project, global

The same scan runs at three scopes:

- **Per-image** — every artifact (a tag/digest) gets its own report. This is what you read
  when you ask "is *this* image clean?"
- **Per-project** — a Harbor project (e.g. `samples`) can require that everything in it is
  scanned, and roll findings up so a team sees its whole registry footprint at a glance.
- **Global** — the platform scans across all projects and can re-scan continuously, so an
  image that was clean last week is re-evaluated when a *new* CVE is published against a
  package it already contains. Nothing about the image changed — the world's knowledge did.

That last point matters: an image is never "scanned once and done." A digest that passed in
January can be flagged in March.

## When the scan runs, and what a gate is

Harbor scans an image **on push** (when it first lands) and **periodically / on demand**
afterwards, storing the report against the artifact. On its own, a report is just
information. The platform turns it into enforcement with a **gate**: a policy that **blocks**
using an image whose findings exceed a threshold.

{{< note >}}
The **scan gate** is a {{< param product_short >}}-specific control — the platform decides the
threshold, the scope, and how the block is enforced in the pull path. See the
[{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/registry/overview).
The scanner ([Trivy](https://trivy.dev/)) and the [CVE](https://www.cve.org/) format are
standard and link to their upstream sources.
{{< /note >}}

You'll read a real report on the next page, then see exactly what the gate does on page 3.
