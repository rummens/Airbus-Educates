---
title: Workshop Overview
---

Welcome to this workshop, part of **{{< param product_name >}}**. In A04 you pulled images
from Harbor and saw that a **scan gate** can block an unsafe one. Here you go inside that
gate: you'll read the *content* of a Harbor scan report, tell **vulnerability** scanning
apart from **compliance** scanning, understand the policy that decides what gets blocked, and
remediate a flagged image — the day-to-day security work on an air-gapped platform.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

On {{< param product_short >}} the registry is the **security checkpoint**. Because the
platform is air-gapped and every image comes from one Harbor, that single source is also the
single place to enforce "nothing unsafe runs here." Scanning is how Harbor knows what is
unsafe; the gate is how it acts on that knowledge.

## What You'll Learn

By the end of this workshop you will be able to:

- Distinguish **vulnerability scanning** (CVEs in image layers) from **compliance scanning**
  (policy/configuration), and explain per-image, per-project, and global scan scope on {{< param product_short >}}.
- Read a Harbor scan report with [`jq`](https://jqlang.github.io/jq/) — severities, CVE IDs,
  and fixed-in versions — and summarise the risk.
- Explain what a **scan gate** does, where it sits in the pull path, and how a severity
  threshold decides block-versus-warn.
- Remediate a flagged image (pick a patched tag, or rebuild on a patched base) and confirm
  the replacement passes.
- Explain the **Security Exception Process** (ITSM) — the escape hatch when a finding can't be
  fixed straight away.

## Prerequisites

- **lab-a04-harbor-registry** — you should be comfortable inspecting an image with
  [`skopeo`](https://github.com/containers/skopeo) and know that Harbor catalogs, robot
  accounts, and a scan gate exist.
- Familiarity with [container images](https://kubernetes.io/docs/concepts/containers/images/),
  the idea of a [CVE](https://www.cve.org/), and basic
  [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) usage.

No experience reading a scan report is assumed — that is what this workshop teaches.

## Your Environment

A **split terminal**, an editor, and the web console, connected to your own
{{< param product_short >}} session namespace. Your session has a read-only Harbor **robot account**, so
`skopeo` can inspect images without a login. The scan reports you'll read are **static
fixtures** in `~/exercises` — a real Harbor scanner isn't guaranteed reachable in a session,
so shipping the reports lets you practise reading them the same way every time. Commands are
run with `oc`, `skopeo`, and `jq` in the terminal.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Intermediate

## Further Reading

- [{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/registry/overview)
- [Trivy documentation](https://trivy.dev/)
- [CVE program](https://www.cve.org/)
- [`jq` manual](https://jqlang.github.io/jq/manual/)
