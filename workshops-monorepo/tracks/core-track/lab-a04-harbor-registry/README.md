# Working with Harbor

**The one place every image on DCS comes from — and how you get images in and out.**

DCS is air-gapped: the public internet and every public registry like `docker.io` or
`quay.io` are unreachable. That puts the Harbor registry at the centre of everything you
run. In this lab you find images in catalogs, inspect and pull one with `skopeo`, run it on
the cluster, browse it in the Harbor UI, and see how vulnerability scanning decides what is
allowed to run. Pulling is hands-on; pushing and mirroring are covered as concepts.

- **Track:** Core — DCS Foundations · Lab 4 of 9
- **Audience:** Beginner — familiar with container images and basic `oc`; no Harbor or `skopeo` experience assumed
- **Duration:** ~45 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** lab-a02-kubernetes-essentials

## By the end of this lab you'll be able to

- Explain why DCS uses a single, air-gapped registry, and how images arrive through catalogs (DCS Catalogs, Allowed External Registries, Proxy-Cached Catalog).
- Inspect and pull a catalog image with `skopeo` — and say why `skopeo`, not `docker`/`podman`.
- Run a catalog image on the cluster and confirm the pull landed.
- Browse a Harbor project — its tags, digests, and scan results.
- Explain how external images are brought in via an image-mirroring ITSM request.
- Read a Harbor vulnerability scan result and explain the gate that blocks unsafe images.
- Know that Harbor also stores Helm charts, that PROD namespaces cannot use the Proxy-Cached Catalog, and that pushing needs a dedicated project.

## What you'll do

Your session comes with a read-only Harbor robot account, so you can inspect and pull
images without logging in. You'll use `skopeo` to inspect and pull a catalog image, run it
on the cluster, then open the Harbor UI to explore a project's tags, digests, and scan
results — and read a scan result to see the gate in action.
