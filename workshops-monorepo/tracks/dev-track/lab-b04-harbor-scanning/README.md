# Harbor & Image Scanning

**Where your images live and what guards them — catalogs, robot accounts, and the scan gate on air-gapped DCS.**

Every image on the Digital Container Service (DCS) comes from exactly one place: Harbor.
This lab takes you inside it. You'll navigate DCS's Harbor catalogs and robot accounts,
pull and inspect an image with `skopeo`, confirm the image you built in B02 landed in its
project, read a real vulnerability and compliance scan report with `jq`, understand the
**scan gate** that decides what may run, remediate a flagged image, and see how mirroring
and quota increases happen through ITSM rather than an admin request.

- **Track:** Developer — Build on DCS · Lab 4
- **Audience:** Intermediate — comfortable with `oc`, container images, and the basics of a CVE
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-b02-image-buildconfigs; comfortable with the Linux CLI.

## By the end of this lab you'll be able to

- Navigate DCS Harbor catalogs (DCS Catalogs, Allowed External Registries, Proxy-Cached
  Catalog) and explain what a robot account is.
- Pull and inspect an image with `skopeo` using a read-only robot account.
- Explain how the image you built in B02 reaches Harbor and confirm it landed.
- Distinguish vulnerability scanning from compliance scanning, and read a scan report with
  `jq` — severities, CVE IDs, fixed-in versions.
- Explain what a scan gate does and its per-image / per-project scope.
- Remediate a flagged image and confirm the replacement passes.
- Explain how mirroring and quota increases happen via ITSM.

## What you'll do

- Browse Harbor's catalogs and robot-account model, and open the Harbor UI in a dashboard tab.
- Inspect and pull `samples/hello-dcs:1.0` with `skopeo` using a read-only robot account.
- Confirm the image you'd push from B02 already lives in its Harbor project.
- Read a clean scan report and a flagged one with `jq`, and trace what the scan gate does
  in the pull path.
- Remediate the flagged image and confirm it passes, then see the ITSM path for mirroring
  and quota requests.
