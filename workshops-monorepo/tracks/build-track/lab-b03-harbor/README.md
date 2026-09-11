# Harbor: Projects, Push & Scan

**The registry is not a URL in your manifest. It is the thing that decides what may run.**

You inspect an image without pulling it — digest, layers, runtime config — and copy one
between registries with `skopeo`, no Docker daemon involved.

Then you read two real vulnerability reports and work out which image the PROD gate refuses,
and what to do about it.

Around that are the rules that shape everything on DCS: the **catalogs**, the Harbor project
your namespace may get, and the asymmetry to remember — **DEV takes pushes of anything, PROD
takes none and pulls only below the CVE threshold**.

It ends on the only two ways an image reaches PROD: promotion by mirror, or the green catalog
of already-cleared images.

> **⚠️ Watch out:** no `docker`, no `podman`. `skopeo` talks to registries directly, which is
> why it is the tool you get on a platform that will not give you a daemon.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~30 min
- **Format:** Hands-on, guided — split terminal + editor, in your own OpenShift session namespace
- **Prerequisites:** **Build Your Image on DCS** and **From Docker to Kubernetes**.

## By the end of this lab you'll be able to

- Inspect an image without pulling it, and say why its digest matters more than its tag.
- Copy an image between registries with `skopeo`.
- Name the DCS catalogs and what each is for.
- State the DEV/PROD project rules, including the CVE threshold.
- Read a scan report and decide whether an image passes the gate.
- Describe the two routes into a PROD project.

## What you'll do

1. **Pull** from the registry, and name the rules behind it.
2. **Inspect** an image's metadata and runtime config without downloading it.
3. **Copy** an image into your own namespace's registry.
4. **Read** a clean report and a failing one.
5. **List** the Critical findings and decide what to do about each.
