# Image Scanning & Harbor Gates

**Go inside the Harbor scan gate: read what a scan report says, understand what gets blocked, and fix a flagged image — the daily security work on air-gapped DCS.**

On the Digital Container Service (DCS) the registry is the security checkpoint. Because the platform is air-gapped and every image comes from one Harbor, that single source is also the one place to enforce "nothing unsafe runs here." This lab takes you inside that enforcement: you'll read the *content* of a Harbor scan report with `jq`, tell vulnerability scanning apart from compliance scanning, understand the gate policy that blocks unsafe images at pull time, and remediate a flagged image. Scan reports ship as static fixtures, so every step is reproducible and examiner-verifiable in the air-gap.

- **Track:** Security & Compliance — Secure on DCS · Lab 1 of 5
- **Audience:** Intermediate — comfortable with `oc`, container images, and the idea of a CVE
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a04-harbor-registry; comfortable with the Linux CLI and familiar with containers and CVEs.

## By the end of this lab you'll be able to

- Distinguish vulnerability scanning (CVEs in image layers) from compliance scanning (policy/configuration), and explain per-image, per-project, and global scan scope.
- Read a Harbor scan report with `jq` — severities, CVE IDs, fixed-in versions — and summarise the risk.
- Explain what the scan gate does, where it sits in the pull path, and how a severity threshold decides block-versus-warn.
- Remediate a flagged image by picking a patched tag or rebuilding on a patched base, and confirm the replacement passes.
- Explain the Security Exception Process (ITSM) — the escape hatch when a finding can't be fixed straight away.

## What you'll do

- Contrast vulnerability and compliance scanning and where each runs on DCS.
- Read a real Harbor scan report with `jq`, pulling out severities, CVE IDs, and fixed-in versions.
- Trace the scan gate in the pull path and see how its threshold decides what is blocked.
- Remediate a flagged image with `skopeo` and confirm the replacement clears the gate.
