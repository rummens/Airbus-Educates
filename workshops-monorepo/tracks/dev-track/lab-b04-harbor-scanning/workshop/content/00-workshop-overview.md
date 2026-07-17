---
title: "Harbor & Image Scanning"
---

Welcome to this workshop, part of **{{< param product_name >}}**. You've built an image
in B02 and deployed images before — now you'll go inside the registry they all live in.
On {{< param product_short >}} that registry is [Harbor](https://goharbor.io/docs/): the
platform's single, air-gapped source of images and the place where every image is
**scanned** before it's trusted to run. More on how {{< param product_short >}} runs it in
the [{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/services/registry).
You'll navigate its catalogs and robot accounts, pull and inspect an image with `skopeo`,
confirm an image landed in its project, read a real scan report, understand the **scan
gate** that decides what may run, remediate a flagged image, and see how mirroring and
quota increases happen through **ITSM** rather than a direct admin request.

{{< note >}}
**First time in one of these labs?** Take two minutes to read the
[DCS Academy environment guide]({{< param dcs_docs_base_url >}}/academy/environment-guide) —
it explains the terminal, editor, console, slides and the clickable actions you'll use here.
{{< /note >}}

## What You'll Learn

By the end of this workshop you will be able to:

- Navigate {{< param product_short >}} Harbor catalogs (DCS Catalogs, Allowed External
  Registries, the Proxy-Cached Catalog) and explain what a robot account is.
- Pull and inspect an image with [`skopeo`](https://github.com/containers/skopeo) using a
  read-only robot account.
- Explain how the image you built in B02 reaches Harbor, and confirm it landed in its
  project.
- Distinguish **vulnerability** scanning from **compliance** scanning, and read a scan
  report — severities, CVE IDs, fixed-in versions — with
  [`jq`](https://jqlang.github.io/jq/).
- Explain what a **scan gate** does — blocking a pull above a severity threshold — and its
  per-image / per-project scope.
- Remediate a flagged image (a patched tag, or a rebuild on a patched base) and confirm the
  replacement passes.
- Explain how mirroring an external image and requesting a quota increase both happen via
  **ITSM**.

## Prerequisites

- **B02 — Building Images with BuildConfigs.** This workshop picks up the image built
  there. If you haven't done B02, `samples/hello-dcs:1.0` — the same image A02 deployed —
  stands in for it throughout.
- Familiarity with [container images](https://kubernetes.io/docs/concepts/containers/images/)
  and basic [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
  usage.

No prior experience with registries, `skopeo`, or vulnerability scanning is assumed — that
is what this workshop teaches.

## Your Environment

A split **terminal** and an **editor**, in your own {{< param product_short >}} session
namespace. No per-session virtual cluster is needed here — every exercise talks to Harbor
directly or reads a local fixture, with nothing cluster-scoped to create. Your session
carries a read-only Harbor **robot account**, and `skopeo` and `jq` are already installed
on the workshop image (no install step needed). Commands are run with `skopeo`, `jq`, and
`oc`.

## Time and Difficulty

- **Estimated time:** 40 minutes
- **Difficulty:** Intermediate

## Further Reading

- [{{< param product_short >}} registry documentation]({{< param dcs_docs_base_url >}}/services/registry)
- [Harbor documentation](https://goharbor.io/docs/)
- [Trivy documentation](https://trivy.dev/)
- [CVE program](https://www.cve.org/)
- [`skopeo` documentation](https://github.com/containers/skopeo)
- [`jq` manual](https://jqlang.github.io/jq/manual/)
